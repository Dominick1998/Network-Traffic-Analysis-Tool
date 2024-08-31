import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import App from '../App';
import { fetchTrafficData } from '../utils/api';

jest.mock('../utils/api');

describe('App Component', () => {
  test('renders loading spinner initially', () => {
    fetchTrafficData.mockResolvedValue([]);
    render(<App />);
    expect(screen.getByText(/loading/i)).toBeInTheDocument();
  });

  test('renders network traffic table after loading', async () => {
    fetchTrafficData.mockResolvedValue([
      { source: '192.168.1.1', destination: '192.168.1.2', protocol: 'TCP', length: 60, timestamp: '2024-08-23T12:00:00Z' },
    ]);
    render(<App />);
    await waitFor(() => {
      expect(screen.getByText(/captured network traffic/i)).toBeInTheDocument();
    });
  });

  test('renders network traffic chart after loading', async () => {
    fetchTrafficData.mockResolvedValue([
      { source: '192.168.1.1', destination: '192.168.1.2', protocol: 'TCP', length: 60, timestamp: '2024-08-23T12:00:00Z' },
    ]);
    render(<App />);
    await waitFor(() => {
      expect(screen.getByText(/network traffic visualization/i)).toBeInTheDocument();
    });
  });
});
