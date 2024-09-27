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
      <h2>Detected Threats</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {threats.length > 0 ? (
        <table>
          <thead>
            <tr>
              <th>Source IP</th>
              <th>Request Count</th>
            </tr>
          </thead>
          <tbody>
            {threats.map((threat, index) => (
              <tr key={index}>
                <td>{threat.source_ip}</td>
                <td>{threat.count}</td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : (
        <p>No threats detected at this time.</p>
      )}
    </div>
  );
};

export default ThreatList;
