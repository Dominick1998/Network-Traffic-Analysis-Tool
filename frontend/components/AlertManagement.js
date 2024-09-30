import React, { useState, useEffect } from 'react';

const AlertManagement = () => {
  const [alerts, setAlerts] = useState([]);
  const [name, setName] = useState('');
  const [condition, setCondition] = useState('');
  const [action, setAction] = useState('');
  const [error, setError] = useState(null);
  const [message, setMessage] = useState(null);

  useEffect(() => {
    fetchAlerts();
  }, []);

  const fetchAlerts = async () => {
    try {
      const response = await fetch('/api/alerts');
      if (!response.ok) {
        throw new Error('Error fetching alerts');
      }
      const data = await response.json();
      setAlerts(data);
    } catch (error) {
      setError('Failed to load alerts.');
    }
  };

  const createAlert = async () => {
    const alertData = { name, condition, action };
    try {
      const response = await fetch('/api/alerts', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(alertData),
      });
      if (!response.ok) {
        throw new Error('Error creating alert');
      }
      setMessage('Alert created successfully');
      setName('');
      setCondition('');
      setAction('');
      fetchAlerts(); // Reload alerts
    } catch (error) {
      setError('Failed to create alert.');
    }
  };

  const deleteAlert = async (id) => {
    try {
      const response = await fetch(`/api/alerts/${id}`, {
        method: 'DELETE',
      });
      if (!response.ok) {
        throw new Error('Error deleting alert');
      }
      setMessage('Alert deleted successfully');
      fetchAlerts(); // Reload alerts
    } catch (error) {
      setError('Failed to delete alert.');
    }
  };

  return (
    <div className="alert-management">
      <h2>Alert Management</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {message && <p style={{ color: 'green' }}>{message}</p>}
      <div className="create-alert">
        <h3>Create Alert</h3>
        <input
          type="text"
          placeholder="Alert Name"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />
        <input
          type="text"
          placeholder="Condition"
          value={condition}
          onChange={(e) => setCondition(e.target.value)}
        />
        <input
          type="text"
          placeholder="Action"
          value={action}
          onChange={(e) => setAction(e.target.value)}
        />
        <button onClick={createAlert}>Create Alert</button>
      </div>
      <h3>Existing Alerts</h3>
      <ul>
        {alerts.map((alert) => (
          <li key={alert.id}>
            {alert.name} - {alert.condition} - {alert.action}
            <button onClick={() => deleteAlert(alert.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default AlertManagement;
