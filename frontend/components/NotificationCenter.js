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
        setNotifications(data);
      } catch (error) {
        setError('Failed to load notifications.');
      }
    };

    fetchNotifications();
  }, []);

  return (
    <div className="notification-center">
      <h2>Notification Center</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {notifications.length > 0 ? (
        <ul>
          {notifications.map((notification, index) => (
            <li key={index}>
              <strong>{notification.type.toUpperCase()}:</strong> {notification.message} ({new Date(notification.timestamp).toLocaleString()})
            </li>
          ))}
        </ul>
      ) : (
        <p>No notifications available.</p>
      )}
    </div>
  );
};

export default NotificationCenter;
