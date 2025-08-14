import GenericSidebar from '~/shared/components/GenericSidebar';
import { useContacts } from '../../hooks/useContacts'; // hypothetical hook
import ContactListItem from './ContactListItem';

const ContactListSidebar = () => {
  const { contactList, selectContact, selectedContact } = useContacts();

  return (
    <GenericSidebar
      title="Contacts"
      items={contactList}
      selectedId={selectedContact}
      onSelect={selectContact}
      renderItem={(contact) => <ContactListItem contact={contact}
      emoji='👥' />}
    />
  );
};

export default ContactListSidebar;
