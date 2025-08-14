import { useContext } from 'react';
import { ContactContext } from './ContactContextProvider';

export const useContacts = () => {
  const context = useContext(ContactContext);

  if (!context) {
    throw new Error('ContactContext not found!');
  }

  return context;
};
