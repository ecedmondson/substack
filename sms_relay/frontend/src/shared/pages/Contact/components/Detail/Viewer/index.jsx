import { useContactDetail } from '~/api/contact';
import { useContacts } from '../../../hooks/useContacts';
import '../styles.less';

const ContactDetailViewer = () => {
  const {
    selectedContact,
    deselectContact,
    startEditing,
  } = useContacts();

  const {
    data: contactData,
  } = useContactDetail(selectedContact);

  const { first_name, last_name, note, phone_numbers } = contactData;

  return (
    <div className="contact-detail">
      <div className="contact-detail-header">
        <h2>Contact Detail</h2>
        <div className="buttons-container">
          <button onClick={startEditing} className="edit-button">Edit</button>
          <button onClick={deselectContact} className="back-button">← Back</button>
        </div>
      </div>

      <div className="contact-card">
        <p><strong>Name:</strong> {first_name} {last_name || ''}</p>
        <p><strong>Note:</strong> {note || 'None'}</p>
        <p><strong>Associated Phone Numbers:</strong></p>
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
