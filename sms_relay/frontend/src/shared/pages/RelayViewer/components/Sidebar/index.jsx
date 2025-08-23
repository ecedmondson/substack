import GenericSidebar from '~/shared/components/GenericSidebar';
import { useRelayMessages } from '../../hooks/useRelayMessages';
import ThreadListItem from './ThreadListItem';

const ThreadListSidebar = () => {
  const {
    conversationThreadList,
    selectThread,
    selectedThread,
  } = useRelayMessages();


  return (
    <GenericSidebar
      title="Conversation Threads"
      items={conversationThreadList}
      selectedId={selectedThread?.id || null}
      onSelect={selectThread}
      renderItem={(thread) => <ThreadListItem thread={thread} />}
    />
  );
};

export default ThreadListSidebar;
