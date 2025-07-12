import { createContext, useState, useCallback, useMemo } from 'react';
import { useContactList, useContactDetail } from '~/api/contact';

export const ContactContext = createContext();

export const ContactProvider = ({ children }) => {
  const {
      data: contactList,
      isLoading: contactLoading,
      isError: contactError,
  } = useContactList();

  const [selectedContact, setSelectedContact] = useState(null);

  const selectContact = useCallback((item) => {
    console.log('item', item);
      setSelectedContact(item.id);
  }, [setSelectedContact]);

  const deselectContact = useCallback((id) => {
      setSelectedContact(null);
  }, [setSelectedContact]);


  const value = useMemo(() => {
    return {
      contactList,
      contactLoading,
      contactError,
      selectContact,
      selectedContact,
      deselectContact,
    };
  }, [
    contactList,
    contactLoading,
    contactError,
    selectContact,
    selectedContact,
    deselectContact,
  ]);
  return (
    <ContactContext.Provider value={value}>
      {children}
    </ContactContext.Provider>
  );
};
