import React from "react";
import { Link, useLocation} from 'react-router-dom';
import log from '../resources/icon/logo.svg';
import file_upload_icon from '../resources/icon/file.png';
import arrow from '../resources/icon/arrow.png';
import transcribe_icon from '../resources/icon/live-transcribe-svgrepo-com.svg';
import result_icon from '../resources/icon/test-data-svgrepo-com.svg';

import "./about.css"

function About(){
    const location = useLocation(); // Get location object
    const { demoData = {} } = location.state || {}; // Prevent location.state from being undefined
    console.log(demoData); // You can use formData as needed
    return(
        <>
            <div className="header">
                <div className="logo">
                    <img src={log} alt="logo" />
                </div>
            <nav className="nav-links">
                <Link to="/about">Home</Link>
                <Link to="/transcription">Transcription</Link>
                <Link to="/historylogin">History</Link>
            </nav>
            </div>
            <hr/>
            <section  className="hero-section">
                <h3>Transcription Aide Platform</h3>
                <p>Everything you need to transcribe audio files,
                    at your fingertips. Our platform is 100% free and easy to use!
                    Upload, process, and receive your transcriptions with just
                    a few clicks — no login required. Identify different speakers,
                    handle multiple files, and receive results directly via email.</p>
            </section >

            {/* Tools Section */}
            <section className="tools-section">
                <h2>All the tools you need for transcription in one place</h2>
                <div className="tools-cards">
                    <div className="tool-card">
                        <Link to="/Transcription">
                        <div className="about-logo">
                            <h3>Upload your files</h3>
                            <img src={file_upload_icon} alt="file_upload_icon" />
                        </div>
                        </Link>
                        <p>Upload your audio files from your device or from any cloud storage platform.</p>
                    </div>

                    <div className="arrow-log">
                        <img src={arrow} alt="arrow" />
                    </div>

                    <div className="tool-card">
                        <Link to="/Transcription">
                        <div className="about-logo">
                            <h3>Transcribe</h3>
                            <img src={transcribe_icon} alt="transcribe_icon" />
                        </div>
                        </Link>
                        <p>Process your files using our advanced speech recognition and speaker identification.</p>
                    </div>

                    <div className="arrow-log">
                        <img src={arrow} alt="arrow" />
                    </div>

                    <div className="tool-card">
                        <Link to="/historylogin">
                        <div className="about-logo">
                            <h3>Get Results</h3>
                            <img src={result_icon} alt="result_icon" />
                        </div>
                        </Link>
                        <p>
                            Receive your transcription results in your preferred file format, with advanced
                            formatting for clarity and ease of use.
                        </p>
                    </div>
                </div>
            </section>

            {/* Footer */}
            <footer className="footer">
                <p>2023 TAP. All Rights Reserved.</p>
            </footer>
        </>
    );
}export default About;
