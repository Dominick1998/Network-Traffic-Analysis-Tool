export const pauseScheduler = async () => {
  try {
    const response = await fetch('/api/scheduler/pause', { method: 'POST' });
    if (!response.ok) {
      throw new Error('Failed to pause scheduler');
    }
    return true;
  } catch (error) {
    console.error('Error pausing scheduler:', error);
    return false;
  }
};

export const resumeScheduler = async () => {
  try {
    const response = await fetch('/api/scheduler/resume', { method: 'POST' });
    if (!response.ok) {
      throw new Error('Failed to resume scheduler');
    }
    return true;
  } catch (error) {
    console.error('Error resuming scheduler:', error);
    return false;
  }
};
