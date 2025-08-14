
import Layout from '~/shared/components/Layout';
import ContactViewer from './components/Viewer';
import ErrorMessage from '~/shared/components/ErrorMessage';
import LoadingSpinner from '~/shared/components/Loader';
import { ContactProvider } from './hooks/useContacts/ContactContextProvider';
import { useContacts } from './hooks/useContacts';

const ContactViewerPageContent = () => {
    const {
        contactsLoading,
        contactsError
    } = useContacts();

    if (contactsLoading) {
        return <LoadingSpinner Contact="Fetching Contacts..." />;
      }
    
      if (contactsError) {
        return (
          <Layout>
            <ErrorMessage error={contactsError} />
          </Layout>
        );
      }

      return (
        <Layout>
          <ContactViewer />
        </Layout>
      );



}

const ContactViewerPage = () => {
  return (
      <ContactProvider>
        <ContactViewerPageContent />
      </ContactProvider>
  )




};

export default ContactViewerPage;
