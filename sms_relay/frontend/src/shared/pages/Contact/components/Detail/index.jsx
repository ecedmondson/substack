import { useContactDetail } from '~/api/contact'; // assuming this hook exists
import { useContacts } from '../../hooks/useContacts'; // hypothetical similar hook to useMessages
import ErrorMessage from '~/shared/components/ErrorMessage';
import NoData from '~/shared/components/NoData';
import LoadingSpinner from '~/shared/components/Loader';
import ContactDetailViewer from './Viewer';
import ContactDetailForm from './Form';
import ContactRelayConfigForm from './Config';
import './styles.less';

const ContactDetailManager = () => {
  const {
    selectedContact,
    isEditing,
    isConfiguringRules,
  } = useContacts();

  const {
    data: contactData,
    isLoading,
    isError,
  } = useContactDetail(selectedContact);

  if (!selectedContact) return <NoData message="No contact selected." />;
  if (isLoading) return <LoadingSpinner />;
  if (isError) return <ErrorMessage />;

  if(isEditing) return <ContactDetailForm contact={contactData} />;
  if(isConfiguringRules) {
    return <ContactRelayConfigForm contact={contactData} />;
  }
  return <ContactDetailViewer />;
};

export default ContactDetailManager;
