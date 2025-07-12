import React from 'react';
import { Toaster } from 'react-hot-toast';

const ErrorProvider = ({ children }) => (
  <>
    {children}
    <Toaster position="top-right" />
  </>
);

export default ErrorProvider;
