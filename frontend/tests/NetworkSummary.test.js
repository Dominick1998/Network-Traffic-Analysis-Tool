import React from 'react';
import { render, screen } from '@testing-library/react';
import NetworkSummary from '../components/NetworkSummary';

describe('NetworkSummary Component', () => {
  test('renders the network summary correctly', () => {
    const summary = {
      total_packets: 100,
      average_length: 512.34,
      top_sources: [['192.168.1.1', 30], ['192.168.1.2', 25], ['192.168.1.3', 20]],
      top_destinations: [['192.168.1.4', 35], ['192.168.1.5', 30], ['192.168.1.6', 20]],
    };
    render(<NetworkSummary summary={summary} />);
    expect(screen.getByText('Total Packets: 100')).toBeInTheDocument();
    expect(screen.getByText('Average Packet Length: 512.34')).toBeInTheDocument();
    expect(screen.getByText('192.168.1.1 (30 packets)')).toBeInTheDocument();
    expect(screen.getByText('192.168.1.4 (35 packets)')).toBeInTheDocument();
  });
});
