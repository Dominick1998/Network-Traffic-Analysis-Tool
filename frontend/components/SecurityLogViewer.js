import React, { useState, useEffect } from 'react';

const SecurityLogViewer = () => {
  const [logs, setLogs] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchSecurityLogs = async () => {
      try {
        const response = await fetch('/api/logs/security');
        if (!response.ok) {
          throw new Error('Error fetching security logs');
        }
        const data = await response.json();
        setLogs(data);
      } catch (error) {
        setError('Failed to load security logs.');
      }
    };

    fetchSecurityLogs();
  }, []);

  return (
    <div className="security-log-viewer">
      <h2>Security Log Viewer</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {logs.length > 0 ? (
        <ul>
          {logs.map((log, index) => (
            <li key={index}>{log}</li>
          ))}
        </ul>
      ) : (
        <p>No security logs available.</p>
      )}
    </div>
  );
};

export default SecurityLogViewer;
