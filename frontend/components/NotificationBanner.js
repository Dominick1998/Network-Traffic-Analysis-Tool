import React from 'react';
import './NotificationBanner.css';

const NotificationBanner = ({ message, type }) => {
  return (
    <div className={`notification-banner ${type}`}>
      <p>{message}</p>
    </div>
  );
};

export default NotificationBanner;
