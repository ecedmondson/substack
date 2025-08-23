const ThreadListItem = ({ thread }) => {
    const contactName = thread.contact?.first_name ?? "Unknown";
    const recentMessage = thread.most_recent_message;
    const isFromUser =
      recentMessage?.contact?.id === thread.integration_contact?.id;
  
    return (
      <div className="thread-item space-y-1">
        <div className="thread-meta flex gap-2">
          <span className="font-medium">From:</span>
          <span>{contactName}</span>
        </div>
  
        {recentMessage && (
          <div className="thread-snippet flex flex-col gap-1">
            <div>
              <span className="font-medium">Message preview:</span>{" "}
              <span>{recentMessage.message.slice(0, 15)}...</span>
            </div>
            <div>
              <span className="font-medium">Sent:</span>{" "}
              <span>{recentMessage.date}</span>
            </div>
            <div>
              <span className="font-medium">By:</span>{" "}
              <span>{isFromUser ? "You" : contactName}</span>
            </div>
          </div>
        )}
      </div>
    );
  };
  
  export default ThreadListItem;
  