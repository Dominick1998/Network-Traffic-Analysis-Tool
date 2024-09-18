import React, { useState, useEffect } from 'react';

const SchedulerControl = () => {
  const [status, setStatus] = useState('Running');
  const [error, setError] = useState(null);

  const pauseScheduler = async () => {
    try {
      const response = await fetch('/api/scheduler/pause', { method: 'POST' });
      if (!response.ok) {
        throw new Error('Error pausing scheduler');
      }
      setStatus('Paused');
    } catch (error) {
      setError('Failed to pause scheduler.');
    }
  };

  const resumeScheduler = async () => {
    try {
      const response = await fetch('/api/scheduler/resume', { method: 'POST' });
      if (!response.ok) {
        throw new Error('Error resuming scheduler');
      }
      setStatus('Running');
    } catch (error) {
      setError('Failed to resume scheduler.');
    }
  };

  return (
    <div className="scheduler-control">
      <h2>Scheduler Control</h2>
      <p>Status: {status}</p>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <button onClick={pauseScheduler} disabled={status === 'Paused'}>
        Pause Scheduler
      </button>
      <button onClick={resumeScheduler} disabled={status === 'Running'}>
        Resume Scheduler
      </button>
    </div>
  );
};

export default SchedulerControl;
