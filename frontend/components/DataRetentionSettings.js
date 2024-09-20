import React, { useState } from 'react';

const DataRetentionSettings = () => {
  const [days, setDays] = useState(30);
  const [statusMessage, setStatusMessage] = useState('');

  const updateRetentionPolicy = async () => {
    try {
      const response = await fetch('/api/settings/retention', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ days })
      });
      if (!response.ok) {
        throw new Error('Failed to update retention policy');
      }
      setStatusMessage('Retention policy updated successfully.');
    } catch (error) {
      setStatusMessage('Error updating retention policy.');
    }
  };

  return (
    <div className="retention-settings">
      <h2>Data Retention Settings</h2>
      <label>
        Delete data older than:
        <input
          type="number"
          value={days}
          onChange={(e) => setDays(e.target.value)}
        />
        days
      </label>
      <button onClick={updateRetentionPolicy}>Update Policy</button>
      {statusMessage && <p>{statusMessage}</p>}
    </div>
  );
};

export default DataRetentionSettings;
