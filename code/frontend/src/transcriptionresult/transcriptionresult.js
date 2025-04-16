import React, { useState } from "react";
import './transcriptionresult.css';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import log from '../resources/icon/logo.svg';
import downloadLogo from '../resources/icon/download.svg';
import jsPDF from 'jspdf';
import { Document, Packer, Paragraph, TextRun } from 'docx';

function TranscriptionResult() {
  const navigate = useNavigate();
  const location = useLocation();
  const { demoData = {} } = location.state || {};
  const [isDownloading, setIsDownloading] = useState(false);

  console.log(demoData);

  // Generate TXT
  const generateTXTBlob = (text) => {
    return new Blob([text], { type: 'text/plain' });
  };

  // Generate PDF
  const generatePDFBlob = (text) => {
    const doc = new jsPDF();
    const lines = doc.splitTextToSize(text, 180);
    doc.text(lines, 10, 10);
    return doc.output('blob');
  };

  // Generate DOCX
  const generateDOCXBlob = async (text) => {
    const doc = new Document({
      sections: [
        {
          properties: {},
          children: text.split('\n').map(
            line => new Paragraph({
              children: [new TextRun(line)],
            })
          ),
        },
      ],
    });

    const blob = await Packer.toBlob(doc);
    return blob;
  };

  // Dispatcher
  const generateBlobByFormat = async (text, format) => {
    switch (format) {
      case 'txt':
        return generateTXTBlob(text);
      case 'pdf':
        return generatePDFBlob(text);
      case 'docx':
        return await generateDOCXBlob(text);
      default:
        return generateTXTBlob(text);
    }
  };

  const handleDownload = async () => {
    if (isDownloading) return;

    try {
      setIsDownloading(true);
      const blob = await generateBlobByFormat(demoData.result, demoData.outputFormat);
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      const filename = `${demoData.file ? demoData.file.name.replace(/\.[^/.]+$/, '') : 'download'}.${demoData.outputFormat}`;

      link.href = url;
      link.download = filename;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      URL.revokeObjectURL(url);
    } catch (error) {
      console.error("Download failed:", error);
    } finally {
      setIsDownloading(false);
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
      <div className="container2">
        <div className="file-result">
          <h3>Transcription Completed</h3>
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
                <td>{demoData.file ? demoData.file.name.replace(/\.[^/.]+$/, '') : 'Unknown file'}</td>
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
                  <button onClick={handleDownload} disabled={isDownloading}>
                    <img src={downloadLogo} alt="Download" className="download-icon" />
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <div className="buttons">
          <button onClick={() => navigate('/historylogin')}>Transcription History</button>
          <button onClick={() => navigate('/transcription')}>New Transcription</button>
        </div>
      </div>
    </>
  );
}

export default TranscriptionResult;