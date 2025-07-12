import { useMessageDetail } from '~/api/message';
import { useMessages } from '../../hooks/useMessages';
import ErrorMessage from '~/shared/components/ErrorMessage';
import NoData from '~/shared/components/NoData';
import LoadingSpinner from '~/shared/components/Loader';

const MessageDetailViewer = () => {
  const {
    selectedMessage,
    deselectMessage,
  } = useMessages();
  const {
    data: messageData,
    isLoading: messageLoading,
    isError: messageError,
  } = useMessageDetail(selectedMessage);

  if(!selectedMessage) {
    return <NoData message={'No message selected.'}/>
  }

  if(selectedMessage && messageLoading) {
    return <LoadingSpinner />
  }

  if(selectedMessage && messageError) {
    return <ErrorMessage />
  }

  return (
    <div style={{ padding: '1rem' }}>
      <h2>Message Detail</h2>
      <p><strong>ID:</strong> {messageData.id}</p>
      <p><strong>Message:</strong> {messageData.message}</p>
    </div>
  );
};

export default MessageDetailViewer;
