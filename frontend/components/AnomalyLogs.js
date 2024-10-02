import React, { useEffect, useState } from 'react';

const AnomalyLogs = () => {
  const [logs, setLogs] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchAnomalyLogs = async () => {
      try {
        const response = await fetch('/api/anomaly_logs');
        if (!response.ok) {
          throw new Error('Error fetching anomaly logs');
        }
        const data = await response.json();
        setLogs(data);
      } catch (error) {
        setError('Failed to load anomaly logs.');
      }
    };

    fetchAnomalyLogs();
  }, []);

  return (
    <div className="anomaly-logs">
      <h2>Network Anomaly Logs</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {logs.length > 0 ? (
        <table>
          <thead>
            <tr>
              <th>Source IP</th>
              <th>Destination IP</th>
              <th>Protocol</th>
              <th>Length</th>
              <th>Anomaly Type</th>
              <th>Timestamp</th>
            </tr>
          </thead>
          <tbody>
            {logs.map((log, index) => (
              <tr key={index}>
                <td>{log.source_ip}</td>
                <td>{log.destination_ip}</td>
                <td>{log.protocol}</td>
                <td>{log.length}</td>
                <td>{log.anomaly_type}</td>
                <td>{log.timestamp}</td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : (
        <p>No anomaly logs found.</p>
      )}
    </div>
  );
};

export default AnomalyLogs;
