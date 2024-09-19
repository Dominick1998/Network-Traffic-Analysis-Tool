import React, { useState, useEffect } from 'react';
import TrafficTable from './components/TrafficTable';
import TrafficChart from './components/TrafficChart';
import AnomalyTable from './components/AnomalyTable';
import NetworkSummary from './components/NetworkSummary';
import AlertsList from './components/AlertsList';
import SchedulerControl from './components/SchedulerControl';
import LoadingSpinner from './components/LoadingSpinner';
import ErrorMessage from './components/ErrorMessage';
import NotificationBanner from './components/NotificationBanner';
import { fetchTrafficData, fetchAnomalousTraffic, fetchNetworkSummary, fetchAlerts } from './utils/api';
import { login, isLoggedIn, logout } from './utils/auth';
import './styles.css';

function App() {
  const [trafficData, setTrafficData] = useState([]);
  const [anomalyData, setAnomalyData] = useState([]);
  const [networkSummary, setNetworkSummary] = useState(null);
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [authenticated, setAuthenticated] = useState(isLoggedIn());
  const [error, setError] = useState(null);
  const [notification, setNotification] = useState(null);

  useEffect(() => {
    if (authenticated) {
      const loadData = async () => {
        try {
          const data = await fetchTrafficData();
          const anomalies = await fetchAnomalousTraffic();
          const summary = await fetchNetworkSummary();
          const alertsData = await fetchAlerts();
          setTrafficData(data);
          setAnomalyData(anomalies);
          setNetworkSummary(summary);
          setAlerts(alertsData);
        } catch (e) {
          setError('Failed to load traffic data. Please try again.');
        } finally {
          setLoading(false);
        }
      };

      loadData();
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
            <h2>Anomalous Network Traffic</h2>
            <AnomalyTable anomalyData={anomalyData} />
            <h2>Network Summary</h2>
            {networkSummary && <NetworkSummary summary={networkSummary} />}
            <h2>Network Alerts</h2>
            <AlertsList alerts={alerts} />
            <SchedulerControl />
          </>
        ) : (
          <LoginForm onLogin={handleLogin} />
        )}
      </main>
    </div>
  );
}

export default App;
