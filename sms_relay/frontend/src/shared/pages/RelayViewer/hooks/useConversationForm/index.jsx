import { useCallback, useMemo, useEffect } from 'react';
import { useMessagesByThread } from '~/api/conversation';
import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { useRespondToThread } from '~/api/conversation';

  

const useConversationForm = (activeThread) => {
  const { mutate: postResponse } = useRespondToThread();
  const formMethods = useForm({
    mode: 'onBlur',
    values: {response: null},
  });

  const {
    data: threadMessages,
    isLoading: threadLoading,
    isError: threadError,
  } = useMessagesByThread(activeThread.id);

  const threadContent = useMemo(
    () => {
        if(threadMessages && threadMessages.length > 0) {
            return threadMessages;
        }
        return [];

    }, [threadMessages]
);

const [currentThreadContentState, setCurrentThreadContentState] = useState([]);
useEffect(() => {
  setCurrentThreadContentState(threadContent);
}, [threadContent]);

const { setError, dirtyFields, resetField } = formMethods;

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

  const sendSms = useCallback((values) => {
    postResponse(
      {
        threadId: activeThread.id,
        payloadBody: {message_body: values.response,
        phone_number_used: activeThread.phone_number_used,
        integration_contact_id: activeThread.integration_contact.id}
      },
      {
        onSuccess: (data ) => {
          resetField('response', { defaultValue: '' });
          setCurrentThreadContentState(
            [
              ...currentThreadContentState,
              {
                date: data.date,
                id: data.id,
                message: data.message,
                // can assume integration contact since this is coming from UI
                sender: {
                  source: 'internal',
                }
              },
            ]
          )

          },
        onError: revealServerValidationErrors,
      }
    )

  }, [activeThread, dirtyFields, currentThreadContentState, setCurrentThreadContentState, resetField])



  const methods = useMemo(
    () => ({
      currentThreadContentState,
      threadLoading,
      threadError,
      sendResponse: () => {
        const handleSubmitFunction = formMethods.handleSubmit((formData) => {
          sendSms(formData);
        });
        handleSubmitFunction();
      },
    }),
    [currentThreadContentState, threadLoading, threadError, sendSms, formMethods]
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

export default useConversationForm;
