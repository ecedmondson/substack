import { useContacts } from '../../../hooks/useContacts';
import ControlledTextInput from '~/shared/components/Form/ControlledTextInput';
import ControlledTextAreaInput from '~/shared/components/Form/ControlledTextAreaInput';
import '../styles.less';
import { FormProvider } from 'react-hook-form';
import useContactForm from '../../../hooks/useContactForm';


const FormContent = ( { save }) => {
    return (
        <div className="contact-card">
        <div className="form-inputs">
        <ControlledTextInput
          name='first_name'
          label='First Name'
        />
        <ControlledTextInput
          name='last_name'
          label='Last Name'
        />
        <ControlledTextAreaInput
        rows={3}
        name='note'
        label='Note'
      />
    <div className="buttons-container">
          <button onClick={save} className="back-button">Save</button>
        </div>
      </div>
      </div>
    )

}

const ContactDetailForm = ({ contact }) => {
  const {
    formMethods,
  } = useContactForm({
    contact
  });

  const {
    stopEditing,
  } = useContacts();

  const save = () => {
      formMethods.writeContact(stopEditing);
  }

  return (
    <div className="contact-detail">
      <div className="contact-detail-header">
        <h2>Edit Contact Detail</h2>
        <div className="buttons-container">
          <button onClick={stopEditing} className="back-button">← Stop Editing</button>
        </div>
      </div>
      <div className='contact-form'>
      <FormProvider {...formMethods}>
          <FormContent save={save} />
      </FormProvider>

      <div className="contact-card">
        <p><strong>Associated Phone Numbers:</strong></p>
        <ul>
          {contact.phone_numbers?.length
            ? contact.phone_numbers.map((phone) => (
                <li key={phone.id}>{phone.number}</li>
              ))
            : <li>—</li>}
        </ul>
      </div>
      </div>
    </div>
  );
};

export default ContactDetailForm;
