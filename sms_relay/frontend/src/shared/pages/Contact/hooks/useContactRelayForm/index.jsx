import { useCallback, useMemo } from 'react';
import { useRuleList, useAddRuleToConfig, useDisableRuleInConfig} from '~/api/relay';
import { useState } from 'react';

  

const useContactRelayForm = ({ contact }) => {
    const {
        data: rulesList,
        isLoading: ruleLoading,
        isError: ruleError,
    } = useRuleList();

    const contactRules = useMemo(
        () => {
            if(contact) {
                return contact.rules[0].rule_links;
            }
            return [];

        }, [contact]
    );

    const contactConfigId = useMemo(
        () => {
            if(contact) {
                return contact.rules[0].id;
            }
            return null;
        }, [contact]
    )

    const [contactRuleConfig, setContactRuleConfig] = useState(contactRules);


  const { mutate: createRuleAssociation} = useAddRuleToConfig(contact.id);
  const {mutate: disableRuleMutation } = useDisableRuleInConfig(contact.id);

  const addRuleToConfig= useCallback(
    (values) => {
      createRuleAssociation(
        {
          config_id: contactConfigId,
          rule_id: values.rule_id,
        },
        {
            onSuccess: () => {
                let foundValue = false;
                for (let i = 0; i < contactRuleConfig.length; i++) {
                    if(values.rule_id === contactRuleConfig[i].rule_id) {
                        contactRuleConfig[i].enabled = true;
                        foundValue = true;
                    }
                    
                  }
                if(!foundValue) {
                    setContactRuleConfig([ {enabled: true, rule_id: values.rule_id, config_id: contactConfigId}, ...contactRuleConfig ]);
                }
                else {
                    setContactRuleConfig([...contactRuleConfig])
                }

                }

          },
      );
    },
    [contactConfigId, setContactRuleConfig, contactRuleConfig, createRuleAssociation],
  );

  const removeRuleFromConfig = useCallback(
      (values) => {
          disableRuleMutation(
          {
            config_id: contactConfigId,
              rule_id: values.rule_id,
          },
          {
              onSuccess: () => {
                for (let i = 0; i < contactRuleConfig.length; i++) {
                    if(values.rule_id === contactRuleConfig[i].rule_id) {
                        contactRuleConfig[i].enabled = false;
                    }
                    
                  }
                  setContactRuleConfig([...contactRuleConfig])
              }
          }
          )

      }, [contactConfigId, setContactRuleConfig, contactRuleConfig, disableRuleMutation]
  );

  const handleRuleConfigMutation = useCallback(
    (switchClickEvent) => {
        if(switchClickEvent.target.checked) {
            addRuleToConfig(
                {
                    rule_id: switchClickEvent.target.value,
                }
            )
        }
        else {
            removeRuleFromConfig(
                {
                    rule_id: switchClickEvent.target.value,
                }
            )
        }
    },
    [addRuleToConfig, contactConfigId],
  );

  
  const disabledChecker = useCallback(
      (ruleValue) => {
      return false;
  }, [contactRuleConfig]
  );

  const methods = useMemo(
    () => ({
      addRuleToConfig,
      rulesList,
      contactRuleConfig,
      disabledChecker,
      handleRuleConfigMutation,
    }),
    [addRuleToConfig, rulesList, disabledChecker, handleRuleConfigMutation],
  );

  return methods;
};

export default useContactRelayForm;
