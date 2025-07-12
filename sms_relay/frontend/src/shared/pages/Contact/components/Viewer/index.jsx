
import ContactListSidebar from '../Sidebar';
import ContactDetailViewer from '../Detail';
import './styles.less';

const ContactViewer = () => {
  return (
    <div className="contact-viewer">
      <ContactListSidebar />
      <ContactDetailViewer />
    </div>
  );
};

export default ContactViewer;
