import React, { useEffect, useState } from "react";
import {Link, useSearchParams} from "react-router-dom";
import log from "../resources/icon/logo.svg";
import './history.css';

const History = () => {
    const [searchParams] = useSearchParams();
    const [historyData, setHistoryData] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const token = searchParams.get("token");

    useEffect(() => {
        if (!token) {
            setError("Invalid or expired link.");
            setLoading(false);
            return;
        }

        fetch("http://127.0.0.1:8000/api/admin/history/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ token }),
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
    }, [token]);

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
            <p>This section displays your past transcription tasks, including details like task name, type, creation date,
                and output format. You can quickly download completed files from this list. The Data will be maintained for 30 Days.</p>

            {loading && <p>Loading...</p>}
            {error && <error className="error">{error}</error>}

            {!loading && !error && (
                <table>
                    <thead>
                    <tr>
                        <th>ID</th>
                        <th>Task Name</th>
                        <th>Task Type</th>
                        <th>Creation Date</th>
                        <th>Days Until Expiry</th>
                        <th>Output type</th>
                        <th>Statue</th>
                        <th>Download</th>
                    </tr>
                    </thead>
                    <tbody>
                    {historyData.map((record) => {
                        // count dys left
                        //const expiryDate = new Date(record.expiryDate);
                        //const today = new Date();
                        //const daysLeft = Math.max(0, Math.ceil((expiryDate - today) / (1000 * 60 * 60 * 24)));

                        return (
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
                                        <span className="no-download">🚫</span> // 失败状态显示禁用符号
                                    )}
                                </td>
                            </tr>
                        );
                    })}
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
