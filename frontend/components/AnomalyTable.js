import React from 'react';

const AnomalyTable = ({ anomalyData }) => {
  return (
    <table>
      <thead>
        <tr>
          <th>Source</th>
          <th>Destination</th>
          <th>Protocol</th>
          <th>Length</th>
          <th>Timestamp</th>
        </tr>
      </thead>
      <tbody>
        {anomalyData.map((packet, index) => (
          <tr key={index}>
            <td>{packet.source}</td>
            <td>{packet.destination}</td>
            <td>{packet.protocol}</td>
            <td>{packet.length}</td>
            <td>{packet.timestamp}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default AnomalyTable;
