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
