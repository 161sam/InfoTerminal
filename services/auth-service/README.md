# InfoTerminal Auth Service

Enterprise-grade user management and authentication service for the InfoTerminal OSINT platform.

## Features

### Core Authentication
- **JWT-based Authentication**: Secure token-based authentication with access and refresh tokens
- **Multi-Factor Authentication (MFA)**: TOTP-based 2FA with backup codes
- **OAuth Integration**: Support for Google, GitHub, Microsoft OAuth providers
- **Session Management**: Comprehensive session tracking and management
- **Rate Limiting**: Brute-force protection with intelligent rate limiting

### User Management
- **Complete User CRUD**: Create, read, update, delete user accounts
- **Role-Based Access Control (RBAC)**: Granular permissions system
- **Account Status Management**: Active/inactive, verified/unverified states
- **Profile Management**: User profiles with avatars, preferences, metadata
- **API Key Management**: Personal API keys for programmatic access

### Security Features
- **Password Security**: Advanced password validation and strength checking
- **Account Lockout**: Automatic lockout after failed login attempts
- **Audit Logging**: Comprehensive audit trail for compliance
- **Security Headers**: Standard security headers and CORS protection
- **Email Validation**: Disposable email detection and validation

### Admin Features
- **User Statistics**: Dashboard with user metrics and analytics
- **Bulk Operations**: Bulk user management operations
- **Role Management**: Create and manage custom roles and permissions
- **Session Monitoring**: View and manage active user sessions
- **Audit Trail**: Complete audit log access for administrators

## Quick Start

### Environment Variables

```bash
# Database
AUTH_DATABASE_URL=postgresql://user:pass@localhost:5432/infoterminal_auth

# JWT Configuration
JWT_SECRET_KEY=your-secret-key-change-in-production
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7

# Server Configuration
HOST=0.0.0.0
PORT=8080
WORKERS=1
LOG_LEVEL=info
ENVIRONMENT=development

# CORS & Security
CORS_ORIGINS=http://localhost:3000,https://app.infoterminal.io
TRUSTED_HOSTS=localhost,127.0.0.1,app.infoterminal.io

# Feature Flags
USER_REGISTRATION_ENABLED=false
PASSWORD_MIN_LENGTH=8
MFA_ENABLED=true
</bash>

### Docker Deployment

```bash
# Build the container
docker build -t infoterminal-auth-service .

# Run the service
docker run -d \
  --name auth-service \
  -p 8080:8080 \
  --env-file .env \
  infoterminal-auth-service
```

### Development Setup

```bash
# Install dependencies
pip install -e .

# Run database migrations
python -m auth_service.models.database

# Start development server
uvicorn src.auth_service.app:app --reload --host 0.0.0.0 --port 8080
```

## API Documentation

### Authentication Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/login` | User login with email/password |
| POST | `/auth/refresh` | Refresh access token |
| POST | `/auth/logout` | Logout and invalidate session |
| GET | `/auth/me` | Get current user information |
| POST | `/auth/change-password` | Change user password |
| POST | `/auth/request-password-reset` | Request password reset |

### MFA Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/mfa/setup` | Setup MFA (get QR code) |
| POST | `/auth/mfa/enable` | Enable MFA with verification |
| POST | `/auth/mfa/disable` | Disable MFA |

### User Management Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/users/` | List users (paginated) |
| POST | `/users/` | Create new user |
| GET | `/users/{id}` | Get user by ID |
| PUT | `/users/{id}` | Update user |
| DELETE | `/users/{id}` | Delete user |
| POST | `/users/{id}/activate` | Activate user account |
| POST | `/users/{id}/deactivate` | Deactivate user account |

### Role Management Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/roles/` | List all roles |
| POST | `/roles/` | Create new role |
| GET | `/roles/{id}` | Get role by ID |
| PUT | `/roles/{id}` | Update role |
| DELETE | `/roles/{id}` | Delete role |
| GET | `/roles/permissions/` | List all permissions |

## Default Roles

The service comes with predefined roles for OSINT operations:

### Admin
- **Full system access** and user management
- **All permissions** across all services
- **Color**: Red (#dc2626) • **Icon**: shield-check

### Security Analyst
- **Advanced security** and verification features
- **Search, Graph, Security, Verification** permissions
- **Color**: Orange (#ea580c) • **Icon**: shield

### Intelligence Analyst
- **Full OSINT capabilities** and analysis tools
- **Search, Graph, NLP, Agent** permissions
- **Color**: Cyan (#0891b2) • **Icon**: search

### Analyst
- **Standard analysis** and research capabilities
- **Read-only access** to core services
- **Color**: Green (#059669) • **Icon**: user-check

### Viewer
- **Read-only access** to search and basic features
- **Minimal permissions** for viewing content
- **Color**: Gray (#6b7280) • **Icon**: eye

## Permissions System

Permissions follow the format `service:action`:

- **search:read** - View search results
- **search:write** - Create and modify searches
- **graph:analysis** - Run graph analytics
- **admin:users** - Manage users and roles
- **security:analysis** - Run security analysis

## Database Schema

### Core Tables

- **users** - User accounts and profiles
- **roles** - Role definitions and hierarchy
- **permissions** - Granular permission definitions
- **user_roles** - Many-to-many user-role assignments
- **role_permissions** - Many-to-many role-permission assignments

### Security Tables

- **user_sessions** - Active user sessions
- **api_keys** - Personal API keys
- **audit_logs** - Complete audit trail

## Security Considerations

### Password Security
- Bcrypt hashing with configurable rounds
- Password strength validation
- Common password detection
- Breach database checking (optional)

### Session Security
- Secure session token generation
- Automatic session expiration
- Device fingerprinting
- IP-based session validation

### API Security
- Rate limiting per IP and user
- Request size limits
- Security headers enforcement
- CORS configuration

## Monitoring & Observability

### Prometheus Metrics
- Request count and duration
- Error rates by type
- Authentication success/failure rates
- Active session counts

### Health Checks
- Database connectivity
- Service dependencies
- Resource utilization
- Component status

### Audit Logging
- All authentication events
- User management actions
- Permission changes
- Failed access attempts

## Integration

### Frontend Integration

```typescript
// Initialize auth client
const authClient = new AuthClient({
  baseURL: 'http://localhost:8080',
  apiKey: 'your-api-key'
});

// Login
const result = await authClient.login({
  email: 'user@example.com',
  password: 'password123'
});

// Check permissions
if (authClient.hasPermission('search:write')) {
  // User can create searches
}
```

### Service Integration

```python
# Validate JWT token
from auth_service.core.auth import TokenManager

payload = TokenManager.verify_token(token)
if payload:
    user_id = payload['sub']
    permissions = payload['permissions']
```

## Development

### Testing

```bash
# Run tests
pytest tests/

# Run with coverage
pytest --cov=src tests/

# Run integration tests
pytest tests/integration/
```

### Code Quality

```bash
# Format code
black src/ tests/

# Lint code
ruff src/ tests/

# Type checking
mypy src/
```

## Support

For issues and questions:
- **Documentation**: `/docs` endpoint
- **Health Status**: `/health` endpoint
- **Metrics**: `/metrics` endpoint

## License

Copyright (c) 2024 InfoTerminal Team. All rights reserved.
