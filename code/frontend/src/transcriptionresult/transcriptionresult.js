import React from "react";
import './transcriptionresult.css';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import log from '../resources/icon/logo.svg';
import downloadLogo from '../resources/icon/download.svg';

function TranscriptionResult() {
  const navigate = useNavigate();
  const location = useLocation();
  const { demoData = {} } = location.state || {};
  console.log(demoData);

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
      <div className="container2">
        <div className="file-result">
          <h3>Transcription Finished</h3>
          <p>
            The following file(s) have been transcribed and have been sent to the email address: {demoData.email}.
          </p>
          <table>
            <thead>
              <tr>
                <th>File Name</th>
                <th>Task Format</th>
                <th>Creation Date</th>
                <th>Expiry Date</th>
                <th>Output Type</th>
                <th>Status</th>
                <th>Download</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                {demoData.file ? (
                  <td>{demoData.file.name.replace(/\.[^/.]+$/, '')}</td>
                ) : (
                  <td>Unknown file</td>
                )}
                <td>
                  {demoData.file && demoData.file.type.startsWith('audio/')
                    ? 'Audio'
                    : demoData.file && demoData.file.type.startsWith('video/')
                    ? 'Video'
                    : 'File'}
                </td>
                <td>
                  {demoData.file &&
                    new Date(demoData.file.lastModifiedDate).toLocaleDateString('en-GB', {
                      day: '2-digit',
                      month: 'short',
                      year: 'numeric',
                    })}
                </td>
                <td>
                  {demoData.file &&
                    new Date(
                      new Date(demoData.file.lastModifiedDate).setMonth(new Date(demoData.file.lastModifiedDate).getMonth() + 1)
                    ).toLocaleDateString('en-GB', {
                      day: '2-digit',
                      month: 'short',
                      year: 'numeric',
                    })}
                </td>
                <td>{demoData.outputFormat}</td>
                <td>
                  <span className="status-completed">Completed</span>
                </td>
                <td>
                  <a
                    href={URL.createObjectURL(
                      new Blob([demoData.result], { type: demoData.outputFormat })
                    )}
                    download={`${demoData.file ? demoData.file.name.replace(/\.[^/.]+$/, '') : 'download'}.${demoData.outputFormat}`}
                  >
                    <img src={downloadLogo} alt="Download" className="download-icon" />
                  </a>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <div className="buttons">
          <button>Go to History Section</button>
          <button onClick={() => navigate('/transcription')}>Transcribe a New Task</button>
        </div>
      </div>
    </>
  );
}

export default TranscriptionResult;
