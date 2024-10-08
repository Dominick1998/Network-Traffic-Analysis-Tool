import React, { useEffect, useState } from 'react';

const ThreatList = () => {
  const [threats, setThreats] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchThreats = async () => {
      try {
        const response = await fetch('/api/threats');
        if (!response.ok) {
          throw new Error('Error fetching threats');
        }
        const data = await response.json();
        setThreats(data);
      } catch (error) {
        setError('Failed to load threats.');
      }
    };

    fetchThreats();
  }, []);

  return (
    <div className="threat-list">
      <h2>Detected Network Threats</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {threats.length > 0 ? (
        <table>
          <thead>
            <tr>
              <th>Type</th>
              <th>Source IP</th>
              <th>Details</th>
            </tr>
          </thead>
          <tbody>
            {threats.map((threat, index) => (
              <tr key={index}>
                <td>{threat.type}</td>
                <td>{threat.source_ip}</td>
                <td>
                  {threat.type === 'DDoS Attack' ? `Traffic Count: ${threat.traffic_count}` :
                   threat.type === 'Port Scan' ? `Scanned Ports: ${threat.scanned_ports}` :
                   threat.type === 'Suspicious IP Range' ? `IP Range: ${threat.ip_range}` : ''}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : (
        <p>No threats detected.</p>
      )}
    </div>
  );
};

export default ThreatList;
