import React from "react";

export type InputProps = React.InputHTMLAttributes<HTMLInputElement>;

/**
 * Simple styled input used across the app.
 */
const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ className = "", ...props }, ref) => {
    const base =
      "block w-full rounded-md border border-gray-300 bg-white px-3 py-2 text-sm text-gray-900 placeholder-gray-400 shadow-sm focus:border-primary-500 focus:outline-none focus:ring-2 focus:ring-primary-500 disabled:cursor-not-allowed disabled:opacity-50 dark:border-gray-700 dark:bg-gray-900 dark:text-slate-100";
    return <input ref={ref} className={`${base} ${className}`} {...props} />;
  },
);
Input.displayName = "Input";

export { Input };
export default Input;
