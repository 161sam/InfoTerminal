import React from "react";

export interface FieldProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label: string;
  helper?: string;
  error?: string;
}

/**
 * Form field with label, input and helper/error text.
 */
const Field: React.FC<FieldProps> = ({
  label,
  helper,
  error,
  id,
  className = "",
  ...props
}) => {
  const inputId = id || props.name || Math.random().toString(36).slice(2);
  return (
    <div className={className}>
      <label htmlFor={inputId} className="mb-1 block text-sm font-medium">
        {label}
      </label>
      <input
        id={inputId}
        className="w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
        {...props}
      />
      {helper && !error && (
        <p className="mt-1 text-xs text-gray-500">{helper}</p>
      )}
      {error && <p className="mt-1 text-xs text-red-600">{error}</p>}
    </div>
  );
};

export default Field;
