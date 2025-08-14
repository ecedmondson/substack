import './styles.less';


import React from 'react';
import './styles.less';

const ErrorMessage = ({
  error,
  message = 'Something went wrong. Please refresh and try again.',
}) => {
  if (!error) return null;

  return (
    <div className="error-banner" role="alert">
      <div className="error-icon" aria-hidden="true">❌</div>
      <div className="error-text">
        <strong>Error: </strong> {error.message || message}
      </div>
    </div>
  );
};

export default ErrorMessage;
