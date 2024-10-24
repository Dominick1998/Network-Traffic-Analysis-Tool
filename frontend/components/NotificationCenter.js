import React, { useEffect, useState } from 'react';

const NotificationCenter = () => {
  const [notifications, setNotifications] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchNotifications = async () => {
      try {
        const response = await fetch('/api/notifications');
        if (!response.ok) {
          throw new Error('Error fetching notifications');
        }
        const data = await response.json();
        setNotifications(data.notifications);
      } catch (error) {
        setError('Failed to load notifications.');
      }
    };

    fetchNotifications();
  }, []);

  const clearNotifications = async () => {
    try {
      const response = await fetch('/api/notifications/clear', {
        method: 'POST',
      });
      if (!response.ok) {
        throw new Error('Error clearing notifications');
      }
      setNotifications([]);
    } catch (error) {
      setError('Failed to clear notifications.');
    }
  };

  return (
    <div className="notification-center">
      <h2>Notification Center</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {notifications.length > 0 ? (
        <ul>
          {notifications.map((notification, index) => (
            <li key={index}>
              <strong>{notification.type.toUpperCase()}: </strong>{notification.message}
            </li>
          ))}
        </ul>
      ) : (
        <p>No notifications available.</p>
      )}
      <button onClick={clearNotifications}>Clear Notifications</button>
    </div>
  );
};

export default NotificationCenter;
