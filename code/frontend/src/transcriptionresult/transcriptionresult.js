// src/pages/TranscriptionResult.js

import React, { useState } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import jsPDF           from 'jspdf';
import { Document,
         Packer,
         Paragraph,
         TextRun }     from 'docx';

import './transcriptionresult.css';
import log          from '../resources/icon/logo.svg';
import downloadLogo from '../resources/icon/download.svg';

/* ─── Tool: Output in three formats ─── */
const genTXT  = (txt)      => new Blob([txt], { type: 'text/plain' });
const genPDF  = (txt)      => {
  const d = new jsPDF();
  d.text(d.splitTextToSize(txt, 180), 10, 10);
  return d.output('blob');
};
const genDOCX = async (txt) => {
  const doc = new Document({
    sections: [
      {
        children: txt.split('\n').map(line =>
          new Paragraph({ children: [ new TextRun(line) ] })
        )
      }
    ]
  });
  return Packer.toBlob(doc);
};
const getBlob = async (txt, fmt) =>
  fmt === 'pdf'   ? genPDF(txt)
  : fmt === 'docx'? await genDOCX(txt)
  : genTXT(txt);

/* ─── Tool: Format objects/arrays into plain text ─── */
const toPlain = (r) => {
  if (Array.isArray(r) && r.length > 0 && typeof r[0] === 'object') {
    return r
      .map(t => `Speaker ${t.speaker ?? ''}: ${t.text ?? ''}`)
      .join('\n\n');
  }
  if (typeof r === 'string') {
    return r;
  }
  // fallback: stringify other types
  return JSON.stringify(r, null, 2);
};

function TranscriptionResult() {
  const navigate = useNavigate();
  const location = useLocation();
  const { demoData = {} } = location.state || {};

  /* ─── Disassemble multiple files ─── */
  const files = Array.isArray(demoData.files)
    ? demoData.files
    : demoData.file
      ? [demoData.file]
      : [];
  const resultsRaw = Array.isArray(demoData.results)
    ? demoData.results
    : demoData.result
      ? [demoData.result]
      : [];

  /* ─── Convert to a plain text array ─── */
  const results = resultsRaw.map(toPlain);

  /* ─── Download status —— idx → boolean ─── */
  const [downloading, setDownloading] = useState({});

  const handleDownload = async (idx) => {
    if (downloading[idx]) return;
    try {
      setDownloading(s => ({ ...s, [idx]: true }));
      const text = results[idx] || '';
      const blob = await getBlob(text, demoData.outputFormat);
      const url  = URL.createObjectURL(blob);
      const a    = document.createElement('a');
      const base = files[idx]
        ? files[idx].name.replace(/\.[^/.]+$/, '')
        : `download_${idx}`;
      a.href     = url;
      a.download = `${base}.${demoData.outputFormat}`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    } catch (e) {
      console.error('Download failed:', e);
    } finally {
      setDownloading(s => ({ ...s, [idx]: false }));
    }
  };

  const downloadAll = () => {
    files.forEach((_, idx) => handleDownload(idx));
  };

  return (
    <>
      {/* — Navigation Bar — */}
      <div className="header">
        <div className="logo"><img src={log} alt="logo" /></div>
        <nav className="nav-links">
          <Link to="/about">About</Link>
          <Link to="/transcription">Transcription</Link>
          <Link to="/historylogin">History</Link>
        </nav>
      </div>

      {/* — Result subject — */}
      <div className="container2">
        <div className="file-result">
          <h3>Transcription Completed</h3>
          <p>
            The following file(s) have been transcribed and emailed to&nbsp;
            <strong>{demoData.email}</strong>
          </p>

          <table>
            <thead>
              <tr>
                <th>File Name</th>
                <th>Type</th>
                <th>Created</th>
                <th>Expires</th>
                <th>Output</th>
                <th>Status</th>
                <th>Download</th>
              </tr>
            </thead>
            <tbody>
              {files.map((file, idx) => (
                <tr key={idx}>
                  <td>{file.name.replace(/\.[^/.]+$/, '')}</td>
                  <td>
                    {file.type.startsWith('audio/') ? 'Audio'
                      : file.type.startsWith('video/') ? 'Video'
                      : 'File'
                    }
                  </td>
                  <td>
                    {new Date(file.lastModified).toLocaleDateString()}
                  </td>
                  <td>
                    {new Date(
                      file.lastModified + 30*24*3600*1000
                    ).toLocaleDateString()}
                  </td>
                  <td>{demoData.outputFormat}</td>
                  <td>
                    <span className="status-completed">Completed</span>
                  </td>
                  <td>
                    <button
                      className="download-small-btn"
                      onClick={() => handleDownload(idx)}
                      disabled={downloading[idx]}
                    >
                      <img
                        src={downloadLogo}
                        alt="dl"
                        className="download-icon"
                      />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>

          {/* — Batch download — */}
          {files.length > 1 && (
            <div className="download-area">
              <button
                className="download-big-btn"
                onClick={downloadAll}
                disabled={Object.values(downloading).some(v => v)}
              >
                <img
                  src={downloadLogo}
                  alt=""
                  className="download-icon"
                />
                &nbsp;{Object.values(downloading).some(v => v)
                  ? 'Downloading…'
                  : 'Download All'
                }
              </button>
            </div>
          )}
        </div>

        {/* — Bottom button — */}
        <div className="buttons buttons-with-gap">
          <div className="tooltip-wrapper">
            <button onClick={() => navigate('/historylogin')}>
              Transcription History
            </button>
            <span className="history-tooltip">
              View your transcription history from the last&nbsp;30&nbsp;days.
            </span>
          </div>
          <button onClick={() => navigate('/transcription')}>
            New Transcription
          </button>
        </div>
      </div>
    </>
  );
}

export default TranscriptionResult;