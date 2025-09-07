// apps/frontend/src/components/forms/FormComponents.tsx
import React, { useState } from 'react';
import type { LucideIcon } from 'lucide-react';
import { Eye, EyeOff, AlertCircle, Mail } from 'lucide-react';

// Validation ---------------------------------------------------------------

export interface ValidationRule {
  required?: boolean;
  minLength?: number;
  maxLength?: number;
  pattern?: RegExp;
  email?: boolean;
  url?: boolean;
  phone?: boolean;
  custom?: (value: string, values: Record<string, string>) => string | null;
}

export function validateField(
  value: string,
  rules: ValidationRule,
  values: Record<string, string> = {}
): string | null {
  if (rules.required && value.trim() === '') {
    return 'This field is required';
  }

  if (rules.minLength && value.length < rules.minLength) {
    return `Minimum length is ${rules.minLength} characters`;
  }

  if (rules.maxLength && value.length > rules.maxLength) {
    return `Maximum length is ${rules.maxLength} characters`;
  }

  if (rules.pattern && !rules.pattern.test(value)) {
    return 'Invalid format';
  }

  if (rules.email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) {
    return 'Invalid email address';
  }

  if (rules.url && !/^https?:\/\/.+/.test(value)) {
    return 'Invalid URL (must start with http:// or https://)';
  }

  if (rules.phone && !/^\+?[\d\s\-\(\)]+$/.test(value)) {
    return 'Invalid phone number';
  }

  if (rules.custom) {
    return rules.custom(value, values);
  }

  return null;
}

// Input -------------------------------------------------------------------

export type InputProps = Omit<React.ComponentProps<'input'>, 'value' | 'onChange'> & {
  label: string;
  value: string;
  onChange: (value: string) => void;
  helpText?: string;
  error?: string;
  icon?: LucideIcon;
  rightElement?: React.ReactNode;
};

export const Input = React.forwardRef<HTMLInputElement, InputProps>(
  (
    {
      label,
      value,
      onChange,
      helpText,
      error,
      icon: Icon,
      rightElement,
      type = 'text',
      className,
      ...rest
    },
    ref
  ) => {
    const [showPassword, setShowPassword] = useState(false);
    const inputType = type === 'password' && showPassword ? 'text' : type;

    return (
      <div className={`space-y-1 ${className ?? ''}`}>
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
          {label}
          {rest.required && <span className="text-red-500 ml-1">*</span>}
        </label>

        <div className="relative">
          {Icon && (
            <div className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400">
              <Icon size={16} />
            </div>
          )}

          <input
            {...rest}
            ref={ref}
            type={inputType}
            value={value}
            onChange={(e) => onChange(e.target.value)}
            className={`
              w-full px-3 py-2 border rounded-lg transition-colors
              ${Icon ? 'pl-10' : ''}
              ${type === 'password' || rightElement ? 'pr-10' : ''}
              ${error
                ? 'border-red-300 focus:border-red-500 focus:ring-red-500'
                : 'border-gray-300 dark:border-gray-600'}
              ${rest.disabled
                ? 'bg-gray-50 dark:bg-gray-800 text-gray-500 cursor-not-allowed'
                : 'bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100'}
              focus:outline-none focus:ring-2 focus:ring-opacity-20
            `}
          />

          {type === 'password' && (
            <button
              type="button"
              onClick={() => setShowPassword(!showPassword)}
              className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600"
            >
              {showPassword ? <EyeOff size={16} /> : <Eye size={16} />}
            </button>
          )}

          {rightElement && (
            <div className="absolute right-3 top-1/2 -translate-y-1/2">{rightElement}</div>
          )}
        </div>

        {error ? (
          <div className="flex items-center gap-1 text-sm text-red-600 dark:text-red-400">
            <AlertCircle size={14} />
            <span>{error}</span>
          </div>
        ) : (
          helpText && (
            <p className="text-sm text-gray-500 dark:text-gray-400">{helpText}</p>
          )
        )}
      </div>
    );
  }
);
Input.displayName = 'Input';

export const EmailInput = React.forwardRef<HTMLInputElement, Omit<InputProps, 'type' | 'icon'>>(
  (props, ref) => <Input {...props} ref={ref} type="email" icon={Mail} />
);
EmailInput.displayName = 'EmailInput';

export const PasswordInput = React.forwardRef<HTMLInputElement, Omit<InputProps, 'type'>>(
  (props, ref) => <Input {...props} ref={ref} type="password" />
);
PasswordInput.displayName = 'PasswordInput';

// Form --------------------------------------------------------------------

export type FormProps = React.ComponentProps<'form'>;

export function Form({ children, ...rest }: FormProps) {
  return (
    <form noValidate {...rest}>
      {children}
    </form>
  );
}

// useForm -----------------------------------------------------------------

export function useForm<T extends Record<string, string>>(
  initialValues: T,
  rules: Partial<Record<keyof T, ValidationRule>> = {}
) {
  const [values, setValues] = useState<T>(initialValues);
  const [errors, setErrors] = useState<Partial<Record<keyof T, string>>>({});
  const [touched, setTouched] = useState<Partial<Record<keyof T, boolean>>>({});

  const setValue = (field: keyof T, value: string) => {
    setValues((prev) => ({ ...prev, [field]: value }));
    if (errors[field]) {
      setErrors((prev) => ({ ...prev, [field]: undefined }));
    }
  };

  const setFieldTouched = (field: keyof T) => {
    setTouched((prev) => ({ ...prev, [field]: true }));
  };

  const validateFieldValue = (field: keyof T) => {
    const rule = rules[field];
    if (!rule) return null;
    const error = validateField(values[field], rule, values as Record<string, string>);
    setErrors((prev) => ({ ...prev, [field]: error || undefined }));
    return error;
  };

  const validateAll = () => {
    let ok = true;
    (Object.keys(initialValues) as (keyof T)[]).forEach((field) => {
      const err = validateFieldValue(field);
      setTouched((prev) => ({ ...prev, [field]: true }));
      if (err) ok = false;
    });
    return ok;
  };

  const reset = () => {
    setValues(initialValues);
    setErrors({});
    setTouched({});
  };

  return {
    values,
    errors,
    touched,
    setValue,
    setFieldTouched,
    validateField: validateFieldValue,
    validateAll,
    reset,
  };
}

