import React, { useState, useEffect } from 'react';
import TrafficTable from './components/TrafficTable';

function App() {
  const [trafficData, setTrafficData] = useState([]);

  useEffect(() => {
    // Fetch traffic data from the backend API
    fetch('/api/traffic')
      .then(response => response.json())
      .then(data => setTrafficData(data))
      .catch(error => console.error('Error fetching traffic data:', error));
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1>Network Traffic Analysis and Visualization Tool</h1>
      </header>
      <main>
        <h2>Captured Network Traffic</h2>
        <TrafficTable trafficData={trafficData} />
      </main>
    </div>
  );
}

export default App;
