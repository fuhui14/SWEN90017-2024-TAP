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

        // 发送包含加密信息的请求获取历史记录
        fetch("http://127.0.0.1:8000/history/api/admin/history/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ enc: encrypted }),
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

    // 前端下载功能：不在界面显示ID，仅作为参数传递到后端
    const handleDownload = async (recordId, originalFilename) => {
        try {
            const response = await fetch("http://127.0.0.1:8000/history/api/download/", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ id: recordId })
            });
            if (!response.ok) {
                throw new Error("下载失败");
            }
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const link = document.createElement("a");
            link.href = url;
            // 如果提供原始文件名，则使用该名称，否则使用默认名称
            const filename = originalFilename ? originalFilename : "transcription";
            link.setAttribute("download", filename + ".txt");
            document.body.appendChild(link);
            link.click();
            link.parentNode.removeChild(link);
        } catch (error) {
            console.error("Download error:", error);
            alert("下载失败，请重试。");
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

            <div className="container">
                <div className="file-result">
                    <h1>History Transcriptions</h1>
                    <p>
                        This section displays your past transcription tasks, including details like task name, type, creation date,
                        and output format. You can quickly download completed files from this list. The data will be maintained for 30 days.
                    </p>

                    {loading && <p className="loading">Loading...</p>}
                    {error && <div className="error">{error}</div>}
                    {/* 成功加载后的提示 */}
                    {!loading && !error && historyData.length > 0 && (
                        <div className="notification success">历史记录加载成功！</div>
                    )}

                    {!loading && !error && historyData.length > 0 && (
                        <table>
                            <thead>
                                <tr>
                                    {/* 隐藏 ID 列 */}
                                    {/* <th>ID</th> */}
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
                                        {/* 隐藏ID数据，不在UI上展示 */}
                                        {/* <td>{record.id}</td> */}
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
                                                <button
                                                    className="download-btn"
                                                    onClick={() => handleDownload(record.id, record.taskName)}
                                                >
                                                    Download
                                                </button>
                                            ) : (
                                                <span className="no-download">Unavailable</span>
                                            )}
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    )}

                    {!loading && !error && historyData.length === 0 && (
                        <p className="no-history">No transcription history available.</p>
                    )}
                </div>
            </div>
        </>
    );
};

export default History;
