import React, { useState, useEffect } from 'react';
import TrafficTable from './components/TrafficTable';
import TrafficChart from './components/TrafficChart';
import LoadingSpinner from './components/LoadingSpinner';
import { fetchTrafficData } from './utils/api';
import './styles.css';

function App() {
  const [trafficData, setTrafficData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadTrafficData = async () => {
      const data = await fetchTrafficData();
      setTrafficData(data);
      setLoading(false);
    };

    loadTrafficData();
  }, []);

  if (loading) {
    return <LoadingSpinner />;
  }

  return (
    <div className="App">
      <header className="App-header">
        <h1>Network Traffic Analysis and Visualization Tool</h1>
      </header>
      <main>
        <h2>Captured Network Traffic</h2>
        <TrafficTable trafficData={trafficData} />
        <h2>Network Traffic Visualization</h2>
        <TrafficChart trafficData={trafficData} />
      </main>
    </div>
  );
}

export default App;
