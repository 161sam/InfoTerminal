# InfoTerminal Docker Setup - Complete Guide

This document provides a complete guide to set up InfoTerminal v0.2.0 using Docker and docker-compose.

## 🚀 Quick Start

### Prerequisites

- Docker Engine 20.10+ 
- Docker Compose 2.0+ (or docker-compose 1.29+)
- At least 8GB RAM available for Docker
- 20GB disk space for images and volumes

### 1. Clone and Prepare

```bash
git clone <repository-url>
cd InfoTerminal
cp .env.example .env
```

### 2. Environment Configuration

Edit `.env` file and set required variables:

```bash
# Core Configuration
IT_HOSTNAME=localhost
POSTGRES_PASSWORD=your_secure_password
NEO4J_PASSWORD=your_neo4j_password
REDIS_PASSWORD=your_redis_password

# Service Ports (optional, defaults provided)
IT_PORT_FRONTEND=3000
IT_PORT_VERIFICATION=8617
IT_PORT_OPS_CONTROLLER=8618
IT_PORT_SEARCH=8001
IT_PORT_GRAPH=8612

# NiFi & n8n Credentials
NIFI_PASSWORD=adminpassword
N8N_PASSWORD=adminpassword
```

### 3. Validate Docker Setup

Run the verification script to ensure all Dockerfiles are present and valid:

```bash
bash docker-build-verification.sh
```

### 4. Start InfoTerminal

Full verification stack (recommended):

```bash
docker-compose -f docker-compose.verification.yml up -d
```

Or core services only:

```bash
docker-compose up -d
```

### 5. Verify Services

Check all services are running:

```bash
docker-compose -f docker-compose.verification.yml ps
```

Access the applications:
- **Frontend**: http://localhost:3000
- **Verification Dashboard**: http://localhost:8617
- **Ops Controller**: http://localhost:8618
- **Apache NiFi**: http://localhost:8619 (admin/adminpassword)
- **n8n**: http://localhost:5678 (admin/adminpassword)
- **Neo4j Browser**: http://localhost:7474 
- **OpenSearch**: http://localhost:9200

## 🏗️ Architecture Overview

### Core Services (Custom Built)

| Service | Port | Description | Dockerfile Location |
|---------|------|-------------|-------------------|
| **Frontend** | 3000 | Next.js React Application | `apps/frontend/Dockerfile` |
| **Verification Service** | 8617 | Data verification & validation | `services/verification/Dockerfile` |
| **Ops Controller** | 8618 | Operations orchestration | `services/ops-controller/Dockerfile` |
| **Search API** | 8001 | OpenSearch integration | `services/search-api/Dockerfile` |
| **Graph API** | 8612 | Neo4j graph operations | `services/graph-api/Dockerfile` |
| **Doc Entities** | 8613 | NLP entity extraction | `services/doc-entities/Dockerfile` |
| **Egress Gateway** | 8615 | Secure external requests | `services/egress-gateway/Dockerfile` |

### Infrastructure Services (Docker Hub Images)

| Service | Port | Image | Purpose |
|---------|------|-------|---------|
| **PostgreSQL** | 5432 | `postgres:16-alpine` | Primary database |
| **Neo4j** | 7474/7687 | `neo4j:5.15` | Graph database |
| **OpenSearch** | 9200/9600 | `opensearchproject/opensearch:2.11.1` | Search engine |
| **Redis** | 6379 | `redis:7.2-alpine` | Caching layer |
| **Apache NiFi** | 8619 | `apache/nifi:2.0.0` | Data pipeline orchestration |
| **n8n** | 5678 | `n8nio/n8n:1.58.2` | Workflow automation |

## 🔧 Service Details

### Verification Service

Advanced data verification and validation engine with ML capabilities.

**Features:**
- Entity extraction and validation
- Data quality scoring
- Integration with NiFi pipelines
- REST API for verification requests

**Configuration:**
```yaml
environment:
  - VERIFICATION_SERVICE_PORT=8617
  - POSTGRES_URL=postgresql://...
  - OPENSEARCH_URL=http://opensearch:9200
  - CACHE_ENABLED=true
```

### Ops Controller

Central operations controller for service orchestration and security management.

**Features:**
- Docker container management
- Security session management (incognito mode)
- Service health monitoring
- Integration with NiFi and n8n

**Security Features:**
- Isolated containers for sensitive operations
- Auto-wipe functionality
- Memory-only mode
- Secure data overwriting

### Frontend

Modern React/Next.js application with comprehensive OSINT tools.

**Features:**
- Responsive dashboard
- Graph visualization
- Data pipeline management
- Real-time verification status
- Mobile-optimized interface

## 🐳 Docker Compose Configurations

### Full Verification Stack

`docker-compose.verification.yml` - Complete production-ready stack with all services and tools.

**Use for:**
- Production deployments
- Full feature testing
- Data pipeline development
- Complete OSINT workflow

### Core Services Only

`docker-compose.yml` - Essential services for basic functionality.

**Use for:**
- Development
- Testing individual components
- Resource-constrained environments
- Minimal deployments

### Gateway Configuration

`docker-compose.gateway.yml` - API gateway and security layer.

**Use for:**
- Production traffic management
- Authentication integration
- Rate limiting
- Security policies

## 🔍 Troubleshooting

### Common Issues

**1. Build Failures**

```bash
# Verify all Dockerfiles exist
bash docker-build-verification.sh

# Clean Docker cache
docker system prune -a

# Rebuild specific service
docker-compose -f docker-compose.verification.yml build --no-cache <service-name>
```

**2. Port Conflicts**

```bash
# Check port usage
netstat -tulpn | grep <port>

# Modify .env file to use different ports
IT_PORT_FRONTEND=3001
IT_PORT_VERIFICATION=8618
```

**3. Memory Issues**

```bash
# Increase Docker memory limit (Docker Desktop)
# Recommended: 8GB minimum, 16GB optimal

# Check memory usage
docker stats

# Reduce services if needed
docker-compose -f docker-compose.yml up -d  # Core services only
```

**4. Volume Permission Issues**

```bash
# Fix volume permissions
sudo chown -R $USER:$USER ./data

# Or use Docker volume management
docker volume prune
docker-compose down -v  # Remove volumes
docker-compose up -d    # Recreate
```

### Service Health Checks

All services include health checks. Monitor status:

```bash
# Check health status
docker-compose ps

# View service logs
docker-compose logs <service-name>

# Follow logs in real-time
docker-compose logs -f <service-name>
```

### Performance Tuning

**PostgreSQL:**
```yaml
environment:
  - POSTGRES_SHARED_BUFFERS=256MB
  - POSTGRES_EFFECTIVE_CACHE_SIZE=1GB
```

**Neo4j:**
```yaml
environment:
  - NEO4J_dbms_memory_heap_max__size=2G
  - NEO4J_dbms_memory_pagecache_size=1G
```

**OpenSearch:**
```yaml
environment:
  - "OPENSEARCH_JAVA_OPTS=-Xms2g -Xmx2g"
```

## 🚀 Deployment Scenarios

### Development Environment

```bash
# Start core services for development
docker-compose up -d postgres neo4j opensearch redis
```

### Testing Environment  

```bash
# Full stack with verification
docker-compose -f docker-compose.verification.yml up -d
```

### Production Environment

```bash
# Use external managed databases, minimal containers
docker-compose -f docker-compose.production.yml up -d
```

## 📋 Maintenance

### Regular Maintenance Tasks

```bash
# Update images
docker-compose pull
docker-compose up -d

# Backup data
docker run --rm -v infoterminal-postgres-data:/data -v $(pwd):/backup alpine tar czf /backup/postgres-backup.tar.gz /data

# Clean up old containers and images
docker system prune -a

# View resource usage
docker stats
```

### Monitoring

Monitor service health via:

- **Logs**: `docker-compose logs -f`
- **Health endpoints**: `curl http://localhost:<port>/health`
- **Service dashboards**: Access via web interfaces
- **System resources**: `docker stats`

## 🔐 Security Considerations

### Production Security

1. **Change default passwords** in `.env`
2. **Use Docker secrets** for sensitive data
3. **Enable TLS** for external access  
4. **Restrict network access** via firewall
5. **Regular security updates**

### Network Security

```yaml
# Use custom networks for isolation
networks:
  frontend:
  backend:
  database:
```

### Data Security

- All data stored in named Docker volumes
- Database encryption at rest
- TLS for service communication
- Audit logging enabled

---

## 📞 Support

For issues and questions:
1. Check this documentation
2. Run `docker-build-verification.sh` for diagnostics
3. Review service logs: `docker-compose logs <service>`
4. Check the project's issue tracker

**Version**: InfoTerminal v0.2.0  
**Last Updated**: September 2025
