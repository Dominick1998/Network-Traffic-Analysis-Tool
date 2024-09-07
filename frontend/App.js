import React, { useState, useEffect } from 'react';
import TrafficTable from './components/TrafficTable';
import TrafficChart from './components/TrafficChart';
import LoadingSpinner from './components/LoadingSpinner';
import ErrorMessage from './components/ErrorMessage';
import NotificationBanner from './components/NotificationBanner';
import { fetchTrafficData } from './utils/api';
import { login, isLoggedIn, logout } from './utils/auth';
import './styles.css';

function App() {
  const [trafficData, setTrafficData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [authenticated, setAuthenticated] = useState(isLoggedIn());
  const [error, setError] = useState(null);
  const [notification, setNotification] = useState(null);

  useEffect(() => {
    if (authenticated) {
      const loadTrafficData = async () => {
        try {
          const data = await fetchTrafficData();
          setTrafficData(data);
        } catch (e) {
          setError('Failed to load traffic data. Please try again.');
        } finally {
          setLoading(false);
        }
      };

      loadTrafficData();
    } else {
      setLoading(false);
    }
  }, [authenticated]);

  const handleLogin = async (username, password) => {
    const success = await login(username, password);
    if (success) {
      setAuthenticated(true);
      setNotification({ message: 'Login successful!', type: 'success' });
    } else {
      setError('Invalid credentials');
      setNotification({ message: 'Login failed. Please try again.', type: 'error' });
    }
  };

  const handleLogout = () => {
    logout();
    setAuthenticated(false);
    setNotification({ message: 'You have logged out.', type: 'success' });
  };

  if (loading) {
    return <LoadingSpinner />;
  }

  if (error) {
    return (
      <div className="App">
        <header className="App-header">
          <h1>Network Traffic Analysis and Visualization Tool</h1>
        </header>
        <main>
          <ErrorMessage message={error} />
        </main>
      </div>
    );
  }

  return (
    <div className="App">
      <header className="App-header">
        <h1>Network Traffic Analysis and Visualization Tool</h1>
        {notification && <NotificationBanner message={notification.message} type={notification.type} />}
        {authenticated && <button onClick={handleLogout}>Logout</button>}
      </header>
      <main>
        {authenticated ? (
          <>
            <h2>Captured Network Traffic</h2>
            <TrafficTable trafficData={trafficData} />
            <h2>Network Traffic Visualization</h2>
            <TrafficChart trafficData={trafficData} />
          </>
        ) : (
          <LoginForm onLogin={handleLogin} />
        )}
      </main>
    </div>
  );
}

const LoginForm = ({ onLogin }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    onLogin(username, password);
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label>Username:</label>
        <input type="text" value={username} onChange={(e) => setUsername(e.target.value)} />
      </div>
      <div>
        <label>Password:</label>
        <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
      </div>
      <button type="submit">Login</button>
    </form>
  );
};

export default App;
