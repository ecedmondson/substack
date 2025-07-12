const LoadingSpinner = ({ message = 'Loading...' }) => (
  <div style={{
    padding: '2rem',
    textAlign: 'center',
    fontSize: '1.2rem',
  }}>
    <span role="status" aria-live="polite">{message}</span>
  </div>
);

export default LoadingSpinner;
