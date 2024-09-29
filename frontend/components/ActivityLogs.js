import React, { useEffect, useState } from 'react';

const ActivityLogs = () => {
  const [activityLogs, setActivityLogs] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchActivityLogs = async () => {
      try {
        const response = await fetch('/api/user_activity');
        if (!response.ok) {
          throw new Error('Error fetching activity logs');
        }
        const data = await response.json();
        setActivityLogs(data);
      } catch (error) {
        setError('Failed to load activity logs.');
      }
    };

    fetchActivityLogs();
  }, []);

  return (
    <div className="activity-logs">
      <h2>User Activity Logs</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {activityLogs.length > 0 ? (
        <table>
          <thead>
            <tr>
              <th>User ID</th>
              <th>Activity</th>
              <th>Timestamp</th>
            </tr>
          </thead>
          <tbody>
            {activityLogs.map((log, index) => (
              <tr key={index}>
                <td>{log.user_id}</td>
                <td>{log.activity}</td>
                <td>{log.timestamp}</td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : (
        <p>No activity logs found.</p>
      )}
    </div>
  );
};

export default ActivityLogs;
