import React from 'react';

const MessageListSidebar = ({ messages, selectedId, onSelect }) => {
  return (
    <div style={{ width: 250, borderRight: '1px solid #ccc', overflowY: 'auto', height: '100vh' }}>
      <h3 style={{ padding: '1rem' }}>Messages</h3>
      <ul style={{ listStyle: 'none', padding: 0 }}>
        {messages.map((msg) => (
          <li
            key={msg.id}
            onClick={() => onSelect(msg.id)}
            style={{
              padding: '0.5rem 1rem',
              cursor: 'pointer',
              backgroundColor: msg.id === selectedId ? '#eee' : 'transparent',
            }}
          >
            {msg.message.slice(0, 30)}{/* preview snippet */}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default MessageListSidebar;
