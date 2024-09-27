import React, { useEffect, useState } from 'react';

const PerformanceMonitor = () => {
  const [performanceData, setPerformanceData] = useState({});
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchPerformanceData = async () => {
      try {
        const response = await fetch('/api/performance');
        if (!response.ok) {
          throw new Error('Error fetching performance data');
        }
        const data = await response.json();
        setPerformanceData(data);
      } catch (error) {
        setError('Failed to load performance metrics.');
      }
    };

    fetchPerformanceData();
  }, []);

  return (
    <div className="performance-monitor">
      <h2>System Performance Metrics</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {performanceData ? (
        <ul>
          <li>CPU Usage: {performanceData.cpu_usage}%</li>
          <li>Memory Usage: {performanceData.memory_usage && performanceData.memory_usage.percentage}%</li>
        </ul>
      ) : (
        <p>Loading performance metrics...</p>
      )}
    </div>
  );
};

export default PerformanceMonitor;
