import { useController, useFormContext } from 'react-hook-form';
import TextField from '@mui/material/TextField';
import './styles.less';

const ControlledTextInput = ({
  name,
  autoFocus,
  label,
  disabled,
  placeholder = '',
  helperText,
  maxLength,
  onChange = (v) => v,
  size = 'small',
  rules = { required: false },
  relatedFields,
  ...props
}) => {
  const { control } = useFormContext();
  const {
    field: textField,
    fieldState: { error },
  } = useController({ name, control, rules });

  return (
    <div className='container'>
      <TextField
        ref={textField.ref}
        autoFocus={autoFocus}
        disabled={disabled}
        size={size}
        maxLength={maxLength}
        name={name}
        label={label}
        placeholder={placeholder}
        onChange={(v) => {
          textField.onChange(v);
          onChange(v);
        }}
        onBlur={textField.onBlur}
        value={textField.value || ''}
        errors={error ? [error?.message] : null}
        helperText={helperText}
        dataTestId={name}
        dataHelpId={name}
        {...props}
      />
    </div>
  );
};


export default ControlledTextInput;
