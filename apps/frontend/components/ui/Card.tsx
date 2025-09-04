import React from "react";

export interface CardProps {
  className?: string;
  children: React.ReactNode;
}

/**
 * Simple container card with rounded corners and shadow.
 */
const Card: React.FC<CardProps> = ({ className = "", children }) => {
  return (
    <div className={`rounded-2xl shadow p-4 bg-white dark:bg-zinc-900 ${className}`}>
      {children}
    </div>
  );
};

export default Card;
