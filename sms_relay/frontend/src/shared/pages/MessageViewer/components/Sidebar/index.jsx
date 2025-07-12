import './styles.less';
import { useMessages } from '../../hooks/useMessages';

const MessageListSidebar = () => {
  const {       
    messagesList,
    selectMessage,
  } = useMessages();
  return (
    <div className="message-sidebar">
      <h3 className="message-sidebar-title">Messages</h3>
      <ul className="message-sidebar-list">
        {messagesList.map((msg) => (
          <li
            key={msg.id}
            className={`message-sidebar-item${msg.id === selectedId ? ' selected' : ''}`}
            onClick={() => selectMessage(msg.id)}
          >
            {msg.message.slice(0, 30)}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default MessageListSidebar;
