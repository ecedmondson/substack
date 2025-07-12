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
  const [isEditing, setIsEditing] = useState(null);

  const selectContact = useCallback((item) => {
      setSelectedContact(item.id);
  }, [setSelectedContact]);

  const deselectContact = useCallback((id) => {
      setSelectedContact(null);
  }, [setSelectedContact]);

  const startEditing = useCallback(() => {
    setIsEditing(true);
  }, [setIsEditing]);

  const stopEditing = useCallback(() => {
    setIsEditing(false);
  }, [setIsEditing]);

  const value = useMemo(() => {
    return {
      contactList,
      contactLoading,
      contactError,
      selectContact,
      selectedContact,
      deselectContact,
      isEditing,
      startEditing,
      stopEditing,
    };
  }, [
    contactList,
    contactLoading,
    contactError,
    selectContact,
    selectedContact,
    deselectContact,
    isEditing,
    startEditing,
    stopEditing,
  ]);
  return (
    <ContactContext.Provider value={value}>
      {children}
    </ContactContext.Provider>
  );
};
