const MessageListItem = ({ msg }) => (
  <>
    <div className="msg-snippet">{msg.message.slice(0, 60)}</div>
    <div className="msg-meta">
      <span>{msg.contact?.first_name ?? 'Unknown'}</span>
      <span className="msg-date">{msg.date}</span>
    </div>
  </>
);

export default MessageListItem;
