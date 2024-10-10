import React from "react";
import './process.css';
import { Link , useNavigate} from 'react-router-dom';
import log from '../logo-blue.png';

function Process(){
    const navigate = useNavigate(); // Initialize useHistory
    return(
        <>
            <div className="header">
                <div className="logo">
                    <img src={log} alt="logo" />
                </div>
            <nav className="nav-links">
                <Link to="/about">About</Link>
                <Link to="/transcription">Transcription</Link>
                <Link to="/history">History</Link>
            </nav>
            </div>
            <div className="container1">
                <div className="process-status">
                    <span><h3>Status...</h3></span>
                    <span><p>Your place in the queue is: </p></span>
                    <span><p>Estimate time: </p></span>
                </div>

                <div className="file-process">
                    <p>The file(s) is currently being processed. 
                        Once the transcription is complete, 
                        it will be automatically sent to your email address.</p>
                        <ul>
                            file lists in here....
                        </ul>
                </div>

                <div className="buttons">
                    <button>Go to History Section</button>
                    <button onClick={() => navigate('/transcription')}>Transcribe a New Task</button>
                </div>
            </div>
        </>
    );
}export default Process;