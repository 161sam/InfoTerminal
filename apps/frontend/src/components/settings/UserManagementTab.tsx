import React, { useState, useEffect } from 'react';
import { 
  Users, 
  User, 
  Plus, 
  Search, 
  Filter, 
  MoreVertical, 
  Edit,
  Trash2,
  Shield,
  Clock,
  Mail,
  Phone,
  Building,
  AlertCircle,
  CheckCircle,
  UserPlus,
  UserMinus,
  Settings,
  Key,
  Download,
  Upload,
  RefreshCw,
  UserCheck,
  UserX,
  Eye
} from 'lucide-react';
import { Tabs, TabsList, TabsTrigger, TabsContent } from '@/components/ui/tabs';

// Types
interface UserProfile {
  id: string;
  email: string;
  name?: string;
  first_name?: string;
  last_name?: string;
  display_name?: string;
  avatar_url?: string;
  role: 'Admin' | 'Security' | 'Analyst' | 'Viewer' | 'Guest';
  status: 'active' | 'inactive' | 'pending' | 'suspended';
  phone?: string;
  department?: string;
  lastLogin?: Date;
  createdAt: Date;
  permissions: string[];
  sessionsCount?: number;
  is_active?: boolean;
  is_verified?: boolean;
  email_verified?: boolean;
  mfa_enabled?: boolean;
  roles?: string[];
  last_login?: string;
  created_at?: string;
}

interface Role {
  id: string;
  name: string;
  display_name?: string;
  description: string;
  permissions: string[];
  color: string;
  user_count?: number;
}

interface UserManagementTabProps {
  mode?: 'demo' | 'api';
  className?: string;
}

// Demo data
const DEMO_USERS: UserProfile[] = [
  {
    id: '1',
    name: 'Dr. Sarah Chen',
    email: 'sarah.chen@infoterminal.io',
    role: 'Admin',
    status: 'active',
    phone: '+1-555-0123',
    department: 'Research',
    lastLogin: new Date('2024-03-15T14:30:00Z'),
    createdAt: new Date('2023-01-15T09:00:00Z'),
    permissions: ['read', 'write', 'delete', 'admin', 'user_management'],
    sessionsCount: 3,
    mfa_enabled: true,
    is_verified: true
  },
  {
    id: '2',
    name: 'Marcus Rodriguez',
    email: 'marcus.r@infoterminal.io', 
    role: 'Security',
    status: 'active',
    phone: '+1-555-0124',
    department: 'Security',
    lastLogin: new Date('2024-03-14T09:15:00Z'),
    createdAt: new Date('2023-02-20T10:30:00Z'),
    permissions: ['read', 'write', 'security', 'threat_analysis'],
    sessionsCount: 1,
    mfa_enabled: true,
    is_verified: true
  },
  {
    id: '3',
    name: 'Alex Thompson',
    email: 'alex.thompson@infoterminal.io',
    role: 'Analyst',
    status: 'active',
    phone: '+1-555-0125',
    department: 'Intelligence',
    lastLogin: new Date('2024-03-13T16:45:00Z'),
    createdAt: new Date('2023-03-10T11:15:00Z'),
    permissions: ['read', 'write', 'analysis'],
    sessionsCount: 2,
    mfa_enabled: false,
    is_verified: true
  },
  {
    id: '4',
    name: 'Emma Wilson',
    email: 'emma.wilson@infoterminal.io',
    role: 'Viewer',
    status: 'inactive',
    department: 'Compliance',
    lastLogin: new Date('2024-02-28T08:20:00Z'),
    createdAt: new Date('2023-04-05T14:00:00Z'),
    permissions: ['read'],
    sessionsCount: 0,
    mfa_enabled: false,
    is_verified: true
  },
  {
    id: '5',
    name: 'James Park',
    email: 'james.park@infoterminal.io',
    role: 'Analyst',
    status: 'pending',
    department: 'Research',
    createdAt: new Date('2024-03-01T12:00:00Z'),
    permissions: ['read'],
    sessionsCount: 0,
    mfa_enabled: false,
    is_verified: false
  }
];

const ROLES: Role[] = [
  {
    id: 'admin',
    name: 'admin',
    display_name: 'Admin',
    description: 'Full system access with user management capabilities',
    permissions: ['read', 'write', 'delete', 'admin', 'user_management', 'system_config'],
    color: 'red'
  },
  {
    id: 'security',
    name: 'security_analyst',
    display_name: 'Security Analyst',
    description: 'Security-focused analysis and threat assessment',
    permissions: ['read', 'write', 'security', 'threat_analysis', 'incident_response'],
    color: 'orange'
  },
  {
    id: 'analyst',
    name: 'intelligence_analyst',
    display_name: 'Intelligence Analyst',
    description: 'Data analysis and investigation capabilities',
    permissions: ['read', 'write', 'analysis', 'graph_access', 'nlp_access'],
    color: 'blue'
  },
  {
    id: 'viewer',
    name: 'viewer',
    display_name: 'Viewer',
    description: 'Read-only access to approved content',
    permissions: ['read'],
    color: 'green'
  },
  {
    id: 'guest',
    name: 'guest',
    display_name: 'Guest',
    description: 'Limited access for external collaborators',
    permissions: ['read_limited'],
    color: 'gray'
  }
];

// Utility functions
const STATUS_COLORS = {
  active: 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-300',
  inactive: 'bg-gray-100 text-gray-800 dark:bg-gray-900/30 dark:text-gray-300',
  pending: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-300',
  suspended: 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-300'
};

const ROLE_COLORS = {
  red: 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-300',
  orange: 'bg-orange-100 text-orange-800 dark:bg-orange-900/30 dark:text-orange-300',
  blue: 'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-300',
  green: 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-300',
  gray: 'bg-gray-100 text-gray-800 dark:bg-gray-900/30 dark:text-gray-300'
};

const normalizeUser = (user: any): UserProfile => {
  return {
    id: user.id,
    email: user.email,
    name: user.name || user.display_name || `${user.first_name || ''} ${user.last_name || ''}`.trim() || 'Unnamed User',
    role: user.role || (user.roles && user.roles[0]) || 'Viewer',
    status: user.status || (user.is_active ? 'active' : 'inactive'),
    phone: user.phone,
    department: user.department,
    lastLogin: user.lastLogin || (user.last_login ? new Date(user.last_login) : undefined),
    createdAt: user.createdAt || (user.created_at ? new Date(user.created_at) : new Date()),
    permissions: user.permissions || [],
    sessionsCount: user.sessionsCount || 0,
    mfa_enabled: user.mfa_enabled || false,
    is_verified: user.is_verified || false,
    avatar_url: user.avatar_url
  };
};

const UserManagementTab: React.FC<UserManagementTabProps> = ({ 
  mode = 'demo',
  className = '' 
}) => {
  // State management
  const [users, setUsers] = useState<UserProfile[]>([]);
  const [roles, setRoles] = useState<Role[]>(ROLES);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string>('');
  
  // Pagination and filtering
  const [currentPage, setCurrentPage] = useState(1);
  const [pageSize, setPageSize] = useState(20);
  const [totalUsers, setTotalUsers] = useState(0);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedRole, setSelectedRole] = useState<string>('');
  const [statusFilter, setStatusFilter] = useState<string>('');
  
  // Selection and actions
  const [selectedUsers, setSelectedUsers] = useState<Set<string>>(new Set());
  const [showCreateUser, setShowCreateUser] = useState(false);
  const [editingUser, setEditingUser] = useState<UserProfile | null>(null);
  const [actionLoading, setActionLoading] = useState<string>('');
  const [activeTab, setActiveTab] = useState('users');

  // Load data on component mount and when filters change
  useEffect(() => {
    if (mode === 'demo') {
      loadDemoUsers();
    } else {
      loadApiUsers();
    }
    if (mode === 'api') {
      loadApiRoles();
    }
  }, [mode, currentPage, pageSize, searchTerm, selectedRole, statusFilter]);

  const loadDemoUsers = () => {
    // Apply filters to demo data
    let filteredUsers = DEMO_USERS.filter(user => {
      const matchesSearch = user.name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
                           user.email.toLowerCase().includes(searchTerm.toLowerCase()) ||
                           (user.department || '').toLowerCase().includes(searchTerm.toLowerCase());
      
      const matchesStatus = statusFilter === '' || user.status === statusFilter;
      const matchesRole = selectedRole === '' || user.role === selectedRole;

      return matchesSearch && matchesStatus && matchesRole;
    });

    // Apply pagination
    const startIndex = (currentPage - 1) * pageSize;
    const paginatedUsers = filteredUsers.slice(startIndex, startIndex + pageSize);

    setUsers(paginatedUsers.map(normalizeUser));
    setTotalUsers(filteredUsers.length);
    setLoading(false);
  };

  const loadApiUsers = async () => {
    try {
      setLoading(true);
      
      const params = new URLSearchParams({
        page: currentPage.toString(),
        size: pageSize.toString(),
        ...(searchTerm && { search: searchTerm }),
        ...(selectedRole && { role: selectedRole }),
        ...(statusFilter === 'active' && { is_active: 'true' }),
        ...(statusFilter === 'inactive' && { is_active: 'false' }),
        ...(statusFilter === 'verified' && { is_verified: 'true' }),
        ...(statusFilter === 'unverified' && { is_verified: 'false' })
      });

      const response = await fetch(`/api/users?${params}`, {
        credentials: 'include'
      });

      if (!response.ok) {
        throw new Error('Failed to load users');
      }

      const data = await response.json();
      setUsers((data.users || []).map(normalizeUser));
      setTotalUsers(data.total || 0);
      
    } catch (err: any) {
      setError(err.message);
      // Fallback to demo data on API error
      loadDemoUsers();
    } finally {
      setLoading(false);
    }
  };

  const loadApiRoles = async () => {
    try {
      const response = await fetch('/api/roles', {
        credentials: 'include'
      });

      if (response.ok) {
        const data: Role[] = await response.json();
        setRoles(data.length > 0 ? data : ROLES);
      }
    } catch (err) {
      console.error('Failed to load roles:', err);
      setRoles(ROLES);
    }
  };

  // Filter users based on search and filters for demo mode
  const filteredUsers = users.filter(user => {
    if (mode === 'api') return true; // API handles filtering

    const matchesSearch = user.name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         user.email.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         (user.department || '').toLowerCase().includes(searchTerm.toLowerCase());
    
    const matchesStatus = statusFilter === '' || user.status === statusFilter;
    const matchesRole = selectedRole === '' || user.role === selectedRole;

    return matchesSearch && matchesStatus && matchesRole;
  });

  // Get stats
  const stats = {
    total: mode === 'api' ? totalUsers : users.length,
    active: users.filter(u => u.status === 'active').length,
    pending: users.filter(u => u.status === 'pending').length,
    suspended: users.filter(u => u.status === 'suspended').length
  };

  const handleUserSelect = (userId: string) => {
    setSelectedUsers(prev => {
      const newSelection = new Set(prev);
      if (newSelection.has(userId)) {
        newSelection.delete(userId);
      } else {
        newSelection.add(userId);
      }
      return newSelection;
    });
  };

  const handleSelectAll = () => {
    setSelectedUsers(
      selectedUsers.size === filteredUsers.length 
        ? new Set() 
        : new Set(filteredUsers.map(u => u.id))
    );
  };

  const handleStatusChange = async (userId: string, newStatus: UserProfile['status']) => {
    if (mode === 'api') {
      await handleUserAction(newStatus === 'active' ? 'activate' : 'deactivate', userId);
    } else {
      setUsers(prev => prev.map(user => 
        user.id === userId 
          ? { ...user, status: newStatus }
          : user
      ));
    }
  };

  const handleDeleteUser = async (userId: string) => {
    if (!confirm('Are you sure you want to delete this user? This action cannot be undone.')) {
      return;
    }

    if (mode === 'api') {
      try {
        setActionLoading(`delete-${userId}`);
        
        const response = await fetch(`/api/users/${userId}`, {
          method: 'DELETE',
          credentials: 'include'
        });

        if (!response.ok) {
          const error = await response.json();
          throw new Error(error.error || 'Failed to delete user');
        }

        await loadApiUsers();
        
      } catch (err: any) {
        setError(err.message);
      } finally {
        setActionLoading('');
      }
    } else {
      setUsers(prev => prev.filter(user => user.id !== userId));
      setSelectedUsers(prev => {
        const newSelection = new Set(prev);
        newSelection.delete(userId);
        return newSelection;
      });
    }
  };

  const handleUserAction = async (action: string, userId: string) => {
    if (mode === 'demo') {
      // Handle demo mode actions
      if (action === 'activate' || action === 'deactivate') {
        setUsers(prev => prev.map(user => 
          user.id === userId 
            ? { ...user, status: action === 'activate' ? 'active' : 'inactive' }
            : user
        ));
      }
      return;
    }

    try {
      setActionLoading(`${action}-${userId}`);
      
      const response = await fetch(`/api/users/${userId}/${action}`, {
        method: 'POST',
        credentials: 'include'
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.error || `Failed to ${action} user`);
      }

      await loadApiUsers();
      
    } catch (err: any) {
      setError(err.message);
    } finally {
      setActionLoading('');
    }
  };

  const handleBulkAction = async (action: string) => {
    if (selectedUsers.size === 0) return;

    if (mode === 'demo') {
      // Handle demo mode bulk actions
      switch (action) {
        case 'activate':
          setUsers(prev => prev.map(user => 
            selectedUsers.has(user.id) 
              ? { ...user, status: 'active' as const }
              : user
          ));
          break;
        case 'deactivate':
          setUsers(prev => prev.map(user => 
            selectedUsers.has(user.id) 
              ? { ...user, status: 'inactive' as const }
              : user
          ));
          break;
        case 'delete':
          if (confirm(`Are you sure you want to delete ${selectedUsers.size} users? This action cannot be undone.`)) {
            setUsers(prev => prev.filter(user => !selectedUsers.has(user.id)));
            setSelectedUsers(new Set());
          }
          break;
      }
      return;
    }

    try {
      setActionLoading(`bulk-${action}`);
      
      const promises = Array.from(selectedUsers).map(userId => 
        fetch(`/api/users/${userId}/${action}`, {
          method: 'POST',
          credentials: 'include'
        })
      );

      await Promise.all(promises);
      setSelectedUsers(new Set());
      await loadApiUsers();
      
    } catch (err: any) {
      setError(err.message);
    } finally {
      setActionLoading('');
    }
  };

  const exportUsers = () => {
    const dataStr = JSON.stringify(users, null, 2);
    const dataUri = 'data:application/json;charset=utf-8,'+ encodeURIComponent(dataStr);
    const exportFileDefaultName = 'infoterminal-users.json';
    
    const linkElement = document.createElement('a');
    linkElement.setAttribute('href', dataUri);
    linkElement.setAttribute('download', exportFileDefaultName);
    linkElement.click();
  };

  const formatDate = (date?: Date | string) => {
    if (!date) return 'Never';
    const d = date instanceof Date ? date : new Date(date);
    return d.toLocaleDateString();
  };

  const getStatusIcon = (user: UserProfile) => {
    if (user.status !== 'active') return <UserX className="w-4 h-4 text-red-500" />;
    if (!user.is_verified) return <Clock className="w-4 h-4 text-yellow-500" />;
    if (user.mfa_enabled) return <Shield className="w-4 h-4 text-green-500" />;
    return <UserCheck className="w-4 h-4 text-blue-500" />;
  };

  const getRoleColor = (roleName: string) => {
    const role = roles.find(r => r.name === roleName || r.display_name === roleName);
    return role?.color || 'gray';
  };

  const totalPages = Math.ceil((mode === 'api' ? totalUsers : filteredUsers.length) / pageSize);
  const displayUsers = mode === 'api' ? users : filteredUsers.slice((currentPage - 1) * pageSize, currentPage * pageSize);

  return (
    <div className={`space-y-6 ${className}`}>
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-semibold text-gray-900 dark:text-white">User Management</h2>
          <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
            Manage user accounts, roles, and permissions
            {mode === 'demo' && (
              <span className="ml-2 px-2 py-1 text-xs bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-300 rounded">
                Demo Mode
              </span>
            )}
          </p>
        </div>
        
        <div className="flex items-center gap-3">
          <button
            onClick={exportUsers}
            className="inline-flex items-center gap-2 px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 dark:bg-gray-800 dark:text-gray-300 dark:border-gray-600 dark:hover:bg-gray-700"
          >
            <Download size={16} />
            Export
          </button>
          
          <button
            onClick={() => setShowCreateUser(true)}
            className="inline-flex items-center gap-2 px-4 py-2 text-sm font-medium text-white bg-primary-600 rounded-lg hover:bg-primary-700"
          >
            <UserPlus size={16} />
            Add User
          </button>
        </div>
      </div>

      {/* Error Display */}
      {error && (
        <div className="flex items-center gap-2 p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg">
          <AlertCircle size={18} className="text-red-600 dark:text-red-400" />
          <span className="text-red-800 dark:text-red-200">{error}</span>
          <button 
            onClick={() => setError('')}
            className="ml-auto text-red-600 dark:text-red-400 hover:text-red-800 dark:hover:text-red-200"
          >
            ×
          </button>
        </div>
      )}

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-white dark:bg-gray-800 p-4 rounded-lg border border-gray-200 dark:border-gray-700">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Total Users</p>
              <p className="text-2xl font-semibold text-gray-900 dark:text-white">{stats.total}</p>
            </div>
            <Users className="h-8 w-8 text-gray-400" />
          </div>
        </div>
        
        <div className="bg-white dark:bg-gray-800 p-4 rounded-lg border border-gray-200 dark:border-gray-700">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Active</p>
              <p className="text-2xl font-semibold text-green-600">{stats.active}</p>
            </div>
            <CheckCircle className="h-8 w-8 text-green-400" />
          </div>
        </div>
        
        <div className="bg-white dark:bg-gray-800 p-4 rounded-lg border border-gray-200 dark:border-gray-700">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Pending</p>
              <p className="text-2xl font-semibold text-yellow-600">{stats.pending}</p>
            </div>
            <Clock className="h-8 w-8 text-yellow-400" />
          </div>
        </div>
        
        <div className="bg-white dark:bg-gray-800 p-4 rounded-lg border border-gray-200 dark:border-gray-700">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Suspended</p>
              <p className="text-2xl font-semibold text-red-600">{stats.suspended}</p>
            </div>
            <AlertCircle className="h-8 w-8 text-red-400" />
          </div>
        </div>
      </div>

      {/* Main Content Tabs */}
      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList className="bg-gray-50 dark:bg-gray-800 p-1 rounded-lg">
          <TabsTrigger value="users" className="inline-flex items-center gap-2">
            <Users size={16} />
            Users
          </TabsTrigger>
          <TabsTrigger value="roles" className="inline-flex items-center gap-2">
            <Shield size={16} />
            Roles & Permissions
          </TabsTrigger>
          <TabsTrigger value="sessions" className="inline-flex items-center gap-2">
            <Key size={16} />
            Active Sessions
          </TabsTrigger>
        </TabsList>

        {/* Users Tab */}
        <TabsContent value="users" className="mt-6">
          {/* Filters and Search */}
          <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700">
            <div className="p-4 border-b border-gray-200 dark:border-gray-700">
              <div className="flex flex-col sm:flex-row gap-4">
                {/* Search */}
                <div className="flex-1">
                  <div className="relative">
                    <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={18} />
                    <input
                      type="text"
                      placeholder="Search users by name, email, or department..."
                      value={searchTerm}
                      onChange={(e) => setSearchTerm(e.target.value)}
                      className="w-full pl-10 pr-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
                    />
                  </div>
                </div>

                {/* Filters */}
                <div className="flex gap-2">
                  <select
                    value={statusFilter}
                    onChange={(e) => setStatusFilter(e.target.value)}
                    className="px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
                  >
                    <option value="">All Status</option>
                    <option value="active">Active</option>
                    <option value="inactive">Inactive</option>
                    <option value="pending">Pending</option>
                    <option value="suspended">Suspended</option>
                  </select>

                  <select
                    value={selectedRole}
                    onChange={(e) => setSelectedRole(e.target.value)}
                    className="px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
                  >
                    <option value="">All Roles</option>
                    {roles.map(role => (
                      <option key={role.id} value={role.display_name || role.name}>
                        {role.display_name || role.name}
                      </option>
                    ))}
                  </select>
                </div>
              </div>

              {/* Bulk Actions */}
              {selectedUsers.size > 0 && (
                <div className="mt-4 flex items-center gap-4 p-3 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
                  <span className="text-sm text-blue-700 dark:text-blue-300">
                    {selectedUsers.size} user{selectedUsers.size > 1 ? 's' : ''} selected
                  </span>
                  
                  <div className="flex gap-2">
                    <button
                      onClick={() => handleBulkAction('activate')}
                      disabled={actionLoading.startsWith('bulk-')}
                      className="px-3 py-1 text-xs font-medium text-green-700 bg-green-100 rounded hover:bg-green-200 dark:bg-green-900/30 dark:text-green-300 dark:hover:bg-green-900/50 disabled:opacity-50"
                    >
                      Activate
                    </button>
                    <button
                      onClick={() => handleBulkAction('deactivate')}
                      disabled={actionLoading.startsWith('bulk-')}
                      className="px-3 py-1 text-xs font-medium text-gray-700 bg-gray-100 rounded hover:bg-gray-200 dark:bg-gray-700 dark:text-gray-300 dark:hover:bg-gray-600 disabled:opacity-50"
                    >
                      Deactivate
                    </button>
                    <button
                      onClick={() => handleBulkAction('delete')}
                      disabled={actionLoading.startsWith('bulk-')}
                      className="px-3 py-1 text-xs font-medium text-red-700 bg-red-100 rounded hover:bg-red-200 dark:bg-red-900/30 dark:text-red-300 dark:hover:bg-red-900/50 disabled:opacity-50"
                    >
                      Delete
                    </button>
                  </div>
                </div>
              )}
            </div>

            {/* Users Table */}
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-gray-50 dark:bg-gray-700/50">
                  <tr>
                    <th className="px-4 py-3 text-left">
                      <input
                        type="checkbox"
                        checked={selectedUsers.size === displayUsers.length && displayUsers.length > 0}
                        onChange={handleSelectAll}
                        className="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
                      />
                    </th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                      User
                    </th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                      Role
                    </th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                      Status
                    </th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                      Last Login
                    </th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                      Sessions
                    </th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                      Actions
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
                  {loading ? (
                    <tr>
                      <td colSpan={7} className="px-4 py-8 text-center text-gray-500 dark:text-gray-400">
                        <RefreshCw className="w-5 h-5 mx-auto mb-2 animate-spin" />
                        Loading users...
                      </td>
                    </tr>
                  ) : displayUsers.length === 0 ? (
                    <tr>
                      <td colSpan={7} className="px-4 py-8 text-center text-gray-500 dark:text-gray-400">
                        <Users className="mx-auto h-12 w-12 text-gray-400" />
                        <h3 className="mt-2 text-sm font-medium text-gray-900 dark:text-white">No users found</h3>
                        <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
                          Try adjusting your search or filter criteria.
                        </p>
                      </td>
                    </tr>
                  ) : (
                    displayUsers.map((user) => {
                      const role = roles.find(r => r.name === user.role || r.display_name === user.role);
                      return (
                        <tr key={user.id} className="hover:bg-gray-50 dark:hover:bg-gray-700/50">
                          <td className="px-4 py-4">
                            <input
                              type="checkbox"
                              checked={selectedUsers.has(user.id)}
                              onChange={() => handleUserSelect(user.id)}
                              className="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
                            />
                          </td>
                          <td className="px-4 py-4">
                            <div className="flex items-center gap-3">
                              <div className="w-8 h-8 rounded-full bg-primary-100 dark:bg-primary-900/30 flex items-center justify-center flex-shrink-0">
                                {user.avatar_url ? (
                                  <img 
                                    src={user.avatar_url} 
                                    alt={user.name}
                                    className="w-8 h-8 rounded-full object-cover"
                                  />
                                ) : (
                                  <User size={16} className="text-primary-600 dark:text-primary-400" />
                                )}
                              </div>
                              <div className="min-w-0 flex-1">
                                <div className="text-sm font-medium text-gray-900 dark:text-white truncate">
                                  {user.name}
                                </div>
                                <div className="text-xs text-gray-500 dark:text-gray-400 truncate">
                                  {user.email}
                                </div>
                                {user.department && (
                                  <div className="text-xs text-gray-400 dark:text-gray-500 truncate">
                                    {user.department}
                                  </div>
                                )}
                              </div>
                            </div>
                          </td>
                          <td className="px-4 py-4">
                            <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${
                              role ? ROLE_COLORS[role.color as keyof typeof ROLE_COLORS] : ROLE_COLORS.gray
                            }`}>
                              {role?.display_name || user.role}
                            </span>
                          </td>
                          <td className="px-4 py-4">
                            <div className="flex items-center gap-2">
                              {getStatusIcon(user)}
                              <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${
                                STATUS_COLORS[user.status]
                              }`}>
                                {user.status}
                              </span>
                            </div>
                          </td>
                          <td className="px-4 py-4">
                            <div className="text-sm text-gray-900 dark:text-white">
                              {formatDate(user.lastLogin)}
                            </div>
                            {user.lastLogin && (
                              <div className="text-xs text-gray-500 dark:text-gray-400">
                                {user.lastLogin instanceof Date ? user.lastLogin.toLocaleTimeString() : 
                                 new Date(user.lastLogin).toLocaleTimeString()}
                              </div>
                            )}
                          </td>
                          <td className="px-4 py-4">
                            <div className="text-sm text-gray-900 dark:text-white">
                              {user.sessionsCount || 0}
                            </div>
                          </td>
                          <td className="px-4 py-4">
                            <div className="flex items-center gap-2">
                              <button
                                onClick={() => setEditingUser(user)}
                                className="p-1 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
                                title="Edit user"
                              >
                                <Edit size={16} />
                              </button>
                              
                              {user.status === 'active' ? (
                                <button
                                  onClick={() => handleUserAction('deactivate', user.id)}
                                  disabled={actionLoading === `deactivate-${user.id}`}
                                  className="p-1 text-yellow-500 hover:text-yellow-700 disabled:opacity-50"
                                  title="Deactivate user"
                                >
                                  <UserX size={16} />
                                </button>
                              ) : (
                                <button
                                  onClick={() => handleUserAction('activate', user.id)}
                                  disabled={actionLoading === `activate-${user.id}`}
                                  className="p-1 text-green-500 hover:text-green-700 disabled:opacity-50"
                                  title="Activate user"
                                >
                                  <UserCheck size={16} />
                                </button>
                              )}
                              
                              <button
                                onClick={() => handleDeleteUser(user.id)}
                                disabled={actionLoading === `delete-${user.id}`}
                                className="p-1 text-red-500 hover:text-red-700 disabled:opacity-50"
                                title="Delete user"
                              >
                                <Trash2 size={16} />
                              </button>
                            </div>
                          </td>
                        </tr>
                      );
                    })
                  )}
                </tbody>
              </table>
            </div>
          </div>

          {/* Pagination */}
          {totalPages > 1 && (
            <div className="flex items-center justify-between">
              <div className="text-sm text-gray-500 dark:text-gray-400">
                Showing {((currentPage - 1) * pageSize) + 1} to {Math.min(currentPage * pageSize, mode === 'api' ? totalUsers : filteredUsers.length)} of {mode === 'api' ? totalUsers : filteredUsers.length} users
              </div>
              
              <div className="flex items-center gap-2">
                <button
                  onClick={() => setCurrentPage(prev => Math.max(1, prev - 1))}
                  disabled={currentPage === 1}
                  className="px-3 py-1 border border-gray-300 dark:border-gray-600 rounded text-sm disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50 dark:hover:bg-gray-700"
                >
                  Previous
                </button>
                
                <div className="flex items-center gap-1">
                  {Array.from({ length: Math.min(5, totalPages) }, (_, i) => {
                    const page = i + 1;
                    return (
                      <button
                        key={page}
                        onClick={() => setCurrentPage(page)}
                        className={`px-3 py-1 rounded text-sm ${
                          currentPage === page
                            ? 'bg-primary-600 text-white'
                            : 'border border-gray-300 dark:border-gray-600 hover:bg-gray-50 dark:hover:bg-gray-700'
                        }`}
                      >
                        {page}
                      </button>
                    );
                  })}
                </div>
                
                <button
                  onClick={() => setCurrentPage(prev => Math.min(totalPages, prev + 1))}
                  disabled={currentPage === totalPages}
                  className="px-3 py-1 border border-gray-300 dark:border-gray-600 rounded text-sm disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50 dark:hover:bg-gray-700"
                >
                  Next
                </button>
              </div>
            </div>
          )}
        </TabsContent>

        {/* Roles Tab */}
        <TabsContent value="roles" className="mt-6">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {roles.map((role) => (
              <div key={role.id} className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-4">
                <div className="flex items-start justify-between mb-3">
                  <div className="flex items-center gap-3">
                    <div className={`p-2 rounded-lg ${ROLE_COLORS[role.color as keyof typeof ROLE_COLORS]}`}>
                      <Shield size={16} />
                    </div>
                    <div>
                      <h3 className="font-medium text-gray-900 dark:text-white">{role.display_name || role.name}</h3>
                      <p className="text-sm text-gray-500 dark:text-gray-400">{role.description}</p>
                    </div>
                  </div>
                  <button className="p-1 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300">
                    <Settings size={16} />
                  </button>
                </div>
                
                <div className="space-y-2">
                  <div className="text-xs font-medium text-gray-700 dark:text-gray-300">Permissions:</div>
                  <div className="flex flex-wrap gap-1">
                    {role.permissions.map((permission) => (
                      <span 
                        key={permission}
                        className="inline-flex items-center px-2 py-1 rounded text-xs font-medium bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300"
                      >
                        {permission.replace('_', ' ')}
                      </span>
                    ))}
                  </div>
                </div>
                
                <div className="mt-4 pt-3 border-t border-gray-200 dark:border-gray-700">
                  <div className="text-xs text-gray-500 dark:text-gray-400">
                    {users.filter(u => u.role === role.name || u.role === role.display_name).length} users assigned
                  </div>
                </div>
              </div>
            ))}
          </div>
        </TabsContent>

        {/* Sessions Tab */}
        <TabsContent value="sessions" className="mt-6">
          <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700">
            <div className="p-4 border-b border-gray-200 dark:border-gray-700">
              <h3 className="text-lg font-medium text-gray-900 dark:text-white">Active Sessions</h3>
              <p className="text-sm text-gray-500 dark:text-gray-400">Monitor and manage user sessions</p>
            </div>
            
            <div className="p-8 text-center">
              <Key className="mx-auto h-12 w-12 text-gray-400" />
              <h3 className="mt-2 text-sm font-medium text-gray-900 dark:text-white">Session Management</h3>
              <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
                Session monitoring and management features will be available in the full implementation.
              </p>
            </div>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default UserManagementTab;
