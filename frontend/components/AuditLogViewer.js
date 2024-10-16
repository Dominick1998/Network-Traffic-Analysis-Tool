import React, { useState, useEffect } from 'react';

const AuditLogViewer = () => {
  const [logs, setLogs] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchAuditLogs = async () => {
      try {
        const response = await fetch('/api/logs/audit');
        if (!response.ok) {
          throw new Error('Error fetching audit logs');
        }
        const data = await response.json();
        setLogs(data);
      } catch (error) {
        setError('Failed to load audit logs.');
      }
    };

    fetchAuditLogs();
  }, []);

  return (
    <div className="audit-log-viewer">
      <h2>Audit Log Viewer</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {logs.length > 0 ? (
        <ul>
          {logs.map((log, index) => (
            <li key={index}>{log}</li>
          ))}
        </ul>
      ) : (
        <p>No audit logs available.</p>
      )}
    </div>
  );
};

export default AuditLogViewer;
