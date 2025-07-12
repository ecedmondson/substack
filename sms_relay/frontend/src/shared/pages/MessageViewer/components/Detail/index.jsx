import React from 'react';

import { useMessageDetail } from '~/api/message';
import LoadingSpinner from '~/shared/components/Loader';

const MessageDetailViewer = ({ messageId, setError }) => {
  const {
    data,
    isLoading,
    isError,
    error,
  } = useMessageDetail(messageId, { enabled: !!messageId });

  React.useEffect(() => {
    if (isError) setError(error);
  }, [isError, error, setError]);

  if (!messageId) return <p style={{ padding: '1rem' }}>Select a message from the list</p>;
  if (isLoading) return <LoadingSpinner message="Loading message..." />;

  return (
    <div style={{ padding: '1rem' }}>
      <h2>Message Detail</h2>
      <p><strong>ID:</strong> {data.id}</p>
      <p><strong>Message:</strong> {data.message}</p>
    </div>
  );
};

export default MessageDetailViewer;
