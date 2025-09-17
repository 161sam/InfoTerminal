# Outputs for Neo4j Module

# Instance Information
output "instance_ids" {
  description = "List of Neo4j instance IDs"
  value       = aws_autoscaling_group.neo4j.instances
}

output "security_group_id" {
  description = "ID of the Neo4j security group"
  value       = aws_security_group.neo4j.id
}

output "iam_role_arn" {
  description = "ARN of the Neo4j IAM role"
  value       = aws_iam_role.neo4j.arn
}

output "instance_profile_name" {
  description = "Name of the Neo4j instance profile"
  value       = aws_iam_instance_profile.neo4j.name
}

# Connection Information
output "bolt_endpoint" {
  description = "Neo4j Bolt protocol endpoint"
  value       = var.enable_load_balancer ? "${aws_lb.neo4j[0].dns_name}:7687" : "Use individual instance IPs on port 7687"
}

output "http_endpoint" {
  description = "Neo4j HTTP endpoint"
  value       = var.enable_load_balancer ? "http://${aws_lb.neo4j[0].dns_name}" : "Use individual instance IPs on port 7474"
}

output "https_endpoint" {
  description = "Neo4j HTTPS endpoint"
  value       = var.enable_load_balancer ? "https://${aws_lb.neo4j[0].dns_name}" : "Use individual instance IPs on port 7473"
}

output "load_balancer_dns_name" {
  description = "DNS name of the load balancer"
  value       = var.enable_load_balancer ? aws_lb.neo4j[0].dns_name : null
}

output "load_balancer_zone_id" {
  description = "Zone ID of the load balancer"
  value       = var.enable_load_balancer ? aws_lb.neo4j[0].zone_id : null
}

# Database Information
output "database_name" {
  description = "Default Neo4j database name"
  value       = "neo4j"
}

output "username" {
  description = "Neo4j username"
  value       = "neo4j"
}

output "password_secret_arn" {
  description = "ARN of the Secrets Manager secret containing Neo4j password"
  value       = aws_secretsmanager_secret.neo4j_credentials.arn
  sensitive   = true
}

# Storage Information
output "backup_bucket_name" {
  description = "Name of the S3 bucket for Neo4j backups"
  value       = aws_s3_bucket.neo4j_backups.bucket
}

output "backup_bucket_arn" {
  description = "ARN of the S3 bucket for Neo4j backups"
  value       = aws_s3_bucket.neo4j_backups.arn
}

# Monitoring Information
output "cloudwatch_log_group_name" {
  description = "Name of the CloudWatch log group for Neo4j"
  value       = aws_cloudwatch_log_group.neo4j.name
}

output "sns_topic_arn" {
  description = "ARN of the SNS topic for Neo4j alerts"
  value       = aws_sns_topic.neo4j_alerts.arn
}

# Cluster Information
output "cluster_mode" {
  description = "Whether Neo4j is running in cluster mode"
  value       = var.cluster_mode
}

output "cluster_name" {
  description = "Name of the Neo4j cluster"
  value       = var.cluster_name
}

output "auto_scaling_group_name" {
  description = "Name of the Auto Scaling Group"
  value       = aws_autoscaling_group.neo4j.name
}

output "auto_scaling_group_arn" {
  description = "ARN of the Auto Scaling Group"
  value       = aws_autoscaling_group.neo4j.arn
}

# Target Group Information
output "http_target_group_arn" {
  description = "ARN of the HTTP target group"
  value       = aws_lb_target_group.neo4j_http.arn
}

output "bolt_target_group_arn" {
  description = "ARN of the Bolt target group"
  value       = aws_lb_target_group.neo4j_bolt.arn
}

# Configuration Information
output "heap_size" {
  description = "Configured heap size for Neo4j"
  value       = var.heap_size
}

output "pagecache_size" {
  description = "Configured page cache size for Neo4j"
  value       = var.pagecache_size
}

output "enabled_plugins" {
  description = "List of enabled Neo4j plugins"
  value = concat(
    var.enable_apoc ? ["apoc"] : [],
    var.enable_gds ? ["graph-data-science"] : [],
    [for plugin in var.custom_plugins : plugin.name]
  )
}

# Connection Strings
output "connection_uri" {
  description = "Neo4j connection URI for applications"
  value       = var.enable_load_balancer ? "bolt://${aws_lb.neo4j[0].dns_name}:7687" : "bolt://INSTANCE_IP:7687"
  sensitive   = true
}

output "connection_string" {
  description = "Complete connection string with authentication info"
  value       = var.enable_load_balancer ? "bolt://neo4j:PASSWORD@${aws_lb.neo4j[0].dns_name}:7687" : "bolt://neo4j:PASSWORD@INSTANCE_IP:7687"
  sensitive   = true
}

# Performance Configuration
output "performance_config" {
  description = "Performance configuration summary"
  value = {
    instance_type           = var.instance_type
    heap_size              = var.heap_size
    pagecache_size         = var.pagecache_size
    data_volume_size       = var.data_volume_size
    data_volume_iops       = var.data_volume_iops
    data_volume_throughput = var.data_volume_throughput
    transaction_timeout    = var.transaction_timeout
  }
}

# Security Configuration
output "security_config" {
  description = "Security configuration summary"
  value = {
    ssl_enabled             = var.enable_ssl
    vpc_id                 = var.vpc_id
    security_group_id      = aws_security_group.neo4j.id
    secrets_manager_arn    = aws_secretsmanager_secret.neo4j_credentials.arn
    backup_encryption      = true
    volume_encryption      = true
  }
}

# Tags
output "tags" {
  description = "Tags applied to Neo4j resources"
  value       = var.tags
}

# Environment Information
output "environment" {
  description = "Deployment environment"
  value       = var.environment
}

# Launch Template Information
output "launch_template_id" {
  description = "ID of the launch template"
  value       = aws_launch_template.neo4j.id
}

output "launch_template_version" {
  description = "Version of the launch template"
  value       = aws_launch_template.neo4j.latest_version
}

# Alarm ARNs
output "cpu_alarm_arn" {
  description = "ARN of the CPU utilization alarm"
  value       = aws_cloudwatch_metric_alarm.neo4j_cpu_high.arn
}

output "memory_alarm_arn" {
  description = "ARN of the memory utilization alarm"
  value       = aws_cloudwatch_metric_alarm.neo4j_memory_high.arn
}
