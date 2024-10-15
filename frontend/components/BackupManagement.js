import React, { useState } from 'react';

const BackupManagement = () => {
  const [message, setMessage] = useState(null);
  const [error, setError] = useState(null);
  const [backupFilename, setBackupFilename] = useState('');

  const handleCreateBackup = async () => {
    try {
      const response = await fetch('/api/backup/create', {
        method: 'POST',
      });
      if (!response.ok) {
        throw new Error('Failed to create backup');
      }
      const data = await response.json();
      setMessage(data.message);
      setError(null);
    } catch (error) {
      setMessage(null);
      setError('Failed to create backup.');
    }
  };

  const handleRestoreBackup = async () => {
    const restoreData = { backup_filename: backupFilename };

    try {
      const response = await fetch('/api/backup/restore', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(restoreData),
      });
      if (!response.ok) {
        throw new Error('Failed to restore backup');
      }
      const data = await response.json();
      setMessage(data.message);
      setError(null);
    } catch (error) {
      setMessage(null);
      setError('Failed to restore backup.');
    }
  };

  return (
    <div className="backup-management">
      <h2>Backup Management</h2>
      {message && <p style={{ color: 'green' }}>{message}</p>}
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <button onClick={handleCreateBackup}>Create Backup</button>
      <div>
        <input
          type="text"
          placeholder="Backup Filename"
          value={backupFilename}
          onChange={(e) => setBackupFilename(e.target.value)}
        />
        <button onClick={handleRestoreBackup}>Restore Backup</button>
      </div>
    </div>
  );
};

export default BackupManagement;
