import GenericItem from "~/shared/components/GenericItem"

const formatName = (contact) => {
    if(contact.first_name && contact.last_name) {
        return `* ${contact.first_name} ${contact.last_name}`
    }
    if(contact.first_name) {
        if (contact.first_name !== 'Unknown') {
          return `* ${contact.first_name} Null`
        }
        return contact.first_name
    }
    if(contact.last_name) {
        return `* Null ${contact.last_name}`
    }
    return '* Unknown *'
}

const ContactListItem = ({ contact }) => {
  const note = contact.note?.slice(0, 12)
  
  return (
  <GenericItem>
    <div className="msg-snippet">{formatName(contact)}</div>
    <div className="msg-meta">
      <span>{contact.phone_numbers?.[0]?.number ?? 'No phone'}</span>
    </div>
    <div className="msg-meta">
      <span><b>Note:</b></span>
      <span className="msg-date">{note ? `${note}...` : ""}</span>
    </div>
    </GenericItem>
  );
};

export default ContactListItem;
