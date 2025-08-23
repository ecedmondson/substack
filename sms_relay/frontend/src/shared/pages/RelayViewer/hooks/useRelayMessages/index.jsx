import { useContext } from 'react';
import { RelayMessagesContext } from './RelayMessagesContextProvider';

export const useRelayMessages = () => {
  const context = useContext(RelayMessagesContext);

  if (!context) {
    throw new Error('RelayMessagesContext not found!');
  }

  return context;
};
