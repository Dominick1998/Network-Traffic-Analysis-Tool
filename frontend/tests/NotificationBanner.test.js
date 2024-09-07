import React from 'react';
import { render, screen } from '@testing-library/react';
import NotificationBanner from '../components/NotificationBanner';

describe('NotificationBanner Component', () => {
  test('renders success notification', () => {
    render(<NotificationBanner message="Success message" type="success" />);
    expect(screen.getByText('Success message')).toBeInTheDocument();
    expect(screen.getByText('Success message')).toHaveClass('success');
  });

  test('renders error notification', () => {
    render(<NotificationBanner message="Error message" type="error" />);
    expect(screen.getByText('Error message')).toBeInTheDocument();
    expect(screen.getByText('Error message')).toHaveClass('error');
  });

  test('renders warning notification', () => {
    render(<NotificationBanner message="Warning message" type="warning" />);
    expect(screen.getByText('Warning message')).toBeInTheDocument();
    expect(screen.getByText('Warning message')).toHaveClass('warning');
  });
});
