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
    const value = e.target.value;
    setEmail(value);
    setIsEmailValid(/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value));
  };

  const handleConfirm = async () => {
    if (!isEmailValid) {
      alert('Please input a valid Email address.');
      return;
    }
    setIsSubmitting(true);

    const API =
      process.env.REACT_APP_API_URL || 'http://127.0.0.1:8000';

    try {
      const res = await fetch(
        `${API}/historylogin/api/send-history-link/`,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email }),
        },
      );
      const data = await res.json();

      if (res.ok) {
        setMessage(
          'A login link has been sent to your email. Please check your inbox.',
        );
      } else {
        setMessage(`Error: ${data.message}`);
      }
    } catch {
      setMessage('An error occurred while requesting access.');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <>
      {/* ── Header Navigation Section ─────────────────── */}

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

{/* ▼ Added history-wrapper to center this section locally ▼ */}
      <div className="history-wrapper">
        <div className="file-result">
          <h3>History Transcriptions</h3>
          <p>
            This section allows you to access your previously transcribed
            files. To maintain efficient storage, files older than 30&nbsp;days
            are automatically removed.
          </p>

          <h3>Input your Email Address</h3>
          <p>
            Please enter the email address you used for transcription. This will
            allow you to check your past transcription history.
          </p>

          <div className="email-input-row">
            <input
              type="email"
              placeholder="you@example.com"
              value={email}
              onChange={handleEmailChange}
              required
            />
            {isEmailValid && (
              <img
                className="small-feedback"
                src={correctLog}
                alt="Valid email"
              />
            )}
          </div>

          <button
            className="history-confirm-btn"
            onClick={handleConfirm}
            disabled={isSubmitting}
          >
            {isSubmitting ? 'Sending…' : 'Send Email'}
          </button>

          {message && <p className="message">{message}</p>}
        </div>
      </div>
    </>
  );
}

export default HistoryLogin;
