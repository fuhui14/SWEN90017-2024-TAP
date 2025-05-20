import React, { useEffect, useState } from "react";
import { Link, useSearchParams } from "react-router-dom";
import log from "../resources/icon/logo.svg";
import downloadLogo from '../resources/icon/download.svg';
import './history.css';

const History = () => {
    const [searchParams] = useSearchParams();
    const [historyData, setHistoryData] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    // Retrieve encrypted user info from the URL
    const encrypted = searchParams.get("enc");

    // Pagination states
    const [currentPage, setCurrentPage] = useState(1);
    const recordsPerPage = 10;

    useEffect(() => {
        if (!encrypted) {
            setError("Invalid or expired link.");
            setLoading(false);
            return;
        }

        // Send a request with the encrypted info to get history records
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

    // Reset current page when history data changes
    useEffect(() => {
        setCurrentPage(1);
    }, [historyData]);

    // Front-end download functionality: the record ID is used for backend parameter
    const handleDownload = async (recordId, originalFilename) => {
        try {
            const response = await fetch("http://127.0.0.1:8000/history/api/download/", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ id: recordId })
            });
            if (!response.ok) {
                throw new Error("Download failed");
            }
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const link = document.createElement("a");
            link.href = url;
            // Use the original filename if provided; otherwise, a default name is used
            const filename = originalFilename ? originalFilename : "transcription";
            link.setAttribute("download", filename + ".txt");
            document.body.appendChild(link);
            link.click();
            link.parentNode.removeChild(link);
        } catch (error) {
            console.error("Download error:", error);
            alert("Download failed, please try again.");
        }
    };

    // Calculate pagination values
    const totalPages = Math.ceil(historyData.length / recordsPerPage);
    const indexOfLastRecord = currentPage * recordsPerPage;
    const indexOfFirstRecord = indexOfLastRecord - recordsPerPage;
    const currentRecords = historyData.slice(indexOfFirstRecord, indexOfLastRecord);

    // Pagination handlers
    const handlePageChange = (pageNumber) => {
        setCurrentPage(pageNumber);
    };

    const handlePrevPage = () => {
        if (currentPage > 1) setCurrentPage(currentPage - 1);
    };

    const handleNextPage = () => {
        if (currentPage < totalPages) setCurrentPage(currentPage + 1);
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
                    {/* Success message upon loading */}
                    {!loading && !error && historyData.length > 0 && (
                        <div className="notification success">History loaded successfully!</div>
                    )}

                    {!loading && !error && historyData.length > 0 && (
                        <>
                            <table>
                                <thead>
                                    <tr>
                                        {/* ID column is hidden */}
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
                                    {currentRecords.map((record) => (
                                        <tr key={record.id}>
                                            {/* ID data is hidden and not displayed */}
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
                                                        <img src={downloadLogo} alt="Download" className="download-icon" />
                                                    </button>
                                                ) : (
                                                    <span className="no-download">Unavailable</span>
                                                )}
                                            </td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                            {/* Pagination controls */}
                            {totalPages > 1 && (
                                <div className="pagination">
                                    <button onClick={handlePrevPage} disabled={currentPage === 1}>
                                        Prev
                                    </button>
                                    {Array.from({ length: totalPages }, (_, index) => index + 1).map((number) => (
                                        <button
                                            key={number}
                                            onClick={() => handlePageChange(number)}
                                            className={currentPage === number ? "active" : ""}
                                        >
                                            {number}
                                        </button>
                                    ))}
                                    <button onClick={handleNextPage} disabled={currentPage === totalPages}>
                                        Next
                                    </button>
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
};

export default History;