import './transpage.css';
import { Link , useNavigate } from 'react-router-dom';
import log from '../resources/icon/logo.svg';
import addLog from '../resources/icon/add.svg';
import correctLog from '../resources/icon/correct.svg';
import React, { useState } from 'react';

function Transpage() {
  const [email, setEmail] = useState(''); // State for email
  const [isEmailValid, setIsEmailValid] = useState(false); // State for email validation
  const [files, setFiles] = useState([]); // State for file uploads
  const [uploadProgress, setUploadProgress] = useState([]); // Track upload progress
  const [uploaded, setUploaded] = useState([]); // Track upload completion
  const navigate = useNavigate(); // Initialize useHistory
  const fileInputRef = React.useRef(null); // Create a ref for the file input

  // Handle changes to the email input field
  const handleEmailChange = (e) => {
    const value = e.target.value;
    setEmail(value);
    // Simple regex for email validation
    setIsEmailValid(/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value));
  };

   // Handle changes to the email input field
   const handleFileChange = (e) => {
    const newFiles = [...e.target.files]; // Get new files
    setFiles((prevFiles) => [...prevFiles, ...newFiles]); // Update files state to keep previous files
    
    // Simulate file upload progress for each file
    const progressArray = new Array(newFiles.length + files.length).fill(0); // Adjust progress array size
    setUploadProgress(progressArray);
    
    // Simulate file upload for each file
    [...files, ...newFiles].forEach((file, index) => {
      // Check if the file has already been uploaded
      if (uploaded[index]) {
        // If already uploaded, set progress to 100%
        setUploadProgress((prevProgress) => {
          const updatedProgress = [...prevProgress];
          updatedProgress[index] = 100; // Set progress to 100% for uploaded files
          return updatedProgress;
        });
      } else {
        simulateUpload(file, index); // Simulate upload for new files
      }
    });
  };

  // Simulate the upload process for a file
  const simulateUpload = (file, index) => {
    // Simulate upload progress using intervals
    const interval = setInterval(() => {
      setUploadProgress((prevProgress) => {
        const updatedProgress = [...prevProgress];
        if (updatedProgress[index] < 100) {
          updatedProgress[index] += 49; // Increase progress
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

  // Handle file drop events
  const handleDrop = (e) => {
    e.preventDefault(); // Prevent default behavior
    const droppedFiles = e.dataTransfer.files; // Get files from dataTransfer
    handleFileChange({ target: { files: droppedFiles } }); // Call handleFileChange with dropped files
  };

  // Handle the deletion of a file from the upload list
  const handleDeleteFile = (index) => {
    const updatedFiles = files.filter((_, i) => i !== index); // Remove file at the specified index
    setFiles(updatedFiles); // Update files state

    // Update progress and uploaded arrays when deleting files
    const updatedProgress = uploadProgress.filter((_, i) => i !== index);
    setUploadProgress(updatedProgress);

    const updatedUploaded = uploaded.filter((_, i) => i !== index);
    setUploaded(updatedUploaded);
  };

  // Function to obtain a CSRF token from cookies
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        // Determine whether this cookie string starts with the name we want
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  // Handle the confirmation of the upload process
  const handleConfirm = async () => {
    if (!isEmailValid || files.length === 0) {
      alert("Please fill out all required fields."); // Alert for missing fields
      return;
    }

    //for demo usage only
    const demoData = new FormData();

    // Prepare the form data
    const formData = new FormData();
    formData.append('email', email);
    demoData.append('email', email);
    files.forEach((file) => {
      formData.append('file', file); // Append each file
    });

    files.forEach((file) => {
      demoData.append('file', file); // Append each file
    });
    const outputFormat = document.querySelector('select[name="outputFormat"]').value; // Get selected output format
    const language = document.querySelector('select[name="language"]').value; // Get selected language
    formData.append('outputFormat', outputFormat);
    formData.append('language', language);

    demoData.append('outputFormat', outputFormat);
    demoData.append('language', language);

    console.log("files: ");
    console.log(files);

    // 获取 CSRF 令牌
    const csrftoken = getCookie('csrftoken');

    // Send data to the backend
    try {
      const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://127.0.0.1:8000'; 
      const response = await fetch(`${API_BASE_URL}/transcription/`, {
        method: 'POST',
        headers: {
          'X-CSRFToken': csrftoken, // Add CSRF token to request header
        },
        body: formData,
        credentials: 'include', // Contains credentials (cookies, etc.)
      });

      if (response.ok) {
        const Data = await response.json();
        console.log(Data);

        // Format the transcription into a conversation style
        const formattedTranscription = Data.transcription.map(item => 
          `Speaker ${item.speaker}: ${item.text}`).join('\n\n');
        console.log(formattedTranscription);
        alert("Files uploaded successfully!"); // Confirmation message
        demoData.append('result', formattedTranscription);
        //----------------------------------------------------
        //---------This part is only for the demo use---------
        // Convert formData to a plain object
        const formDataObject = {};
        demoData.forEach((value, key) => {
          formDataObject[key] = value;
        });
        console.log(demoData);
        console.log(formDataObject);
        console.log("navigating....");
        navigate('/transcription/transcriptionresult', { state: { demoData: formDataObject } }); // Pass formData as state
        //----------------------------------------------------
      } else {
        const errorData = await response.json();
        const errorMessage = errorData.error
        alert(`Error: ${errorMessage}`); // Handle error response
      }
    } catch (error) {
      alert("An error occurred while uploading files."); // Handle network errors
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
          <span className="valid-email small-feedback">
            <img className="small-feedback" src={correctLog}
                  alt="Valid email" ></img>
            </span>} {/* Validation feedback */}
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
          
          <h3>Upload file(s)</h3>
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
                <p>Drag a file(s) here or choose a file to upload</p>
              </label>
            </div>
          ) : (
            <div className="uploaded-files">
              <span className='file-add'>
                <h5>File Added:</h5>
                {/* <img src={addLog} alt="add" className="add-icon" /> */}
                <input 
                  type="file" 
                  id="file-upload"
                  accept=".wav,.mp3,.m4a,.flac,.ogg,.aac"
                  multiple  
                  onChange={handleFileChange} // Handle file change
                  style={{ display: 'none' }}
                  ref={fileInputRef} // Attach the ref to the file input
                />
                <img 
                  src={addLog} 
                  alt="Add file" 
                  className="add-icon" 
                  onClick={() => fileInputRef.current.click()} // Trigger file input click
                  style={{ cursor: 'pointer' }} // Change cursor to pointer for better UX
                />
                </span>
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
