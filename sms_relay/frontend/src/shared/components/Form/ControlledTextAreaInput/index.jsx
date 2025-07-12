import { useController, useFormContext } from 'react-hook-form';
import TextField from '@mui/material/TextField';

/**
 * React Hook From Controlled TextArea Input
 * @param {string} name
 * @param {string} label
 * @param {object} rules
 * @see {Documentation} https://react-hook-form.com/docs/usecontroller
 * @returns {React.Component}
 */
const ControlledTextAreaInput = ({
  name,
  autoFocus,
  rows,
  disabled,
  label,
  showCharacterCount = false,
  maxLength,
  rules = { required: false },
}) => {
  const { control } = useFormContext();
  const {
    field,
    fieldState: { error },
  } = useController({ name, control, rules });

  return (
    <div data-help-id={name}>
      <TextField
        multiline
        ref={field.ref}
        autoFocus={autoFocus}
        size='small'
        name={name}
        label={label}
        disabled={disabled}
        onChange={field.onChange}
        onBlur={field.onBlur}
        value={field.value}
        rows={rows}
        errors={error ? [error?.message] : null}
        dataTestId={name}
        showCharacterCount={showCharacterCount}
        maxLength={maxLength}
      />
    </div>
  );
};

export default ControlledTextAreaInput;
