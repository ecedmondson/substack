
import ContactListSidebar from '../Sidebar';
import ContactDetailManager from '../Detail';
import './styles.less';

const ContactViewer = () => {
  return (
    <div className="contact-viewer">
      <ContactListSidebar />
      <ContactDetailManager />
    </div>
  );
};

export default ContactViewer;
