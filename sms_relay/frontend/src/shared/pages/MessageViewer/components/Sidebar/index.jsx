import './styles.less';
import { useMessages } from '../../hooks/useMessages';

const MessageListSidebar = () => {
  const {
    messagesList,
    selectMessage,
    selectedMessage,
  } = useMessages();

  return (
    <div className="message-sidebar">
      <h3 className="message-sidebar-title">Messages</h3>
      <ul className="message-sidebar-list">
        {messagesList.map((msg) => (
          <li
            key={msg.id}
            className={`message-sidebar-item${
              msg.id === selectedMessage ? ' selected' : ''
            }`}
            onClick={() => selectMessage(msg.id)}
          >
            <div className="msg-snippet">{msg.message.slice(0, 60)}</div>
            <div className="msg-meta">
              <span>{msg.contact?.first_name ?? 'Unknown'}</span>
              <span className="msg-date">{msg.date}</span>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default MessageListSidebar;
