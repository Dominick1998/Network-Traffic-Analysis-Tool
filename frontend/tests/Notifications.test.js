import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import Notifications from '../components/Notifications';

describe('Notifications Component', () => {
  beforeEach(() => {
    global.fetch = jest.fn(() =>
      Promise.resolve({
        ok: true,
        json: () => Promise.resolve([{ message: 'Log rotation completed' }, { message: 'Daily summary sent' }]),
      })
    );
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  test('displays notifications fetched from the backend', async () => {
    render(<Notifications />);
    await waitFor(() => expect(screen.getByText('Log rotation completed')).toBeInTheDocument());
    await waitFor(() => expect(screen.getByText('Daily summary sent')).toBeInTheDocument());
  });

  test('displays error message when notifications cannot be fetched', async () => {
    global.fetch.mockImplementationOnce(() => Promise.resolve({ ok: false }));
    render(<Notifications />);
    await waitFor(() => expect(screen.getByText('Error fetching notifications')).toBeInTheDocument());
  });
});
