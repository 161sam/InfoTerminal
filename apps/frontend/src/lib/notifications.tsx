// apps/frontend/src/lib/notifications.tsx
import React, { createContext, useContext, useState, useCallback } from 'react';
import { 
  CheckCircle, 
  AlertTriangle, 
  XCircle, 
  Info, 
  X, 
  Bell,
  Zap
} from 'lucide-react';

export type NotificationType = 'success' | 'error' | 'warning' | 'info';

export interface Notification {
  id: string;
  type: NotificationType;
  title: string;
  message?: string;
  duration?: number;
  persistent?: boolean;
  action?: {
    label: string;
    onClick: () => void;
  };
  timestamp: Date;
}

interface NotificationContextType {
  notifications: Notification[];
  addNotification: (notification: Omit<Notification, 'id' | 'timestamp'>) => void;
  removeNotification: (id: string) => void;
  clearAll: () => void;
  // Convenience methods
  success: (title: string, message?: string, options?: Partial<Notification>) => void;
  error: (title: string, message?: string, options?: Partial<Notification>) => void;
  warning: (title: string, message?: string, options?: Partial<Notification>) => void;
  info: (title: string, message?: string, options?: Partial<Notification>) => void;
}

const NotificationContext = createContext<NotificationContextType | undefined>(undefined);

export function NotificationProvider({ children }: { children: React.ReactNode }) {
  const [notifications, setNotifications] = useState<Notification[]>([]);

  const addNotification = useCallback((notificationData: Omit<Notification, 'id' | 'timestamp'>) => {
    const id = Math.random().toString(36).substr(2, 9);
    const notification: Notification = {
      ...notificationData,
      id,
      timestamp: new Date(),
      duration: notificationData.duration ?? 5000,
    };

    setNotifications(prev => [notification, ...prev]);

    // Auto-remove non-persistent notifications
    if (!notification.persistent && notification.duration > 0) {
      setTimeout(() => {
        removeNotification(id);
      }, notification.duration);
    }
  }, []);

  const removeNotification = useCallback((id: string) => {
    setNotifications(prev => prev.filter(notification => notification.id !== id));
  }, []);

  const clearAll = useCallback(() => {
    setNotifications([]);
  }, []);

  const success = useCallback((title: string, message?: string, options?: Partial<Notification>) => {
    addNotification({ ...options, type: 'success', title, message });
  }, [addNotification]);

  const error = useCallback((title: string, message?: string, options?: Partial<Notification>) => {
    addNotification({ ...options, type: 'error', title, message, persistent: options?.persistent ?? true });
  }, [addNotification]);

  const warning = useCallback((title: string, message?: string, options?: Partial<Notification>) => {
    addNotification({ ...options, type: 'warning', title, message });
  }, [addNotification]);

  const info = useCallback((title: string, message?: string, options?: Partial<Notification>) => {
    addNotification({ ...options, type: 'info', title, message });
  }, [addNotification]);

  return (
    <NotificationContext.Provider
      value={{
        notifications,
        addNotification,
        removeNotification,
        clearAll,
        success,
        error,
        warning,
        info,
      }}
    >
      {children}
      <NotificationContainer />
    </NotificationContext.Provider>
  );
}

export function useNotifications() {
  const context = useContext(NotificationContext);
  if (!context) {
    throw new Error('useNotifications must be used within a NotificationProvider');
  }
  return context;
}

// Notification Container Component
function NotificationContainer() {
  const { notifications } = useNotifications();

  return (
    <div className="fixed top-4 right-4 z-50 space-y-2 max-w-sm w-full">
      {notifications.map(notification => (
        <NotificationToast key={notification.id} notification={notification} />
      ))}
    </div>
  );
}

// Individual Toast Component
function NotificationToast({ notification }: { notification: Notification }) {
  const { removeNotification } = useNotifications();
  const [isVisible, setIsVisible] = useState(false);
  const [isLeaving, setIsLeaving] = useState(false);

  React.useEffect(() => {
    // Trigger animation
    requestAnimationFrame(() => {
      setIsVisible(true);
    });
  }, []);

  const handleClose = () => {
    setIsLeaving(true);
    setTimeout(() => {
      removeNotification(notification.id);
    }, 200);
  };

  const getIcon = () => {
    switch (notification.type) {
      case 'success':
        return <CheckCircle size={20} className="text-green-600" />;
      case 'error':
        return <XCircle size={20} className="text-red-600" />;
      case 'warning':
        return <AlertTriangle size={20} className="text-orange-600" />;
      case 'info':
        return <Info size={20} className="text-blue-600" />;
      default:
        return <Bell size={20} className="text-gray-600" />;
    }
  };

  const getStyles = () => {
    const baseStyles = "border-l-4 shadow-lg";
    switch (notification.type) {
      case 'success':
        return `${baseStyles} bg-green-50 border-green-400 dark:bg-green-900/20 dark:border-green-400`;
      case 'error':
        return `${baseStyles} bg-red-50 border-red-400 dark:bg-red-900/20 dark:border-red-400`;
      case 'warning':
        return `${baseStyles} bg-orange-50 border-orange-400 dark:bg-orange-900/20 dark:border-orange-400`;
      case 'info':
        return `${baseStyles} bg-blue-50 border-blue-400 dark:bg-blue-900/20 dark:border-blue-400`;
      default:
        return `${baseStyles} bg-gray-50 border-gray-400 dark:bg-gray-800 dark:border-gray-400`;
    }
  };

  return (
    <div
      className={`
        ${getStyles()}
        rounded-lg p-4 transition-all duration-200 transform
        ${isVisible && !isLeaving ? 'translate-x-0 opacity-100' : 'translate-x-full opacity-0'}
        ${isLeaving ? '-translate-x-full opacity-0' : ''}
      `}
    >
      <div className="flex items-start">
        <div className="flex-shrink-0 mr-3 pt-0.5">
          {getIcon()}
        </div>
        
        <div className="flex-1 min-w-0">
          <h4 className="text-sm font-medium text-gray-900 dark:text-gray-100">
            {notification.title}
          </h4>
          
          {notification.message && (
            <p className="mt-1 text-sm text-gray-700 dark:text-gray-300">
              {notification.message}
            </p>
          )}
          
          {notification.action && (
            <div className="mt-3">
              <button
                onClick={notification.action.onClick}
                className="text-sm font-medium text-primary-600 hover:text-primary-500 dark:text-primary-400 dark:hover:text-primary-300"
              >
                {notification.action.label}
              </button>
            </div>
          )}
          
          <div className="mt-2 text-xs text-gray-500 dark:text-gray-400">
            {notification.timestamp.toLocaleTimeString()}
          </div>
        </div>
        
        <div className="flex-shrink-0 ml-4">
          <button
            onClick={handleClose}
            className="inline-flex text-gray-400 hover:text-gray-600 dark:text-gray-500 dark:hover:text-gray-300 transition-colors"
          >
            <X size={18} />
          </button>
        </div>
      </div>
      
      {/* Progress bar for timed notifications */}
      {!notification.persistent && notification.duration && notification.duration > 0 && (
        <div className="absolute bottom-0 left-0 right-0 h-1 bg-gray-200 dark:bg-gray-700 rounded-b-lg overflow-hidden">
          <div
            className="h-full bg-primary-500 transition-all ease-linear"
            style={{
              animation: `shrink ${notification.duration}ms linear forwards`
            }}
          />
        </div>
      )}
      
      <style jsx>{`
        @keyframes shrink {
          from { width: 100%; }
          to { width: 0%; }
        }
      `}</style>
    </div>
  );
}

// Notification Center Component (for viewing all notifications)
export function NotificationCenter({ isOpen, onClose }: { isOpen: boolean; onClose: () => void }) {
  const { notifications, clearAll, removeNotification } = useNotifications();

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 overflow-hidden">
      <div className="absolute inset-0 bg-black bg-opacity-50" onClick={onClose} />
      
      <div className="absolute top-0 right-0 h-full w-96 bg-white dark:bg-gray-800 shadow-xl transform transition-transform">
        <div className="p-6 border-b border-gray-200 dark:border-gray-700">
          <div className="flex items-center justify-between">
            <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-100">
              Notifications
            </h2>
            <div className="flex items-center gap-2">
              {notifications.length > 0 && (
                <button
                  onClick={clearAll}
                  className="text-sm text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200"
                >
                  Clear All
                </button>
              )}
              <button
                onClick={onClose}
                className="p-1 text-gray-400 hover:text-gray-600 dark:text-gray-500 dark:hover:text-gray-300"
              >
                <X size={20} />
              </button>
            </div>
          </div>
        </div>
        
        <div className="flex-1 overflow-y-auto p-4 space-y-3">
          {notifications.length === 0 ? (
            <div className="text-center py-12">
              <Bell size={48} className="mx-auto text-gray-400 mb-4" />
              <p className="text-gray-500 dark:text-gray-400">No notifications</p>
            </div>
          ) : (
            notifications.map(notification => (
              <div
                key={notification.id}
                className="p-4 border border-gray-200 dark:border-gray-700 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors"
              >
                <div className="flex items-start justify-between">
                  <div className="flex items-start gap-3 flex-1">
                    <div className="flex-shrink-0 mt-0.5">
                      {notification.type === 'success' && <CheckCircle size={16} className="text-green-600" />}
                      {notification.type === 'error' && <XCircle size={16} className="text-red-600" />}
                      {notification.type === 'warning' && <AlertTriangle size={16} className="text-orange-600" />}
                      {notification.type === 'info' && <Info size={16} className="text-blue-600" />}
                    </div>
                    <div className="min-w-0 flex-1">
                      <p className="text-sm font-medium text-gray-900 dark:text-gray-100">
                        {notification.title}
                      </p>
                      {notification.message && (
                        <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                          {notification.message}
                        </p>
                      )}
                      <p className="text-xs text-gray-500 dark:text-gray-500 mt-1">
                        {notification.timestamp.toLocaleString()}
                      </p>
                    </div>
                  </div>
                  <button
                    onClick={() => removeNotification(notification.id)}
                    className="flex-shrink-0 p-1 text-gray-400 hover:text-gray-600 dark:text-gray-500 dark:hover:text-gray-300"
                  >
                    <X size={14} />
                  </button>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}

// Hook for common notification patterns
export function useNotificationPatterns() {
  const notifications = useNotifications();
  
  return {
    // API request patterns
    apiSuccess: (action: string) => {
      notifications.success('Success', `${action} completed successfully`);
    },
    
    apiError: (action: string, error?: string) => {
      notifications.error('Error', error || `Failed to ${action}`, {
        action: {
          label: 'Retry',
          onClick: () => {
            // Custom retry logic can be passed here
            notifications.info('Retrying...', 'Please wait');
          }
        }
      });
    },
    
    // File operation patterns
    fileUploaded: (filename: string) => {
      notifications.success('File Uploaded', `${filename} was uploaded successfully`);
    },
    
    fileUploadError: (filename: string, error: string) => {
      notifications.error('Upload Failed', `Failed to upload ${filename}: ${error}`);
    },
    
    // System patterns
    systemMaintenance: () => {
      notifications.warning('System Maintenance', 'The system will be under maintenance in 10 minutes', {
        persistent: true,
        action: {
          label: 'Learn More',
          onClick: () => window.open('/maintenance', '_blank')
        }
      });
    },
    
    connectionLost: () => {
      notifications.error('Connection Lost', 'Check your internet connection', {
        persistent: true
      });
    },
    
    connectionRestored: () => {
      notifications.success('Connection Restored', 'You are back online');
    }
  };
}