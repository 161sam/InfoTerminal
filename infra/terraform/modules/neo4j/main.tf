# Neo4j Module for InfoTerminal
# Optimized for OSINT graph analysis workloads

terraform {
  required_version = ">= 1.5.0"
  
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.5"
    }
  }
}

# Data sources
data "aws_availability_zones" "available" {
  state = "available"
}

# Random password for Neo4j
resource "random_password" "neo4j_password" {
  length  = 32
  special = true
}

# Security group for Neo4j
resource "aws_security_group" "neo4j" {
  name_prefix = "${var.name}-neo4j"
  vpc_id      = var.vpc_id
  description = "Security group for Neo4j database"

  # Bolt protocol
  ingress {
    from_port   = 7687
    to_port     = 7687
    protocol    = "tcp"
    cidr_blocks = var.allowed_cidr_blocks
    description = "Neo4j Bolt protocol"
  }

  # HTTP
  ingress {
    from_port   = 7474
    to_port     = 7474
    protocol    = "tcp"
    cidr_blocks = var.allowed_cidr_blocks
    description = "Neo4j HTTP"
  }

  # HTTPS
  ingress {
    from_port   = 7473
    to_port     = 7473
    protocol    = "tcp"
    cidr_blocks = var.allowed_cidr_blocks
    description = "Neo4j HTTPS"
  }

  # Cluster communication
  dynamic "ingress" {
    for_each = var.cluster_mode ? [1] : []
    content {
      from_port   = 5000
      to_port     = 5999
      protocol    = "tcp"
      cidr_blocks = var.allowed_cidr_blocks
      description = "Neo4j cluster communication"
    }
  }

  # Backup port
  dynamic "ingress" {
    for_each = var.enable_backup_port ? [1] : []
    content {
      from_port   = 6362
      to_port     = 6362
      protocol    = "tcp"
      cidr_blocks = var.allowed_cidr_blocks
      description = "Neo4j backup port"
    }
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
    description = "All outbound traffic"
  }

  tags = merge(var.tags, {
    Name = "${var.name}-neo4j-sg"
    Component = "neo4j"
  })
}

# IAM role for Neo4j instances
resource "aws_iam_role" "neo4j" {
  name = "${var.name}-neo4j-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      }
    ]
  })

  tags = var.tags
}

# IAM policy for Neo4j instances
resource "aws_iam_policy" "neo4j" {
  name_prefix = "${var.name}-neo4j-policy"
  description = "Policy for Neo4j instances"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:DeleteObject",
          "s3:ListBucket"
        ]
        Resource = [
          aws_s3_bucket.neo4j_backups.arn,
          "${aws_s3_bucket.neo4j_backups.arn}/*"
        ]
      },
      {
        Effect = "Allow"
        Action = [
          "ec2:DescribeInstances",
          "ec2:DescribeInstanceAttribute",
          "ec2:DescribeInstanceStatus",
          "ec2:DescribeVolumes",
          "ec2:DescribeVolumeStatus",
          "ec2:CreateSnapshot",
          "ec2:DescribeSnapshots",
          "ec2:CreateTags"
        ]
        Resource = "*"
      },
      {
        Effect = "Allow"
        Action = [
          "cloudwatch:PutMetricData",
          "logs:PutLogEvents",
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:DescribeLogStreams"
        ]
        Resource = "*"
      },
      {
        Effect = "Allow"
        Action = [
          "secretsmanager:GetSecretValue"
        ]
        Resource = aws_secretsmanager_secret.neo4j_credentials.arn
      }
    ]
  })

  tags = var.tags
}

resource "aws_iam_role_policy_attachment" "neo4j" {
  role       = aws_iam_role.neo4j.name
  policy_arn = aws_iam_policy.neo4j.arn
}

resource "aws_iam_instance_profile" "neo4j" {
  name = "${var.name}-neo4j-profile"
  role = aws_iam_role.neo4j.name

  tags = var.tags
}

# S3 bucket for Neo4j backups
resource "aws_s3_bucket" "neo4j_backups" {
  bucket = "${var.name}-neo4j-backups-${random_id.bucket_suffix.hex}"

  tags = merge(var.tags, {
    Purpose = "neo4j-backups"
  })
}

resource "random_id" "bucket_suffix" {
  byte_length = 4
}

resource "aws_s3_bucket_versioning" "neo4j_backups" {
  bucket = aws_s3_bucket.neo4j_backups.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_encryption" "neo4j_backups" {
  bucket = aws_s3_bucket.neo4j_backups.id

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "neo4j_backups" {
  bucket = aws_s3_bucket.neo4j_backups.id

  rule {
    id     = "backup_lifecycle"
    status = "Enabled"

    expiration {
      days = var.backup_retention_days
    }

    noncurrent_version_expiration {
      noncurrent_days = 30
    }
  }
}

resource "aws_s3_bucket_public_access_block" "neo4j_backups" {
  bucket = aws_s3_bucket.neo4j_backups.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# Secrets Manager for Neo4j credentials
resource "aws_secretsmanager_secret" "neo4j_credentials" {
  name_prefix = "${var.name}-neo4j-credentials"
  description = "Neo4j database credentials"

  tags = var.tags
}

resource "aws_secretsmanager_secret_version" "neo4j_credentials" {
  secret_id = aws_secretsmanager_secret.neo4j_credentials.id
  secret_string = jsonencode({
    username = "neo4j"
    password = random_password.neo4j_password.result
  })
}

# Launch template for Neo4j instances
resource "aws_launch_template" "neo4j" {
  name_prefix   = "${var.name}-neo4j"
  image_id      = data.aws_ami.neo4j.id
  instance_type = var.instance_type

  vpc_security_group_ids = [aws_security_group.neo4j.id]
  
  iam_instance_profile {
    name = aws_iam_instance_profile.neo4j.name
  }

  user_data = base64encode(templatefile("${path.module}/user_data.sh", {
    neo4j_password           = random_password.neo4j_password.result
    heap_size               = var.heap_size
    pagecache_size          = var.pagecache_size
    cluster_mode            = var.cluster_mode
    cluster_name            = var.cluster_name
    backup_bucket           = aws_s3_bucket.neo4j_backups.bucket
    cloudwatch_log_group    = aws_cloudwatch_log_group.neo4j.name
    apoc_enabled            = var.enable_apoc
    gds_enabled            = var.enable_gds
    custom_plugins         = jsonencode(var.custom_plugins)
    bolt_ssl_enabled       = var.enable_ssl
    https_ssl_enabled      = var.enable_ssl
    metrics_enabled        = var.enable_metrics
    region                 = data.aws_region.current.name
  }))

  block_device_mappings {
    device_name = "/dev/sda1"
    ebs {
      volume_type           = "gp3"
      volume_size           = var.root_volume_size
      encrypted            = true
      delete_on_termination = true
    }
  }

  block_device_mappings {
    device_name = "/dev/xvdb"
    ebs {
      volume_type           = "gp3"
      volume_size           = var.data_volume_size
      iops                 = var.data_volume_iops
      throughput           = var.data_volume_throughput
      encrypted            = true
      delete_on_termination = false
    }
  }

  monitoring {
    enabled = true
  }

  tag_specifications {
    resource_type = "instance"
    tags = merge(var.tags, {
      Name = "${var.name}-neo4j"
      Component = "neo4j"
    })
  }

  tag_specifications {
    resource_type = "volume"
    tags = merge(var.tags, {
      Name = "${var.name}-neo4j-volume"
      Component = "neo4j"
    })
  }

  tags = var.tags
}

# Auto Scaling Group for Neo4j
resource "aws_autoscaling_group" "neo4j" {
  name                = "${var.name}-neo4j-asg"
  vpc_zone_identifier = var.subnet_ids
  target_group_arns   = [aws_lb_target_group.neo4j_http.arn, aws_lb_target_group.neo4j_bolt.arn]
  health_check_type   = "ELB"
  health_check_grace_period = 300

  min_size         = var.cluster_mode ? 3 : 1
  max_size         = var.cluster_mode ? var.max_cluster_size : 1
  desired_capacity = var.cluster_mode ? 3 : 1

  launch_template {
    id      = aws_launch_template.neo4j.id
    version = "$Latest"
  }

  dynamic "tag" {
    for_each = var.tags
    content {
      key                 = tag.key
      value               = tag.value
      propagate_at_launch = true
    }
  }

  tag {
    key                 = "Name"
    value               = "${var.name}-neo4j"
    propagate_at_launch = true
  }

  lifecycle {
    create_before_destroy = true
  }
}

# Application Load Balancer for Neo4j
resource "aws_lb" "neo4j" {
  count = var.enable_load_balancer ? 1 : 0

  name               = "${var.name}-neo4j-alb"
  internal           = var.internal_load_balancer
  load_balancer_type = "application"
  security_groups    = [aws_security_group.neo4j.id]
  subnets            = var.subnet_ids

  enable_deletion_protection = var.environment == "production"

  tags = merge(var.tags, {
    Name = "${var.name}-neo4j-alb"
  })
}

# Target group for HTTP
resource "aws_lb_target_group" "neo4j_http" {
  name     = "${var.name}-neo4j-http-tg"
  port     = 7474
  protocol = "HTTP"
  vpc_id   = var.vpc_id

  health_check {
    enabled             = true
    healthy_threshold   = 2
    interval            = 30
    matcher             = "200"
    path                = "/"
    port                = "traffic-port"
    protocol            = "HTTP"
    timeout             = 5
    unhealthy_threshold = 2
  }

  tags = var.tags
}

# Target group for Bolt
resource "aws_lb_target_group" "neo4j_bolt" {
  name     = "${var.name}-neo4j-bolt-tg"
  port     = 7687
  protocol = "TCP"
  vpc_id   = var.vpc_id

  health_check {
    enabled             = true
    healthy_threshold   = 2
    interval            = 30
    port                = "7474"
    protocol            = "HTTP"
    path                = "/"
    timeout             = 5
    unhealthy_threshold = 2
  }

  tags = var.tags
}

# Listeners for the load balancer
resource "aws_lb_listener" "neo4j_http" {
  count = var.enable_load_balancer ? 1 : 0

  load_balancer_arn = aws_lb.neo4j[0].arn
  port              = "80"
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.neo4j_http.arn
  }
}

resource "aws_lb_listener" "neo4j_bolt" {
  count = var.enable_load_balancer ? 1 : 0

  load_balancer_arn = aws_lb.neo4j[0].arn
  port              = "7687"
  protocol          = "TCP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.neo4j_bolt.arn
  }
}

# CloudWatch Log Group
resource "aws_cloudwatch_log_group" "neo4j" {
  name              = "/aws/ec2/neo4j/${var.name}"
  retention_in_days = var.log_retention_days

  tags = var.tags
}

# CloudWatch Alarms
resource "aws_cloudwatch_metric_alarm" "neo4j_cpu_high" {
  alarm_name          = "${var.name}-neo4j-cpu-high"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "2"
  metric_name         = "CPUUtilization"
  namespace           = "AWS/EC2"
  period              = "300"
  statistic           = "Average"
  threshold           = "80"
  alarm_description   = "This metric monitors neo4j cpu utilization"
  alarm_actions       = [aws_sns_topic.neo4j_alerts.arn]

  dimensions = {
    AutoScalingGroupName = aws_autoscaling_group.neo4j.name
  }

  tags = var.tags
}

resource "aws_cloudwatch_metric_alarm" "neo4j_memory_high" {
  alarm_name          = "${var.name}-neo4j-memory-high"
  comparison_operator = "LessThanThreshold"
  evaluation_periods  = "2"
  metric_name         = "MemoryAvailable"
  namespace           = "CWAgent"
  period              = "300"
  statistic           = "Average"
  threshold           = "1073741824"  # 1GB in bytes
  alarm_description   = "This metric monitors neo4j available memory"
  alarm_actions       = [aws_sns_topic.neo4j_alerts.arn]

  dimensions = {
    AutoScalingGroupName = aws_autoscaling_group.neo4j.name
  }

  tags = var.tags
}

# SNS topic for alerts
resource "aws_sns_topic" "neo4j_alerts" {
  name = "${var.name}-neo4j-alerts"

  tags = var.tags
}

# Get current AWS region
data "aws_region" "current" {}

# AMI for Neo4j
data "aws_ami" "neo4j" {
  most_recent = true
  owners      = ["self", "amazon"]

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}
