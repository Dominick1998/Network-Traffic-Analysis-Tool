import React from 'react';

const NetworkSummary = ({ summary }) => {
  return (
    <div className="network-summary">
      <h2>Network Summary</h2>
      <p><strong>Total Packets:</strong> {summary.total_packets}</p>
      <p><strong>Average Packet Length:</strong> {summary.average_length.toFixed(2)}</p>
      <h3>Top Sources:</h3>
      <ul>
        {summary.top_sources.map((source, index) => (
          <li key={index}>{source[0]} ({source[1]} packets)</li>
        ))}
      </ul>
      <h3>Top Destinations:</h3>
      <ul>
        {summary.top_destinations.map((destination, index) => (
          <li key={index}>{destination[0]} ({destination[1]} packets)</li>
        ))}
      </ul>
    </div>
  );
};

export default NetworkSummary;
