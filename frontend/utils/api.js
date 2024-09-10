export const fetchTrafficData = async () => {
  try {
    const response = await fetch('/api/traffic');
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error fetching traffic data:', error);
    return [];
  }
};

export const fetchAnomalousTraffic = async () => {
  try {
    const response = await fetch('/api/anomalies');
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    const anomalies = await response.json();
    return anomalies;
  } catch (error) {
    console.error('Error fetching anomalous traffic:', error);
    return [];
  }
};
