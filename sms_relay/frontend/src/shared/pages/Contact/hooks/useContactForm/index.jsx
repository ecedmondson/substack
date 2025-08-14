import { useCallback, useMemo } from 'react';
import { useForm } from 'react-hook-form';
import { useUpdateContact } from '~/api/contact';

const deserializeContact = (contact) => {
    return {
      first_name: contact.first_name,
      last_name: contact.last_name,
      note: contact.note,
      primary_phone_number: contact.phone_numbers?.[0]?.number || null,
    };
  };

const serializeContact = (contact, formValues) => {
  const data = {
    id: contact.id,
    first_name: formValues.first_name,
    last_name: formValues.last_name,
    note: formValues.note,
    phone_numbers: contact.phone_numbers.map((entry) => ({
    number: entry.number
    }))
};
console.log('serializdd', data);
return data;
};
  

const useContactForm = ({ contact }) => {
  const { mutate: putContact } = useUpdateContact();
  const contactValues = deserializeContact(contact);
  console.log('contactValues', contactValues);

  const formMethods = useForm({
    mode: 'onBlur',
    values: contactValues,
  });

  const { setError, dirtyFields, reset } = formMethods;

  const clearAndClose = useCallback(
    (close) => {
      reset();
      close();
    },
    [reset],
  );

  const setErrorOnField = useCallback(
    (errors, field) => {
      const firstErrorMessage = errors[0];
      setError(field, { type: 'server', message: firstErrorMessage });
    },
    [setError],
  );

  const revealServerValidationErrors = useCallback(
    (errorResp) => {
      _forOwn(errorResp.body, setErrorOnField);
    },
    [setErrorOnField],
  );

  const editContact = useCallback(
    (values, close) => {
      putContact(
        {
          id: contact.id,
          updatedData: serializeContact(contact, values),
        },
        {
          onSuccess: () => {
            close();
          },
          onError: revealServerValidationErrors,
        },
      );
    },
    [contact, putContact, close, reset, dirtyFields],
  );


  const methods = useMemo(
    () => ({
      writeContact: (close) => {
        const handleSubmitFunction = formMethods.handleSubmit((formData) => {
          editContact(formData, close);
        });
        handleSubmitFunction();
      },
      clearAndClose,
    }),
    [formMethods, editContact, clearAndClose],
  );

  const returnedMethods = useMemo(
    () => ({
      formMethods: {
        ...formMethods,
        ...methods,
      },
    }),
    [formMethods, methods],
  );

  return returnedMethods;
};

export default useContactForm;
