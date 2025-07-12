import React from 'react';
import ThemeProvider from './ThemeProvider';
import QueryProvider from './QueryProvider';
import ErrorProvider from './ErrorProvider';

const AppProviders = ({ children }) => (
  <ThemeProvider>
    <QueryProvider>
      <ErrorProvider>
        {children}
      </ErrorProvider>
    </QueryProvider>
  </ThemeProvider>
);

export default AppProviders;
