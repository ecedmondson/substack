import { useMessageDetail } from '~/api/message';
import { useMessages } from '../../hooks/useMessages';
import ErrorMessage from '~/shared/components/ErrorMessage';
import NoData from '~/shared/components/NoData';
import LoadingSpinner from '~/shared/components/Loader';
import './styles.less';

const MessageDetailViewer = () => {
  const {
    selectedMessage,
    deselectMessage,
  } = useMessages();

  const {
    data: messageData,
    isLoading,
    isError,
  } = useMessageDetail(selectedMessage);

  if (!selectedMessage) return <NoData message="No message selected." />;
  if (isLoading) return <LoadingSpinner />;
  if (isError) return <ErrorMessage />;

  const { id, message, date, created, contact } = messageData;

  return (
    <div className="message-detail">
      <div className="message-detail-header">
        <h2>Message Detail</h2>
        <button onClick={deselectMessage} className="back-button">← Back</button>
      </div>

      <div className="message-card">
        <p><strong>ID:</strong> {id}</p>
        <p><strong>Message:</strong> {message}</p>
        <p><strong>Date:</strong> {date}</p>
        <p><strong>Created:</strong> {new Date(created).toLocaleString()}</p>
      </div>

      <div className="contact-card">
        <h3>Contact Info</h3>
        <p><strong>Name:</strong> {contact.first_name || 'Unknown'}</p>
        <p><strong>Note:</strong> {contact.note || 'None'}</p>
        <p><strong>Phone:</strong> {contact.phone_numbers?.[0]?.number || '—'}</p>
      </div>
    </div>
  );
};

export default MessageDetailViewer;
