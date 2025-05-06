import React, { useState, useRef } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import './transpage.css';

import log from '../resources/icon/logo.svg';
import closeIcon from '../resources/icon/close.png';
import correctLog from '../resources/icon/correct.svg';

function Transpage() {
  const [email, setEmail] = useState('');
  const [isEmailValid, setIsEmailValid] = useState(false);
  const [files, setFiles] = useState([]);
  const [uploadProgress, setUploadProgress] = useState([]);
  const [uploaded, setUploaded] = useState([]);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const navigate = useNavigate();
  const fileInputRef = useRef(null);

  /* ---------- helpers ---------- */
  const getCookie = (name) =>
    document.cookie
      .split(';')
      .map((c) => c.trim().split('='))
      .find(([k]) => k === name)?.[1] || null;

  const handleEmailChange = (e) => {
    const v = e.target.value;
    setEmail(v);
    setIsEmailValid(/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v));
  };

  const handleFileChange = (e) => {
    const newFiles = Array.from(e.target.files);
    const base = files.length;
    setFiles((f) => [...f, ...newFiles]);
    setUploadProgress((p) => [...p, ...newFiles.map(() => 0)]);
    setUploaded((u) => [...u, ...newFiles.map(() => false)]);
    newFiles.forEach((_, idx) => simulateUpload(base + idx));
  };

  const simulateUpload = (idx) => {
    const timer = setInterval(() => {
      setUploadProgress((p) => {
        const copy = [...p];
        if (copy[idx] < 100) copy[idx] = Math.min(copy[idx] + 50, 100);
        else {
          clearInterval(timer);
          setUploaded((u) => {
            const c = [...u];
            c[idx] = true;
            return c;
          });
        }
        return copy;
      });
    }, 200);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    handleFileChange({ target: { files: e.dataTransfer.files } });
  };

  const handleDelete = (i) => {
    setFiles((f) => f.filter((_, idx) => idx !== i));
    setUploadProgress((p) => p.filter((_, idx) => idx !== i));
    setUploaded((u) => u.filter((_, idx) => idx !== i));
  };

  const handleConfirm = async () => {
    if (!isEmailValid || files.length === 0) {
      return alert('Please fill out all required fields.');
    }
    setIsSubmitting(true);

    const formData = new FormData();
    formData.append('email', email);
    files.forEach((f) => formData.append('file', f));
    formData.append(
      'outputFormat',
      document.querySelector('select[name="outputFormat"]').value,
    );
    formData.append(
      'language',
      document.querySelector('select[name="language"]').value,
    );

    try {
      const res = await fetch(
        `${process.env.REACT_APP_API_URL || 'http://127.0.0.1:8000'}/transcription/`,
        {
          method: 'POST',
          headers: { 'X-CSRFToken': getCookie('csrftoken') },
          credentials: 'include',
          body: formData,
        },
      );
      if (!res.ok) throw new Error();
      const data = await res.json();
      const formatted = data.transcription
        .map((i) => `Speaker ${i.speaker}: ${i.text}`)
        .join('\n\n');

      navigate('/transcription/transcriptionresult', {
        state: {
          demoData: {
            email,
            file: files[0],
            outputFormat: formData.get('outputFormat'),
            result: formatted,
          },
        },
      });
    } catch {
      alert('An error occurred.');
      setIsSubmitting(false);
    }
  };

  /* ---------- render ---------- */
  return (
    <>
      {/* top bar */}
      <div className="header">
        <div className="logo">
          <img src={log} alt="logo" />
        </div>
        <nav className="nav-links">
          <Link to="/about">About</Link>
          <Link to="/transcription">Transcription</Link>
          <Link to="/historylogin">History</Link>
        </nav>
      </div>

      {/* 2‑column area */}
      <div className="container">
        {/* LEFT = upload / transcribe */}
        <div
          className="upload-section"
          onDragOver={(e) => e.preventDefault()}
          onDrop={handleDrop}
        >
          <h3>Transcribe file(s)</h3>
          <p>
            Our platform supports: WAV, MP3, M4A, FLAC, OGG, AAC, MP4, AVI, MOV.
          </p>

          {files.length === 0 ? (
            <div
              className="upload-box"
              onClick={() => fileInputRef.current.click()}
            >
              <input
                type="file"
                accept=".wav,.mp3,.m4a,.flac,.ogg,.aac,.mp4,.avi,.mov"
                multiple
                onChange={handleFileChange}
                ref={fileInputRef}
                style={{ display: 'none' }}
              />
              <div className="upload-icon">⬆️</div>
              <p>Drag files here or click to select</p>
            </div>
          ) : (
            <div className="uploaded-files">
              {files.map((file, i) => (
                <div key={i} className="file-item">
                  <div className="file-info">
                    <span className="file-icon">
                      {file.type.startsWith('audio/') ? '🎧' : '🎬'}
                    </span>
                    <span className="file-name">{file.name}</span>
                    <span className="file-size">
                      {(file.size / 1024 / 1024).toFixed(1)}MB
                    </span>
                    <img
                      src={closeIcon}
                      alt="delete"
                      className="delete-button"
                      onClick={() => handleDelete(i)}
                    />
                  </div>
                  <div className="file-progress">
                    <div
                      className="progress-bar"
                      style={{ width: `${uploadProgress[i]}%` }}
                    />
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* RIGHT = email & settings */}
        <div className="input-section">
          {/* block‑1 */}
          <div className="form-block">
            <h3>Email address to receive results</h3>
            <p>Please input your email address.</p>
            <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
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

          {/* block‑2 */}
          <div className="form-block">
            <h3>Select output file format</h3>
            <p>Choose your desired transcription file type.</p>
            <select name="outputFormat">
              <option value="docx">docx</option>
              <option value="pdf">pdf</option>
              <option value="txt">txt</option>
            </select>
          </div>

          {/* block‑3 */}
          <div className="form-block">
            <h3>Select transcription language</h3>
            <p>Choose the language for your transcript.</p>
            <select name="language">
              <option value="english">English</option>
              <option value="spanish">Spanish</option>
              <option value="french">French</option>
            </select>
          </div>
        </div>
      </div>

      {/* Sticky bottom CTA */}
<div className="transcribe-footer">
  {/* tooltip‑wrapper 负责按钮+浮窗 */}
  <div className="tooltip-wrapper">
    <button
      className="transcribe-button"
      onClick={handleConfirm}
      disabled={isSubmitting}
    >
      {isSubmitting ? 'Transcribing…' : 'Transcribe'}
    </button>

    {/* 浮窗提示 */}
    <span className="transcribe-tooltip">
      Ensure all fields are filled in. After you click, the system will start
      transcribing and the button will be disabled for a moment.
    </span>
  </div>

  {/* 提示文字放在按钮下方 */}
  <p className="transcribe-note">
    Please complete all above fields before clicking <strong>Transcribe</strong>.
  </p>
</div>

    </>
  );
}

export default Transpage;
