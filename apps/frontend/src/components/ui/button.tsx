import React from "react";

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "secondary" | "outline" | "destructive" | "default" | "ghost" | "link";
  size?: "sm" | "md" | "lg" | "icon";
  isLoading?: boolean;
}

/**
 * Tailwind button supporting primary and secondary variants.
 */
const Button: React.FC<ButtonProps> = ({
  variant = "primary",
  size = "md",
  isLoading = false,
  disabled,
  className = "",
  children,
  ...props
}) => {
  const variantClasses =
    variant === "primary"
      ? "bg-primary-600 text-white hover:bg-primary-700"
      : variant === "secondary"
        ? "bg-gray-200 text-gray-800 hover:bg-gray-300"
        : variant === "destructive"
          ? "bg-red-600 text-white hover:bg-red-700"
          : variant === "ghost"
            ? "bg-transparent text-gray-700 hover:bg-gray-100 dark:text-slate-200 dark:hover:bg-gray-800"
            : variant === "link"
              ? "bg-transparent text-primary-600 hover:underline dark:text-primary-400"
              : variant === "default"
                ? "bg-gray-900 text-white hover:bg-gray-800 dark:bg-gray-100 dark:text-gray-900 dark:hover:bg-white"
                : "border border-gray-300 text-gray-700 bg-transparent hover:bg-gray-100 dark:border-gray-600 dark:text-slate-200 dark:hover:bg-gray-800"; // outline

  const sizeClasses =
    size === "sm"
      ? "px-3 py-1.5 text-xs"
      : size === "lg"
        ? "px-5 py-3 text-base"
        : size === "icon"
          ? "h-9 w-9 p-0"
          : "px-4 py-2 text-sm"; // md

  return (
    <button
      className={`inline-flex items-center justify-center rounded-md font-medium focus:outline-none focus:ring-2 focus:ring-primary-500 disabled:opacity-50 disabled:cursor-not-allowed ${sizeClasses} ${variantClasses} ${className}`}
      disabled={disabled || isLoading}
      aria-busy={isLoading}
      {...props}
    >
      {isLoading && (
        <svg
          className="mr-2 h-4 w-4 animate-spin text-current"
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
        >
          <circle
            className="opacity-25"
            cx="12"
            cy="12"
            r="10"
            stroke="currentColor"
            strokeWidth="4"
          ></circle>
          <path
            className="opacity-75"
            fill="currentColor"
            d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"
          ></path>
        </svg>
      )}
      {children}
    </button>
  );
};

export { Button };
export default Button;
