import React from 'react';
import { render, fireEvent, screen } from '@testing-library/react';
import SchedulerControl from '../components/SchedulerControl';

describe('SchedulerControl Component', () => {
  beforeEach(() => {
    global.fetch = jest.fn(() =>
      Promise.resolve({
        ok: true,
      })
    );
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  test('displays Running status initially', () => {
    render(<SchedulerControl />);
    expect(screen.getByText('Status: Running')).toBeInTheDocument();
  });

  test('pauses the scheduler when Pause button is clicked', async () => {
    render(<SchedulerControl />);
    fireEvent.click(screen.getByText('Pause Scheduler'));
    expect(await screen.findByText('Status: Paused')).toBeInTheDocument();
    expect(global.fetch).toHaveBeenCalledWith('/api/scheduler/pause', { method: 'POST' });
  });

  test('resumes the scheduler when Resume button is clicked', async () => {
    render(<SchedulerControl />);
    fireEvent.click(screen.getByText('Pause Scheduler'));
    fireEvent.click(screen.getByText('Resume Scheduler'));
    expect(await screen.findByText('Status: Running')).toBeInTheDocument();
    expect(global.fetch).toHaveBeenCalledWith('/api/scheduler/resume', { method: 'POST' });
  });

  test('displays error message on failure to pause or resume', async () => {
    global.fetch.mockImplementationOnce(() => Promise.resolve({ ok: false }));

    render(<SchedulerControl />);
    fireEvent.click(screen.getByText('Pause Scheduler'));
    expect(await screen.findByText('Failed to pause scheduler.')).toBeInTheDocument();
  });
});
