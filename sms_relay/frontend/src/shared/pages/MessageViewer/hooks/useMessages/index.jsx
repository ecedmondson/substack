import { useContext } from 'react';
import { MessagesContext } from './MessagesContextProvider';

export const useMessages = () => {
  const context = useContext(MessagesContext);

  if (!context) {
    throw new Error('MessagesContext not found!');
  }

  return context;
};
