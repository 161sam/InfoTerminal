# Variables for Neo4j Module

variable "name" {
  description = "Name prefix for all resources"
  type        = string
}

variable "environment" {
  description = "Environment (production, staging, development)"
  type        = string
  default     = "production"
}

variable "vpc_id" {
  description = "VPC ID where Neo4j will be deployed"
  type        = string
}

variable "subnet_ids" {
  description = "List of subnet IDs for Neo4j deployment"
  type        = list(string)
}

variable "allowed_cidr_blocks" {
  description = "CIDR blocks allowed to access Neo4j"
  type        = list(string)
  default     = ["10.0.0.0/8"]
}

# Instance Configuration
variable "instance_type" {
  description = "EC2 instance type for Neo4j"
  type        = string
  default     = "r5.large"

  validation {
    condition = contains([
      "t3.medium", "t3.large", "t3.xlarge",
      "r5.large", "r5.xlarge", "r5.2xlarge", "r5.4xlarge",
      "r6i.large", "r6i.xlarge", "r6i.2xlarge", "r6i.4xlarge",
      "c5.large", "c5.xlarge", "c5.2xlarge", "c5.4xlarge"
    ], var.instance_type)
    error_message = "Instance type must be suitable for Neo4j workloads."
  }
}

# Storage Configuration
variable "root_volume_size" {
  description = "Root volume size in GB"
  type        = number
  default     = 50

  validation {
    condition     = var.root_volume_size >= 20 && var.root_volume_size <= 1000
    error_message = "Root volume size must be between 20 and 1000 GB."
  }
}

variable "data_volume_size" {
  description = "Data volume size in GB"
  type        = number
  default     = 500

  validation {
    condition     = var.data_volume_size >= 100 && var.data_volume_size <= 16384
    error_message = "Data volume size must be between 100 and 16384 GB."
  }
}

variable "data_volume_iops" {
  description = "IOPS for data volume (gp3 only)"
  type        = number
  default     = 3000

  validation {
    condition     = var.data_volume_iops >= 3000 && var.data_volume_iops <= 16000
    error_message = "Data volume IOPS must be between 3000 and 16000."
  }
}

variable "data_volume_throughput" {
  description = "Throughput for data volume in MB/s (gp3 only)"
  type        = number
  default     = 250

  validation {
    condition     = var.data_volume_throughput >= 125 && var.data_volume_throughput <= 1000
    error_message = "Data volume throughput must be between 125 and 1000 MB/s."
  }
}

# Neo4j Configuration
variable "heap_size" {
  description = "Neo4j heap size (e.g., '4G', '8G')"
  type        = string
  default     = "4G"

  validation {
    condition     = can(regex("^[0-9]+[GM]$", var.heap_size))
    error_message = "Heap size must be in format like '4G' or '8192M'."
  }
}

variable "pagecache_size" {
  description = "Neo4j page cache size (e.g., '4G', '8G')"
  type        = string
  default     = "4G"

  validation {
    condition     = can(regex("^[0-9]+[GM]$", var.pagecache_size))
    error_message = "Page cache size must be in format like '4G' or '8192M'."
  }
}

# Cluster Configuration
variable "cluster_mode" {
  description = "Enable Neo4j cluster mode (Causal Cluster)"
  type        = bool
  default     = false
}

variable "cluster_name" {
  description = "Name for the Neo4j cluster"
  type        = string
  default     = "neo4j-cluster"
}

variable "max_cluster_size" {
  description = "Maximum size of the Neo4j cluster"
  type        = number
  default     = 5

  validation {
    condition     = var.max_cluster_size >= 3 && var.max_cluster_size <= 10
    error_message = "Cluster size must be between 3 and 10 nodes."
  }
}

# Plugin Configuration
variable "enable_apoc" {
  description = "Enable APOC (Awesome Procedures on Cypher) plugin"
  type        = bool
  default     = true
}

variable "enable_gds" {
  description = "Enable Graph Data Science plugin"
  type        = bool
  default     = true
}

variable "custom_plugins" {
  description = "List of custom Neo4j plugins to install"
  type = list(object({
    name    = string
    url     = string
    version = string
  }))
  default = []
}

# Security Configuration
variable "enable_ssl" {
  description = "Enable SSL/TLS for Neo4j connections"
  type        = bool
  default     = true
}

variable "ssl_certificate_arn" {
  description = "ARN of ACM certificate for SSL/TLS"
  type        = string
  default     = ""
}

# Monitoring and Logging
variable "enable_metrics" {
  description = "Enable Neo4j metrics collection"
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

# Backup Configuration
variable "backup_retention_days" {
  description = "Backup retention period in days"
  type        = number
  default     = 30

  validation {
    condition     = var.backup_retention_days >= 7 && var.backup_retention_days <= 365
    error_message = "Backup retention must be between 7 and 365 days."
  }
}

variable "backup_schedule" {
  description = "Backup schedule in cron format"
  type        = string
  default     = "0 3 * * *"  # Daily at 3 AM
}

variable "enable_continuous_backup" {
  description = "Enable continuous backup to S3"
  type        = bool
  default     = false
}

# Load Balancer Configuration
variable "enable_load_balancer" {
  description = "Enable Application Load Balancer for Neo4j"
  type        = bool
  default     = true
}

variable "internal_load_balancer" {
  description = "Make the load balancer internal (private)"
  type        = bool
  default     = true
}

# Performance Configuration
variable "enable_backup_port" {
  description = "Enable backup port (6362) for online backups"
  type        = bool
  default     = true
}

variable "query_cache_size" {
  description = "Query cache size"
  type        = string
  default     = "1000"
}

variable "bolt_thread_pool_min_size" {
  description = "Minimum size of Bolt thread pool"
  type        = number
  default     = 5
}

variable "bolt_thread_pool_max_size" {
  description = "Maximum size of Bolt thread pool"
  type        = number
  default     = 400
}

# OSINT-specific Configuration
variable "osint_config" {
  description = "OSINT-specific Neo4j configuration"
  type = object({
    enable_fulltext_indexes     = bool
    enable_spatial_indexes      = bool
    max_concurrent_transactions = number
    query_timeout_seconds       = number
    result_cache_ttl_seconds   = number
  })
  default = {
    enable_fulltext_indexes     = true
    enable_spatial_indexes      = true
    max_concurrent_transactions = 1000
    query_timeout_seconds       = 300
    result_cache_ttl_seconds   = 600
  }
}

# Data Import Configuration
variable "enable_import_tools" {
  description = "Enable Neo4j import tools and utilities"
  type        = bool
  default     = true
}

variable "max_import_batch_size" {
  description = "Maximum batch size for data imports"
  type        = number
  default     = 10000
}

# Memory Configuration
variable "enable_memory_mapping" {
  description = "Enable memory mapping for large datasets"
  type        = bool
  default     = true
}

variable "memory_mapping_threshold" {
  description = "File size threshold for memory mapping in MB"
  type        = number
  default     = 256
}

# Network Configuration
variable "bolt_listen_address" {
  description = "Bolt protocol listen address"
  type        = string
  default     = "0.0.0.0:7687"
}

variable "http_listen_address" {
  description = "HTTP listen address"
  type        = string
  default     = "0.0.0.0:7474"
}

variable "https_listen_address" {
  description = "HTTPS listen address"
  type        = string
  default     = "0.0.0.0:7473"
}

# Transaction Configuration
variable "transaction_timeout" {
  description = "Transaction timeout in seconds"
  type        = number
  default     = 300

  validation {
    condition     = var.transaction_timeout >= 30 && var.transaction_timeout <= 3600
    error_message = "Transaction timeout must be between 30 and 3600 seconds."
  }
}

variable "lock_acquisition_timeout" {
  description = "Lock acquisition timeout in seconds"
  type        = number
  default     = 60
}

# Logging Configuration
variable "enable_query_logging" {
  description = "Enable query logging for performance analysis"
  type        = bool
  default     = true
}

variable "slow_query_threshold_ms" {
  description = "Threshold for logging slow queries in milliseconds"
  type        = number
  default     = 1000
}

variable "enable_gc_logging" {
  description = "Enable JVM garbage collection logging"
  type        = bool
  default     = true
}

# High Availability Configuration
variable "enable_read_replicas" {
  description = "Enable read replica instances"
  type        = bool
  default     = false
}

variable "read_replica_count" {
  description = "Number of read replica instances"
  type        = number
  default     = 2

  validation {
    condition     = var.read_replica_count >= 1 && var.read_replica_count <= 5
    error_message = "Read replica count must be between 1 and 5."
  }
}

# Alerting Configuration
variable "enable_alerting" {
  description = "Enable CloudWatch alerting for Neo4j"
  type        = bool
  default     = true
}

variable "alert_email_addresses" {
  description = "Email addresses for alerts"
  type        = list(string)
  default     = []
}

variable "cpu_alarm_threshold" {
  description = "CPU utilization threshold for alarms (percentage)"
  type        = number
  default     = 80

  validation {
    condition     = var.cpu_alarm_threshold >= 50 && var.cpu_alarm_threshold <= 95
    error_message = "CPU alarm threshold must be between 50 and 95 percent."
  }
}

variable "memory_alarm_threshold" {
  description = "Available memory threshold for alarms in GB"
  type        = number
  default     = 1

  validation {
    condition     = var.memory_alarm_threshold >= 0.5 && var.memory_alarm_threshold <= 10
    error_message = "Memory alarm threshold must be between 0.5 and 10 GB."
  }
}

# Tags
variable "tags" {
  description = "Tags to apply to all resources"
  type        = map(string)
  default     = {}
}

# Development Configuration
variable "enable_debug_mode" {
  description = "Enable debug mode for development"
  type        = bool
  default     = false
}

variable "enable_jmx" {
  description = "Enable JMX monitoring"
  type        = bool
  default     = false
}
