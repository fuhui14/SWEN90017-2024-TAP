import './history.css';
import React, { useState, useEffect } from 'react';

// Main History component for displaying past transcriptions
function History() {
    const [records, setRecords] = useState([]); // State to store history records
    const [currentPage, setCurrentPage] = useState(1); // State to track current page for pagination
    const [totalPages, setTotalPages] = useState(1); // State to track total pages

    // Fetch history records from the backend
    useEffect(() => {
        fetchHistoryRecords(currentPage);
    }, [currentPage]);

    // Fetch history data based on the current page
    const fetchHistoryRecords = async (page) => {
        try {
            const response = await fetch(`/api/history?page=${page}`); // API call to fetch history records
            const data = await response.json();
            setRecords(data.records);
            setTotalPages(data.totalPages);
        } catch (error) {
            console.error('Error fetching history records:', error); // Error handling
        }
    };

    // Handle page change for pagination
    const handlePageChange = (newPage) => {
        setCurrentPage(newPage);
    };

    return (
        <div className="history-container">
            <h3>History Transcriptions</h3>
            <p>This section displays your past transcription tasks, including details like task name, type, creation date, and output format. You can quickly download completed files from this list. Data will be maintained for 30 days.</p>
            <table className="history-table">
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
                {records.map((record) => (
                    <tr key={record.id}>
                        <td>{record.id}</td>
                        <td>{record.taskName}</td>
                        <td>{record.taskType}</td>
                        <td>{record.creationDate}</td>
                        <td>{record.daysUntilExpiry}</td>
                        <td>{record.outputType}</td>
                        <td>{record.status}</td>
                        <td>
                            {record.status === 'Completed' && (
                                <button className="download-button">Download</button>
                            )}
                        </td>
                    </tr>
                ))}
                </tbody>
            </table>

            <div className="pagination">
                <button
                    onClick={() => handlePageChange(currentPage - 1)}
                    disabled={currentPage === 1}
                >
                    Previous
                </button>
                <span>Page {currentPage} of {totalPages}</span>
                <button
                    onClick={() => handlePageChange(currentPage + 1)}
                    disabled={currentPage === totalPages}
                >
                    Next
                </button>
            </div>
        </div>
    );
}

export default History;
