import ErrorMessage from '~/shared/components/ErrorMessage';
import NoData from '~/shared/components/NoData';
import LoadingSpinner from '~/shared/components/Loader';
import { useRelayMessages } from '../../hooks/useRelayMessages';
import useConversationForm from '../../hooks/useConversationForm';
import ControlledTextAreaInput from '~/shared/components/Form/ControlledTextAreaInput';
import './styles.less';
import { FormProvider } from 'react-hook-form';
import { useRef, useLayoutEffect } from 'react';

const formatDate = (isoString) => {
    if (!isoString) return '';
    const date = new Date(isoString);
    return date.toLocaleString(undefined, {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

const MessageItem = ({ message }) => {
    const alignmentClass =
      message?.sender?.source === "external"
        ? "messageItemLeft"
        : "messageItemRight";
  
    return (
      <div className={`messageItem ${alignmentClass}`}>
        <span className="messageText">
            {message.message}
            <span className="messageDate">{formatDate(message.date)}</span>
        </span>
        
      </div>
    );
  };
  
  

  const ExistingMessages = ({ threadMessages }) => {
    const containerRef = useRef(null);

    useLayoutEffect(() => {
        if (containerRef.current) {
          containerRef.current.scrollTop = containerRef.current.scrollHeight;
        }
      }, [threadMessages]);

    return (
      <div className="existingMessageContainer" ref={containerRef}>
        {threadMessages.map((message) => (
          <MessageItem key={message.id} message={message} />
        ))}
      </div>
    );
  };

  const SendMessage = ({ submit }) => {
      return (
        <div className="responseInput">
            <ControlledTextAreaInput
            rows={3}
            name='response'
            label='Response'
        />
        <div className="buttons-container">
          <button onClick={submit} className="send-button">Send ➤</button>
        </div>
        </div>
      )

  }

const CovnersationDetailViewer = () => {
  const {
    selectedThread,
    deselectThread,
  } = useRelayMessages();

  if (!selectedThread) return <NoData message="No conversation selected." />;

  const {
    formMethods,
  } = useConversationForm(selectedThread);

  const { currentThreadContentState: threadMessages, threadLoading, threadError, sendResponse } = formMethods;

  console.log('threadMessages', threadMessages);
  if (threadLoading) return <LoadingSpinner />;
  if (threadError) return <ErrorMessage />;



  return (
    <div className="contact-detail">
      <div className="contact-detail-header">
        <h2>Conversation</h2>
        <div className="buttons-container">
          <button onClick={deselectThread} className="back-button">← Return</button>
        </div>
      </div>
      <div className="conversationContent">
        <ExistingMessages threadMessages={threadMessages} />
        <FormProvider {...formMethods}>
            <SendMessage submit={sendResponse}/>
        </FormProvider>
      </div>
    </div>
  );
};

export default CovnersationDetailViewer;
