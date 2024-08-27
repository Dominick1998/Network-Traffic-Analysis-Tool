import React, { useState, useEffect } from 'react';

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
        <table>
          <thead>
            <tr>
              <th>Source</th>
              <th>Destination</th>
              <th>Protocol</th>
              <th>Length</th>
            </tr>
          </thead>
          <tbody>
            {trafficData.map((packet, index) => (
              <tr key={index}>
                <td>{packet.source}</td>
                <td>{packet.destination}</td>
                <td>{packet.protocol}</td>
                <td>{packet.length}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </main>
    </div>
  );
}

export default App;
