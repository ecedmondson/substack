import React, { useState } from 'react';
import { Outlet, Link } from 'react-router-dom';
import ErrorMessage from '~/shared/components/ErrorMessage';
import './styles.less';

const Layout = () => {
  const [error, setError] = useState(null);

  return (
    <div className="layout-container">
      <header className="navbar">
        <Link to="/">Home</Link>
        {/* Add more links here */}
      </header>

      <main className="content">
        <ErrorMessage error={error} onClose={() => setError(null)} />
        <Outlet context={{ setError }} />
      </main>

      <footer className="footer">
        <small>&copy; 2025 My App</small>
      </footer>
    </div>
  );
};

export default Layout;
