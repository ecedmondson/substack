import PropTypes from 'prop-types';
import { useController, useFormContext } from 'react-hook-form';
import Switch from '@mui/material/Switch';
import styles from './styles.module.less';

/**
 * React Hook From Controlled Switch Input
 * @param {string} name
 * @param {string} label
 * @param {string} ariaLabel
 * @param {object} rules
 * @see {Documentation} https://react-hook-form.com/docs/usecontroller
 * @returns {React.Component}
 */

const ControlledSwitchInput = ({ name, label, ariaLabel, rules, disabled }) => {
  const { control } = useFormContext();
  const {
    field: switchInput,
    fieldState: { error },
  } = useController({ name, control, rules });
  return (
    <div className={styles.switch}>
      <Switch
        label={label}
        name={name}
        ariaLabel={ariaLabel || label}
        checked={switchInput.value}
        disabled={disabled}
        onChange={switchInput.onChange}
      />
    </div>
  );
};

ControlledSwitchInput.propTypes = {
  name: PropTypes.string.isRequired,
  label: PropTypes.string,
  ariaLabel: PropTypes.string,
  rules: PropTypes.object,
  disabled: PropTypes.bool,
};

export default ControlledSwitchInput;
