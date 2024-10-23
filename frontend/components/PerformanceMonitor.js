import React, { useEffect, useState } from 'react';

const PerformanceMonitor = () => {
  const [cpuData, setCpuData] = useState(null);
  const [memoryData, setMemoryData] = useState(null);
  const [diskData, setDiskData] = useState([]);
  const [latencyData, setLatencyData] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchCpuData = async () => {
      try {
        const response = await fetch('/api/performance/cpu');
        if (!response.ok) throw new Error('Error fetching CPU data');
        const data = await response.json();
        setCpuData(data.cpu_usage);
      } catch (err) {
        setError('Failed to fetch CPU data');
      }
    };

    const fetchMemoryData = async () => {
      try {
        const response = await fetch('/api/performance/memory');
        if (!response.ok) throw new Error('Error fetching memory data');
        const data = await response.json();
        setMemoryData(data);
      } catch (err) {
        setError('Failed to fetch memory data');
      }
    };

    const fetchDiskData = async () => {
      try {
        const response = await fetch('/api/performance/disk');
        if (!response.ok) throw new Error('Error fetching disk data');
        const data = await response.json();
        setDiskData(data);
      } catch (err) {
        setError('Failed to fetch disk data');
      }
    };

    const fetchLatencyData = async () => {
      try {
        const response = await fetch('/api/performance/latency');
        if (!response.ok) throw new Error('Error fetching network latency data');
        const data = await response.json();
        setLatencyData(data.network_latency_ms);
      } catch (err) {
        setError('Failed to fetch network latency data');
      }
    };

    fetchCpuData();
    fetchMemoryData();
    fetchDiskData();
    fetchLatencyData();
  }, []);

  return (
    <div className="performance-monitor">
      <h2>System Performance Monitor</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <div>
        <h3>CPU Usage</h3>
        <p>{cpuData !== null ? `${cpuData}%` : 'Loading...'}</p>
      </div>
      <div>
        <h3>Memory Usage</h3>
        <p>{memoryData !== null ? `${memoryData.memory_usage}%` : 'Loading...'}</p>
      </div>
      <div>
        <h3>Disk Usage</h3>
        <ul>
          {diskData.length > 0
            ? diskData.map((disk, index) => (
                <li key={index}>
                  {disk.partition}: {disk.percent}% used
                </li>
              ))
            : 'Loading...'}
        </ul>
      </div>
      <div>
        <h3>Network Latency</h3>
        <p>{latencyData !== null ? `${latencyData} ms` : 'Loading...'}</p>
      </div>
    </div>
  );
};

export default PerformanceMonitor;
