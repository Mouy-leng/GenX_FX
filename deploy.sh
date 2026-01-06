#!/bin/bash

# GenX_FX Deployment Script
# This script automates the deployment process for the ProductionApp

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
PROJECT_DIR="/var/www/genx-fx"
APP_DIR="$PROJECT_DIR/ProductionApp"
BACKUP_DIR="$PROJECT_DIR/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Functions
print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}ℹ️  $1${NC}"
}

# Check if running as root or with sudo
if [ "$EUID" -ne 0 ]; then 
    print_error "Please run as root or with sudo"
    exit 1
fi

print_info "Starting GenX_FX deployment..."

# Step 1: Create backup directory
print_info "Creating backup directory..."
mkdir -p "$BACKUP_DIR"
print_success "Backup directory ready"

# Step 2: Backup current deployment
if [ -d "$APP_DIR" ]; then
    print_info "Creating backup of current deployment..."
    tar -czf "$BACKUP_DIR/backup_$TIMESTAMP.tar.gz" -C "$PROJECT_DIR" ProductionApp
    print_success "Backup created: backup_$TIMESTAMP.tar.gz"
fi

# Step 3: Navigate to project directory
print_info "Navigating to project directory..."
cd "$PROJECT_DIR" || exit 1

# Step 4: Pull latest changes
print_info "Pulling latest changes from repository..."
git fetch origin
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
git pull origin "$CURRENT_BRANCH"
print_success "Repository updated"

# Step 5: Navigate to ProductionApp
cd "$APP_DIR" || exit 1

# Step 6: Check if .env exists
if [ ! -f .env ]; then
    print_error ".env file not found!"
    print_info "Please create .env file from .env.example"
    exit 1
fi

# Step 7: Stop running containers
print_info "Stopping running containers..."
docker-compose down
print_success "Containers stopped"

# Step 8: Remove old images (optional, uncomment to enable)
# print_info "Removing old Docker images..."
# docker-compose down --rmi all

# Step 9: Build and start containers
print_info "Building and starting containers..."
docker-compose up -d --build
print_success "Containers started"

# Step 10: Wait for services to be ready
print_info "Waiting for services to be ready..."
sleep 10

# Step 11: Check service health
print_info "Checking service health..."
if docker-compose ps | grep -q "Up"; then
    print_success "Services are running"
else
    print_error "Some services failed to start"
    print_info "Checking logs..."
    docker-compose logs --tail=50
    exit 1
fi

# Step 12: Test health endpoint
print_info "Testing health endpoint..."
if curl -sf http://localhost:3000/health > /dev/null; then
    print_success "Health check passed"
else
    print_error "Health check failed"
    print_info "Application may not be responding correctly"
fi

# Step 13: Show running containers
print_info "Running containers:"
docker-compose ps

# Step 14: Clean up old backups (keep last 10)
print_info "Cleaning up old backups..."
cd "$BACKUP_DIR"
ls -t | tail -n +11 | xargs -r rm --
print_success "Old backups cleaned"

# Step 15: Restart Nginx (if installed)
if command -v nginx &> /dev/null; then
    print_info "Restarting Nginx..."
    systemctl restart nginx
    print_success "Nginx restarted"
fi

print_success "Deployment completed successfully!"
print_info "Application is now running"
print_info "Check logs with: cd $APP_DIR && docker-compose logs -f"
print_info ""
print_info "Access your application at:"
print_info "  - Local: http://localhost:3000"
print_info "  - Health: http://localhost:3000/health"
print_info ""
print_success "Deployment finished at $(date)"

exit 0
