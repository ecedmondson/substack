import React from 'react';
import { useOutletContext } from 'react-router-dom';

const Home = () => {
  const { setError } = useOutletContext();

  React.useEffect(() => {
    // Example: simulate an error after 2 seconds
    const timer = setTimeout(() => setError(new Error('Oops, something went wrong')), 2000);
    return () => clearTimeout(timer);
  }, [setError]);

  return <div>Welcome to the Home page!</div>;
};

export default Home;
