import React, { useEffect, useState } from 'react';

const LogsViewer = () => {
  const [logs, setLogs] = useState('');

  useEffect(() => {
    const fetchLogs = async () => {
      try {
        const response = await fetch('/api/logs');
        if (!response.ok) {
          throw new Error('Error fetching logs');
        }
        const logText = await response.text();
        setLogs(logText);
      } catch (error) {
        setLogs('Failed to load logs.');
      }
    };

    fetchLogs();
  }, []);

  return (
    <div className="logs-container">
      <h2>Request Logs</h2>
      <pre>{logs}</pre>
    </div>
  );
};

export default LogsViewer;
