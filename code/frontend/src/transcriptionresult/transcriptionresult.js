import React, { useState } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import jsPDF from 'jspdf';
import { Document, Packer, Paragraph, TextRun } from 'docx';

import './transcriptionresult.css';
import log from '../resources/icon/logo.svg';
import downloadLogo from '../resources/icon/download.svg';

function TranscriptionResult() {
  const navigate = useNavigate();
  const location = useLocation();
  const { demoData = {} } = location.state || {};
  const [isDownloading, setIsDownloading] = useState(false);

  /* ---------- 生成各种格式 ---------- */
  const generateTXT = (t) => new Blob([t], { type: 'text/plain' });
  const generatePDF = (t) => {
    const doc = new jsPDF();
    doc.text(doc.splitTextToSize(t, 180), 10, 10);
    return doc.output('blob');
  };
  const generateDOCX = async (t) => {
    const doc = new Document({
      sections: [
        {
          children: t.split('\n').map(
            (line) =>
              new Paragraph({
                children: [new TextRun(line)],
              }),
          ),
        },
      ],
    });
    return Packer.toBlob(doc);
  };
  const getBlob = async (txt, fmt) =>
    fmt === 'pdf'
      ? generatePDF(txt)
      : fmt === 'docx'
      ? await generateDOCX(txt)
      : generateTXT(txt);

  /* ---------- 点击下载 ---------- */
  const handleDownload = async () => {
    if (isDownloading) return;
    try {
      setIsDownloading(true);
      const blob = await getBlob(demoData.result, demoData.outputFormat);
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `${
        demoData.file
          ? demoData.file.name.replace(/\.[^/.]+$/, '')
          : 'download'
      }.${demoData.outputFormat}`;
      document.body.appendChild(a);
      a.click();
      a.remove();
      URL.revokeObjectURL(url);
    } catch (e) {
      console.error('Download failed:', e);
    } finally {
      setIsDownloading(false);
    }
  };

  return (
    <>
      {/* ---------- 顶部导航 ---------- */}
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

      {/* ---------- 结果主体 ---------- */}
      <div className="container2">
        <div className="file-result">
          <h3>Transcription Completed</h3>
          <p>
            The following file(s) have been transcribed and sent to:&nbsp;
            {demoData.email}
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
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>
                  {demoData.file
                    ? demoData.file.name.replace(/\.[^/.]+$/, '')
                    : 'Unknown file'}
                </td>
                <td>
                  {demoData.file?.type.startsWith('audio/')
                    ? 'Audio'
                    : demoData.file?.type.startsWith('video/')
                    ? 'Video'
                    : 'File'}
                </td>
                <td>
                  {demoData.file &&
                    new Date(
                      demoData.file.lastModifiedDate,
                    ).toLocaleDateString('en-GB', {
                      day: '2-digit',
                      month: 'short',
                      year: 'numeric',
                    })}
                </td>
                <td>
                  {demoData.file &&
                    new Date(
                      new Date(
                        demoData.file.lastModifiedDate,
                      ).setMonth(
                        new Date(
                          demoData.file.lastModifiedDate,
                        ).getMonth() + 1,
                      ),
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
              </tr>
            </tbody>
          </table>

          {/* ---- 表格下方醒目的下载按钮 ---- */}
          <div className="download-area">
            <button
              className="download-big-btn"
              onClick={handleDownload}
              disabled={isDownloading}
            >
              <img src={downloadLogo} alt="" className="download-icon" />
              &nbsp;{isDownloading ? 'Downloading…' : 'Download'}
            </button>
          </div>
        </div>

        {/* 底部两个操作按钮 */}
        <div className="buttons buttons-with-gap">
          <div className="tooltip-wrapper">
            <button onClick={() => navigate('/historylogin')}>
              Transcription History
            </button>
            <span className="history-tooltip">
              Click to browse your transcription history.<br />
              (Records are kept for the last&nbsp;30&nbsp;days)
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
