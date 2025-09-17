# Outputs for InfoTerminal AWS Infrastructure

# Cluster Information
output "cluster_name" {
  description = "Name of the EKS cluster"
  value       = module.eks.cluster_name
}

output "cluster_endpoint" {
  description = "Endpoint for EKS control plane"
  value       = module.eks.cluster_endpoint
  sensitive   = true
}

output "cluster_security_group_id" {
  description = "Security group ID attached to the EKS cluster"
  value       = module.eks.cluster_security_group_id
}

output "cluster_iam_role_arn" {
  description = "IAM role ARN associated with EKS cluster"
  value       = module.eks.cluster_iam_role_arn
}

output "cluster_certificate_authority_data" {
  description = "Base64 encoded certificate data required to communicate with the cluster"
  value       = module.eks.cluster_certificate_authority_data
  sensitive   = true
}

output "cluster_primary_security_group_id" {
  description = "Cluster security group that was created by Amazon EKS for the cluster"
  value       = module.eks.cluster_primary_security_group_id
}

output "cluster_version" {
  description = "The Kubernetes version for the EKS cluster"
  value       = module.eks.cluster_version
}

# Node Groups Information
output "node_groups" {
  description = "EKS managed node groups"
  value       = module.eks.eks_managed_node_groups
  sensitive   = true
}

output "node_security_group_id" {
  description = "ID of the node shared security group"
  value       = module.eks.node_security_group_id
}

# Network Information
output "vpc_id" {
  description = "ID of the VPC"
  value       = module.vpc.vpc_id
}

output "vpc_cidr_block" {
  description = "The CIDR block of the VPC"
  value       = module.vpc.vpc_cidr_block
}

output "private_subnet_ids" {
  description = "List of IDs of private subnets"
  value       = module.vpc.private_subnets
}

output "public_subnet_ids" {
  description = "List of IDs of public subnets"
  value       = module.vpc.public_subnets
}

output "database_subnet_ids" {
  description = "List of IDs of database subnets"
  value       = module.vpc.database_subnets
}

output "database_subnet_group_name" {
  description = "Name of database subnet group"
  value       = module.vpc.database_subnet_group_name
}

# Database Information
output "postgres_endpoint" {
  description = "RDS PostgreSQL instance endpoint"
  value       = module.postgres.db_instance_endpoint
  sensitive   = true
}

output "postgres_port" {
  description = "RDS PostgreSQL instance port"
  value       = module.postgres.db_instance_port
}

output "postgres_database_name" {
  description = "RDS PostgreSQL database name"
  value       = module.postgres.db_instance_name
}

output "postgres_username" {
  description = "RDS PostgreSQL master username"
  value       = module.postgres.db_instance_username
  sensitive   = true
}

output "postgres_security_group_id" {
  description = "ID of the PostgreSQL security group"
  value       = aws_security_group.rds.id
}

# Redis Information
output "redis_primary_endpoint" {
  description = "Redis primary endpoint"
  value       = aws_elasticache_replication_group.redis.primary_endpoint_address
  sensitive   = true
}

output "redis_reader_endpoint" {
  description = "Redis reader endpoint"
  value       = aws_elasticache_replication_group.redis.reader_endpoint_address
  sensitive   = true
}

output "redis_port" {
  description = "Redis port"
  value       = aws_elasticache_replication_group.redis.port
}

output "redis_security_group_id" {
  description = "ID of the Redis security group"
  value       = aws_security_group.elasticache.id
}

# OpenSearch Information
output "opensearch_endpoint" {
  description = "OpenSearch domain endpoint"
  value       = aws_opensearch_domain.main.endpoint
  sensitive   = true
}

output "opensearch_domain_arn" {
  description = "OpenSearch domain ARN"
  value       = aws_opensearch_domain.main.arn
}

output "opensearch_domain_id" {
  description = "OpenSearch domain ID"
  value       = aws_opensearch_domain.main.domain_id
}

output "opensearch_kibana_endpoint" {
  description = "OpenSearch Kibana endpoint"
  value       = aws_opensearch_domain.main.kibana_endpoint
  sensitive   = true
}

# Load Balancer Information
output "alb_dns_name" {
  description = "DNS name of the load balancer"
  value       = module.alb.lb_dns_name
}

output "alb_zone_id" {
  description = "Zone ID of the load balancer"
  value       = module.alb.lb_zone_id
}

output "alb_arn" {
  description = "ARN of the load balancer"
  value       = module.alb.lb_arn
}

output "alb_security_group_id" {
  description = "ID of the ALB security group"
  value       = aws_security_group.alb.id
}

# Domain and SSL Information
output "domain_name" {
  description = "Primary domain name"
  value       = var.domain_name
}

output "certificate_arn" {
  description = "ARN of the ACM certificate"
  value       = aws_acm_certificate.main.arn
}

output "route53_zone_id" {
  description = "Route53 hosted zone ID"
  value       = aws_route53_zone.main.zone_id
}

output "route53_name_servers" {
  description = "Route53 name servers"
  value       = aws_route53_zone.main.name_servers
}

# Security Information
output "waf_web_acl_arn" {
  description = "ARN of the WAF Web ACL"
  value       = aws_wafv2_web_acl.main.arn
}

output "secrets_manager_arn" {
  description = "ARN of the Secrets Manager secret"
  value       = aws_secretsmanager_secret.database_credentials.arn
}

output "admin_role_arn" {
  description = "ARN of the InfoTerminal admin IAM role"
  value       = aws_iam_role.infoterminal_admin.arn
}

# Storage Information
output "s3_data_bucket_name" {
  description = "Name of the S3 data storage bucket"
  value       = aws_s3_bucket.data_storage.id
}

output "s3_data_bucket_arn" {
  description = "ARN of the S3 data storage bucket"
  value       = aws_s3_bucket.data_storage.arn
}

output "s3_alb_logs_bucket_name" {
  description = "Name of the S3 ALB logs bucket"
  value       = aws_s3_bucket.alb_logs.id
}

# Connection Information
output "database_connection_info" {
  description = "Database connection information for applications"
  value = {
    postgres_host        = module.postgres.db_instance_endpoint
    postgres_port        = module.postgres.db_instance_port
    postgres_database    = module.postgres.db_instance_name
    redis_host          = aws_elasticache_replication_group.redis.primary_endpoint_address
    redis_port          = aws_elasticache_replication_group.redis.port
    opensearch_endpoint = aws_opensearch_domain.main.endpoint
  }
  sensitive = true
}

# Kubernetes Configuration
output "kubeconfig" {
  description = "kubectl config as generated by the module"
  value = {
    cluster_name                      = module.eks.cluster_name
    endpoint                         = module.eks.cluster_endpoint
    certificate_authority_data       = module.eks.cluster_certificate_authority_data
    region                          = var.aws_region
  }
  sensitive = true
}

# Application URLs
output "application_urls" {
  description = "Application access URLs"
  value = {
    main_application = "https://${var.domain_name}"
    api_endpoint     = "https://api.${var.domain_name}"
    websocket_endpoint = "wss://ws.${var.domain_name}"
    alb_dns_name     = module.alb.lb_dns_name
  }
}

# Resource ARNs
output "resource_arns" {
  description = "ARNs of key resources for cross-referencing"
  value = {
    cluster_arn      = module.eks.cluster_arn
    vpc_arn          = module.vpc.vpc_arn
    postgres_arn     = module.postgres.db_instance_arn
    opensearch_arn   = aws_opensearch_domain.main.arn
    alb_arn          = module.alb.lb_arn
    certificate_arn  = aws_acm_certificate.main.arn
    secrets_arn      = aws_secretsmanager_secret.database_credentials.arn
  }
}

# Monitoring Information
output "cloudwatch_log_groups" {
  description = "CloudWatch log group names for monitoring setup"
  value = {
    opensearch_logs = aws_cloudwatch_log_group.opensearch.name
    redis_slow_logs = aws_cloudwatch_log_group.redis_slow.name
  }
}

# Environment Information
output "environment_info" {
  description = "Environment and deployment information"
  value = {
    environment      = var.environment
    aws_region      = var.aws_region
    availability_zones = local.azs
    cluster_version = var.kubernetes_version
    deployment_time = timestamp()
  }
}

# Cost Tracking Tags
output "cost_allocation_tags" {
  description = "Tags for cost allocation and tracking"
  value = local.common_tags
}

# Security Group IDs
output "security_group_ids" {
  description = "Security group IDs for network configuration"
  value = {
    cluster_sg       = module.eks.cluster_security_group_id
    node_sg         = module.eks.node_security_group_id
    additional_node_sg = aws_security_group.additional_node_group.id
    postgres_sg     = aws_security_group.rds.id
    redis_sg        = aws_security_group.elasticache.id
    opensearch_sg   = aws_security_group.opensearch.id
    alb_sg          = aws_security_group.alb.id
  }
}

# Helm Values Override
output "helm_values_override" {
  description = "Helm values to override for InfoTerminal deployment"
  value = {
    global = {
      environment = var.environment
      aws_region  = var.aws_region
    }
    
    postgresql = {
      enabled = false
      external = {
        host     = module.postgres.db_instance_endpoint
        port     = module.postgres.db_instance_port
        database = module.postgres.db_instance_name
        username = module.postgres.db_instance_username
      }
    }
    
    redis = {
      enabled = false
      external = {
        host = aws_elasticache_replication_group.redis.primary_endpoint_address
        port = aws_elasticache_replication_group.redis.port
      }
    }
    
    opensearch = {
      enabled = false
      external = {
        endpoint = aws_opensearch_domain.main.endpoint
      }
    }
    
    ingress = {
      hosts = [
        {
          host = var.domain_name
          paths = [
            {
              path = "/"
              pathType = "Prefix"
              service = "frontend"
            }
          ]
        },
        {
          host = "api.${var.domain_name}"
          paths = [
            {
              path = "/"
              pathType = "Prefix"
              service = "gateway"
            }
          ]
        },
        {
          host = "ws.${var.domain_name}"
          paths = [
            {
              path = "/ws"
              pathType = "Prefix"
              service = "websocket-manager"
            }
          ]
        }
      ]
      
      tls = [
        {
          secretName = "infoterminal-tls"
          hosts = [
            var.domain_name,
            "api.${var.domain_name}",
            "ws.${var.domain_name}"
          ]
        }
      ]
    }
    
    secrets = {
      secretsManager = {
        secretName = aws_secretsmanager_secret.database_credentials.name
        region     = var.aws_region
      }
    }
  }
  sensitive = true
}
