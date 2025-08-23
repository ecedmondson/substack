
import Layout from '~/shared/components/Layout';
import MessageViewer from './components/Viewer';
import ErrorMessage from '~/shared/components/ErrorMessage';
import LoadingSpinner from '~/shared/components/Loader';
import { MessagesProvider } from './hooks/useMessages/MessagesContextProvider';
import { useMessages } from './hooks/useMessages';

const MessageViewerPageContent = () => {
    const {
        messagesLoading,
        messagesError
    } = useMessages();

    if (messagesLoading) {
        return <LoadingSpinner message="Fetching messages..." />;
      }
    
      if (messagesError) {
        return (
          <Layout>
            <ErrorMessage error={messagesError} />
          </Layout>
        );
      }

      return (
        <Layout>
          <MessageViewer />
        </Layout>
      );



}

const MessageViewerPage = () => {
  return (
      <MessagesProvider>
        <MessageViewerPageContent />
      </MessagesProvider>
  )




};

export default MessageViewerPage;
