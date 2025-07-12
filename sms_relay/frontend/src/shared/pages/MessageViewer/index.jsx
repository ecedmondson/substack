import React, { useState } from 'react';
import { useMessagesList } from '~/api/message';
import Layout from '~/shared/components/Layout';
import MessageViewer from './components/Viewer';
import ErrorMessage from '~/shared/components/ErrorMessage';
import LoadingSpinner from '~/shared/components/Loader';

const MessageViewerPage = () => {
  const [error, setError] = useState(null);
  const { isLoading, isError, error: queryError } = useMessagesList();

  if (isLoading) {
    return <LoadingSpinner message="Fetching messages..." />;
  }

  if (isError) {
    return (
      <Layout>
        <ErrorMessage error={queryError} onClose={() => setError(null)} />
        <div style={{ padding: '2rem' }}>
          <p>Could not load messages.</p>
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <MessageViewer setError={setError} />
    </Layout>
  );
};

export default MessageViewerPage;
