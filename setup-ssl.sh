#!/bin/bash

# SSL Certificate Setup Script for GenX_FX
# This script helps set up SSL certificates for your domain

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_success() { echo -e "${GREEN}✅ $1${NC}"; }
print_error() { echo -e "${RED}❌ $1${NC}"; }
print_info() { echo -e "${YELLOW}ℹ️  $1${NC}"; }
print_header() { echo -e "${BLUE}=== $1 ===${NC}"; }

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    print_error "Please run as root or with sudo"
    exit 1
fi

print_header "SSL Certificate Setup for GenX_FX"

# Get domain name
read -p "Enter your domain name (e.g., example.com): " DOMAIN
read -p "Enter your email for certificate notifications: " EMAIL

if [ -z "$DOMAIN" ] || [ -z "$EMAIL" ]; then
    print_error "Domain and email are required"
    exit 1
fi

print_info "Domain: $DOMAIN"
print_info "Email: $EMAIL"

# Confirm
read -p "Continue with these settings? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    print_info "Setup cancelled"
    exit 0
fi

# Install Certbot if not already installed
if ! command -v certbot &> /dev/null; then
    print_info "Installing Certbot..."
    apt-get update
    apt-get install -y certbot python3-certbot-nginx
    print_success "Certbot installed"
else
    print_success "Certbot already installed"
fi

# Check DNS configuration
print_info "Checking DNS configuration for $DOMAIN..."
if host "$DOMAIN" > /dev/null 2>&1; then
    print_success "DNS is configured for $DOMAIN"
else
    print_error "DNS not configured or not propagated yet for $DOMAIN"
    print_info "Please configure your DNS records and wait for propagation"
    print_info "Add an A record pointing to this server's IP address"
    exit 1
fi

# Get certificate method choice
echo ""
print_header "Certificate Method"
echo "1) Standalone (requires port 80 to be free)"
echo "2) Nginx plugin (requires nginx to be running)"
read -p "Choose method (1 or 2): " METHOD

case $METHOD in
    1)
        print_info "Using standalone method..."
        # Stop nginx temporarily
        if systemctl is-active --quiet nginx; then
            print_info "Stopping Nginx temporarily..."
            systemctl stop nginx
        fi
        
        # Get certificate
        certbot certonly --standalone \
            --non-interactive \
            --agree-tos \
            --email "$EMAIL" \
            -d "$DOMAIN" \
            -d "www.$DOMAIN"
        
        # Start nginx again
        if command -v nginx &> /dev/null; then
            print_info "Starting Nginx..."
            systemctl start nginx
        fi
        ;;
    2)
        print_info "Using Nginx plugin..."
        certbot --nginx \
            --non-interactive \
            --agree-tos \
            --email "$EMAIL" \
            -d "$DOMAIN" \
            -d "www.$DOMAIN"
        ;;
    *)
        print_error "Invalid choice"
        exit 1
        ;;
esac

if [ $? -eq 0 ]; then
    print_success "SSL certificate obtained successfully!"
    
    # Certificate locations
    print_info "Certificate locations:"
    echo "  Certificate: /etc/letsencrypt/live/$DOMAIN/fullchain.pem"
    echo "  Private Key: /etc/letsencrypt/live/$DOMAIN/privkey.pem"
    
    # Test auto-renewal
    print_info "Testing certificate renewal..."
    certbot renew --dry-run
    
    if [ $? -eq 0 ]; then
        print_success "Auto-renewal is configured correctly"
    else
        print_error "Auto-renewal test failed"
    fi
    
    # Check renewal timer
    print_info "Certbot renewal timer status:"
    systemctl status certbot.timer --no-pager | head -5
    
    print_success "SSL setup completed!"
    print_info ""
    print_info "Next steps:"
    print_info "1. Update your Nginx configuration with the certificate paths"
    print_info "2. Update your .env file with DOMAIN=$DOMAIN"
    print_info "3. Restart your services: docker-compose restart"
    print_info "4. Test your site: https://$DOMAIN"
    
else
    print_error "Failed to obtain SSL certificate"
    print_info "Please check the error messages above"
    exit 1
fi

exit 0
