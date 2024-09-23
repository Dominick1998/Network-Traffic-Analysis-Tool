import React from 'react';

const ExportData = () => {
  const exportData = async (format) => {
    try {
      const response = await fetch(`/api/export/${format}`);
      if (!response.ok) {
        throw new Error(`Failed to export data as ${format}`);
      }

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `network_traffic.${format}`;
      document.body.appendChild(a);
      a.click();
      a.remove();
    } catch (error) {
      console.error(`Error exporting data: ${error.message}`);
    }
  };

  return (
    <div className="export-data">
      <h2>Export Network Traffic Data</h2>
      <button onClick={() => exportData('csv')}>Export as CSV</button>
      <button onClick={() => exportData('json')}>Export as JSON</button>
    </div>
  );
};

export default ExportData;
