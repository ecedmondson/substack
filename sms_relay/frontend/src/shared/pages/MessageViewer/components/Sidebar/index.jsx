import GenericSidebar from '~/shared/components/GenericSidebar';
import { useMessages } from '../../hooks/useMessages';
import MessageListItem from './MessageListItem';

const MessageListSidebar = () => {
  const { messagesList, selectMessage, selectedMessage } = useMessages();

  return (
    <GenericSidebar
      title="Messages"
      items={messagesList}
      selectedId={selectedMessage}
      onSelect={selectMessage}
      renderItem={(msg) => <MessageListItem msg={msg} />}
    />
  );
};

export default MessageListSidebar;
