// apps/frontend/src/components/forms/FormComponents.tsx
import React, { useState, useRef, useEffect } from 'react';
import { 
  Eye, 
  EyeOff, 
  Check, 
  X, 
  AlertCircle, 
  Upload, 
  Search,
  Calendar,
  Clock,
  MapPin,
  Mail,
  Phone,
  Link as LinkIcon,
  Hash,
  DollarSign
} from 'lucide-react';

// Form validation utilities
export interface ValidationRule {
  required?: boolean;
  minLength?: number;
  maxLength?: number;
  pattern?: RegExp;
  email?: boolean;
  url?: boolean;
  phone?: boolean;
  custom?: (value: any) => string | null;
}

export interface FormFieldProps {
  label: string;
  name: string;
  value: any;
  onChange: (value: any) => void;
  onBlur?: () => void;
  error?: string;
  disabled?: boolean;
  required?: boolean;
  placeholder?: string;
  helperText?: string;
  className?: string;
}

export function validateField(value: any, rules: ValidationRule): string | null {
  if (rules.required && (!value || value.toString().trim() === '')) {
    return 'This field is required';
  }

  if (value && typeof value === 'string') {
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
  }

  if (rules.custom) {
    return rules.custom(value);
  }

  return null;
}

// Base Input Component
interface InputProps extends FormFieldProps {
  type?: 'text' | 'email' | 'password' | 'number' | 'tel' | 'url' | 'search';
  icon?: React.ComponentType<{ size?: number; className?: string }>;
  rightElement?: React.ReactNode;
}

export function Input({
  label,
  name,
  type = 'text',
  value,
  onChange,
  onBlur,
  error,
  disabled,
  required,
  placeholder,
  helperText,
  icon: Icon,
  rightElement,
  className = ''
}: InputProps) {
  const [isFocused, setIsFocused] = useState(false);
  const [showPassword, setShowPassword] = useState(false);

  const inputType = type === 'password' && showPassword ? 'text' : type;

  return (
    <div className={`space-y-1 ${className}`}>
      <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
        {label}
        {required && <span className="text-red-500 ml-1">*</span>}
      </label>
      
      <div className="relative">
        {Icon && (
          <div className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400">
            <Icon size={16} />
          </div>
        )}
        
        <input
          type={inputType}
          name={name}
          value={value}
          onChange={(e) => onChange(e.target.value)}
          onBlur={() => {
            setIsFocused(false);
            onBlur?.();
          }}
          onFocus={() => setIsFocused(true)}
          disabled={disabled}
          placeholder={placeholder}
          className={`
            w-full px-3 py-2 border rounded-lg transition-colors
            ${Icon ? 'pl-10' : ''}
            ${type === 'password' || rightElement ? 'pr-10' : ''}
            ${error 
              ? 'border-red-300 focus:border-red-500 focus:ring-red-500' 
              : isFocused 
                ? 'border-primary-500 ring-2 ring-primary-500 ring-opacity-20' 
                : 'border-gray-300 dark:border-gray-600'
            }
            ${disabled 
              ? 'bg-gray-50 dark:bg-gray-800 text-gray-500 cursor-not-allowed' 
              : 'bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100'
            }
            focus:outline-none focus:ring-2 focus:ring-opacity-20
          `}
        />
        
        {type === 'password' && (
          <button
            type="button"
            onClick={() => setShowPassword(!showPassword)}
            className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600"
          >
            {showPassword ? <EyeOff size={16} /> : <Eye size={16} />}
          </button>
        )}
        
        {rightElement && (
          <div className="absolute right-3 top-1/2 transform -translate-y-1/2">
            {rightElement}
          </div>
        )}
      </div>
      
      {error && (
        <div className="flex items-center gap-1 text-sm text-red-600 dark:text-red-400">
          <AlertCircle size={14} />
          <span>{error}</span>
        </div>
      )}
      
      {helperText && !error && (
        <p className="text-sm text-gray-500 dark:text-gray-400">{helperText}</p>
      )}
    </div>
  );
}

// Textarea Component
interface TextareaProps extends FormFieldProps {
  rows?: number;
  resize?: boolean;
}

export function Textarea({
  label,
  name,
  value,
  onChange,
  onBlur,
  error,
  disabled,
  required,
  placeholder,
  helperText,
  rows = 4,
  resize = true,
  className = ''
}: TextareaProps) {
  const [isFocused, setIsFocused] = useState(false);

  return (
    <div className={`space-y-1 ${className}`}>
      <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
        {label}
        {required && <span className="text-red-500 ml-1">*</span>}
      </label>
      
      <textarea
        name={name}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        onBlur={() => {
          setIsFocused(false);
          onBlur?.();
        }}
        onFocus={() => setIsFocused(true)}
        disabled={disabled}
        placeholder={placeholder}
        rows={rows}
        className={`
          w-full px-3 py-2 border rounded-lg transition-colors
          ${!resize ? 'resize-none' : 'resize-y'}
          ${error 
            ? 'border-red-300 focus:border-red-500 focus:ring-red-500' 
            : isFocused 
              ? 'border-primary-500 ring-2 ring-primary-500 ring-opacity-20' 
              : 'border-gray-300 dark:border-gray-600'
          }
          ${disabled 
            ? 'bg-gray-50 dark:bg-gray-800 text-gray-500 cursor-not-allowed' 
            : 'bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100'
          }
          focus:outline-none focus:ring-2 focus:ring-opacity-20
        `}
      />
      
      {error && (
        <div className="flex items-center gap-1 text-sm text-red-600 dark:text-red-400">
          <AlertCircle size={14} />
          <span>{error}</span>
        </div>
      )}
      
      {helperText && !error && (
        <p className="text-sm text-gray-500 dark:text-gray-400">{helperText}</p>
      )}
    </div>
  );
}

// Select Component
interface SelectProps extends FormFieldProps {
  options: { value: any; label: string; disabled?: boolean }[];
  multiple?: boolean;
}

export function Select({
  label,
  name,
  value,
  onChange,
  onBlur,
  error,
  disabled,
  required,
  placeholder = 'Select an option...',
  helperText,
  options,
  multiple = false,
  className = ''
}: SelectProps) {
  const [isOpen, setIsOpen] = useState(false);
  const selectRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (selectRef.current && !selectRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    }

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleSelect = (optionValue: any) => {
    if (multiple) {
      const currentValues = Array.isArray(value) ? value : [];
      const newValues = currentValues.includes(optionValue)
        ? currentValues.filter(v => v !== optionValue)
        : [...currentValues, optionValue];
      onChange(newValues);
    } else {
      onChange(optionValue);
      setIsOpen(false);
    }
  };

  const displayValue = () => {
    if (multiple && Array.isArray(value)) {
      if (value.length === 0) return placeholder;
      return `${value.length} selected`;
    }
    const option = options.find(opt => opt.value === value);
    return option ? option.label : placeholder;
  };

  return (
    <div className={`space-y-1 ${className}`}>
      <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
        {label}
        {required && <span className="text-red-500 ml-1">*</span>}
      </label>
      
      <div ref={selectRef} className="relative">
        <button
          type="button"
          onClick={() => !disabled && setIsOpen(!isOpen)}
          onBlur={onBlur}
          disabled={disabled}
          className={`
            w-full px-3 py-2 border rounded-lg text-left transition-colors flex items-center justify-between
            ${error 
              ? 'border-red-300 focus:border-red-500 focus:ring-red-500' 
              : isOpen 
                ? 'border-primary-500 ring-2 ring-primary-500 ring-opacity-20' 
                : 'border-gray-300 dark:border-gray-600'
            }
            ${disabled 
              ? 'bg-gray-50 dark:bg-gray-800 text-gray-500 cursor-not-allowed' 
              : 'bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 hover:border-gray-400'
            }
            focus:outline-none focus:ring-2 focus:ring-opacity-20
          `}
        >
          <span className={!value ? 'text-gray-500' : ''}>{displayValue()}</span>
          <svg 
            className={`w-4 h-4 transition-transform ${isOpen ? 'rotate-180' : ''}`}
            fill="none" 
            stroke="currentColor" 
            viewBox="0 0 24 24"
          >
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
          </svg>
        </button>
        
        {isOpen && (
          <div className="absolute z-10 w-full mt-1 bg-white dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-lg shadow-lg max-h-60 overflow-auto">
            {options.map((option) => {
              const isSelected = multiple 
                ? Array.isArray(value) && value.includes(option.value)
                : value === option.value;
              
              return (
                <button
                  key={option.value}
                  type="button"
                  onClick={() => !option.disabled && handleSelect(option.value)}
                  disabled={option.disabled}
                  className={`
                    w-full px-3 py-2 text-left hover:bg-gray-50 dark:hover:bg-gray-600 transition-colors flex items-center justify-between
                    ${isSelected ? 'bg-primary-50 dark:bg-primary-900/20 text-primary-700 dark:text-primary-400' : ''}
                    ${option.disabled ? 'text-gray-400 cursor-not-allowed' : 'text-gray-900 dark:text-gray-100'}
                  `}
                >
                  <span>{option.label}</span>
                  {isSelected && <Check size={16} />}
                </button>
              );
            })}
          </div>
        )}
      </div>
      
      {error && (
        <div className="flex items-center gap-1 text-sm text-red-600 dark:text-red-400">
          <AlertCircle size={14} />
          <span>{error}</span>
        </div>
      )}
      
      {helperText && !error && (
        <p className="text-sm text-gray-500 dark:text-gray-400">{helperText}</p>
      )}
    </div>
  );
}

// Checkbox Component
interface CheckboxProps {
  label: string;
  checked: boolean;
  onChange: (checked: boolean) => void;
  disabled?: boolean;
  error?: string;
  helperText?: string;
  className?: string;
}

export function Checkbox({
  label,
  checked,
  onChange,
  disabled,
  error,
  helperText,
  className = ''
}: CheckboxProps) {
  return (
    <div className={`space-y-1 ${className}`}>
      <label className={`flex items-center gap-3 cursor-pointer ${disabled ? 'cursor-not-allowed opacity-60' : ''}`}>
        <div className="relative">
          <input
            type="checkbox"
            checked={checked}
            onChange={(e) => onChange(e.target.checked)}
            disabled={disabled}
            className="sr-only"
          />
          <div className={`
            w-5 h-5 border-2 rounded transition-colors flex items-center justify-center
            ${checked 
              ? error 
                ? 'bg-red-500 border-red-500' 
                : 'bg-primary-600 border-primary-600'
              : error
                ? 'border-red-300'
                : 'border-gray-300 dark:border-gray-600'
            }
            ${disabled ? 'opacity-60' : 'hover:border-primary-400'}
          `}>
            {checked && <Check size={14} className="text-white" />}
          </div>
        </div>
        <span className="text-sm font-medium text-gray-700 dark:text-gray-300">{label}</span>
      </label>
      
      {error && (
        <div className="flex items-center gap-1 text-sm text-red-600 dark:text-red-400 ml-8">
          <AlertCircle size={14} />
          <span>{error}</span>
        </div>
      )}
      
      {helperText && !error && (
        <p className="text-sm text-gray-500 dark:text-gray-400 ml-8">{helperText}</p>
      )}
    </div>
  );
}

// Radio Group Component
interface RadioOption {
  value: any;
  label: string;
  disabled?: boolean;
  helperText?: string;
}

interface RadioGroupProps extends FormFieldProps {
  options: RadioOption[];
  direction?: 'horizontal' | 'vertical';
}

export function RadioGroup({
  label,
  name,
  value,
  onChange,
  onBlur,
  error,
  disabled,
  required,
  helperText,
  options,
  direction = 'vertical',
  className = ''
}: RadioGroupProps) {
  return (
    <div className={`space-y-2 ${className}`}>
      <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
        {label}
        {required && <span className="text-red-500 ml-1">*</span>}
      </label>
      
      <div className={`${direction === 'horizontal' ? 'flex flex-wrap gap-4' : 'space-y-2'}`}>
        {options.map((option) => (
          <label
            key={option.value}
            className={`flex items-center gap-3 cursor-pointer ${
              disabled || option.disabled ? 'cursor-not-allowed opacity-60' : ''
            }`}
          >
            <div className="relative">
              <input
                type="radio"
                name={name}
                value={option.value}
                checked={value === option.value}
                onChange={() => onChange(option.value)}
                onBlur={onBlur}
                disabled={disabled || option.disabled}
                className="sr-only"
              />
              <div className={`
                w-5 h-5 border-2 rounded-full transition-colors flex items-center justify-center
                ${value === option.value
                  ? error 
                    ? 'bg-red-500 border-red-500' 
                    : 'border-primary-600'
                  : error
                    ? 'border-red-300'
                    : 'border-gray-300 dark:border-gray-600'
                }
                ${disabled || option.disabled ? 'opacity-60' : 'hover:border-primary-400'}
              `}>
                {value === option.value && (
                  <div className={`w-2 h-2 rounded-full ${error ? 'bg-white' : 'bg-primary-600'}`} />
                )}
              </div>
            </div>
            <div>
              <span className="text-sm font-medium text-gray-700 dark:text-gray-300">{option.label}</span>
              {option.helperText && (
                <p className="text-xs text-gray-500 dark:text-gray-400">{option.helperText}</p>
              )}
            </div>
          </label>
        ))}
      </div>
      
      {error && (
        <div className="flex items-center gap-1 text-sm text-red-600 dark:text-red-400">
          <AlertCircle size={14} />
          <span>{error}</span>
        </div>
      )}
      
      {helperText && !error && (
        <p className="text-sm text-gray-500 dark:text-gray-400">{helperText}</p>
      )}
    </div>
  );
}

// Form Hook for validation and state management
export function useForm<T extends Record<string, any>>(
  initialValues: T,
  validationRules: Record<keyof T, ValidationRule> = {}
) {
  const [values, setValues] = useState<T>(initialValues);
  const [errors, setErrors] = useState<Partial<Record<keyof T, string>>>({});
  const [touched, setTouched] = useState<Partial<Record<keyof T, boolean>>>({});

  const setValue = (field: keyof T, value: any) => {
    setValues(prev => ({ ...prev, [field]: value }));
    
    // Clear error when user starts typing
    if (errors[field]) {
      setErrors(prev => ({ ...prev, [field]: undefined }));
    }
  };

  const setFieldTouched = (field: keyof T) => {
    setTouched(prev => ({ ...prev, [field]: true }));
  };

  const validateField = (field: keyof T) => {
    const value = values[field];
    const rules = validationRules[field];
    
    if (!rules) return null;
    
    const error = validateField(value, rules);
    setErrors(prev => ({ ...prev, [field]: error || undefined }));
    return error;
  };

  const validateAll = () => {
    const newErrors: Partial<Record<keyof T, string>> = {};
    let hasErrors = false;

    Object.keys(validationRules).forEach(field => {
      const error = validateField(values[field as keyof T], validationRules[field as keyof T]);
      if (error) {
        newErrors[field as keyof T] = error;
        hasErrors = true;
      }
    });

    setErrors(newErrors);
    setTouched(
      Object.keys(initialValues).reduce((acc, key) => {
        acc[key as keyof T] = true;
        return acc;
      }, {} as Partial<Record<keyof T, boolean>>)
    );

    return !hasErrors;
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
    validateField: validateField,
    validateAll,
    reset,
    isValid: Object.keys(errors).length === 0,
    isDirty: JSON.stringify(values) !== JSON.stringify(initialValues)
  };
}

// Form wrapper component
interface FormProps {
  children: React.ReactNode;
  onSubmit: (e: React.FormEvent) => void;
  className?: string;
}

export function Form({ children, onSubmit, className = '' }: FormProps) {
  return (
    <form onSubmit={onSubmit} noValidate className={`space-y-6 ${className}`}>
      {children}
    </form>
  );
}

// Common Input Components with Icons
export const EmailInput = (props: Omit<InputProps, 'type' | 'icon'>) => (
  <Input {...props} type="email" icon={Mail} />
);

export const PasswordInput = (props: Omit<InputProps, 'type'>) => (
  <Input {...props} type="password" />
);

export const PhoneInput = (props: Omit<InputProps, 'type' | 'icon'>) => (
  <Input {...props} type="tel" icon={Phone} />
);

export const UrlInput = (props: Omit<InputProps, 'type' | 'icon'>) => (
  <Input {...props} type="url" icon={LinkIcon} />
);

export const SearchInput = (props: Omit<InputProps, 'type' | 'icon'>) => (
  <Input {...props} type="search" icon={Search} />
);

export const NumberInput = (props: Omit<InputProps, 'type' | 'icon'>) => (
  <Input {...props} type="number" icon={Hash} />
);

export const CurrencyInput = (props: Omit<InputProps, 'type' | 'icon'>) => (
  <Input {...props} type="number" icon={DollarSign} />
);