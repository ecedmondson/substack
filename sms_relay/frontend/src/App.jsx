import React from 'react';
import AppRoutes from './routes';
import ErrorBoundary from './shared/components/ErrorBoundary';

function App() {
  return (
    <ErrorBoundary>
      <AppRoutes />
    </ErrorBoundary>
  );
}

export default App;
