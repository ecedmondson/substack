import React, { useState } from 'react';
import { useMessagesList } from '~/api/message';
import MessageListSidebar from '../Sidebar';
import MessageDetailViewer from '../Detail';

const MessageViewer = ({ setError }) => {
  const { data: messages = [] } = useMessagesList(); // uses cache
  const [selectedId, setSelectedId] = useState(messages?.[0]?.id || null);

  return (
    <div style={{ display: 'flex', height: '100vh' }}>
      <MessageListSidebar
        messages={messages}
        selectedId={selectedId}
        onSelect={setSelectedId}
      />
      <MessageDetailViewer messageId={selectedId} setError={setError} />
    </div>
  );
};

export default MessageViewer;
