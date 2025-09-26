export interface User {
  id: string;
  email: string;
  name?: string;
  display_name?: string;
  first_name?: string;
  last_name?: string;
  avatar?: string;
  avatar_url?: string;
  roles: string[];
  permissions: string[];
  tenant?: string;
  status?: string;
  department?: string;
  phone?: string;
  lastLogin?: string;
  createdAt?: string;
  updatedAt?: string;
  preferences?: Record<string, unknown>;
  metadata?: Record<string, unknown>;
  // Optional fields used in Settings UI
  sessionsCount?: number;
  is_active?: boolean;
}
