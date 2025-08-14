import { useState } from 'react';
import { Outlet } from 'react-router-dom';
import Layout from '../Layout';
import Navbar from '../Navbar';
import Footer from '../Footer';
import ErrorMessage from '~/shared/components/ErrorMessage';

const PageLayout = () => {
  const [error, setError] = useState(null);

  return (
    <Layout>
      <Navbar />
      <main className="layout-content">
        <ErrorMessage error={error} />
        <Outlet context={{ setError }} />
      </main>
      <Footer />
    </Layout>
  );
};

export default PageLayout;
