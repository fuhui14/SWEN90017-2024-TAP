import React from "react";
import { Link, useNavigate, useLocation} from 'react-router-dom';
import log from '../resources/icon/logo.svg';
import downloadLogo from '../resources/icon/download.svg';

function History(){
    const navigate = useNavigate(); // Initialize useHistory
    const location = useLocation(); // Get location object
    const { demoData = {} } = location.state || {}; // 防止 location.state 为 undefined
    console.log(demoData); // You can use formData as needed
    
       // 防止直接访问页面时 location.state 为空
       if (!location.state) {
        return <div style={{ textAlign: "center", padding: "20px" }}>
            <h3>No data available.</h3>
            <p>Please transcribe a file first.</p>
            <button onClick={() => navigate('/transcription')}>Go to Transcription</button>
        </div>;
    }
    
    return(
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
                    <p>The following file(s) have been transcribed and have been sent to the email address: ${demoData.email}.</p>
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
                                    {demoData.file.type.startsWith('audio/') ? 
                                    'Audio' : demoData.file.type.startsWith('video/') ? 
                                    'Video' : 'File'}
                                    </td>
                                    <td>{demoData.file.lastModifiedDate.toLocaleDateString('en-GB', 
                                        { day: '2-digit', 
                                        month: 'short', 
                                        year: 'numeric' })}
                                    </td>
                                    <td>{new Date(demoData.file.lastModifiedDate.setMonth(demoData.file.lastModifiedDate.getMonth() + 1)).toLocaleDateString('en-GB', 
                                        { day: '2-digit', 
                                        month: 'short', 
                                        year: 'numeric' })}</td>
                                    <td>{demoData.outputFormat}</td>
                                    <td><span className="status-completed">Completed</span></td>
                                    <td>
                                        <a href={URL.createObjectURL(new Blob([demoData.result], 
                                            { type: demoData.outputFormat }))} 
                                                download={`${demoData.file.name.replace(/\.[^/.]+$/, '')}.${demoData.outputFormat}`}>
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
}export default History;
