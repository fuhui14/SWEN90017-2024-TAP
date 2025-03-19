import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import log from '../resources/icon/logo.svg';
import correctLog from '../resources/icon/correct.svg';
import './historylogin.css';

function HistoryLogin(){
  const [email, setEmail] = useState(''); // State for email
  const [isEmailValid, setIsEmailValid] = useState(false); // State for email validation

    // Handle changes to the email input field
    const handleEmailChange = (e) => {
      const value = e.target.value;
      setEmail(value);
      // Simple regex for email validation
      setIsEmailValid(/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value));
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
    if (!isEmailValid) {
      alert("Please input valid Email address."); // Alert for missing fields
      return;
    }

    // Prepare the form data
    const formData = new FormData();
    formData.append('email', email);

    // 获取 CSRF 令牌
    const csrftoken = getCookie('csrftoken');

    // Send data to the backend
    try {
      const API_BASE_URL = process.env.REACT_APP_API_URL;
      const response = await fetch(`${API_BASE_URL}/history/`, {
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

        alert("Data recieved successfully!"); // Confirmation message

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
              <Link to="/historylogin">History</Link>
            </nav>
          </div>
    
          <div className="container">
            <div className="file-result">
              <h3>History Transcriptions</h3>
              <p>This section allows users to access their previously transcribed files. 
                To maintain efficient storage and remove outdated data, 
                the system automatically deletes transcriptions older than 30 days, 
                ensuring that only recent and relevant files are retained for easy access.</p>

                  <h3>Input your Email Address</h3>
                  <p>Please enter the email address you used for transcription. 
                    This will allow you to check your past transcription history.</p>
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

            </div>
          </div>
          <button type="submit" onClick={handleConfirm}>View History</button>{/* Updated button to handle confirmation */}
        </>
      );
}
export default HistoryLogin;