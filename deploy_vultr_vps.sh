#!/bin/bash
# Vultr VPS Deployment Script for GenX Magic Trading Platform
# This script automates VPS creation and GenX platform deployment on Vultr

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 GenX Trading Platform - Vultr VPS Deployment${NC}"
echo "================================================================"

# Check if credentials are set
if [ -z "$VULTR_API_KEY" ]; then
    echo -e "${RED}❌ Error: Vultr API key not set${NC}"
    echo "Please set the following environment variable:"
    echo "export VULTR_API_KEY='your_vultr_api_key'"
    exit 1
fi

# VPS Configuration
VPS_LABEL="genx-trading-$(date +%s)"
VPS_REGION="${VULTR_REGION:-ewr}"  # Default to New York
VPS_PLAN="${VULTR_PLAN:-vc2-2c-4gb}"  # 2 vCPU, 4GB RAM
VPS_OS="${VULTR_OS_ID:-387}"  # Ubuntu 22.04 LTS

echo -e "${YELLOW}📋 VPS Configuration:${NC}"
echo "Label: $VPS_LABEL"
echo "Region: $VPS_REGION"
echo "Plan: $VPS_PLAN (2 vCPU, 4GB RAM)"
echo "OS: Ubuntu 22.04 LTS"
echo ""

# Generate SSH key if it doesn't exist
SSH_KEY_NAME="genx-vultr-key"
if [ ! -f ~/.ssh/$SSH_KEY_NAME ]; then
    echo -e "${YELLOW}🔑 Generating SSH key pair...${NC}"
    ssh-keygen -t rsa -b 4096 -f ~/.ssh/$SSH_KEY_NAME -N ""
    echo -e "${GREEN}✅ SSH key generated: ~/.ssh/$SSH_KEY_NAME${NC}"
fi

# Create Vultr deployment script
cat > vultr_deploy.py << 'EOF'
#!/usr/bin/env python3
"""
Vultr VPS Creation and GenX Platform Deployment
"""

import os
import requests
import time
import json

class VultrVPS:
    def __init__(self):
        self.api_key = os.getenv('VULTR_API_KEY')
        self.base_url = "https://api.vultr.com/v2"
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
    def upload_ssh_key(self, name, ssh_key_content):
        """Upload SSH key to Vultr"""
        data = {
            'name': name,
            'ssh_key': ssh_key_content
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/ssh-keys",
                headers=self.headers,
                json=data
            )
            
            if response.status_code == 201:
                key_data = response.json()
                print(f"✅ SSH key uploaded: {key_data['ssh_key']['id']}")
                return key_data['ssh_key']['id']
            else:
                print(f"❌ Failed to upload SSH key: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Error uploading SSH key: {e}")
            return None
    
    def create_vps(self, label, region, plan, os_id, ssh_key_id=None):
        """Create a new VPS instance"""
        data = {
            'region': region,
            'plan': plan,
            'label': label,
            'os_id': int(os_id),
            'enable_ipv6': True,
            'backups': 'enabled' if os.getenv('VULTR_ENABLE_BACKUPS') == 'true' else 'disabled',
            'ddos_protection': True if os.getenv('VULTR_ENABLE_DDOS_PROTECTION') == 'true' else False
        }
        
        if ssh_key_id:
            data['sshkey_id'] = [ssh_key_id]
        
        try:
            response = requests.post(
                f"{self.base_url}/instances",
                headers=self.headers,
                json=data
            )
            
            if response.status_code == 202:
                instance_data = response.json()
                instance_id = instance_data['instance']['id']
                print(f"✅ VPS created successfully!")
                print(f"Instance ID: {instance_id}")
                print(f"Label: {label}")
                return instance_id
            else:
                print(f"❌ Failed to create VPS: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Error creating VPS: {e}")
            return None
    
    def get_instance_info(self, instance_id):
        """Get VPS instance information"""
        try:
            response = requests.get(
                f"{self.base_url}/instances/{instance_id}",
                headers=self.headers
            )
            
            if response.status_code == 200:
                return response.json()['instance']
            else:
                print(f"❌ Failed to get instance info: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Error getting instance info: {e}")
            return None
    
    def wait_for_instance(self, instance_id, timeout=600):
        """Wait for instance to be ready"""
        print("⏳ Waiting for VPS to be ready...")
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            instance = self.get_instance_info(instance_id)
            
            if instance and instance['status'] == 'active':
                print(f"✅ VPS is ready!")
                print(f"IP Address: {instance['main_ip']}")
                print(f"Default Password: {instance.get('default_password', 'N/A')}")
                return instance
            
            print(f"Status: {instance['status'] if instance else 'Unknown'}")
            time.sleep(30)
        
        print("❌ Timeout waiting for VPS to be ready")
        return None

if __name__ == "__main__":
    vps = VultrVPS()
    
    # Upload SSH key
    ssh_key_path = os.path.expanduser("~/.ssh/genx-vultr-key.pub")
    ssh_key_id = None
    
    if os.path.exists(ssh_key_path):
        with open(ssh_key_path, 'r') as f:
            ssh_key_content = f.read().strip()
        
        ssh_key_id = vps.upload_ssh_key("genx-trading-key", ssh_key_content)
    
    # Create VPS
    print("🔧 Creating Vultr VPS...")
    instance_id = vps.create_vps(
        label=os.getenv('VPS_LABEL', 'genx-trading'),
        region=os.getenv('VPS_REGION', 'ewr'),
        plan=os.getenv('VPS_PLAN', 'vc2-2c-4gb'),
        os_id=os.getenv('VPS_OS', '387'),
        ssh_key_id=ssh_key_id
    )
    
    if instance_id:
        # Wait for VPS to be ready
        instance = vps.wait_for_instance(instance_id)
        
        if instance:
            # Save instance info
            with open('vultr_instance.json', 'w') as f:
                json.dump(instance, f, indent=2)
            
            print("\n" + "="*50)
            print("🎉 VPS READY FOR DEPLOYMENT!")
            print("="*50)
            print(f"Instance ID: {instance_id}")
            print(f"IP Address: {instance['main_ip']}")
            print(f"Default Password: {instance.get('default_password', 'Use SSH key')}")
            print(f"Region: {instance['region']}")
            print(f"Plan: {instance['plan']}")
            print("\nNext step: Run deployment script")
            print(f"./deploy_genx_to_vultr.sh {instance['main_ip']}")
        else:
            print("❌ Failed to get VPS ready")
    else:
        print("❌ Failed to create VPS")
EOF

# Make the Python script executable
chmod +x vultr_deploy.py

# Set environment variables for the Python script
export VPS_LABEL="$VPS_LABEL"
export VPS_REGION="$VPS_REGION"
export VPS_PLAN="$VPS_PLAN"
export VPS_OS="$VPS_OS"

echo -e "${YELLOW}🔧 Creating VPS with Vultr API...${NC}"
python3 vultr_deploy.py

# Create GenX platform deployment script
cat > deploy_genx_to_vultr.sh << 'EOF'
#!/bin/bash
# Deploy GenX Trading Platform to Vultr VPS

VPS_IP="$1"  # Pass VPS IP as first argument
SSH_KEY="~/.ssh/genx-vultr-key"

if [ -z "$VPS_IP" ]; then
    echo "Usage: $0 <VPS_IP_ADDRESS>"
    exit 1
fi

echo "🚀 Deploying GenX Trading Platform to $VPS_IP"

# Wait for SSH to be ready
echo "⏳ Waiting for SSH to be ready..."
while ! ssh -i $SSH_KEY -o StrictHostKeyChecking=no -o ConnectTimeout=5 root@$VPS_IP exit; do
    echo "SSH not ready, waiting 30 seconds..."
    sleep 30
done

# Copy project files to VPS
echo "📁 Copying project files..."
rsync -avz -e "ssh -i $SSH_KEY -o StrictHostKeyChecking=no" \
    . root@$VPS_IP:/root/GenX_FX/ \
    --exclude='.git' --exclude='__pycache__' --exclude='*.log'

# Connect to VPS and setup environment
ssh -i $SSH_KEY -o StrictHostKeyChecking=no root@$VPS_IP << 'REMOTE_SCRIPT'
# Update system
apt-get update && apt-get upgrade -y

# Install Python and dependencies
apt-get install -y python3 python3-pip python3-venv nginx certbot python3-certbot-nginx \
    curl wget git htop unzip

# Install Node.js (for potential frontend needs)
curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
apt-get install -y nodejs

# Create virtual environment
cd /root/GenX_FX
python3 -m venv venv
source venv/bin/activate

# Install Python requirements
pip install --upgrade pip
pip install fastapi uvicorn MetaTrader5 aiohttp python-multipart
pip install numpy pandas websockets httpx python-dotenv
pip install asyncio logging datetime typing

# Create environment file
cat > .env << 'ENV'
# GenX Trading Platform - Vultr VPS
PROJECT_ROOT=/root/GenX_FX
HOST=0.0.0.0
PORT=8000
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=INFO
TRADING_ENABLED=true
ENV

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
RestartSec=10

[Install]
WantedBy=multi-user.target
SERVICE

# Create systemd service for WebSocket
cat > /etc/systemd/system/genx-websocket.service << 'SERVICE'
[Unit]
Description=GenX WebSocket Service
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/GenX_FX
Environment=PATH=/root/GenX_FX/venv/bin
ExecStart=/root/GenX_FX/venv/bin/python api/websocket_realtime_server.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
SERVICE

# Enable and start services
systemctl daemon-reload
systemctl enable genx-api genx-websocket
systemctl start genx-api genx-websocket

# Configure Nginx with SSL support
cat > /etc/nginx/sites-available/genx-trading << 'NGINX'
server {
    listen 80;
    server_name _;

    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name _;

    # SSL Configuration (self-signed for now)
    ssl_certificate /etc/ssl/certs/genx-selfsigned.crt;
    ssl_certificate_key /etc/ssl/private/genx-selfsigned.key;
    
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;

    # API Routes
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # CORS headers
        add_header Access-Control-Allow-Origin "*";
        add_header Access-Control-Allow-Methods "GET, POST, OPTIONS";
        add_header Access-Control-Allow-Headers "Origin, Content-Type, Accept, Authorization";
    }

    # WebSocket Routes
    location /ws {
        proxy_pass http://localhost:8765;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    # Static files
    location /static {
        alias /root/GenX_FX/static;
        expires 30d;
    }
}
NGINX

# Generate self-signed SSL certificate
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout /etc/ssl/private/genx-selfsigned.key \
    -out /etc/ssl/certs/genx-selfsigned.crt \
    -subj "/C=US/ST=State/L=City/O=GenX Trading/CN=genx-trading"

# Enable Nginx site
ln -sf /etc/nginx/sites-available/genx-trading /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default
nginx -t && systemctl restart nginx

# Setup firewall
ufw allow OpenSSH
ufw allow 'Nginx Full'
ufw allow 8000
ufw allow 8765
ufw --force enable

# Create monitoring script
cat > /root/monitor_genx.sh << 'MONITOR'
#!/bin/bash
# GenX Trading Platform Monitoring Script

echo "GenX Trading Platform Status"
echo "============================"
echo "Date: $(date)"
echo ""

echo "🔧 Services Status:"
systemctl is-active genx-api && echo "✅ API Service: Running" || echo "❌ API Service: Stopped"
systemctl is-active genx-websocket && echo "✅ WebSocket Service: Running" || echo "❌ WebSocket Service: Stopped"
systemctl is-active nginx && echo "✅ Nginx: Running" || echo "❌ Nginx: Stopped"
echo ""

echo "📊 System Resources:"
echo "CPU Usage: $(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | sed 's/%us,//')"
echo "Memory Usage: $(free -h | awk '/^Mem:/ {print $3 "/" $2}')"
echo "Disk Usage: $(df -h / | awk 'NR==2 {print $3 "/" $2}')"
echo ""

echo "🌐 Network Status:"
echo "External IP: $(curl -s ifconfig.me)"
echo "API Health: $(curl -s http://localhost:8000/health | jq -r .status 2>/dev/null || echo "Not responding")"
echo ""

echo "📝 Recent Logs:"
echo "API Logs (last 5 lines):"
journalctl -u genx-api --no-pager -n 5
echo ""
echo "WebSocket Logs (last 5 lines):"
journalctl -u genx-websocket --no-pager -n 5
MONITOR

chmod +x /root/monitor_genx.sh

# Install jq for JSON parsing
apt-get install -y jq

echo ""
echo "✅ GenX Trading Platform deployed successfully!"
echo ""
echo "🎯 Access Information:"
echo "================================"
echo "🌐 HTTPS URL: https://$(curl -s ifconfig.me)/"
echo "📊 API Docs: https://$(curl -s ifconfig.me)/docs"
echo "🔍 Health Check: https://$(curl -s ifconfig.me)/health"
echo "⚡ WebSocket: wss://$(curl -s ifconfig.me)/ws"
echo ""
echo "📋 Management Commands:"
echo "sudo systemctl status genx-api"
echo "sudo systemctl status genx-websocket"
echo "/root/monitor_genx.sh"
echo ""
echo "🔐 SSL Certificate: Self-signed (replace with real certificate for production)"

REMOTE_SCRIPT

echo "✅ Deployment completed!"
EOF

chmod +x deploy_genx_to_vultr.sh

echo -e "${GREEN}✅ Vultr deployment scripts created!${NC}"
echo ""
echo -e "${YELLOW}📋 Next steps:${NC}"
echo "1. Set your Vultr API key:"
echo "   export VULTR_API_KEY='your_vultr_api_key'"
echo ""
echo "2. Run the deployment:"
echo "   ./deploy_vultr_vps.sh"
echo ""
echo "3. The script will automatically deploy GenX platform after VPS creation"
echo ""
echo -e "${GREEN}🎯 Your GenX Trading Platform will be live at: https://YOUR_VPS_IP${NC}"