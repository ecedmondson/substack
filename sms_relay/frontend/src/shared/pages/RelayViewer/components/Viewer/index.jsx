import ThreadListSidebar from '../Sidebar';
import ConversationDetailViewer from '../Detail';
import './styles.less';

const ThreadsViewer = () => {
  return (
    <div className="thread-viewer">
      <ThreadListSidebar />
      <ConversationDetailViewer />
    </div>
  );
};

export default ThreadsViewer;
