import './transpage.css';
import { Link } from 'react-router-dom'; // Add this import
import log from '../logo.svg';
import React, { useState } from 'react';

function Transpage() {
  const [email, setEmail] = useState(''); // State for email
  const [isEmailValid, setIsEmailValid] = useState(false); // State for email validation
  const [files, setFiles] = useState([]); // State for file uploads
  const [uploadProgress, setUploadProgress] = useState([]); // Track upload progress
  const [uploaded, setUploaded] = useState([]); // Track upload completion

  const handleEmailChange = (e) => {
    const value = e.target.value;
    setEmail(value);
    // Simple regex for email validation
    setIsEmailValid(/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value));
  };

  const handleFileChange = (e) => {
    const newFiles = [...e.target.files]; // Get new files
    setFiles(newFiles); // Update files state
    
    // Simulate file upload progress for each file
    const progressArray = new Array(newFiles.length).fill(0);
    setUploadProgress(progressArray);
    
    // Simulate file upload for each file
    newFiles.forEach((file, index) => {
      simulateUpload(file, index);
    });
  };

  const simulateUpload = (file, index) => {
    // Simulate upload progress using intervals
    const interval = setInterval(() => {
      setUploadProgress((prevProgress) => {
        const updatedProgress = [...prevProgress];
        if (updatedProgress[index] < 100) {
          updatedProgress[index] += 49; // Increase progress by 10%
        } else {
          clearInterval(interval); // Clear interval when upload completes
          setUploaded((prevUploaded) => {
            const updatedUploaded = [...prevUploaded];
            updatedUploaded[index] = true; // Mark as uploaded
            return updatedUploaded;
          });
        }
        return updatedProgress;
      });
    }, 500); // Simulate progress every 0.5 seconds
  };

  const handleDrop = (e) => {
    e.preventDefault(); // Prevent default behavior
    const droppedFiles = e.dataTransfer.files; // Get files from dataTransfer
    handleFileChange({ target: { files: droppedFiles } }); // Call handleFileChange with dropped files
  };

  const handleDeleteFile = (index) => {
    const updatedFiles = files.filter((_, i) => i !== index); // Remove file at the specified index
    setFiles(updatedFiles); // Update files state

    // Update progress and uploaded arrays when deleting files
    const updatedProgress = uploadProgress.filter((_, i) => i !== index);
    setUploadProgress(updatedProgress);

    const updatedUploaded = uploaded.filter((_, i) => i !== index);
    setUploaded(updatedUploaded);
  };

  const handleConfirm = () => {
    if (!isEmailValid || files.length === 0) {
      alert("Please fill out all required fields."); // Alert for missing fields
      return;
    }
    // Proceed with form submission logic
    alert("Files uploaded successfully!"); // Confirmation message
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
          <Link to="/history">History</Link>
        </nav>
      </div>

      <div className="container">
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
          {isEmailValid && 
          <span className="valid-email">✔️</span>} {/* Validation feedback */}
          <h3>Select a format for the output file</h3>
          <select name="outputFormat">
            <option value="docx">docx</option>
            <option value="pdf">pdf</option>
            <option value="txt">txt</option>
          </select>

          <h3>Select transcription language</h3>
          <p>Please choose the language in which you would like your transcribed text to be translated.</p>
          <select name="language">
            <option value="english">English</option>
            <option value="spanish">Spanish</option>
            <option value="french">French</option>
          </select>
        </div>

        <div 
          className="upload-section"
          onDragOver={(e) => e.preventDefault()} // Prevent default behavior
          onDrop={handleDrop}
          style={{ position: 'relative' }} // Ensure the upload section is positioned relatively
          > 
          
          <h3>Upload</h3>
          <p>
            Our platform supports the following file formats:<strong> WAV (.wav), MP3 (.mp3), M4A (.m4a), FLAC (.flac), OGG (.ogg), and AAC (.aac)</strong>.
          </p>
          {/* Display uploaded files */}
          {files.length === 0 ? (
            <div className="upload-box">
              <input 
                type="file" 
                id="file-upload"
                accept=".wav,.mp3,.m4a,.flac,.ogg,.aac"
                multiple  
                onChange={handleFileChange} // Handle file change
                style={{ display: 'none' }}
              />
              <label htmlFor="file-upload" className="file-upload-label">
                <div className="upload-icon">&#8682;</div>
                <p>Drag a file here or choose a file to upload</p>
              </label>
            </div>
          ) : (
            <div className="uploaded-files">
              <h5>File Added:</h5>
              <ul className='file_area'>
                {Array.from(files).map((file, index) => (
                  <div key={index} className="file-item">
                    <div className="file-info">
                      <span className="file-icon">
                        {file.type.startsWith('audio/') ? '🎧' : file.type.startsWith('video/') ? '🎬' : '📄'}
                      </span>
                      <span className="file-name">{file.name}</span>
                      <span className="file-size">{(file.size / (1024 * 1024)).toFixed(1)}MB</span>
                      <button className="delete-button" onClick={() => handleDeleteFile(index)}>
                        &times; {/* Close icon */}
                      </button>
                    </div>
                    <div className="file-progress">
                      <div
                        className={`progress-bar ${uploaded[index] ? 'uploaded' : ''}`}
                        style={{
                          width: `${uploadProgress[index]}%`,  // Update the width based on upload progress
                        }}
                      >
                        {uploadProgress[index]}%
                      </div>
                    </div>
                  </div>
                ))}
              </ul>
            </div>
          )}
          <div className="confirm-button">
            <button type="submit" onClick={handleConfirm}>Confirm</button>{/* Updated button to handle confirmation */}
          </div>
        </div>
      </div>
    </>
  );
}

export default Transpage;
