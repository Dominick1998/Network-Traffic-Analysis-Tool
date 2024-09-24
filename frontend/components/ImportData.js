import React, { useState } from 'react';

const ImportData = () => {
  const [file, setFile] = useState(null);
  const [statusMessage, setStatusMessage] = useState('');

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const uploadFile = async () => {
    if (!file) {
      setStatusMessage('Please select a file.');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('/api/import/csv', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        setStatusMessage('File imported successfully.');
      } else {
        setStatusMessage('Error importing file.');
      }
    } catch (error) {
      setStatusMessage('Error importing file.');
    }
  };

  return (
    <div className="import-data">
      <h2>Import Network Traffic Data</h2>
      <input type="file" accept=".csv" onChange={handleFileChange} />
      <button onClick={uploadFile}>Import</button>
      {statusMessage && <p>{statusMessage}</p>}
    </div>
  );
};

export default ImportData;
