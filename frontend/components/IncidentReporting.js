import React, { useState, useEffect } from 'react';

const IncidentReporting = () => {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [severity, setSeverity] = useState('low');
  const [reports, setReports] = useState([]);
  const [message, setMessage] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchReports = async () => {
      try {
        const response = await fetch('/api/incidents');
        if (!response.ok) {
          throw new Error('Error fetching incident reports');
        }
        const data = await response.json();
        setReports(data);
      } catch (error) {
        setError('Failed to load incident reports.');
      }
    };

    fetchReports();
  }, []);

  const handleSubmitReport = async () => {
    const reportData = { title, description, severity };

    try {
      const response = await fetch('/api/incidents', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(reportData),
      });
      if (!response.ok) {
        throw new Error('Error submitting incident report');
      }
      const data = await response.json();
      setMessage(data.message);
      setError(null);
      setTitle('');
      setDescription('');
    } catch (error) {
      setMessage(null);
      setError('Failed to submit incident report.');
    }
  };

  return (
    <div className="incident-reporting">
      <h2>Incident Reporting</h2>
      {message && <p style={{ color: 'green' }}>{message}</p>}
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <div>
        <input
          type="text"
          placeholder="Title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
        />
        <textarea
          placeholder="Description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
        />
        <select value={severity} onChange={(e) => setSeverity(e.target.value)}>
          <option value="low">Low</option>
          <option value="medium">Medium</option>
          <option value="high">High</option>
        </select>
        <button onClick={handleSubmitReport}>Submit Report</button>
      </div>
      <h3>Existing Incident Reports</h3>
      {reports.length > 0 ? (
        <ul>
          {reports.map((report, index) => (
            <li key={index}>
              <strong>{report.title}:</strong> {report.description} ({new Date(report.timestamp).toLocaleString()}) - Severity: {report.severity}
            </li>
          ))}
        </ul>
      ) : (
        <p>No incident reports available.</p>
      )}
    </div>
  );
};

export default IncidentReporting;
