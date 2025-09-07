// apps/frontend/src/components/auth/AuthProvider.tsx
import React, { createContext, useContext, useEffect, useState, useCallback, useRef } from 'react';
import { useRouter } from 'next/router';
import { useNotifications } from '@/lib/notifications';

export interface User {
  id: string;
  email: string;
  name: string;
  avatar?: string;
  roles: string[];
  permissions: string[];
  preferences?: Record<string, any>;
}

export interface AuthContextType {
  user: User | null;
  loading: boolean;
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string, name: string) => Promise<void>;
  logout: () => Promise<void>;
  refreshToken: () => Promise<void>;
  hasRole: (role: string) => boolean;
  hasPermission: (permission: string) => boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const router = useRouter();
  const notifications = useNotifications();

  // Check if user is authenticated on mount
  useEffect(() => {
    checkAuth();
  }, []);

  const checkAuth = async () => {
    try {
      const token = localStorage.getItem('auth_token');
      if (!token) {
        setLoading(false);
        return;
      }

      const response = await fetch('/api/auth/me', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.ok) {
        const userData = await response.json();
        setUser(userData);
      } else {
        localStorage.removeItem('auth_token');
        localStorage.removeItem('refresh_token');
      }
    } catch (error) {
      console.error('Auth check failed:', error);
    } finally {
      setLoading(false);
    }
  };

  const login = async (email: string, password: string) => {
    try {
      const response = await fetch('/api/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.message || 'Login failed');
      }

      const { user: userData, token, refreshToken } = await response.json();
      
      localStorage.setItem('auth_token', token);
      localStorage.setItem('refresh_token', refreshToken);
      setUser(userData);
      
      notifications.success('Welcome back!', `Logged in as ${userData.name}`);
      
      // Redirect to intended page or dashboard
      const returnTo = router.query.returnTo as string || '/';
      router.push(returnTo);
    } catch (error: any) {
      notifications.error('Login Failed', error.message);
      throw error;
    }
  };

  const register = async (email: string, password: string, name: string) => {
    try {
      const response = await fetch('/api/auth/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password, name }),
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.message || 'Registration failed');
      }

      const { user: userData, token, refreshToken } = await response.json();
      
      localStorage.setItem('auth_token', token);
      localStorage.setItem('refresh_token', refreshToken);
      setUser(userData);
      
      notifications.success('Welcome!', 'Your account has been created successfully');
      router.push('/');
    } catch (error: any) {
      notifications.error('Registration Failed', error.message);
      throw error;
    }
  };

  const logout = async () => {
    try {
      const token = localStorage.getItem('auth_token');
      if (token) {
        await fetch('/api/auth/logout', {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
      }
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      localStorage.removeItem('auth_token');
      localStorage.removeItem('refresh_token');
      setUser(null);
      router.push('/login');
      notifications.info('Logged out', 'You have been signed out');
    }
  };

  const refreshToken = async () => {
    try {
      const token = localStorage.getItem('refresh_token');
      if (!token) throw new Error('No refresh token');

      const response = await fetch('/api/auth/refresh', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (!response.ok) throw new Error('Token refresh failed');

      const { token: newToken, refreshToken: newRefreshToken } = await response.json();
      
      localStorage.setItem('auth_token', newToken);
      localStorage.setItem('refresh_token', newRefreshToken);
    } catch (error) {
      console.error('Token refresh failed:', error);
      logout();
    }
  };

  const hasRole = (role: string) => {
    return user?.roles.includes(role) || false;
  };

  const hasPermission = (permission: string) => {
    return user?.permissions.includes(permission) || false;
  };

  const value = {
    user,
    loading,
    isAuthenticated: !!user,
    login,
    register,
    logout,
    refreshToken,
    hasRole,
    hasPermission,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}

// Login Form Component
import { ArrowRight, Loader2 } from 'lucide-react';
import { Form, EmailInput, PasswordInput, useForm } from '@/components/forms/FormComponents';

export function LoginForm() {
  const { login } = useAuth();
  const [isLoading, setIsLoading] = useState(false);
  
  const { values, errors, touched, setValue, setFieldTouched, validateAll } = useForm(
    { email: '', password: '' },
    {
      email: [
        { type: 'required' },
        {
          type: 'regex',
          pattern: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
          message: 'Invalid email address',
        },
      ],
      password: [
        { type: 'required' },
        {
          type: 'custom',
          validate: (v) =>
            typeof v === 'string' && v.length >= 8
              ? true
              : 'Minimum length is 8 characters',
        },
      ],
    }
  );

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!validateAll()) return;
    
    setIsLoading(true);
    try {
      await login(values.email, values.password);
    } catch (error) {
      // Error handled by AuthProvider
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="max-w-md w-full bg-white dark:bg-gray-800 rounded-xl shadow-lg p-8">
      <div className="text-center mb-8">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-gray-100 mb-2">
          Sign In
        </h2>
        <p className="text-gray-600 dark:text-gray-400">
          Welcome back to InfoTerminal
        </p>
      </div>

      <Form onSubmit={handleSubmit}>
        <EmailInput
          label="Email Address"
          name="email"
          value={values.email}
          onChange={(value) => setValue('email', value)}
          onBlur={() => setFieldTouched('email')}
          error={touched.email ? errors.email : null}
          placeholder="Enter your email"
          required
        />

        <PasswordInput
          label="Password"
          name="password"
          value={values.password}
          onChange={(value) => setValue('password', value)}
          onBlur={() => setFieldTouched('password')}
          error={touched.password ? errors.password : null}
          placeholder="Enter your password"
          required
        />

        <div className="flex items-center justify-between">
          <label className="flex items-center">
            <input
              type="checkbox"
              className="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
            />
            <span className="ml-2 text-sm text-gray-600 dark:text-gray-400">
              Remember me
            </span>
          </label>
          
          <button
            type="button"
            className="text-sm text-primary-600 dark:text-primary-400 hover:text-primary-500"
          >
            Forgot password?
          </button>
        </div>

        <button
          type="submit"
          disabled={isLoading}
          className="w-full flex items-center justify-center gap-2 px-4 py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          {isLoading ? (
            <>
              <Loader2 size={18} className="animate-spin" />
              Signing in...
            </>
          ) : (
            <>
              Sign In
              <ArrowRight size={18} />
            </>
          )}
        </button>

        <div className="text-center">
          <span className="text-sm text-gray-600 dark:text-gray-400">
            Don't have an account?{' '}
          </span>
          <button
            type="button"
            className="text-sm text-primary-600 dark:text-primary-400 hover:text-primary-500 font-medium"
          >
            Sign up
          </button>
        </div>
      </Form>
    </div>
  );
}

// Register Form Component
export function RegisterForm() {
  const { register } = useAuth();
  const [isLoading, setIsLoading] = useState(false);
  
  const { values, errors, touched, setValue, setFieldTouched, validateAll } =
    useForm(
      { name: '', email: '', password: '', confirmPassword: '' },
      {
        name: [
          { type: 'required' },
          {
            type: 'custom',
            validate: (v) =>
              typeof v === 'string' && v.length >= 2
                ? true
                : 'Minimum length is 2 characters',
          },
        ],
        email: [
          { type: 'required' },
          {
            type: 'regex',
            pattern: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
            message: 'Invalid email address',
          },
        ],
        password: [
          { type: 'required' },
          {
            type: 'custom',
            validate: (v) =>
              typeof v === 'string' && v.length >= 8
                ? true
                : 'Minimum length is 8 characters',
          },
        ],
        confirmPassword: [
          { type: 'required' },
          {
            type: 'custom',
            validate: (v, form) =>
              v === (form as any)?.password ? true : 'Passwords do not match',
          },
        ],
      }
    );

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!validateAll()) return;
    
    setIsLoading(true);
    try {
      await register(values.email, values.password, values.name);
    } catch (error) {
      // Error handled by AuthProvider
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="max-w-md w-full bg-white dark:bg-gray-800 rounded-xl shadow-lg p-8">
      <div className="text-center mb-8">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-gray-100 mb-2">
          Create Account
        </h2>
        <p className="text-gray-600 dark:text-gray-400">
          Join InfoTerminal today
        </p>
      </div>

      <Form onSubmit={handleSubmit}>
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              Full Name <span className="text-red-500">*</span>
            </label>
            <input
              type="text"
              name="name"
              value={values.name}
              onChange={(e) => setValue('name', e.target.value)}
              onBlur={() => setFieldTouched('name')}
              placeholder="Enter your full name"
              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
            />
            {touched.name && errors.name && (
              <p className="mt-1 text-sm text-red-600">{errors.name}</p>
            )}
          </div>

          <EmailInput
            label="Email Address"
            name="email"
            value={values.email}
            onChange={(value) => setValue('email', value)}
            onBlur={() => setFieldTouched('email')}
            error={touched.email ? errors.email : null}
            placeholder="Enter your email"
            required
          />

          <PasswordInput
            label="Password"
            name="password"
            value={values.password}
            onChange={(value) => setValue('password', value)}
            onBlur={() => setFieldTouched('password')}
            error={touched.password ? errors.password : null}
            placeholder="Create a password"
            helpText="At least 8 characters"
            required
          />

          <PasswordInput
            label="Confirm Password"
            name="confirmPassword"
            value={values.confirmPassword}
            onChange={(value) => setValue('confirmPassword', value)}
            onBlur={() => setFieldTouched('confirmPassword')}
            error={touched.confirmPassword ? errors.confirmPassword : null}
            placeholder="Confirm your password"
            required
          />
        </div>

        <div className="flex items-start gap-3">
          <input
            type="checkbox"
            required
            className="mt-1 rounded border-gray-300 text-primary-600 focus:ring-primary-500"
          />
          <span className="text-sm text-gray-600 dark:text-gray-400">
            I agree to the{' '}
            <button type="button" className="text-primary-600 dark:text-primary-400 hover:text-primary-500">
              Terms of Service
            </button>{' '}
            and{' '}
            <button type="button" className="text-primary-600 dark:text-primary-400 hover:text-primary-500">
              Privacy Policy
            </button>
          </span>
        </div>

        <button
          type="submit"
          disabled={isLoading}
          className="w-full flex items-center justify-center gap-2 px-4 py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          {isLoading ? (
            <>
              <Loader2 size={18} className="animate-spin" />
              Creating account...
            </>
          ) : (
            <>
              Create Account
              <ArrowRight size={18} />
            </>
          )}
        </button>

        <div className="text-center">
          <span className="text-sm text-gray-600 dark:text-gray-400">
            Already have an account?{' '}
          </span>
          <button
            type="button"
            className="text-sm text-primary-600 dark:text-primary-400 hover:text-primary-500 font-medium"
          >
            Sign in
          </button>
        </div>
      </Form>
    </div>
  );
}

// Auth Guard Component
interface AuthGuardProps {
  children: React.ReactNode;
  fallback?: React.ReactNode;
  requireRoles?: string[];
  requirePermissions?: string[];
}

export function AuthGuard({ 
  children, 
  fallback,
  requireRoles = [],
  requirePermissions = [] 
}: AuthGuardProps) {
  const { user, loading, isAuthenticated, hasRole, hasPermission } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!loading && !isAuthenticated) {
      router.push(`/login?returnTo=${encodeURIComponent(router.asPath)}`);
    }
  }, [loading, isAuthenticated, router]);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="flex items-center gap-3">
          <Loader2 size={24} className="animate-spin text-primary-600" />
          <span className="text-gray-600">Loading...</span>
        </div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return fallback || null;
  }

  // Check role requirements
  if (requireRoles.length > 0 && !requireRoles.some(role => hasRole(role))) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-gray-900 mb-2">Access Denied</h1>
          <p className="text-gray-600">You don't have permission to access this page.</p>
        </div>
      </div>
    );
  }

  // Check permission requirements
  if (requirePermissions.length > 0 && !requirePermissions.some(permission => hasPermission(permission))) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-gray-900 mb-2">Access Denied</h1>
          <p className="text-gray-600">You don't have permission to access this page.</p>
        </div>
      </div>
    );
  }

  return <>{children}</>;
}

// User Profile Dropdown
import { Fragment } from 'react';
import { User as UserIcon, Settings, LogOut, Shield } from 'lucide-react';

export function UserProfileDropdown() {
  const { user, logout } = useAuth();
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    }

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  if (!user) return null;

  return (
    <div ref={dropdownRef} className="relative">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center gap-3 p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
      >
        {user.avatar ? (
          <img
            src={user.avatar}
            alt={user.name}
            className="w-8 h-8 rounded-full"
          />
        ) : (
          <div className="w-8 h-8 bg-primary-500 rounded-full flex items-center justify-center">
            <UserIcon size={16} className="text-white" />
          </div>
        )}
        <div className="text-left">
          <p className="text-sm font-medium text-gray-900 dark:text-gray-100">
            {user.name}
          </p>
          <p className="text-xs text-gray-500 dark:text-gray-400">
            {user.email}
          </p>
        </div>
      </button>

      {isOpen && (
        <div className="absolute right-0 mt-2 w-56 bg-white dark:bg-gray-800 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700 py-1 z-50">
          <div className="px-4 py-3 border-b border-gray-200 dark:border-gray-700">
            <p className="text-sm font-medium text-gray-900 dark:text-gray-100">
              {user.name}
            </p>
            <p className="text-xs text-gray-500 dark:text-gray-400 truncate">
              {user.email}
            </p>
            {user.roles.length > 0 && (
              <div className="flex flex-wrap gap-1 mt-2">
                {user.roles.map(role => (
                  <span
                    key={role}
                    className="inline-flex items-center gap-1 px-2 py-0.5 bg-primary-100 dark:bg-primary-900/20 text-primary-800 dark:text-primary-300 text-xs rounded-full"
                  >
                    <Shield size={10} />
                    {role}
                  </span>
                ))}
              </div>
            )}
          </div>

          <button
            onClick={() => {
              setIsOpen(false);
              // Navigate to profile
            }}
            className="w-full flex items-center gap-3 px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
          >
            <UserIcon size={16} />
            Profile
          </button>

          <button
            onClick={() => {
              setIsOpen(false);
              // Navigate to settings
            }}
            className="w-full flex items-center gap-3 px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
          >
            <Settings size={16} />
            Settings
          </button>

          <hr className="border-gray-200 dark:border-gray-700 my-1" />

          <button
            onClick={logout}
            className="w-full flex items-center gap-3 px-4 py-2 text-sm text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20 transition-colors"
          >
            <LogOut size={16} />
            Sign out
          </button>
        </div>
      )}
    </div>
  );
}