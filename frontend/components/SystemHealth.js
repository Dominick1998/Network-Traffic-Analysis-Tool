import React, { useEffect, useState } from 'react';

const SystemHealth = () => {
  const [healthData, setHealthData] = useState({});
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchSystemHealth = async () => {
      try {
        const response = await fetch('/api/system_health');
        if (!response.ok) {
          throw new Error('Error fetching system health data');
        }
        const data = await response.json();
        setHealthData(data);
      } catch (error) {
        setError('Failed to load system health data.');
      }
    };

    fetchSystemHealth();
  }, []);

  return (
    <div className="system-health">
      <h2>System Health</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {healthData ? (
        <div>
          <p>CPU Usage: {healthData.cpu_usage}%</p>
          <p>Memory Usage: {healthData.memory_usage}%</p>
          <p>Disk Usage: {healthData.disk_usage}%</p>
          <p>Network Sent: {healthData.network_sent} bytes</p>
          <p>Network Received: {healthData.network_received} bytes</p>
        </div>
      ) : (
        <p>Loading system health data...</p>
      )}
    </div>
  );
};

export default SystemHealth;
