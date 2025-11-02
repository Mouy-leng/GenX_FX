#!/bin/bash
# NameCheap VPS Deployment Script for GenX Magic Trading Platform
# This script automates VPS creation and GenX platform deployment on NameCheap

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 GenX Trading Platform - NameCheap VPS Deployment${NC}"
echo "================================================================"

# Check if credentials are set
if [ -z "$NAMECHEAP_API_USER" ] || [ -z "$NAMECHEAP_API_KEY" ]; then
    echo -e "${RED}❌ Error: NameCheap credentials not set${NC}"
    echo "Please set the following environment variables:"
    echo "export NAMECHEAP_API_USER='your_username'"
    echo "export NAMECHEAP_API_KEY='your_api_key'"
    echo "export NAMECHEAP_USERNAME='your_account_username'"
    echo "export NAMECHEAP_CLIENT_IP='your_whitelisted_ip'"
    exit 1
fi

# VPS Configuration
VPS_HOSTNAME="genx-trading-$(date +%s)"
VPS_DOMAIN="genx-trading.com"  # Update with your domain
SSH_KEY_NAME="genx-trading-key"

echo -e "${YELLOW}📋 VPS Configuration:${NC}"
echo "Hostname: $VPS_HOSTNAME"
echo "Domain: $VPS_DOMAIN"
echo "Plan: Stellar Plus (2 vCPU, 6GB RAM)"
echo "OS: Ubuntu 22.04 LTS"
echo ""

# Generate SSH key if it doesn't exist
if [ ! -f ~/.ssh/$SSH_KEY_NAME ]; then
    echo -e "${YELLOW}🔑 Generating SSH key pair...${NC}"
    ssh-keygen -t rsa -b 4096 -f ~/.ssh/$SSH_KEY_NAME -N ""
    echo -e "${GREEN}✅ SSH key generated: ~/.ssh/$SSH_KEY_NAME${NC}"
fi

# Create VPS deployment script
cat > namecheap_deploy.py << 'EOF'
#!/usr/bin/env python3
"""
NameCheap VPS Creation and GenX Platform Deployment
"""

import os
import requests
import time
import json
from urllib.parse import urlencode

class NameCheapVPS:
    def __init__(self):
        self.api_user = os.getenv('NAMECHEAP_API_USER')
        self.api_key = os.getenv('NAMECHEAP_API_KEY')
        self.username = os.getenv('NAMECHEAP_USERNAME')
        self.client_ip = os.getenv('NAMECHEAP_CLIENT_IP')
        self.base_url = "https://api.namecheap.com/xml.response"
        
    def create_vps(self, hostname, plan="stellar-plus"):
        """Create a new VPS instance"""
        params = {
            'ApiUser': self.api_user,
            'ApiKey': self.api_key,
            'UserName': self.username,
            'Command': 'namecheap.server.create',
            'ClientIp': self.client_ip,
            'hostname': hostname,
            'plan': plan,
            'os': 'ubuntu-22-04',
            'location': 'phoenix'
        }
        
        try:
            response = requests.get(self.base_url, params=params)
            print(f"VPS Creation Response: {response.status_code}")
            print(f"Response: {response.text}")
            return response.status_code == 200
        except Exception as e:
            print(f"Error creating VPS: {e}")
            return False
    
    def list_servers(self):
        """List all VPS instances"""
        params = {
            'ApiUser': self.api_user,
            'ApiKey': self.api_key,
            'UserName': self.username,
            'Command': 'namecheap.server.getList',
            'ClientIp': self.client_ip
        }
        
        try:
            response = requests.get(self.base_url, params=params)
            print(f"Server List Response: {response.status_code}")
            print(f"Response: {response.text}")
            return response
        except Exception as e:
            print(f"Error listing servers: {e}")
            return None

if __name__ == "__main__":
    vps = NameCheapVPS()
    
    print("🔧 Creating NameCheap VPS...")
    hostname = f"genx-trading-{int(time.time())}"
    
    if vps.create_vps(hostname):
        print("✅ VPS created successfully!")
        print("📋 Listing servers...")
        vps.list_servers()
    else:
        print("❌ Failed to create VPS")
EOF

# Make the Python script executable
chmod +x namecheap_deploy.py

echo -e "${YELLOW}🔧 Creating VPS with NameCheap API...${NC}"
python3 namecheap_deploy.py

# Wait for VPS to be ready
echo -e "${YELLOW}⏳ Waiting for VPS to be ready (this may take 5-10 minutes)...${NC}"
sleep 300  # Wait 5 minutes

# Create GenX platform deployment script
cat > deploy_genx_to_namecheap.sh << 'EOF'
#!/bin/bash
# Deploy GenX Trading Platform to NameCheap VPS

VPS_IP="$1"  # Pass VPS IP as first argument
SSH_KEY="~/.ssh/genx-trading-key"

if [ -z "$VPS_IP" ]; then
    echo "Usage: $0 <VPS_IP_ADDRESS>"
    exit 1
fi

echo "🚀 Deploying GenX Trading Platform to $VPS_IP"

# Copy project files to VPS
echo "📁 Copying project files..."
rsync -avz -e "ssh -i $SSH_KEY -o StrictHostKeyChecking=no" \
    /path/to/GenX_FX/ root@$VPS_IP:/root/GenX_FX/

# Connect to VPS and setup environment
ssh -i $SSH_KEY -o StrictHostKeyChecking=no root@$VPS_IP << 'REMOTE_SCRIPT'
# Update system
apt-get update && apt-get upgrade -y

# Install Python and dependencies
apt-get install -y python3 python3-pip python3-venv nginx certbot python3-certbot-nginx

# Create virtual environment
cd /root/GenX_FX
python3 -m venv venv
source venv/bin/activate

# Install requirements
pip install fastapi uvicorn MetaTrader5 aiohttp python-multipart
pip install numpy pandas websockets httpx

# Create systemd service for GenX API
cat > /etc/systemd/system/genx-api.service << 'SERVICE'
[Unit]
Description=GenX Trading API
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/GenX_FX
Environment=PATH=/root/GenX_FX/venv/bin
ExecStart=/root/GenX_FX/venv/bin/python api/fastapi_server.py
Restart=always

[Install]
WantedBy=multi-user.target
SERVICE

# Enable and start service
systemctl enable genx-api
systemctl start genx-api

# Configure Nginx
cat > /etc/nginx/sites-available/genx-trading << 'NGINX'
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /ws {
        proxy_pass http://localhost:8765;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
NGINX

# Enable Nginx site
ln -s /etc/nginx/sites-available/genx-trading /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default
systemctl restart nginx

# Setup firewall
ufw allow OpenSSH
ufw allow 'Nginx Full'
ufw --force enable

echo "✅ GenX Trading Platform deployed successfully!"
echo "🌐 Access your platform at: http://$(curl -s ifconfig.me)"
echo "📊 API Documentation: http://$(curl -s ifconfig.me)/docs"

REMOTE_SCRIPT

echo "✅ Deployment completed!"
EOF

chmod +x deploy_genx_to_namecheap.sh

echo -e "${GREEN}✅ NameCheap deployment scripts created!${NC}"
echo ""
echo -e "${YELLOW}📋 Next steps:${NC}"
echo "1. Set your NameCheap credentials:"
echo "   export NAMECHEAP_API_USER='your_username'"
echo "   export NAMECHEAP_API_KEY='your_api_key'"
echo "   export NAMECHEAP_USERNAME='your_account_username'"
echo "   export NAMECHEAP_CLIENT_IP='your_ip_address'"
echo ""
echo "2. Run the deployment:"
echo "   ./deploy_namecheap_vps.sh"
echo ""
echo "3. After VPS is created, get the IP and run:"
echo "   ./deploy_genx_to_namecheap.sh <VPS_IP>"
echo ""
echo -e "${GREEN}🎯 Your GenX Trading Platform will be live at: http://YOUR_VPS_IP${NC}"