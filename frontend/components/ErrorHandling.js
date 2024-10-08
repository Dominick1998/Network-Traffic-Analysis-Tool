import React from 'react';

const ErrorHandling = ({ error }) => {
  if (!error) return null;

  return (
    <div className="error-handling">
      <p style={{ color: 'red' }}>{error}</p>
    </div>
  );
};

export default ErrorHandling;
