#!/bin/bash
# GenX FX Trading Platform Startup Script for VPS Environment

# Enable error handling
set -e

# Constants
LOG_FILE="/var/log/genx_fx/startup.log"
DOCKER_COMPOSE_FILE="/opt/genx_fx/docker-compose.yml"
HEALTH_CHECK_INTERVAL=60

# Function to write logs with timestamp
log_message() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Function to check container health
check_container_health() {
    local container_name=$1
    local health_status=$(docker inspect --format='{{.State.Health.Status}}' "$container_name" 2>/dev/null)
    [[ "$health_status" == "healthy" ]]
}

# Create necessary directories
log_message "Creating necessary directories..."
mkdir -p /var/log/genx_fx /opt/genx_fx/{logs,data,expert-advisors,reports}

# Check if Docker is running
log_message "Checking Docker service..."
if ! systemctl is-active --quiet docker; then
    log_message "Starting Docker service..."
    systemctl start docker
    sleep 10
fi

# Navigate to application directory
cd /opt/genx_fx

# Start containers using docker-compose
log_message "Starting containers with docker-compose..."
docker-compose -f $DOCKER_COMPOSE_FILE up -d

# Wait for containers to initialize
log_message "Waiting for containers to initialize..."
sleep 30

# Verify container health
containers=("genxdb_fx_mysql" "genx-redis" "genx-backend" "genxdb_fx_trading")
for container in "${containers[@]}"; do
    log_message "Checking health of container: $container"
    if ! check_container_health "$container"; then
        log_message "Warning: Container $container may not be healthy"
    fi
done

# Install health monitor requirements
log_message "Installing health monitor requirements..."
pip3 install -r health_monitor_requirements.txt

# Start health monitor in background
log_message "Starting health monitor..."
nohup python3 health_monitor.py > logs/health_monitor.log 2>&1 &

# Monitor loop
log_message "Starting monitoring loop..."
while true; do
    # Check container status
    for container in "${containers[@]}"; do
        if ! docker ps -f name=$container --format "{{.Status}}" | grep -q "Up"; then
            log_message "Container $container is down, attempting restart..."
            docker start $container
        fi
    done

    # Check API health
    if ! curl -s -f http://localhost:8080/health > /dev/null; then
        log_message "Warning: API health check failed"
        # Attempt to restart the API container
        docker restart genx-backend
    fi

    # Check trading bot process if running locally
    if [[ -f "/opt/genx_fx/main.py" ]]; then
        if ! pgrep -f "python.*main\.py" > /dev/null; then
            log_message "Trading bot process not found, restarting..."
            cd /opt/genx_fx && nohup python3 main.py > logs/trading_bot.log 2>&1 &
        fi
    fi

    # Check system resources
    memory_usage=$(free -m | awk 'NR==2{printf "%.2f%%", $3*100/$2}')
    disk_usage=$(df -h / | awk 'NR==2{printf "%s", $5}')
    load_avg=$(uptime | awk -F'load average: ' '{print $2}')
    
    log_message "System Status:"
    log_message "- Memory Usage: $memory_usage"
    log_message "- Disk Usage: $disk_usage"
    log_message "- Load Average: $load_avg"
    
    # Alert if resources are critical
    if [[ "${memory_usage%.*}" -gt 90 ]]; then
        log_message "WARNING: High memory usage detected"
    fi
    
    if [[ "${disk_usage%\%}" -gt 90 ]]; then
        log_message "WARNING: High disk usage detected"
    fi

    # Log status
    log_message "System running - All services operational"
    
    # Wait before next check
    sleep $HEALTH_CHECK_INTERVAL
done