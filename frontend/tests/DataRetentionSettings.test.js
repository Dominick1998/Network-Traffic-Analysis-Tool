import React from 'react';
import { render, fireEvent, screen } from '@testing-library/react';
import DataRetentionSettings from '../components/DataRetentionSettings';

describe('DataRetentionSettings Component', () => {
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

  test('updates retention policy successfully', async () => {
    render(<DataRetentionSettings />);
    const input = screen.getByLabelText('Delete data older than:');
    fireEvent.change(input, { target: { value: '60' } });
    fireEvent.click(screen.getByText('Update Policy'));

    expect(await screen.findByText('Retention policy updated successfully.')).toBeInTheDocument();
    expect(global.fetch).toHaveBeenCalledWith('/api/settings/retention', expect.any(Object));
  });

  test('displays error message on failed update', async () => {
    global.fetch.mockImplementationOnce(() => Promise.resolve({ ok: false }));

    render(<DataRetentionSettings />);
    fireEvent.click(screen.getByText('Update Policy'));

    expect(await screen.findByText('Error updating retention policy.')).toBeInTheDocument();
  });
});
