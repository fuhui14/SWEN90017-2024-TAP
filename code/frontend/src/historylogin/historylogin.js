import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import log from '../resources/icon/logo.svg';
import correctLog from '../resources/icon/correct.svg';
import './historylogin.css';

function HistoryLogin() {
  const [email, setEmail] = useState('');
  const [isEmailValid, setIsEmailValid] = useState(false);
  const [message, setMessage] = useState('');

  const handleEmailChange = (e) => {
    const value = e.target.value;
    setEmail(value);
    setIsEmailValid(/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value));
  };

  const handleConfirm = async () => {
    if (!isEmailValid) {
      alert("Please input a valid Email address.");
      return;
    }

    const API_BASE_URL = process.env.REACT_APP_API_URL || "http://127.0.0.1:8000";

    try {
      const response = await fetch(`${API_BASE_URL}/api/send-history-link/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email }),
      });

      const data = await response.json();
      if (response.ok) {
        setMessage("A login link has been sent to your email. Please check your inbox.");
      } else {
        setMessage(`Error: ${data.message}`);
      }
    } catch (error) {
      setMessage("An error occurred while requesting access.");
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
            {isEmailValid && <img className="small-feedback" src={correctLog} alt="Valid email" />}

          </div>
        </div>
            <button type="submit" onClick={handleConfirm}>View History</button>

            {message && <p className="message">{message}</p>} {/* 显示成功/错误信息 */}
      </>
  );
}

export default HistoryLogin;
