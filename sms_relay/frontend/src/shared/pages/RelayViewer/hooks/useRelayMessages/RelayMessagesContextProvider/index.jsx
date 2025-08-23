import { createContext, useState, useCallback, useMemo } from 'react';
import { useConversationThreads } from '~/api/conversation';

export const RelayMessagesContext = createContext();

export const RelayMessagesProvider = ({ children }) => {
  const {
      data: conversationThreadList,
      isLoading: conversationThreadLoading,
      isError: conversationThreadError,
  } = useConversationThreads();

  const [selectedThread, setSelectedThread] = useState(null);

  const selectThread = useCallback((item) => {
      setSelectedThread(item);
  }, [setSelectedThread]);

  const deselectThread = useCallback((id) => {
      setSelectedThread(null);
  }, [setSelectedThread]);


  const value = useMemo(() => {
    return {
      conversationThreadList,
      conversationThreadLoading,
      conversationThreadError,
      selectThread,
      selectedThread,
      deselectThread,
    };
  }, [
    conversationThreadList,
    conversationThreadLoading,
    conversationThreadError,
    selectThread,
    selectedThread,
    deselectThread,
  ]);
  return (
    <RelayMessagesContext.Provider value={value}>
      {children}
    </RelayMessagesContext.Provider>
  );
};
