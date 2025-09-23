import React from 'react';
import { Loader2, RefreshCw, Zap } from 'lucide-react';
import { cva, type VariantProps } from 'class-variance-authority';
import { cn } from '@/lib/utils';

const loadingVariants = cva(
  "flex items-center justify-center",
  {
    variants: {
      variant: {
        default: "text-gray-500 dark:text-gray-400",
        primary: "text-primary-600 dark:text-primary-400", 
        secondary: "text-gray-400 dark:text-gray-500",
        success: "text-green-600 dark:text-green-400",
        warning: "text-yellow-600 dark:text-yellow-400",
        danger: "text-red-600 dark:text-red-400",
      },
      size: {
        xs: "w-3 h-3",
        sm: "w-4 h-4", 
        md: "w-6 h-6",
        lg: "w-8 h-8",
        xl: "w-12 h-12",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "md",
    },
  }
);

const containerVariants = cva(
  "",
  {
    variants: {
      layout: {
        inline: "inline-flex items-center gap-2",
        block: "flex flex-col items-center gap-3 py-8",
        overlay: "absolute inset-0 flex items-center justify-center bg-white/80 dark:bg-gray-900/80 backdrop-blur-sm",
        card: "flex flex-col items-center gap-4 p-6 bg-gray-50 dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700",
      },
    },
    defaultVariants: {
      layout: "inline",
    },
  }
);

export interface LoadingSpinnerProps extends React.HTMLAttributes<HTMLDivElement>,
  VariantProps<typeof loadingVariants> {
  layout?: 'inline' | 'block' | 'overlay' | 'card';
  icon?: 'loader' | 'refresh' | 'zap';
  text?: string;
  subText?: string;
  duration?: number;
}

/**
 * Unified loading spinner component for consistent loading states
 * across the InfoTerminal application.
 */
export function LoadingSpinner({
  variant = 'default',
  size = 'md',
  layout = 'inline',
  icon = 'loader',
  text,
  subText,
  className,
  ...props
}: LoadingSpinnerProps) {
  const IconComponent = {
    loader: Loader2,
    refresh: RefreshCw,
    zap: Zap,
  }[icon];

  const iconSizes = {
    xs: 12,
    sm: 16,
    md: 24,
    lg: 32,
    xl: 48,
  };

  return (
    <div className={cn(containerVariants({ layout }), className)} {...props}>
      <div className={cn(loadingVariants({ variant, size }))}>
        <IconComponent 
          size={iconSizes[size]} 
          className="animate-spin" 
        />
      </div>
      
      {text && (
        <div className={cn(
          "text-center",
          layout === 'inline' && "text-sm",
          layout === 'block' && "text-base",
          layout === 'card' && "text-lg font-medium text-gray-900 dark:text-gray-100"
        )}>
          {text}
          {subText && (
            <div className={cn(
              "text-gray-500 dark:text-gray-400 font-normal",
              layout === 'inline' && "text-xs",
              layout === 'block' && "text-sm",
              layout === 'card' && "text-base mt-1"
            )}>
              {subText}
            </div>
          )}
        </div>
      )}
    </div>
  );
}

// Skeleton loading components for content placeholders
export interface SkeletonProps extends React.HTMLAttributes<HTMLDivElement> {
  lines?: number;
  width?: string | number;
  height?: string | number;
  rounded?: boolean;
  className?: string;
}

export function Skeleton({ 
  lines = 1, 
  width, 
  height, 
  rounded = true, 
  className,
  ...props 
}: SkeletonProps) {
  const skeletonClass = cn(
    "animate-pulse bg-gray-200 dark:bg-gray-700",
    rounded ? "rounded" : "",
    className
  );

  if (lines === 1) {
    return (
      <div 
        className={skeletonClass}
        style={{ 
          width: typeof width === 'number' ? `${width}px` : width,
          height: typeof height === 'number' ? `${height}px` : height || '1rem'
        }}
        {...props}
      />
    );
  }

  return (
    <div className="space-y-2" {...props}>
      {Array.from({ length: lines }).map((_, i) => (
        <div
          key={i}
          className={skeletonClass}
          style={{
            width: i === lines - 1 ? '75%' : '100%',
            height: typeof height === 'number' ? `${height}px` : height || '1rem'
          }}
        />
      ))}
    </div>
  );
}

// Tab loading skeleton
export function TabLoadingSkeleton() {
  return (
    <div className="space-y-6">
      {/* Tab navigation skeleton */}
      <div className="flex items-center gap-2 bg-gray-100 dark:bg-gray-800 p-1 rounded-lg w-fit">
        <Skeleton width={80} height={32} />
        <Skeleton width={100} height={32} />
        <Skeleton width={90} height={32} />
      </div>
      
      {/* Content skeleton */}
      <div className="space-y-4">
        <Skeleton lines={3} />
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="space-y-2">
            <Skeleton height={200} />
            <Skeleton lines={2} />
          </div>
          <div className="space-y-2">
            <Skeleton height={200} />
            <Skeleton lines={2} />
          </div>
        </div>
      </div>
    </div>
  );
}

// Graph loading skeleton
export function GraphLoadingSkeleton() {
  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <Skeleton width={200} height={24} />
        <div className="flex gap-2">
          <Skeleton width={80} height={32} />
          <Skeleton width={80} height={32} />
        </div>
      </div>
      
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <Skeleton height={400} />
        </div>
        <div className="space-y-4">
          <Skeleton height={100} />
          <Skeleton height={120} />
          <Skeleton height={80} />
        </div>
      </div>
    </div>
  );
}

// Table loading skeleton
export function TableLoadingSkeleton({ rows = 5, columns = 4 }: { rows?: number; columns?: number }) {
  return (
    <div className="space-y-3">
      {/* Header */}
      <div className="grid gap-4" style={{ gridTemplateColumns: `repeat(${columns}, 1fr)` }}>
        {Array.from({ length: columns }).map((_, i) => (
          <Skeleton key={i} width="80%" height={20} />
        ))}
      </div>
      
      {/* Rows */}
      {Array.from({ length: rows }).map((_, rowIndex) => (
        <div key={rowIndex} className="grid gap-4" style={{ gridTemplateColumns: `repeat(${columns}, 1fr)` }}>
          {Array.from({ length: columns }).map((_, colIndex) => (
            <Skeleton key={colIndex} width="60%" height={16} />
          ))}
        </div>
      ))}
    </div>
  );
}

// Error state component
export interface ErrorStateProps {
  title?: string;
  message?: string;
  action?: {
    label: string;
    onClick: () => void;
  };
  icon?: React.ElementType;
  variant?: 'error' | 'warning' | 'info';
}

export function ErrorState({ 
  title = "Something went wrong",
  message = "An error occurred while loading this content.",
  action,
  icon: Icon,
  variant = 'error'
}: ErrorStateProps) {
  const variants = {
    error: {
      container: "text-red-600 dark:text-red-400",
      bg: "bg-red-50 dark:bg-red-900/20",
      border: "border-red-200 dark:border-red-900/30"
    },
    warning: {
      container: "text-yellow-600 dark:text-yellow-400", 
      bg: "bg-yellow-50 dark:bg-yellow-900/20",
      border: "border-yellow-200 dark:border-yellow-900/30"
    },
    info: {
      container: "text-blue-600 dark:text-blue-400",
      bg: "bg-blue-50 dark:bg-blue-900/20", 
      border: "border-blue-200 dark:border-blue-900/30"
    }
  };

  const style = variants[variant];

  return (
    <div className={cn(
      "flex flex-col items-center justify-center p-8 rounded-lg border",
      style.bg,
      style.border
    )}>
      {Icon && (
        <div className={cn("mb-4", style.container)}>
          <Icon size={48} />
        </div>
      )}
      
      <h3 className={cn("text-lg font-semibold mb-2", style.container)}>
        {title}
      </h3>
      
      <p className="text-gray-600 dark:text-gray-400 text-center mb-4 max-w-md">
        {message}
      </p>
      
      {action && (
        <button
          onClick={action.onClick}
          className={cn(
            "px-4 py-2 rounded-lg font-medium transition-colors",
            variant === 'error' && "bg-red-600 hover:bg-red-700 text-white",
            variant === 'warning' && "bg-yellow-600 hover:bg-yellow-700 text-white", 
            variant === 'info' && "bg-blue-600 hover:bg-blue-700 text-white"
          )}
        >
          {action.label}
        </button>
      )}
    </div>
  );
}

// Empty state component
export interface EmptyStateProps {
  title?: string;
  message?: string;
  action?: {
    label: string;
    onClick: () => void;
  };
  icon?: React.ElementType;
  illustration?: string;
}

export function EmptyState({ 
  title = "No data available",
  message = "Get started by adding some content.",
  action,
  icon: Icon,
  illustration
}: EmptyStateProps) {
  return (
    <div className="flex flex-col items-center justify-center p-12 text-center">
      {illustration ? (
        <img src={illustration} alt="" className="w-32 h-32 mb-6 opacity-50" />
      ) : Icon ? (
        <div className="mb-6 text-gray-400 dark:text-gray-500">
          <Icon size={64} />
        </div>
      ) : null}
      
      <h3 className="text-xl font-semibold text-gray-900 dark:text-gray-100 mb-2">
        {title}
      </h3>
      
      <p className="text-gray-600 dark:text-gray-400 mb-6 max-w-md">
        {message}
      </p>
      
      {action && (
        <button
          onClick={action.onClick}
          className="px-6 py-3 bg-primary-600 hover:bg-primary-700 text-white rounded-lg font-medium transition-colors"
        >
          {action.label}
        </button>
      )}
    </div>
  );
}

export default LoadingSpinner;
