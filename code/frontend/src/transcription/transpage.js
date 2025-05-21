// src/pages/Transpage.js
import React, { useState, useRef, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import './transpage.css';

import log        from '../resources/icon/logo.svg';
import closeIcon  from '../resources/icon/close.png';
import correctLog from '../resources/icon/correct.svg';

function Transpage() {
  const [email, setEmail]         = useState('');
  const [isEmailValid, setValid]  = useState(false);
  const [files, setFiles]         = useState([]);
  const [uploadProg, setUpProg]   = useState([]);
  const [uploaded, setUploaded]   = useState([]);
  const [tasks, setTasks]         = useState([]);   // {file, taskId, progress, status, result}
  const [isSubmitting, setSubmit] = useState(false);

  const navigate     = useNavigate();
  const fileInputRef = useRef(null);

  /* ---------- helpers ---------- */
  const getCookie = (name)=>
    document.cookie.split(';').map(c=>c.trim().split('='))                    // csrftoken helper
           .find(([k])=>k===name)?.[1] || null;

  const handleEmailChange = e=>{
    const v=e.target.value;
    setEmail(v);
    setValid(/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v));
  };

  /* ---------- 本地上传进度（与原 Demo 保持一致） ---------- */
  const handleFileChange = e=>{
    const newFiles = Array.from(e.target.files);
    const base     = files.length;
    setFiles(f=>[...f,...newFiles]);
    setUpProg(p=>[...p,...newFiles.map(()=>0)]);
    setUploaded(u=>[...u,...newFiles.map(()=>false)]);
    newFiles.forEach((_,i)=>simulateUpload(base+i));
  };
  const simulateUpload = idx=>{
    const t=setInterval(()=>{
      setUpProg(p=>{
        const c=[...p];
        if(c[idx] < 100) c[idx] = Math.min(c[idx]+50,100);
        else{
          clearInterval(t);
          setUploaded(u=>{const copy=[...u];copy[idx]=true;return copy;});
        }
        return c;
      });
    },200);
  };

  const handleDrop   = e=>{e.preventDefault();handleFileChange({target:{files:e.dataTransfer.files}});};
  const handleDelete = i=>{
    setFiles   (f=>f.filter((_,idx)=>idx!==i));
    setUpProg  (p=>p.filter((_,idx)=>idx!==i));
    setUploaded(u=>u.filter((_,idx)=>idx!==i));
  };

  /* ───────────────────────────────────────────
       1. 并发上传；拿到各自 task_id
     ─────────────────────────────────────────── */
  const handleConfirm = async()=>{
    if(!isEmailValid || files.length===0){
      alert('Please fill out all required fields.'); return;
    }
    setSubmit(true);

    const API   = process.env.REACT_APP_API_URL || 'http://127.0.0.1:8000';
    const fmt   = document.querySelector('select[name="outputFormat"]').value;
    const lang  = document.querySelector('select[name="language"]').value;

    try{
      const newTasks = await Promise.all(
        files.map(async file=>{
          const fd = new FormData();
          fd.append('email', email);
          fd.append('file' , file);
          fd.append('outputFormat', fmt);
          fd.append('language'    , lang);

          const res = await fetch(`${API}/transcription/`,{
            method:'POST',
            headers:{ 'X-CSRFToken': getCookie('csrftoken') },
            credentials:'include',
            body:fd
          });
          if(!res.ok) throw new Error('Upload failed');
          const data = await res.json();

          /* ★ 后端两种返回格式兼容 */
          let taskId = data.task_id;
          if(!taskId && Array.isArray(data.tasks) && data.tasks.length){
            taskId = data.tasks[0].task_id;
          }
          if(!taskId) throw new Error('No task_id in response');

          return { file, taskId, progress:0, status:'processing', result:null };
        })
      );

      setTasks(newTasks);
      newTasks.forEach(t=>startPolling(t.taskId, fmt));
    }catch(err){
      console.error(err);
      alert('An error occurred: '+ err.message);
      setSubmit(false);
    }
  };

  /* ───────────────────────────────────────────
       2. 轮询单个 task_id
     ─────────────────────────────────────────── */
  const startPolling = (taskId, fmt)=>{
    const API = process.env.REACT_APP_API_URL || 'http://127.0.0.1:8000';
    const timer = setInterval(async()=>{
      try{
        const res = await fetch(`${API}/transcription/api/status/${taskId}/`);
        if(!res.ok){                         // 后端可能返回 404 已失效；忽略
          console.warn(`status ${res.status} for ${taskId}`); return;
        }
        const data = await res.json();

        setTasks(prev=>prev.map(t=>{
          if(t.taskId!==taskId) return t;

          if(data.status==='processing'){
            return {...t, progress: Math.round((data.progress||0)*100)};
          }
          if(data.status==='completed'){
            clearInterval(timer);
            return {...t, progress:100, status:'done',
                    result:data.transcription || data.transcripts};
          }
          if(data.status==='error'){
            clearInterval(timer);
            return {...t, status:'error'};
          }
          return t;
        }));
      }catch(e){
        console.error('poll error:',e);
      }
    }, 1000);
  };

  /* ───────────────────────────────────────────
       3. 全部任务完成 => 跳转结果页
     ─────────────────────────────────────────── */
  useEffect(()=>{
    if(isSubmitting && tasks.length && tasks.every(t=>t.status==='done')){
      navigate('/transcription/transcriptionresult',{
        state:{
          demoData:{
            email,
            files,
            results: tasks.map(t=>t.result),
            outputFormat: document.querySelector('select[name="outputFormat"]').value
          }
        }
      });
    }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  },[tasks]);

  /* ---------- 平均进度 ---------- */
  const avgProg = tasks.length
    ? Math.round(tasks.reduce((s,t)=>s+(t.progress||0),0)/tasks.length)
    : 0;

  /* ---------- UI ---------- */
  return (
    <>
      {/* — 顶栏 — */}
      <div className="header">
        <div className="logo"><img src={log} alt="logo"/></div>
        <nav className="nav-links">
          <Link to="/about">About</Link>
          <Link to="/transcription">Transcription</Link>
          <Link to="/historylogin">History</Link>
        </nav>
      </div>

      {/* — 主体 — */}
      <div className="container">
        {/* 左列：文件上传 */}
        <div className="upload-section"
             onDragOver={e=>e.preventDefault()}
             onDrop={handleDrop}>
          <h3>Transcribe file(s)</h3>
          <p>Our platform supports: WAV, MP3, M4A, FLAC, OGG, AAC, MP4, AVI, MOV.</p>

          {files.length===0 ? (
            <div className="upload-box" onClick={()=>fileInputRef.current.click()}>
              <input type="file"
                     multiple
                     accept=".wav,.mp3,.m4a,.flac,.ogg,.aac,.mp4,.avi,.mov"
                     onChange={handleFileChange}
                     ref={fileInputRef}
                     style={{display:'none'}}/>
              <div className="upload-icon">⬆️</div>
              <p>Drag files here or click to select</p>
            </div>
          ):(
            <div className="uploaded-files">
              {files.map((file,i)=>(
                <div key={i} className="file-item">
                  <div className="file-info">
                    <span className="file-icon">{file.type.startsWith('audio/')?'🎧':'🎬'}</span>
                    <span className="file-name">{file.name}</span>
                    <span className="file-size">{(file.size/1048576).toFixed(1)} MB</span>
                    <img src={closeIcon} alt="x" className="delete-button" onClick={()=>handleDelete(i)}/>
                  </div>
                  <div className="file-progress">
                    <div className="progress-bar" style={{width:`${uploadProg[i]}%`}}/>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* 右列：表单 */}
        <div className="input-section">
          {/* block-1 */}
          <div className="form-block">
            <h3>Email address to receive results</h3>
            <div
              style={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}
            >
              <input
                type="email"
                placeholder="you@example.com"
                value={email}
                onChange={handleEmailChange}
                required
              />
              {isEmailValid && (
                <img src={correctLog} alt="valid" className="small-feedback" />
              )}
            </div>
          </div>
          <div className="form-block">
            <h3>Select output file format</h3>
            <select name="outputFormat">
              <option value="docx">docx</option><option value="pdf">pdf</option><option value="txt">txt</option>
            </select>
          </div>
          <div className="form-block">
            <h3>Select transcription language</h3>
            <select name="language">
              <option value="english">English</option>
              <option value="spanish">Spanish</option>
              <option value="french" >French </option>
              <option value="chinese">Chinese</option>
            </select>
          </div>
        </div>
      </div>

      {/* 全局进度条 */}
      {isSubmitting && tasks.length>0 && (
        <div className="transcribing-status">
          <span>Transcribing: {avgProg}%</span>
          <div className="progress-bar-bg">
            <div className="progress-bar-fill" style={{width:`${avgProg}%`}}/>
          </div>
        </div>
      )}

      {/* 底部按钮 */}
      <div className="transcribe-footer">
        <div className="tooltip-wrapper">
          <button className="transcribe-button"
                  onClick={handleConfirm}
                  disabled={isSubmitting}>
            {isSubmitting ? 'Transcribing…' : 'Transcribe'}
          </button>
          <span className="transcribe-tooltip">
            Ensure all fields are filled in. After you click,
            the system will start transcribing and the button will be disabled for a moment.
          </span>
        </div>
        <p className="transcribe-note">
          Please complete all above fields before clicking <strong>Transcribe</strong>.
        </p>
      </div>
    </>
  );
}

export default Transpage;
