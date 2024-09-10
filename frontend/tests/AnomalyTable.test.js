import React from 'react';
import { render, screen } from '@testing-library/react';
import AnomalyTable from '../components/AnomalyTable';

describe('AnomalyTable Component', () => {
  test('renders anomaly data correctly', () => {
    const anomalyData = [
      { source: '192.168.1.1', destination: '192.168.1.2', protocol: 'TCP', length: 1200, timestamp: '2024-08-23T12:00:00Z' },
      { source: '192.168.1.3', destination: '192.168.1.4', protocol: 'UDP', length: 1500, timestamp: '2024-08-23T13:00:00Z' }
    ];
    render(<AnomalyTable anomalyData={anomalyData} />);
    expect(screen.getByText('192.168.1.1')).toBeInTheDocument();
    expect(screen.getByText('192.168.1.3')).toBeInTheDocument();
    expect(screen.getByText('TCP')).toBeInTheDocument();
    expect(screen.getByText('UDP')).toBeInTheDocument();
  });
});
