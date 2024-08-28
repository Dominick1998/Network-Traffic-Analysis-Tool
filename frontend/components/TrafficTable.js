import React from 'react';

const TrafficTable = ({ trafficData }) => {
  return (
    <table>
      <thead>
        <tr>
          <th>Source</th>
          <th>Destination</th>
          <th>Protocol</th>
          <th>Length</th>
        </tr>
      </thead>
      <tbody>
        {trafficData.map((packet, index) => (
          <tr key={index}>
            <td>{packet.source}</td>
            <td>{packet.destination}</td>
            <td>{packet.protocol}</td>
            <td>{packet.length}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default TrafficTable;
