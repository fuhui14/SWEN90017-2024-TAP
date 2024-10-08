import React from 'react';
import './transpage.css';
import { Link } from 'react-router-dom'; // Add this import
import log from '../logo.svg'

function Transpage(){
  return (
    <>
        <div className="header">
            <div className="logo">
              <img src={log} alt="logo"/>
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
              <input type="email" placeholder="Email Address" />
    
              <h3>Select a format for the output file</h3>
              <select>
                <option value="docx">docx.</option>
                <option value="pdf">pdf</option>
                <option value="txt">txt</option>
              </select>
    
              <h3>Select transcription language</h3>
              <p>Please choose the language in which you would like your transcribed text to be translated.</p>
              <select>
                <option value="english">English</option>
                <option value="spanish">Spanish</option>
                <option value="french">French</option>
              </select>
            </div>
    
            <div className="upload-section">
              <h3>Upload</h3>
              <p>
                Our platform supports the following file formats: WAV (.wav), MP3 (.mp3), M4A (.m4a), FLAC (.flac), OGG
                (.ogg), and AAC (.aac).
              </p>
              <div className="upload-box">
                <input type="file" id="file-upload" />
                <label htmlFor="file-upload" className="file-upload-label">
                  <div className="upload-icon">&#8682;</div>
                  <p>Drag a file here or choose a file to upload</p>
                </label>
              </div>
            </div>
          </div>
    
          <div className="confirm-button">
            <button>Confirm</button>
          </div>
      </>
  );
}

export default Transpage;