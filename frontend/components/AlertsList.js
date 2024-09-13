import React from 'react';

const AlertsList = ({ alerts }) => {
  return (
    <div className="alerts-list">
      <h2>Network Alerts</h2>
      {alerts.length > 0 ? (
        <ul>
          {alerts.map((alert, index) => (
            <li key={index}>
              <strong>{alert.type}</strong>: {alert.message}
            </li>
          ))}
        </ul>
      ) : (
        <p>No alerts at the moment.</p>
      )}
    </div>
  );
};

export default AlertsList;
