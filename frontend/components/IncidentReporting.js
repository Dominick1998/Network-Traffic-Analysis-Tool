import React, { useState, useEffect } from 'react';

const IncidentReporting = () => {
  const [incidents, setIncidents] = useState([]);
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [severity, setSeverity] = useState('low');
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchIncidents = async () => {
      try {
        const response = await fetch('/api/incidents');
        if (!response.ok) throw new Error('Error fetching incidents');
        const data = await response.json();
        setIncidents(data.incidents);
      } catch (error) {
        setError('Failed to load incidents.');
      }
    };

    fetchIncidents();
  }, []);

  const handleReportIncident = async () => {
    try {
      const response = await fetch('/api/incidents', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title, description, severity }),
      });
      if (!response.ok) throw new Error('Error reporting incident');
      const data = await response.json();
      setIncidents([...incidents, { title, description, severity, timestamp: new Date().toISOString() }]);
      setTitle('');
      setDescription('');
      setSeverity('low');
    } catch (error) {
      setError('Failed to report incident.');
    }
  };

  return (
    <div className="incident-reporting">
      <h2>Incident Reporting</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <input
        type="text"
        placeholder="Incident Title"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
      />
      <textarea
        placeholder="Incident Description"
        value={description}
        onChange={(e) => setDescription(e.target.value)}
      />
      <select value={severity} onChange={(e) => setSeverity(e.target.value)}>
        <option value="low">Low</option>
        <option value="medium">Medium</option>
        <option value="high">High</option>
      </select>
      <button onClick={handleReportIncident}>Report Incident</button>
      <h3>Existing Incidents</h3>
      {incidents.length > 0 ? (
        <ul>
          {incidents.map((incident, index) => (
            <li key={index}>
              <strong>{incident.title}</strong>: {incident.description} (Severity: {incident.severity})
              <br />
              <small>{new Date(incident.timestamp).toLocaleString()}</small>
            </li>
          ))}
        </ul>
      ) : (
        <p>No incidents reported.</p>
      )}
    </div>
  );
};

export default IncidentReporting;
