#!/bin/bash

# Neo4j Instance Initialization Script for InfoTerminal OSINT Platform
# Optimized for Ubuntu 20.04 LTS

set -euo pipefail

# Variables from Terraform
NEO4J_PASSWORD="${neo4j_password}"
HEAP_SIZE="${heap_size}"
PAGECACHE_SIZE="${pagecache_size}"
CLUSTER_MODE="${cluster_mode}"
CLUSTER_NAME="${cluster_name}"
BACKUP_BUCKET="${backup_bucket}"
CLOUDWATCH_LOG_GROUP="${cloudwatch_log_group}"
APOC_ENABLED="${apoc_enabled}"
GDS_ENABLED="${gds_enabled}"
CUSTOM_PLUGINS='${custom_plugins}'
BOLT_SSL_ENABLED="${bolt_ssl_enabled}"
HTTPS_SSL_ENABLED="${https_ssl_enabled}"
METRICS_ENABLED="${metrics_enabled}"
REGION="${region}"

# System configuration
export DEBIAN_FRONTEND=noninteractive
INSTANCE_ID=$(curl -s http://169.254.169.254/latest/meta-data/instance-id)
INSTANCE_IP=$(curl -s http://169.254.169.254/latest/meta-data/local-ipv4)
AZ=$(curl -s http://169.254.169.254/latest/meta-data/placement/availability-zone)

# Logging setup
LOG_FILE="/var/log/neo4j-init.log"
exec > >(tee -a $LOG_FILE)
exec 2>&1

echo "Starting Neo4j initialization at $(date)"
echo "Instance ID: $INSTANCE_ID"
echo "Instance IP: $INSTANCE_IP"
echo "Availability Zone: $AZ"

# Install required packages
echo "Updating system packages..."
apt-get update
apt-get install -y \
    openjdk-11-jdk \
    wget \
    curl \
    gnupg \
    software-properties-common \
    awscli \
    jq \
    htop \
    iotop \
    unzip \
    cloudwatch-logs-agent \
    amazon-cloudwatch-agent

# Set JAVA_HOME
export JAVA_HOME="/usr/lib/jvm/java-11-openjdk-amd64"
echo 'export JAVA_HOME="/usr/lib/jvm/java-11-openjdk-amd64"' >> /etc/environment

# Add Neo4j repository
echo "Adding Neo4j repository..."
wget -O - https://debian.neo4j.com/neotechnology.gpg.key | apt-key add -
echo 'deb https://debian.neo4j.com stable latest' | tee -a /etc/apt/sources.list.d/neo4j.list
apt-get update

# Install Neo4j Community Edition
echo "Installing Neo4j..."
apt-get install -y neo4j=1:5.13.0

# Configure data volume
echo "Configuring data volume..."
if [ ! -b "/dev/xvdb" ]; then
    echo "Waiting for data volume to be attached..."
    sleep 10
fi

# Format and mount data volume if not already done
if ! blkid /dev/xvdb; then
    echo "Formatting data volume..."
    mkfs.ext4 /dev/xvdb
fi

mkdir -p /var/lib/neo4j-data
mount /dev/xvdb /var/lib/neo4j-data

# Add to fstab for persistent mounting
DEVICE_UUID=$(blkid -s UUID -o value /dev/xvdb)
echo "UUID=$DEVICE_UUID /var/lib/neo4j-data ext4 defaults,nofail 0 2" >> /etc/fstab

# Set up directory structure
mkdir -p /var/lib/neo4j-data/{databases,transactions,certificates,import,logs,plugins,backups}
chown -R neo4j:neo4j /var/lib/neo4j-data

# Create symbolic links
rm -rf /var/lib/neo4j/data
ln -s /var/lib/neo4j-data /var/lib/neo4j/data

# Configure Neo4j
echo "Configuring Neo4j..."
NEO4J_CONF="/etc/neo4j/neo4j.conf"

# Backup original config
cp $NEO4J_CONF $NEO4J_CONF.backup

# Basic configuration
cat > $NEO4J_CONF << EOF
# Neo4j Configuration for InfoTerminal OSINT Platform
# Generated automatically - do not edit manually

# Database location
server.directories.data=/var/lib/neo4j-data
server.directories.logs=/var/lib/neo4j-data/logs
server.directories.import=/var/lib/neo4j-data/import
server.directories.plugins=/var/lib/neo4j/plugins

# Memory configuration
server.memory.heap.initial_size=$HEAP_SIZE
server.memory.heap.max_size=$HEAP_SIZE
server.memory.pagecache.size=$PAGECACHE_SIZE

# Network configuration
server.default_listen_address=0.0.0.0
server.bolt.listen_address=0.0.0.0:7687
server.http.listen_address=0.0.0.0:7474
server.https.listen_address=0.0.0.0:7473

# Enable remote connections
server.bolt.advertised_address=$INSTANCE_IP:7687
server.http.advertised_address=$INSTANCE_IP:7474

# Transaction configuration
db.transaction.timeout=300s
db.lock.acquisition.timeout=60s
db.transaction.concurrent.maximum=1000

# Query configuration
db.query_cache_size=1000
db.logs.query.enabled=true
db.logs.query.threshold=1000ms

# Performance tuning for OSINT workloads
dbms.memory.transaction.global_max_size=1g
dbms.memory.transaction.max_size=10m

# Enable query logging
dbms.logs.query.enabled=true
dbms.logs.query.threshold=1000ms
dbms.logs.query.parameter_logging_enabled=true

# Enable metrics
metrics.enabled=true
metrics.csv.enabled=true
metrics.csv.interval=30s
metrics.graphite.enabled=false
metrics.jmx.enabled=true

# Security configuration
dbms.security.auth_enabled=true
dbms.security.procedures.unrestricted=apoc.*,gds.*
dbms.security.procedures.allowlist=apoc.*,gds.*

# SSL Configuration
EOF

# Configure SSL if enabled
if [ "$BOLT_SSL_ENABLED" = "true" ] || [ "$HTTPS_SSL_ENABLED" = "true" ]; then
    echo "Configuring SSL certificates..."
    mkdir -p /var/lib/neo4j/certificates/bolt /var/lib/neo4j/certificates/https
    
    # Generate self-signed certificates (replace with proper certs in production)
    openssl req -newkey rsa:2048 -nodes -keyout /var/lib/neo4j/certificates/bolt/private.key \
        -x509 -days 365 -out /var/lib/neo4j/certificates/bolt/public.crt \
        -subj "/C=US/ST=State/L=City/O=InfoTerminal/OU=OSINT/CN=$INSTANCE_IP"
    
    cp /var/lib/neo4j/certificates/bolt/* /var/lib/neo4j/certificates/https/
    
    chown -R neo4j:neo4j /var/lib/neo4j/certificates
    
    if [ "$BOLT_SSL_ENABLED" = "true" ]; then
        cat >> $NEO4J_CONF << EOF

# Bolt SSL Configuration
server.bolt.tls_level=REQUIRED
dbms.ssl.policy.bolt.enabled=true
dbms.ssl.policy.bolt.base_directory=/var/lib/neo4j/certificates/bolt
dbms.ssl.policy.bolt.private_key=private.key
dbms.ssl.policy.bolt.public_certificate=public.crt
EOF
    fi
    
    if [ "$HTTPS_SSL_ENABLED" = "true" ]; then
        cat >> $NEO4J_CONF << EOF

# HTTPS SSL Configuration
dbms.ssl.policy.https.enabled=true
dbms.ssl.policy.https.base_directory=/var/lib/neo4j/certificates/https
dbms.ssl.policy.https.private_key=private.key
dbms.ssl.policy.https.public_certificate=public.crt
EOF
    fi
fi

# Configure clustering if enabled
if [ "$CLUSTER_MODE" = "true" ]; then
    echo "Configuring cluster mode..."
    
    # Get cluster member IPs from Auto Scaling Group
    ASG_NAME=$(aws autoscaling describe-auto-scaling-instances \
        --instance-ids $INSTANCE_ID \
        --region $REGION \
        --query 'AutoScalingInstances[0].AutoScalingGroupName' \
        --output text)
    
    CLUSTER_MEMBERS=$(aws autoscaling describe-auto-scaling-groups \
        --auto-scaling-group-names $ASG_NAME \
        --region $REGION \
        --query 'AutoScalingGroups[0].Instances[?LifecycleState==`InService`].InstanceId' \
        --output text)
    
    INITIAL_DISCOVERY=""
    for instance in $CLUSTER_MEMBERS; do
        if [ "$instance" != "$INSTANCE_ID" ]; then
            MEMBER_IP=$(aws ec2 describe-instances \
                --instance-ids $instance \
                --region $REGION \
                --query 'Reservations[0].Instances[0].PrivateIpAddress' \
                --output text)
            
            if [ "$INITIAL_DISCOVERY" = "" ]; then
                INITIAL_DISCOVERY="$MEMBER_IP:5000"
            else
                INITIAL_DISCOVERY="$INITIAL_DISCOVERY,$MEMBER_IP:5000"
            fi
        fi
    done
    
    cat >> $NEO4J_CONF << EOF

# Cluster Configuration
causal_clustering.minimum_core_cluster_size_at_formation=3
causal_clustering.minimum_core_cluster_size_at_runtime=3
causal_clustering.initial_discovery_members=$INITIAL_DISCOVERY
causal_clustering.discovery_listen_address=0.0.0.0:5000
causal_clustering.discovery_advertised_address=$INSTANCE_IP:5000
causal_clustering.transaction_listen_address=0.0.0.0:6000
causal_clustering.transaction_advertised_address=$INSTANCE_IP:6000
causal_clustering.raft_listen_address=0.0.0.0:7000
causal_clustering.raft_advertised_address=$INSTANCE_IP:7000
causal_clustering.cluster_topology_refresh=5s
EOF
fi

# Install plugins
echo "Installing Neo4j plugins..."
PLUGIN_DIR="/var/lib/neo4j/plugins"

# Install APOC
if [ "$APOC_ENABLED" = "true" ]; then
    echo "Installing APOC plugin..."
    wget -O $PLUGIN_DIR/apoc-5.13.0-core.jar \
        https://github.com/neo4j-contrib/neo4j-apoc-procedures/releases/download/5.13.0/apoc-5.13.0-core.jar
fi

# Install Graph Data Science
if [ "$GDS_ENABLED" = "true" ]; then
    echo "Installing Graph Data Science plugin..."
    wget -O $PLUGIN_DIR/neo4j-graph-data-science-2.5.0.jar \
        https://github.com/neo4j/graph-data-science/releases/download/2.5.0/neo4j-graph-data-science-2.5.0.jar
fi

# Install custom plugins
if [ "$CUSTOM_PLUGINS" != "[]" ]; then
    echo "Installing custom plugins..."
    echo "$CUSTOM_PLUGINS" | jq -c '.[]' | while read plugin; do
        name=$(echo $plugin | jq -r '.name')
        url=$(echo $plugin | jq -r '.url')
        version=$(echo $plugin | jq -r '.version')
        
        echo "Installing plugin: $name v$version"
        wget -O "$PLUGIN_DIR/$name-$version.jar" "$url"
    done
fi

chown -R neo4j:neo4j $PLUGIN_DIR

# Set Neo4j password
echo "Setting Neo4j password..."
neo4j-admin dbms set-initial-password "$NEO4J_PASSWORD"

# Create systemd override for better resource limits
mkdir -p /etc/systemd/system/neo4j.service.d
cat > /etc/systemd/system/neo4j.service.d/override.conf << EOF
[Unit]
After=network.target

[Service]
LimitNOFILE=65536
LimitMEMLOCK=infinity
OOMScoreAdjust=-200

# Environment variables
Environment=NEO4J_CONF=/etc/neo4j
Environment=NEO4J_HOME=/var/lib/neo4j
Environment=NEO4J_LOGS=/var/lib/neo4j-data/logs

# Restart policy
Restart=always
RestartSec=30s

# Health check
ExecStartPost=/bin/sleep 30
ExecStartPost=/bin/bash -c 'until curl -f http://localhost:7474/; do sleep 5; done'
EOF

# Configure CloudWatch monitoring
echo "Configuring CloudWatch monitoring..."
mkdir -p /opt/aws/amazon-cloudwatch-agent/etc

cat > /opt/aws/amazon-cloudwatch-agent/etc/amazon-cloudwatch-agent.json << EOF
{
    "agent": {
        "metrics_collection_interval": 60,
        "run_as_user": "cwagent"
    },
    "logs": {
        "logs_collected": {
            "files": {
                "collect_list": [
                    {
                        "file_path": "/var/lib/neo4j-data/logs/neo4j.log",
                        "log_group_name": "$CLOUDWATCH_LOG_GROUP",
                        "log_stream_name": "neo4j-{instance_id}",
                        "timezone": "UTC"
                    },
                    {
                        "file_path": "/var/lib/neo4j-data/logs/query.log",
                        "log_group_name": "$CLOUDWATCH_LOG_GROUP",
                        "log_stream_name": "query-{instance_id}",
                        "timezone": "UTC"
                    },
                    {
                        "file_path": "/var/log/neo4j-init.log",
                        "log_group_name": "$CLOUDWATCH_LOG_GROUP",
                        "log_stream_name": "init-{instance_id}",
                        "timezone": "UTC"
                    }
                ]
            }
        }
    },
    "metrics": {
        "namespace": "InfoTerminal/Neo4j",
        "metrics_collected": {
            "cpu": {
                "measurement": [
                    "cpu_usage_idle",
                    "cpu_usage_iowait",
                    "cpu_usage_user",
                    "cpu_usage_system"
                ],
                "metrics_collection_interval": 60,
                "totalcpu": true
            },
            "disk": {
                "measurement": [
                    "used_percent"
                ],
                "metrics_collection_interval": 60,
                "resources": [
                    "*"
                ]
            },
            "diskio": {
                "measurement": [
                    "io_time"
                ],
                "metrics_collection_interval": 60,
                "resources": [
                    "*"
                ]
            },
            "mem": {
                "measurement": [
                    "mem_used_percent",
                    "mem_available"
                ],
                "metrics_collection_interval": 60
            },
            "netstat": {
                "measurement": [
                    "tcp_established",
                    "tcp_time_wait"
                ],
                "metrics_collection_interval": 60
            },
            "swap": {
                "measurement": [
                    "swap_used_percent"
                ],
                "metrics_collection_interval": 60
            }
        },
        "append_dimensions": {
            "AutoScalingGroupName": "\${aws:AutoScalingGroupName}",
            "ImageId": "\${aws:ImageId}",
            "InstanceId": "\${aws:InstanceId}",
            "InstanceType": "\${aws:InstanceType}"
        }
    }
}
EOF

# Start CloudWatch agent
/opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl \
    -a fetch-config \
    -m ec2 \
    -s \
    -c file:/opt/aws/amazon-cloudwatch-agent/etc/amazon-cloudwatch-agent.json

# Create backup script
echo "Creating backup script..."
cat > /usr/local/bin/neo4j-backup.sh << 'EOF'
#!/bin/bash

set -euo pipefail

BACKUP_DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/var/lib/neo4j-data/backups"
BACKUP_FILE="neo4j_backup_$BACKUP_DATE.tar.gz"
S3_BUCKET="BACKUP_BUCKET_PLACEHOLDER"

mkdir -p $BACKUP_DIR

echo "Starting Neo4j backup at $(date)"

# Stop Neo4j temporarily for consistent backup
systemctl stop neo4j

# Create backup
tar -czf $BACKUP_DIR/$BACKUP_FILE -C /var/lib/neo4j-data databases

# Restart Neo4j
systemctl start neo4j

# Upload to S3
aws s3 cp $BACKUP_DIR/$BACKUP_FILE s3://$S3_BUCKET/backups/$BACKUP_FILE

# Cleanup local backup
rm -f $BACKUP_DIR/$BACKUP_FILE

echo "Backup completed at $(date)"
EOF

sed -i "s/BACKUP_BUCKET_PLACEHOLDER/$BACKUP_BUCKET/g" /usr/local/bin/neo4j-backup.sh
chmod +x /usr/local/bin/neo4j-backup.sh

# Set up backup cron job (daily at 2 AM)
echo "0 2 * * * root /usr/local/bin/neo4j-backup.sh >> /var/log/neo4j-backup.log 2>&1" >> /etc/crontab

# Create health check script
cat > /usr/local/bin/neo4j-health-check.sh << EOF
#!/bin/bash

# Simple health check for Neo4j
set -euo pipefail

# Check if Neo4j service is running
if ! systemctl is-active --quiet neo4j; then
    echo "Neo4j service is not running"
    exit 1
fi

# Check if Neo4j is responding to HTTP requests
if ! curl -f -s http://localhost:7474/ > /dev/null; then
    echo "Neo4j HTTP endpoint not responding"
    exit 1
fi

# Check if Neo4j is responding to Bolt requests
if ! echo "RETURN 1;" | cypher-shell -u neo4j -p "$NEO4J_PASSWORD" > /dev/null 2>&1; then
    echo "Neo4j Bolt endpoint not responding"
    exit 1
fi

echo "Neo4j is healthy"
exit 0
EOF

chmod +x /usr/local/bin/neo4j-health-check.sh

# Configure log rotation
cat > /etc/logrotate.d/neo4j << EOF
/var/lib/neo4j-data/logs/*.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    sharedscripts
    postrotate
        systemctl reload neo4j || true
    endscript
}
EOF

# Set up performance tuning
echo "Applying performance tuning..."

# Kernel parameters for Neo4j
cat > /etc/sysctl.d/99-neo4j.conf << EOF
# Neo4j performance tuning
vm.max_map_count=262144
vm.swappiness=1
net.core.somaxconn=65536
net.ipv4.tcp_max_syn_backlog=65536
net.core.netdev_max_backlog=5000
net.ipv4.tcp_congestion_control=bbr
EOF

sysctl -p /etc/sysctl.d/99-neo4j.conf

# Set up file limits
cat > /etc/security/limits.d/neo4j.conf << EOF
neo4j soft nofile 65536
neo4j hard nofile 65536
neo4j soft memlock unlimited
neo4j hard memlock unlimited
EOF

# Reload systemd and enable Neo4j
systemctl daemon-reload
systemctl enable neo4j

# Start Neo4j
echo "Starting Neo4j..."
systemctl start neo4j

# Wait for Neo4j to start
echo "Waiting for Neo4j to become available..."
for i in {1..60}; do
    if curl -f -s http://localhost:7474/ > /dev/null; then
        echo "Neo4j is ready!"
        break
    fi
    echo "Waiting for Neo4j... ($i/60)"
    sleep 5
done

# Run initial OSINT-specific setup
echo "Setting up OSINT-specific configurations..."
cypher-shell -u neo4j -p "$NEO4J_PASSWORD" << 'CYPHER_EOF'
// Create OSINT-specific indexes for better performance

// Person entity indexes
CREATE INDEX person_name_index IF NOT EXISTS FOR (p:Person) ON (p.name);
CREATE INDEX person_email_index IF NOT EXISTS FOR (p:Person) ON (p.email);
CREATE INDEX person_username_index IF NOT EXISTS FOR (p:Person) ON (p.username);
CREATE FULLTEXT INDEX person_fulltext_index IF NOT EXISTS FOR (p:Person) ON EACH [p.name, p.email, p.username, p.bio];

// Organization entity indexes
CREATE INDEX org_name_index IF NOT EXISTS FOR (o:Organization) ON (o.name);
CREATE INDEX org_domain_index IF NOT EXISTS FOR (o:Organization) ON (o.domain);
CREATE FULLTEXT INDEX org_fulltext_index IF NOT EXISTS FOR (o:Organization) ON EACH [o.name, o.description, o.domain];

// Domain entity indexes
CREATE INDEX domain_name_index IF NOT EXISTS FOR (d:Domain) ON (d.name);
CREATE INDEX domain_tld_index IF NOT EXISTS FOR (d:Domain) ON (d.tld);

// IP Address indexes
CREATE INDEX ip_address_index IF NOT EXISTS FOR (ip:IPAddress) ON (ip.address);
CREATE INDEX ip_asn_index IF NOT EXISTS FOR (ip:IPAddress) ON (ip.asn);

// Social Media indexes
CREATE INDEX social_platform_index IF NOT EXISTS FOR (s:SocialMedia) ON (s.platform);
CREATE INDEX social_username_index IF NOT EXISTS FOR (s:SocialMedia) ON (s.username);
CREATE FULLTEXT INDEX social_fulltext_index IF NOT EXISTS FOR (s:SocialMedia) ON EACH [s.username, s.bio, s.location];

// Location indexes
CREATE INDEX location_name_index IF NOT EXISTS FOR (l:Location) ON (l.name);
CREATE INDEX location_country_index IF NOT EXISTS FOR (l:Location) ON (l.country);
CREATE POINT INDEX location_coordinates_index IF NOT EXISTS FOR (l:Location) ON (l.coordinates);

// Phone number indexes
CREATE INDEX phone_number_index IF NOT EXISTS FOR (ph:Phone) ON (ph.number);
CREATE INDEX phone_country_index IF NOT EXISTS FOR (ph:Phone) ON (ph.country);

// Email indexes
CREATE INDEX email_address_index IF NOT EXISTS FOR (e:Email) ON (e.address);
CREATE INDEX email_domain_index IF NOT EXISTS FOR (e:Email) ON (e.domain);

// Document indexes
CREATE INDEX document_hash_index IF NOT EXISTS FOR (doc:Document) ON (doc.hash);
CREATE INDEX document_type_index IF NOT EXISTS FOR (doc:Document) ON (doc.type);
CREATE FULLTEXT INDEX document_content_index IF NOT EXISTS FOR (doc:Document) ON EACH [doc.title, doc.content, doc.description];

// Relationship indexes for common traversals
CREATE INDEX rel_date_index IF NOT EXISTS FOR ()-[r]-() ON (r.date);
CREATE INDEX rel_confidence_index IF NOT EXISTS FOR ()-[r]-() ON (r.confidence);
CREATE INDEX rel_source_index IF NOT EXISTS FOR ()-[r]-() ON (r.source);

// Investigation tracking
CREATE INDEX investigation_id_index IF NOT EXISTS FOR (i:Investigation) ON (i.id);
CREATE INDEX investigation_status_index IF NOT EXISTS FOR (i:Investigation) ON (i.status);
CREATE INDEX investigation_created_index IF NOT EXISTS FOR (i:Investigation) ON (i.created_at);

CYPHER_EOF

# Setup monitoring queries
cat > /var/lib/neo4j-data/monitoring_queries.cypher << 'EOF'
// OSINT Platform Monitoring Queries

// Query 1: Get database statistics
CALL db.stats.retrieve('GRAPH COUNTS') YIELD data 
RETURN data.nodes AS total_nodes, data.relationships AS total_relationships;

// Query 2: Get most connected entities
MATCH (n) 
WITH n, size([(n)-[]->() | 1]) + size([(n)<-[]-() | 1]) AS connections 
WHERE connections > 0 
RETURN labels(n)[0] AS entity_type, n.name AS name, connections 
ORDER BY connections DESC 
LIMIT 10;

// Query 3: Check for orphaned nodes
MATCH (n) 
WHERE NOT (n)--() 
RETURN labels(n)[0] AS entity_type, count(n) AS orphaned_count;

// Query 4: Get investigation status summary  
MATCH (i:Investigation) 
RETURN i.status AS status, count(i) AS count 
ORDER BY count DESC;

// Query 5: Check index usage
CALL db.indexes() YIELD name, type, state, populationPercent
WHERE state <> 'ONLINE' OR populationPercent < 100
RETURN name, type, state, populationPercent;
EOF

# Create monitoring script
cat > /usr/local/bin/neo4j-monitor.sh << 'EOF'
#!/bin/bash

set -euo pipefail

echo "Neo4j Monitoring Report - $(date)"
echo "=================================="

# Check service status
echo "Service Status:"
systemctl status neo4j --no-pager -l

echo -e "\nDatabase Statistics:"
cypher-shell -u neo4j -p "$NEO4J_PASSWORD" --format plain < /var/lib/neo4j-data/monitoring_queries.cypher

echo -e "\nResource Usage:"
echo "Memory Usage:"
free -h

echo "Disk Usage:"
df -h /var/lib/neo4j-data

echo "CPU Usage:"
top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1

echo -e "\nConnection Count:"
ss -tln | grep -E ':(7474|7687|7473)' | wc -l

echo "=================================="
EOF

chmod +x /usr/local/bin/neo4j-monitor.sh

# Set up monitoring cron job (every 5 minutes)
echo "*/5 * * * * root /usr/local/bin/neo4j-monitor.sh >> /var/log/neo4j-monitor.log 2>&1" >> /etc/crontab

# Signal completion
echo "Neo4j initialization completed successfully at $(date)"

# Send completion notification to CloudWatch
aws logs put-log-events \
    --log-group-name "$CLOUDWATCH_LOG_GROUP" \
    --log-stream-name "init-$INSTANCE_ID" \
    --log-events timestamp=$(date +%s)000,message="Neo4j initialization completed successfully on instance $INSTANCE_ID" \
    --region $REGION || true

# Final health check
/usr/local/bin/neo4j-health-check.sh
EOF
