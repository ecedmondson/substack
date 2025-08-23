
import Layout from '~/shared/components/Layout';
import ThreadsViewer from './components/Viewer';
import ErrorMessage from '~/shared/components/ErrorMessage';
import LoadingSpinner from '~/shared/components/Loader';
import { RelayMessagesProvider } from './hooks/useRelayMessages/RelayMessagesContextProvider';
import { useRelayMessages } from './hooks/useRelayMessages';

const RelayViewerPageContent = () => {
    const {
        conversationThreadLoading,
        conversationThreadError,
    } = useRelayMessages();

    if (conversationThreadLoading) {
        return <LoadingSpinner message="Fetching messages..." />;
      }
    
      if (conversationThreadError) {
        return (
          <Layout>
            <ErrorMessage error={messagesError} />
          </Layout>
        );
      }

      return (
        <Layout>
          <ThreadsViewer />
        </Layout>
      );



}

const RelayViewerPage = () => {
  return (
      <RelayMessagesProvider>
        <RelayViewerPageContent />
      </RelayMessagesProvider>
  )




};

export default RelayViewerPage;
