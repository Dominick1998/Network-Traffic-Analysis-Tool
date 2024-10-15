import React, { useState } from 'react';

const LogRotationSettings = () => {
  const [maxFileSize, setMaxFileSize] = useState(5);  // Default 5MB
  const [backupCount, setBackupCount] = useState(5);  // Default 5 backups
  const [message, setMessage] = useState(null);
  const [error, setError] = useState(null);

  const handleUpdateSettings = async () => {
    const settingsData = { max_file_size: maxFileSize, backup_count: backupCount };

    try {
      const response = await fetch('/api/log_rotation/settings', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(settingsData),
      });
      if (!response.ok) {
        throw new Error('Failed to update log rotation settings');
      }
      const data = await response.json();
      setMessage(data.message);
      setError(null);
    } catch (error) {
      setMessage(null);
      setError('Failed to update log rotation settings.');
    }
  };

  return (
    <div className="log-rotation-settings">
      <h2>Log Rotation Settings</h2>
      {message && <p style={{ color: 'green' }}>{message}</p>}
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <div>
        <label>Max File Size (MB):</label>
        <input
          type="number"
          value={maxFileSize}
          onChange={(e) => setMaxFileSize(e.target.value)}
        />
        <label>Number of Backups:</label>
        <input
          type="number"
          value={backupCount}
          onChange={(e) => setBackupCount(e.target.value)}
        />
        <button onClick={handleUpdateSettings}>Update Settings</button>
      </div>
    </div>
  );
};

export default LogRotationSettings;
