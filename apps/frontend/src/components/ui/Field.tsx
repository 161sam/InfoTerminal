import React, { forwardRef, useId } from "react";

export interface FieldProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label: string;
  helper?: string;
  error?: string;
  children?: React.ReactNode;
}

/**
 * Form field with label, input and helper/error text.
 */
const Field = forwardRef<HTMLDivElement, FieldProps>(function Field(
  { label, helper, error, id: idProp, name, className = "", children, ...props },
  ref
) {
  const rid = useId();
  const inputId = idProp || name || `f-${rid}`;
  const describedBy = error
    ? `${inputId}-error`
    : helper
    ? `${inputId}-hint`
    : undefined;

  return (
    <div ref={ref} className={className}>
      <label htmlFor={inputId} className="mb-1 block text-sm font-medium text-gray-700 dark:text-slate-300">
        {label}
      </label>
      {children
        ? React.Children.map(children, (child) =>
            React.isValidElement(child)
              ? React.cloneElement(child as any, {
                  id: (child as any).props?.id ?? inputId,
                  name: (child as any).props?.name ?? name,
                  'aria-describedby': (child as any).props?.['aria-describedby'] ?? describedBy,
                })
              : child
          )
        : (
          <input
            id={inputId}
            name={name}
            aria-describedby={describedBy}
            className="w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
            {...props}
          />
        )}
      {helper && !error && (
        <p id={`${inputId}-hint`} className="mt-1 text-xs text-gray-500 dark:text-slate-400">
          {helper}
        </p>
      )}
      {error && (
        <p id={`${inputId}-error`} className="mt-1 text-xs text-red-600">
          {error}
        </p>
      )}
    </div>
  );
});

export default Field;
