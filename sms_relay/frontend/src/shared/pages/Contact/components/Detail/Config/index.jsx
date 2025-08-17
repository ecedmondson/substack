import { useContacts } from '../../../hooks/useContacts';
import ControlledSwitchInput from '~/shared/components/Form/ControlledSwitchInput';
import '../styles.less';
import Switch from '@mui/material/Switch';
import { FormProvider } from 'react-hook-form';
import { useCallback } from 'react';
import useContactRelayForm from '../../../hooks/useContactRelayForm';

const FormSwitch = ({ rule, contactRuleConfig, onChange, disabledFunc }) => {

    const checkedFunc = useCallback((ruleId) => {
        for (let i = 0; i < contactRuleConfig.length; i++) {
            if(ruleId === contactRuleConfig[i].rule_id) {
                console.log('in checkedFunc', contactRuleConfig[i]);
                return contactRuleConfig[i].enabled;
            }
            
          }
        return false;

    }, [contactRuleConfig]);

    return (
        <div className='form-switch-container'>
        <Switch
          name={rule.category}
          disabled={disabledFunc(rule.category)}
          onChange={onChange}
          value={rule.id}
          checked={checkedFunc(rule.id)}
        />
        <div className='form-switch-label'>
            {rule.category}
        </div>
        </div>
    )
}
const FormContent = ({ contact }) => {
    const {
            rulesList,
            contactRuleConfig,
            disabledChecker,
            handleRuleConfigMutation,
        } = useContactRelayForm({
        contact
    });

    return (
        <div className="contact-rules-card">
        <div className="form-inputs">
        {rulesList?.map(rule =>
          <FormSwitch rule={rule} contactRuleConfig={contactRuleConfig} onChange={handleRuleConfigMutation} disabledFunc={disabledChecker} />
        )}
      </div>
      </div>
    )

}

const ContactRelayConfigForm = ({ contact }) => {
  const {
    stopConfiguringRules,
  } = useContacts();


  return (
    <div className="contact-rules">
      <div className="contact-rules-header">
        <h2>Contact Relay Config</h2>
        <div className="buttons-container">
          <button onClick={stopConfiguringRules} className="back-button">← Return</button>
        </div>
      </div>
      <div className='contact-rules-form'>
          <FormContent contact={contact}/>
      </div>
    </div>
  );
};

export default ContactRelayConfigForm;
