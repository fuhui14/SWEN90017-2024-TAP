import React, { useEffect, useState } from "react";
import { Link, useSearchParams } from "react-router-dom";
import log from "../resources/icon/logo.svg";
import './history.css';

const History = () => {
    const [searchParams] = useSearchParams();
    const [historyData, setHistoryData] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    // 读取 URL 中加密后的用户信息
    const encrypted = searchParams.get("enc");

    useEffect(() => {
        if (!encrypted) {
            setError("Invalid or expired link.");
            setLoading(false);
            return;
        }

        // 发送包含加密信息的请求
        fetch("http://127.0.0.1:8000/history/api/admin/history/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ enc: encrypted }), // 注意这里使用 "enc" 作为键名
        })
            .then((res) => res.json())
            .then((data) => {
                setHistoryData(data);
                setLoading(false);
            })
            .catch((error) => {
                setError("Failed to load history data.");
                setLoading(false);
            });
    }, [encrypted]);

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

            <div className="container">
                <div className="file-result">
                    <h3>History Transcriptions</h3>
                    <p>
                        This section displays your past transcription tasks, including details like task name, type, creation date,
                        and output format. You can quickly download completed files from this list. The data will be maintained for 30 days.
                    </p>

                    {loading && <p>Loading...</p>}
                    {error && <div className="error">{error}</div>}

                    {!loading && !error && historyData.length > 0 && (
                        <table>
                            <thead>
                                <tr>
                                    <th>ID</th>
                                    <th>Task Name</th>
                                    <th>Task Type</th>
                                    <th>Creation Date</th>
                                    <th>Days Until Expiry</th>
                                    <th>Output Type</th>
                                    <th>Status</th>
                                    <th>Download</th>
                                </tr>
                            </thead>
                            <tbody>
                                {historyData.map((record) => (
                                    <tr key={record.id}>
                                        <td>{record.id}</td>
                                        <td>{record.taskName}</td>
                                        <td>{record.taskType}</td>
                                        <td>{new Date(record.creationDate).toLocaleDateString()}</td>
                                        <td>{record.daysLeft}</td>
                                        <td>{record.outputType}</td>
                                        <td>
                                            <span className={`status ${record.status.toLowerCase()}`}>
                                                {record.status === "Completed" ? "Completed" : "Failed"}
                                            </span>
                                        </td>
                                        <td>
                                            {record.status === "Completed" ? (
                                                <a href={record.downloadUrl} download className="download-btn">⬇️</a>
                                            ) : (
                                                <span className="no-download">🚫</span>
                                            )}
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    )}

                    {!loading && !error && historyData.length === 0 && (
                        <p>No transcription history available.</p>
                    )}
                </div>
            </div>
        </>
    );
};

export default History;
