import { useController, useFormContext } from 'react-hook-form';
import TextField from '@mui/material/TextField';

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
        sx={{ width: "100%" }}
      />
    </div>
  );
};

export default ControlledTextAreaInput;
