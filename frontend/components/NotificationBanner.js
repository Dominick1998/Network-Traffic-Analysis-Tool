import React from 'react';

const NotificationBanner = ({ message, type }) => {
  const bannerStyle = {
    padding: '10px 20px',
    backgroundColor: type === 'success' ? '#28a745' : '#dc3545',
    color: 'white',
    textAlign: 'center',
    borderRadius: '4px',
    margin: '20px 0',
  };

  return <div style={bannerStyle}>{message}</div>;
};

export default NotificationBanner;
