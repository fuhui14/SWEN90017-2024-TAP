import React, { useEffect, useState } from 'react';
import { Link, useSearchParams }    from 'react-router-dom';
import log          from '../resources/icon/logo.svg';
import downloadLogo from '../resources/icon/download.svg';
import './history.css';

function History() {
  /* ---------------- state ---------------- */
  const [searchParams]       = useSearchParams();
  const [historyData, setHistoryData] = useState([]);
  const [loading,     setLoading]     = useState(true);
  const [error,       setError]       = useState(null);
  const [currentPage, setCurrentPage] = useState(1);
  const recordsPerPage = 10;
  const encrypted = searchParams.get('enc');   // token in url

  /* ---------------- fetch ---------------- */
  useEffect(() => {
    if (!encrypted) {
      setError('Invalid or expired link.');
      setLoading(false);
      return;
    }
    fetch("http://127.0.0.1:8000/history/api/admin/history/", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ enc: encrypted }),
  })
    .then(res => res.json())
    .then(data => {
      /* sort newest → oldest */
      data.sort(
        (a, b) => new Date(b.creationDate) - new Date(a.creationDate)
      );

      setHistoryData(data);   // update status
      setLoading(false);
    })
    .catch(() => {
      setError("Failed to load history data.");
      setLoading(false);
    });
}, [encrypted]);

  /* reset page when data changes */
  useEffect(() => setCurrentPage(1), [historyData]);

  /* ---------------- download handler ---------------- */
  const handleDownload = async (id, orig) => {
    try{
      const res = await fetch('http://127.0.0.1:8000/history/api/download/', {
        method : 'POST',
        headers: { 'Content-Type': 'application/json' },
        body   : JSON.stringify({ id })
      });
      if(!res.ok) throw new Error();
      const blob = await res.blob();
      const url  = window.URL.createObjectURL(blob);
      const a    = document.createElement('a');
      a.href     = url;
      a.download = (orig || 'transcription') + '.txt';
      document.body.appendChild(a); a.click(); a.remove();
      window.URL.revokeObjectURL(url);
    }catch{ alert('Download failed — please try again.'); }
  };

  /* ---------------- pagination helpers ---------------- */
  const totalPages         = Math.ceil(historyData.length / recordsPerPage) || 1;
  const indexOfLastRecord  = currentPage * recordsPerPage;
  const currentRecords     = historyData.slice(indexOfLastRecord - recordsPerPage, indexOfLastRecord);

  /* ---------------- render ---------------- */
  return (
    <>
      {/* top nav */}
      <div className="header">
        <div className="logo"><img src={log} alt="logo" /></div>
        <nav className="nav-links">
          <Link to="/about">About</Link>
          <Link to="/transcription">Transcription</Link>
          <Link to="/historylogin">History</Link>
        </nav>
      </div>

      {/* only this wrapper is new; gives local centering */}
      <div className="history-wrapper">
        <div className="file-result">
          <h1>History Transcriptions</h1>
          <p>
            This section displays your past transcription tasks. Files are kept
            for 30&nbsp;days and can be downloaded here.
          </p>

          {loading &&  <p className="loading">Loading…</p>}
          {error   &&  <div className="error">{error}</div>}

          {!loading && !error && historyData.length > 0 && (
            <>
              <table>
                <thead>
                  <tr>
                    <th>Task&nbsp;Name</th>
                    <th>Type</th>
                    <th>Created</th>
                    <th>Days&nbsp;Left</th>
                    <th>Output</th>
                    <th>Status</th>
                    <th>Download</th>
                  </tr>
                </thead>
                <tbody>
                  {currentRecords.map(rec=>(
                    <tr key={rec.id}>
                      <td>{rec.taskName}</td>
                      <td>{rec.taskType}</td>
                      <td>{new Date(rec.creationDate).toLocaleDateString()}</td>
                      <td>{rec.daysLeft}</td>
                      <td>{rec.outputType}</td>
                      <td>
                        <span className={`status ${rec.status.toLowerCase()}`}>
                          {rec.status}
                        </span>
                      </td>
                      <td>
                        {rec.status === 'Completed'
                          ? <button className="download-btn"
                                    onClick={()=>handleDownload(rec.id, rec.taskName)}>
                                <img src={downloadLogo} alt="→" className="download-icon"/>
                            </button>
                          : <span className="no-download">—</span>}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>

              {/* pagination */}
              {totalPages > 1 && (
                <div className="pagination">
                  <button onClick={()=>setCurrentPage(p=>Math.max(1, p-1))}
                          disabled={currentPage===1}>Prev</button>

                  {Array.from({length:totalPages},(_,i)=>i+1).map(n=>(
                    <button key={n}
                            className={currentPage===n ? 'active' : ''}
                            onClick={()=>setCurrentPage(n)}>{n}</button>
                  ))}

                  <button onClick={()=>setCurrentPage(p=>Math.min(totalPages, p+1))}
                          disabled={currentPage===totalPages}>Next</button>
                </div>
              )}
            </>
          )}

          {!loading && !error && historyData.length === 0 && (
            <p className="no-history">No transcription history available.</p>
          )}
        </div>
      </div>
    </>
  );
}

export default History;
