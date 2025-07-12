import React from 'react';
import './styles.less';

const ErrorMessage = ({ error, onClose }) => {
  if (!error) return null;

  return (
    <div className="error-message">
      <strong>Error: </strong> {error.message || error.toString()}
      <button onClick={onClose} aria-label="Close error message">×</button>
    </div>
  );
};

export default ErrorMessage;
