import React, { useEffect, useState } from 'react';

const LogsViewer = () => {
  const [logs, setLogs] = useState('');
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchLogs = async () => {
      try {
        const response = await fetch('/api/logs');
        if (!response.ok) {
          throw new Error('Error fetching logs');
        }
        const data = await response.json();
        setLogs(data.logs);
      } catch (error) {
        setError('Failed to load logs.');
      }
    };

    fetchLogs();
  }, []);

  const downloadLogs = async () => {
    try {
      const response = await fetch('/api/logs/download');
      if (!response.ok) {
        throw new Error('Error downloading logs');
      }
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'server_logs.log';
      document.body.appendChild(a);
      a.click();
      a.remove();
    } catch (error) {
      setError('Failed to download logs.');
    }
  };

  return (
    <div className="logs-container">
      <h2>Server Logs</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <pre>{logs}</pre>
      <button onClick={downloadLogs}>Download Logs</button>
    </div>
  );
};

export default LogsViewer;
