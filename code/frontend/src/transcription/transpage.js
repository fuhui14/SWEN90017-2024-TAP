import './transpage.css';
import { Link, useNavigate } from 'react-router-dom';
import log from '../resources/icon/logo.svg';
import addLog from '../resources/icon/add.svg';
import closeIcon from '../resources/icon/close.png';
import correctLog from '../resources/icon/correct.svg';
import React, { useState } from 'react';

function Transpage() {
  const [email, setEmail] = useState(''); // State for email
  const [isEmailValid, setIsEmailValid] = useState(false); // Email validation state
  const [files, setFiles] = useState([]); // State for file uploads
  const [uploadProgress, setUploadProgress] = useState([]); // Track upload progress
  const [uploaded, setUploaded] = useState([]); // Track upload completion
  const [isSubmitting, setIsSubmitting] = useState(false); // 控制按钮状态
  const navigate = useNavigate();
  const fileInputRef = React.useRef(null);

  // Handle email input changes
  const handleEmailChange = (e) => {
    const value = e.target.value;
    setEmail(value);
    setIsEmailValid(/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value));
  };

  // Handle file input changes and append new files
  const handleFileChange = (e) => {
    const newFiles = [...e.target.files];
    const currentFilesCount = files.length; // Number of existing files

    // Append new files to the existing files array
    setFiles((prevFiles) => [...prevFiles, ...newFiles]);

    // Append new progress entries for new files while preserving existing progress
    setUploadProgress((prevProgress) => [
      ...prevProgress,
      ...new Array(newFiles.length).fill(0),
    ]);

    // Append new uploaded state entries (default false for new files)
    setUploaded((prevUploaded) => [
      ...prevUploaded,
      ...new Array(newFiles.length).fill(false),
    ]);

    // Start simulation for new files using an offset for correct indices
    newFiles.forEach((file, index) => {
      const newIndex = currentFilesCount + index;
      simulateUpload(file, newIndex);
    });
  };

  // Simulate the file upload progress
  const simulateUpload = (file, index) => {
    const interval = setInterval(() => {
      setUploadProgress((prevProgress) => {
        const updatedProgress = [...prevProgress];
        if (updatedProgress[index] < 100) {
          updatedProgress[index] = Math.min(updatedProgress[index] + 49, 100);
        } else {
          clearInterval(interval);
          setUploaded((prevUploaded) => {
            const updatedUploaded = [...prevUploaded];
            updatedUploaded[index] = true; // Mark file as uploaded
            return updatedUploaded;
          });
        }
        return updatedProgress;
      });
    }, 200);
  };

  // Handle file drop events
  const handleDrop = (e) => {
    e.preventDefault();
    const droppedFiles = e.dataTransfer.files;
    handleFileChange({ target: { files: droppedFiles } });
  };

  // Handle deletion of a file from the list
  const handleDeleteFile = (index) => {
    const updatedFiles = files.filter((_, i) => i !== index);
    setFiles(updatedFiles);
    const updatedProgress = uploadProgress.filter((_, i) => i !== index);
    setUploadProgress(updatedProgress);
    const updatedUploaded = uploaded.filter((_, i) => i !== index);
    setUploaded(updatedUploaded);
  };

  // Function to get a CSRF token from cookies
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  // Handle the confirmation and submission of the upload process
  const handleConfirm = async () => {
    if (!isEmailValid || files.length === 0) {
      alert('Please fill out all required fields.');
      return;
    }
    setIsSubmitting(true);

    // Prepare formData for submission
    const demoData = new FormData();
    const formData = new FormData();
    formData.append('email', email);
    demoData.append('email', email);

    files.forEach((file) => {
      formData.append('file', file);
      demoData.append('file', file);
    });

    const outputFormat = document.querySelector('select[name="outputFormat"]').value;
    const language = document.querySelector('select[name="language"]').value;
    formData.append('outputFormat', outputFormat);
    formData.append('language', language);
    demoData.append('outputFormat', outputFormat);
    demoData.append('language', language);

    console.log('files: ', files);

    // Retrieve CSRF token
    const csrftoken = getCookie('csrftoken');

    // Send data to the backend
    try {
      const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://127.0.0.1:8000';
      const response = await fetch(`${API_BASE_URL}/transcription/`, {
        method: 'POST',
        headers: {
          'X-CSRFToken': csrftoken,
        },
        body: formData,
        credentials: 'include',
      });

      if (response.ok) {
        const Data = await response.json();
        console.log(Data);
        const formattedTranscription = Data.transcription
          .map((item) => `Speaker ${item.speaker}: ${item.text}`)
          .join('\n\n');

        console.log(formattedTranscription);
        alert('Files uploaded successfully!');
        demoData.append('result', formattedTranscription);

        // Convert formData to a plain object for demonstration purposes
        const formDataObject = {};
        demoData.forEach((value, key) => {
          formDataObject[key] = value;
        });
        console.log(demoData);
        console.log(formDataObject);
        console.log('navigating....');

        setIsSubmitting(false);
        navigate('/transcription/transcriptionresult', { state: { demoData: formDataObject } });
      } else {
        const errorData = await response.json();
        const errorMessage = errorData.error;
        alert(`Error: ${errorMessage}`);
        setIsSubmitting(false);
      }
    } catch (error) {
      alert('An error occurred while uploading files.');
      setIsSubmitting(false);
    }
  };

  return (
    <>
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

      <div className="container">
        {/* Left side: Input section */}
        <div className="input-section">
          <h3>Input your Email Address</h3>
          <p>Please enter your email address to receive your transcription results.</p>
          <input
            type="email"
            placeholder="Enter your email"
            value={email}
            onChange={handleEmailChange}
            required
          />
          {isEmailValid && (
            <span className="valid-email small-feedback">
              <img className="small-feedback" src={correctLog} alt="Valid email" />
            </span>
          )}
          <hr />

          <h3>Select a format for the output file</h3>
          <p>Please choose the desired file format for your transcription output.</p>
          <select name="outputFormat">
            <option value="docx">docx</option>
            <option value="pdf">pdf</option>
            <option value="txt">txt</option>
          </select>
          <hr />

          <h3>Select transcription language</h3>
          <p>Please choose the language in which you would like your transcribed text to be translated.</p>
          <select name="language">
            <option value="english">English</option>
            <option value="spanish">Spanish</option>
            <option value="french">French</option>
          </select>
        </div>

        {/* Right side: Upload section */}
        <div className="upload-section" onDragOver={(e) => e.preventDefault()} onDrop={handleDrop}>
          <h3>Upload file(s)</h3>
          <p>
            Our platform supports the following file formats:
            <strong>
              {' '}
              WAV (.wav), MP3 (.mp3), M4A (.m4a), FLAC (.flac), OGG (.ogg), AAC (.aac),
              MP4 (.mp4), AVI (.avi) and MOV (.mov)
            </strong>.
          </p>
          <hr />

          {files.length === 0 ? (
            <div className="upload-box">
              <input
                type="file"
                id="file-upload"
                accept=".wav,.mp3,.m4a,.flac,.ogg,.aac,.mp4,.avi,.mov"
                multiple
                onChange={handleFileChange}
                style={{ display: 'none' }}
              />
              <label htmlFor="file-upload" className="file-upload-label">
                <div className="upload-icon">&#8682;</div>
                <p>Drag a file(s) here or choose a file to upload</p>
              </label>
            </div>
          ) : (
            <>
              <div className="uploaded-files">
                <span className="file-add">
                  <h5>File Added:</h5>
                  <input
                    type="file"
                    id="file-upload"
                    accept=".wav,.mp3,.m4a,.flac,.ogg,.aac,.mp4,.avi,.mov"
                    multiple
                    onChange={handleFileChange}
                    style={{ display: 'none' }}
                    ref={fileInputRef}
                  />
                  <img
                    src={addLog}
                    alt="Add file"
                    className="add-icon"
                    onClick={() => fileInputRef.current.click()}
                    style={{ cursor: 'pointer' }}
                  />
                </span>

                <div className="file_area">
                  {files.map((file, index) => (
                    <div key={index} className="file-item">
                      <div className="file-info">
                        <span className="file-icon">
                          {file.type.startsWith('audio/')
                            ? '🎧'
                            : file.type.startsWith('video/')
                            ? '🎬'
                            : '📄'}
                        </span>
                        <span className="file-name">{file.name}</span>
                        <span className="file-size">
                          {(file.size / (1024 * 1024)).toFixed(1)}MB
                        </span>
                        <img
                          className="delete-button"
                          src={closeIcon}
                          alt="close icon"
                          onClick={() => handleDeleteFile(index)}
                          style={{ cursor: 'pointer', width: '16px', height: '16px' }}
                        />
                      </div>
                      <div className="file-progress">
                        <div
                          className={`progress-bar ${uploaded[index] ? 'uploaded' : ''}`}
                          style={{ width: `${uploadProgress[index]}%` }}
                        >
                          {uploadProgress[index]}%
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </>
          )}

          <hr />
          <div className="confirm-button">
            <button type="submit" onClick={handleConfirm} disabled={isSubmitting}>
              {isSubmitting ? 'Uploading...' : 'Confirm'}
            </button>
          </div>
        </div>
      </div>
    </>
  );
}

export default Transpage;
