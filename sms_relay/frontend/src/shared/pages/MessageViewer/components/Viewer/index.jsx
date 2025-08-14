
import MessageListSidebar from '../Sidebar';
import MessageDetailViewer from '../Detail';
import './styles.less';

const MessageViewer = () => {
  return (
    <div className="message-viewer">
      <MessageListSidebar />
      <MessageDetailViewer />
    </div>
  );
};

export default MessageViewer;
