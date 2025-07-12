import { useContactDetail } from '~/api/contact'; // assuming this hook exists
import { useContacts } from '../../hooks/useContacts'; // hypothetical similar hook to useMessages
import ErrorMessage from '~/shared/components/ErrorMessage';
import NoData from '~/shared/components/NoData';
import LoadingSpinner from '~/shared/components/Loader';
import './styles.less';

const ContactDetailViewer = () => {
  const {
    selectedContact,
    deselectContact,
  } = useContacts();

  const {
    data: contactData,
    isLoading,
    isError,
  } = useContactDetail(selectedContact);
  console.log('selected', selectedContact);
  console.log('data', contactData);

  if (!selectedContact) return <NoData message="No contact selected." />;
  if (isLoading) return <LoadingSpinner />;
  if (isError) return <ErrorMessage />;

  const { first_name, last_name, note, phone_numbers } = contactData;

  return (
    <div className="contact-detail">
      <div className="contact-detail-header">
        <h2>Contact Detail</h2>
        <button onClick={deselectContact} className="back-button">← Back</button>
      </div>

      <div className="contact-card">
        <p><strong>Name:</strong> {first_name} {last_name || ''}</p>
        <p><strong>Note:</strong> {note || 'None'}</p>
        <p><strong>Phone Numbers:</strong></p>
        <ul>
          {phone_numbers?.length
            ? phone_numbers.map((phone) => (
                <li key={phone.id}>{phone.number}</li>
              ))
            : <li>—</li>}
        </ul>
      </div>
    </div>
  );
};

export default ContactDetailViewer;
