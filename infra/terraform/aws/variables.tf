# Variables for InfoTerminal AWS Infrastructure

variable "aws_region" {
  description = "AWS region where resources will be created"
  type        = string
  default     = "us-west-2"
}

variable "environment" {
  description = "Environment name (production, staging, development)"
  type        = string
  default     = "production"

  validation {
    condition     = contains(["production", "staging", "development"], var.environment)
    error_message = "Environment must be one of: production, staging, development."
  }
}

variable "owner" {
  description = "Owner of the infrastructure resources"
  type        = string
  default     = "InfoTerminal Team"
}

variable "git_repository" {
  description = "Git repository URL"
  type        = string
  default     = "https://github.com/161sam/InfoTerminal"
}

variable "domain_name" {
  description = "Primary domain name for the application"
  type        = string
  default     = "infoterminal.example.com"
}

# Network Configuration
variable "vpc_cidr" {
  description = "CIDR block for VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "allowed_cidr_blocks" {
  description = "CIDR blocks allowed to access the EKS cluster endpoint"
  type        = list(string)
  default     = ["0.0.0.0/0"]
}

# Kubernetes Configuration
variable "kubernetes_version" {
  description = "Kubernetes version for EKS cluster"
  type        = string
  default     = "1.27"
}

variable "aws_auth_users" {
  description = "List of additional AWS users to add to aws-auth ConfigMap"
  type = list(object({
    userarn  = string
    username = string
    groups   = list(string)
  }))
  default = []
}

# Database Configuration
variable "postgres_instance_class" {
  description = "RDS PostgreSQL instance class"
  type        = string
  default     = "db.r6g.large"

  validation {
    condition = contains([
      "db.t3.micro", "db.t3.small", "db.t3.medium", "db.t3.large",
      "db.r6g.large", "db.r6g.xlarge", "db.r6g.2xlarge", "db.r6g.4xlarge"
    ], var.postgres_instance_class)
    error_message = "PostgreSQL instance class must be a valid RDS instance type."
  }
}

variable "postgres_storage_size" {
  description = "RDS PostgreSQL allocated storage in GB"
  type        = number
  default     = 100

  validation {
    condition     = var.postgres_storage_size >= 20 && var.postgres_storage_size <= 65536
    error_message = "PostgreSQL storage size must be between 20 and 65536 GB."
  }
}

variable "postgres_backup_retention" {
  description = "PostgreSQL backup retention period in days"
  type        = number
  default     = 30

  validation {
    condition     = var.postgres_backup_retention >= 0 && var.postgres_backup_retention <= 35
    error_message = "PostgreSQL backup retention must be between 0 and 35 days."
  }
}

# Redis Configuration
variable "redis_node_type" {
  description = "ElastiCache Redis node type"
  type        = string
  default     = "cache.r6g.large"

  validation {
    condition = contains([
      "cache.t3.micro", "cache.t3.small", "cache.t3.medium",
      "cache.r6g.large", "cache.r6g.xlarge", "cache.r6g.2xlarge"
    ], var.redis_node_type)
    error_message = "Redis node type must be a valid ElastiCache instance type."
  }
}

variable "redis_num_cache_clusters" {
  description = "Number of cache clusters in the Redis replication group"
  type        = number
  default     = 2

  validation {
    condition     = var.redis_num_cache_clusters >= 2 && var.redis_num_cache_clusters <= 6
    error_message = "Redis cluster count must be between 2 and 6."
  }
}

# OpenSearch Configuration
variable "opensearch_instance_type" {
  description = "OpenSearch instance type"
  type        = string
  default     = "t3.medium.search"
}

variable "opensearch_instance_count" {
  description = "Number of OpenSearch instances"
  type        = number
  default     = 3

  validation {
    condition     = var.opensearch_instance_count >= 1 && var.opensearch_instance_count <= 20
    error_message = "OpenSearch instance count must be between 1 and 20."
  }
}

variable "opensearch_storage_size" {
  description = "OpenSearch EBS volume size in GB"
  type        = number
  default     = 100

  validation {
    condition     = var.opensearch_storage_size >= 10 && var.opensearch_storage_size <= 1500
    error_message = "OpenSearch storage size must be between 10 and 1500 GB."
  }
}

variable "opensearch_dedicated_master" {
  description = "Whether to use dedicated master nodes for OpenSearch"
  type        = bool
  default     = true
}

# Node Group Configuration
variable "node_groups" {
  description = "Configuration for EKS managed node groups"
  type = map(object({
    instance_types = list(string)
    capacity_type  = string
    min_size      = number
    max_size      = number
    desired_size  = number
    labels        = map(string)
    taints = map(object({
      key    = string
      value  = string
      effect = string
    }))
  }))
  default = {
    system = {
      instance_types = ["t3.medium"]
      capacity_type  = "ON_DEMAND"
      min_size      = 1
      max_size      = 3
      desired_size  = 2
      labels = {
        "node-role.kubernetes.io/system" = "true"
      }
      taints = {
        system = {
          key    = "node-role.kubernetes.io/system"
          value  = "true"
          effect = "NO_SCHEDULE"
        }
      }
    }
    application = {
      instance_types = ["m5.large", "m5a.large"]
      capacity_type  = "ON_DEMAND"
      min_size      = 2
      max_size      = 10
      desired_size  = 3
      labels = {
        "node-role.kubernetes.io/application" = "true"
      }
      taints = {}
    }
    data_processing = {
      instance_types = ["c5.xlarge", "c5a.xlarge"]
      capacity_type  = "SPOT"
      min_size      = 0
      max_size      = 20
      desired_size  = 2
      labels = {
        "node-role.kubernetes.io/processing" = "true"
      }
      taints = {
        processing = {
          key    = "node-role.kubernetes.io/processing"
          value  = "true"
          effect = "NO_SCHEDULE"
        }
      }
    }
  }
}

# Monitoring and Logging Configuration
variable "enable_cloudwatch_logging" {
  description = "Enable CloudWatch logging for various services"
  type        = bool
  default     = true
}

variable "log_retention_days" {
  description = "CloudWatch log retention in days"
  type        = number
  default     = 30

  validation {
    condition = contains([
      1, 3, 5, 7, 14, 30, 60, 90, 120, 150, 180, 365, 400, 545, 731, 1827, 3653
    ], var.log_retention_days)
    error_message = "Log retention days must be a valid CloudWatch retention period."
  }
}

variable "enable_performance_insights" {
  description = "Enable Performance Insights for RDS"
  type        = bool
  default     = true
}

variable "enable_enhanced_monitoring" {
  description = "Enable Enhanced Monitoring for RDS"
  type        = bool
  default     = true
}

# Security Configuration
variable "enable_deletion_protection" {
  description = "Enable deletion protection for critical resources"
  type        = bool
  default     = true
}

variable "enable_encryption" {
  description = "Enable encryption at rest for databases and storage"
  type        = bool
  default     = true
}

variable "enable_waf" {
  description = "Enable AWS WAF for Application Load Balancer"
  type        = bool
  default     = true
}

variable "waf_rate_limit" {
  description = "WAF rate limit per 5 minutes"
  type        = number
  default     = 2000

  validation {
    condition     = var.waf_rate_limit >= 100 && var.waf_rate_limit <= 20000000
    error_message = "WAF rate limit must be between 100 and 20,000,000."
  }
}

# Backup Configuration
variable "enable_automated_backups" {
  description = "Enable automated backups for databases"
  type        = bool
  default     = true
}

variable "backup_retention_period" {
  description = "Backup retention period in days"
  type        = number
  default     = 30
}

variable "backup_window" {
  description = "Daily backup window (UTC)"
  type        = string
  default     = "03:00-06:00"
}

variable "maintenance_window" {
  description = "Weekly maintenance window (UTC)"
  type        = string
  default     = "Mon:00:00-Mon:03:00"
}

# Cost Optimization
variable "enable_spot_instances" {
  description = "Enable spot instances for non-critical workloads"
  type        = bool
  default     = true
}

variable "enable_scheduled_scaling" {
  description = "Enable scheduled auto scaling for predictable workloads"
  type        = bool
  default     = false
}

# Feature Flags
variable "enable_multi_az" {
  description = "Enable Multi-AZ deployment for databases"
  type        = bool
  default     = true
}

variable "enable_cross_region_replication" {
  description = "Enable cross-region replication for disaster recovery"
  type        = bool
  default     = false
}

variable "enable_vpc_flow_logs" {
  description = "Enable VPC flow logs"
  type        = bool
  default     = true
}

# Application Configuration
variable "application_config" {
  description = "Application-specific configuration"
  type = object({
    max_concurrent_analyses = number
    data_retention_days     = number
    api_rate_limit         = number
    websocket_connections  = number
  })
  default = {
    max_concurrent_analyses = 50
    data_retention_days     = 365
    api_rate_limit         = 1000
    websocket_connections  = 10000
  }
}

# External Integration Configuration
variable "external_integrations" {
  description = "Configuration for external service integrations"
  type = object({
    enable_github_integration    = bool
    enable_slack_notifications = bool
    enable_email_alerts         = bool
    webhook_endpoints          = list(string)
  })
  default = {
    enable_github_integration    = true
    enable_slack_notifications = true
    enable_email_alerts         = true
    webhook_endpoints          = []
  }
}

# Disaster Recovery Configuration
variable "disaster_recovery" {
  description = "Disaster recovery configuration"
  type = object({
    enable_cross_region_backup = bool
    backup_region             = string
    rpo_hours                 = number
    rto_hours                 = number
  })
  default = {
    enable_cross_region_backup = true
    backup_region             = "us-east-1"
    rpo_hours                 = 4
    rto_hours                 = 2
  }
}

# Compliance Configuration
variable "compliance" {
  description = "Compliance and audit configuration"
  type = object({
    enable_config_rules        = bool
    enable_cloudtrail         = bool
    enable_guardduty          = bool
    enable_security_hub       = bool
    data_classification_tags  = list(string)
  })
  default = {
    enable_config_rules        = true
    enable_cloudtrail         = true
    enable_guardduty          = true
    enable_security_hub       = true
    data_classification_tags  = ["public", "internal", "confidential", "restricted"]
  }
}

# Development and Testing
variable "enable_development_features" {
  description = "Enable features useful for development and testing"
  type        = bool
  default     = false
}

variable "development_config" {
  description = "Development-specific configuration"
  type = object({
    enable_ssh_access          = bool
    enable_debug_logging       = bool
    reduced_resource_limits    = bool
    mock_external_services     = bool
  })
  default = {
    enable_ssh_access          = false
    enable_debug_logging       = false
    reduced_resource_limits    = false
    mock_external_services     = false
  }
}
