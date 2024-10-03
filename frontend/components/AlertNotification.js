import React from 'react';

const AlertNotification = ({ message, type }) => {
  return (
    <div className={`alert-notification ${type}`}>
      <p>{message}</p>
    </div>
  );
};

export default AlertNotification;
