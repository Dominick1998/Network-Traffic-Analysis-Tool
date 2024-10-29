import React, { useState, useEffect } from 'react';
import TrafficTable from './components/TrafficTable';
import TrafficChart from './components/TrafficChart';
import AnomalyTable from './components/AnomalyTable';
import NetworkSummary from './components/NetworkSummary';
import AlertsList from './components/AlertsList';
import ExportData from './components/ExportData';
import ImportData from './components/ImportData';
import LogsViewer from './components/LogsViewer';
import ThreatList from './components/ThreatList';
import PerformanceMonitor from './components/PerformanceMonitor';
import ActivityLogs from './components/ActivityLogs';
import AlertManagement from './components/AlertManagement';
import AnomalyLogs from './components/AnomalyLogs';
import FirewallManagement from './components/FirewallManagement';
import NotificationCenter from './components/NotificationCenter';
import IncidentReporting from './components/IncidentReporting';
import SystemHealth from './components/SystemHealth';
import LogRotationSettings from './components/LogRotationSettings';
import BackupManagement from './components/BackupManagement';
import AuditLogViewer from './components/AuditLogViewer';
import SecurityLogViewer from './components/SecurityLogViewer';
import AlertNotification from './components/AlertNotification';
import NotificationBanner from './components/NotificationBanner';
import LoadingSpinner from './components/LoadingSpinner';
import ErrorMessage from './components/ErrorMessage';
import { fetchTrafficData, fetchAnomalousTraffic, fetchNetworkSummary, fetchAlerts } from './utils/api';
import { login, isLoggedIn, logout } from './utils/auth';
import jwt_decode from "jwt-decode";
import './styles.css';

function App() {
  const [trafficData, setTrafficData] = useState([]);
  const [anomalyData, setAnomalyData] = useState([]);
  const [networkSummary, setNetworkSummary] = useState(null);
  const [alerts, setAlerts] = useState([]);
  const [notification, setNotification] = useState(null);
  const [loading, setLoading] = useState(true);
  const [authenticated, setAuthenticated] = useState(isLoggedIn());
  const [userRole, setUserRole] = useState(null);  // New state for user role
  const [alertMessage, setAlertMessage] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (authenticated) {
      const token = localStorage.getItem("token");
      if (token) {
        const decoded = jwt_decode(token);
        setUserRole(decoded.role);  // Set user role based on JWT

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

            if (anomalies.length > 0) {
              setNotification({
                message: `Detected ${anomalies.length} network anomalies. Please investigate.`,
                type: 'error',
              });
            }

            if (alertsData.some(alert => alert.condition === 'High Traffic')) {
              setAlertMessage('Custom Alert Triggered: High Traffic');
            }
          } catch (e) {
            setError('Failed to load traffic data. Please try again.');
          } finally {
            setLoading(false);
          }
        };
        loadData();
      }
    } else {
      setLoading(false);
    }
  }, [authenticated]);

  const handleLogin = async (username, password) => {
    const success = await login(username, password);
    if (success) {
      const token = localStorage.getItem("token");
      const decoded = jwt_decode(token);
      setUserRole(decoded.role);  // Set user role on login
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
    setUserRole(null);
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
            <TrafficChart trafficData={trafficData} />
            <AnomalyTable anomalyData={anomalyData} />
            <NetworkSummary summary={networkSummary} />

            {userRole === "Admin" && (
              <>
                <FirewallManagement />
                <IncidentReporting />
                <AuditLogViewer />
                <BackupManagement />
                <LogRotationSettings />
                <SecurityLogViewer />
              </>
            )}

            <AlertsList alerts={alerts} />
            <NotificationCenter />
            <PerformanceMonitor />
            <ActivityLogs />
          </>
        ) : (
          <LoginForm onLogin={handleLogin} />
        )}
      </main>
    </div>
  );
}

export default App;
