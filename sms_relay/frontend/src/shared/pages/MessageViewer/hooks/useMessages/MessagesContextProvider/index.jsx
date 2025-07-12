import { createContext, useState, useCallback, useMemo } from 'react';
import { useMessagesList, useMessageDetail } from '~/api/message';

export const MessagesContext = createContext();

export const MessagesProvider = ({ children }) => {
  const {
      data: messagesList,
      isLoading: messagesLoading,
      isError: messagesError,
  } = useMessagesList();

  const [selectedMessage, setSelectedMessage] = useState(null);

  const selectMessage = useCallback((id) => {
      setSelectedMessage(id);
  }, [setSelectedMessage]);

  const deselectMessage = useCallback((id) => {
      setSelectedMessage(null);
  }, [setSelectedMessage]);


  const value = useMemo(() => {
    return {
      messagesList,
      messagesLoading,
      messagesError,
      selectMessage,
      selectedMessage,
      deselectMessage,
    };
  }, [
    messagesList,
    messagesLoading,
    messagesError,
    selectMessage,
    selectedMessage,
    deselectMessage,
  ]);
  return (
    <MessagesContext.Provider value={value}>
      {children}
    </MessagesContext.Provider>
  );
};
