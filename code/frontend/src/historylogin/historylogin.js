import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import log from '../resources/icon/logo.svg';
import correctLog from '../resources/icon/correct.svg';
import './historylogin.css';

function HistoryLogin() {
  const [email, setEmail] = useState('');
  const [isEmailValid, setIsEmailValid] = useState(false);
  const [message, setMessage] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleEmailChange = (e) => {
    const v = e.target.value;
    setEmail(v);
    setIsEmailValid(/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v));
  };

  const handleConfirm = async () => {
    if (!isEmailValid) { alert('Please input a valid Email address.'); return; }
    setIsSubmitting(true);

    try {
      const API = process.env.REACT_APP_API_URL || 'http://127.0.0.1:8000';
      const res = await fetch(`${API}/api/send-history-link/`, {
        method:'POST',
        headers:{ 'Content-Type':'application/json' },
        body: JSON.stringify({ email }),
      });
      const data = await res.json();
      setMessage(res.ok
        ? 'A login link has been sent to your email. Please check your inbox.'
        : `Error: ${data.message}`,
      );
    } catch {
      setMessage('An error occurred while requesting access.');
    } finally { setIsSubmitting(false); }
  };

  /* ---------- 页面渲染 ---------- */
  return (
    <>
      {/* 顶部导航 */}
      <div className="header">
        <div className="logo"><img src={log} alt="logo" /></div>
        <nav className="nav-links">
          <Link to="/about">About</Link>
          <Link to="/transcription">Transcription</Link>
          <Link to="/historylogin">History</Link>
        </nav>
      </div>

      {/* 主体内容 */}
      <div className="history-wrapper">
        <h3>History Transcriptions</h3>
        <p>
          This section allows you to access your previously transcribed files.
          To maintain efficient storage, files older than 30 days are
          automatically removed.
        </p>

        <h3>Input your Email Address</h3>
        <p>
          Please enter the email address you used for transcription.
          This will allow you to check your past transcription history.
        </p>

        <div style={{ display:'flex', justifyContent:'center', alignItems:'center' }}>
          <input
            type="email"
            placeholder="Enter your email"
            value={email}
            onChange={handleEmailChange}
            required
          />
          {isEmailValid && <img src={correctLog} alt="valid" className="small-feedback" />}
        </div>

        <div className="confirm-button">
          <button onClick={handleConfirm} disabled={isSubmitting}>
            {isSubmitting ? 'Sending…' : 'Send the Email'}
          </button>
        </div>

        {message && <p className="message">{message}</p>}
      </div>
    </>
  );
}

export default HistoryLogin;
