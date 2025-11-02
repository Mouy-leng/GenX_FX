#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NameCheap VPS Deployment - Fixed Unicode
Deploy GenX Trading Platform to NameCheap VPS
"""

import requests
import xml.etree.ElementTree as ET
import os
import json
import time
from datetime import datetime

class NameCheapVPSDeployer:
    def __init__(self):
        self.api_user = os.environ.get('NAMECHEAP_API_USER')
        self.api_key = os.environ.get('NAMECHEAP_API_KEY')
        self.username = os.environ.get('NAMECHEAP_USERNAME')
        self.client_ip = os.environ.get('NAMECHEAP_CLIENT_IP', '117.20.115.126')
        self.sandbox = False  # Use production API
        
        if self.sandbox:
            self.api_url = "https://api.sandbox.namecheap.com/xml.response"
        else:
            self.api_url = "https://api.namecheap.com/xml.response"
    
    def check_credentials(self):
        """Check if NameCheap credentials are properly set"""
        print("Checking NameCheap API Credentials...")
        print("=" * 50)
        
        if not self.api_user:
            print("ERROR: NAMECHEAP_API_USER not set")
            return False
        if not self.api_key:
            print("ERROR: NAMECHEAP_API_KEY not set")
            return False
        if not self.username:
            print("ERROR: NAMECHEAP_USERNAME not set")
            return False
        if not self.client_ip:
            print("ERROR: NAMECHEAP_CLIENT_IP not set")
            return False
        
        print(f"API User: {self.api_user}")
        print(f"Username: {self.username}")
        print(f"Client IP: {self.client_ip}")
        print(f"API Key: {'*' * 20}{self.api_key[-8:]}")
        print("All credentials are set!")
        
        return True
    
    def make_api_request(self, command, params=None):
        """Make API request to NameCheap"""
        base_params = {
            'ApiUser': self.api_user,
            'ApiKey': self.api_key,
            'UserName': self.username,
            'Command': command,
            'ClientIp': self.client_ip
        }
        
        if params:
            base_params.update(params)
        
        print(f"Making API request: {command}")
        
        try:
            response = requests.get(self.api_url, params=base_params, timeout=30)
            response.raise_for_status()
            
            # Parse XML response
            root = ET.fromstring(response.content)
            
            # Check for API errors
            if root.get('Status') == 'ERROR':
                errors = root.findall('.//Error')
                for error in errors:
                    print(f"API Error: {error.text}")
                return None
            
            print(f"API request successful: {command}")
            return root
            
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return None
        except ET.ParseError as e:
            print(f"XML parsing failed: {e}")
            return None
    
    def test_api_connection(self):
        """Test NameCheap API connection"""
        print("\nTesting NameCheap API Connection...")
        print("=" * 50)
        
        # Try to get domain list (simplest API call)
        response = self.make_api_request('namecheap.domains.getList', {
            'PageSize': '1',
            'Page': '1'
        })
        
        if response is not None:
            print("SUCCESS: NameCheap API connection working!")
            return True
        else:
            print("FAILED: Could not connect to NameCheap API")
            return False
    
    def get_available_plans(self):
        """Get available VPS plans"""
        print("\nChecking Available VPS Plans...")
        print("=" * 50)
        
        # Note: NameCheap doesn't have a direct VPS API like cloud providers
        # This would typically be done through their hosting panel
        
        recommended_plan = {
            'name': 'Stellar Plus',
            'cpu': '2 vCPU',
            'ram': '6GB',
            'storage': '120GB SSD',
            'bandwidth': '3TB',
            'price': '$19.98/month',
            'location': 'Phoenix, AZ'
        }
        
        print("Recommended VPS Plan:")
        for key, value in recommended_plan.items():
            print(f"  {key.title()}: {value}")
        
        return recommended_plan
    
    def check_domain_availability(self, domain):
        """Check if domain is available"""
        print(f"\nChecking domain availability: {domain}")
        print("=" * 50)
        
        params = {
            'DomainList': domain
        }
        
        response = self.make_api_request('namecheap.domains.check', params)
        if not response:
            return False
        
        domain_elements = response.findall('.//DomainCheckResult')
        
        for domain_elem in domain_elements:
            domain_name = domain_elem.get('Domain')
            available = domain_elem.get('Available', 'false').lower() == 'true'
            
            if available:
                print(f"AVAILABLE: {domain_name}")
                return True
            else:
                print(f"NOT AVAILABLE: {domain_name}")
                return False
        
        return False
    
    def deploy_to_vps(self):
        """Simulate VPS deployment process"""
        print("\nStarting VPS Deployment Process...")
        print("=" * 50)
        
        # Since NameCheap VPS deployment is typically manual,
        # we'll create the deployment instructions
        
        deployment_steps = [
            "1. Login to NameCheap account",
            "2. Navigate to Hosting > VPS",
            "3. Select Stellar Plus plan ($19.98/month)",
            "4. Choose Phoenix, AZ location",
            "5. Select Ubuntu 22.04 LTS",
            "6. Configure SSH keys",
            "7. Deploy VPS instance",
            "8. Install GenX Trading Platform"
        ]
        
        print("VPS Deployment Steps:")
        for step in deployment_steps:
            print(f"  {step}")
            time.sleep(1)  # Simulate processing time
        
        # Generate deployment script
        self.generate_vps_setup_script()
        
        print("\nVPS deployment instructions generated!")
        return True
    
    def generate_vps_setup_script(self):
        """Generate VPS setup script"""
        setup_script = '''#!/bin/bash
# GenX Trading Platform - VPS Setup Script
# Run this on your NameCheap VPS after deployment

echo "Starting GenX Trading Platform setup on NameCheap VPS..."

# Update system
sudo apt update && sudo apt upgrade -y

# Install Python 3.9+
sudo apt install -y python3 python3-pip python3-venv git nginx

# Create application directory
sudo mkdir -p /opt/genx-trading
sudo chown $USER:$USER /opt/genx-trading
cd /opt/genx-trading

# Clone or upload trading platform
# git clone https://github.com/A6-9V/GenX_FX.git .

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install fastapi uvicorn requests python-multipart

# Create systemd service
sudo tee /etc/systemd/system/genx-trading.service > /dev/null <<EOF
[Unit]
Description=GenX Trading Platform
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=/opt/genx-trading
Environment=PATH=/opt/genx-trading/venv/bin
ExecStart=/opt/genx-trading/venv/bin/python -m uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Configure Nginx reverse proxy
sudo tee /etc/nginx/sites-available/genx-trading > /dev/null <<EOF
server {
    listen 80;
    server_name _;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

# Enable site
sudo ln -s /etc/nginx/sites-available/genx-trading /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Configure firewall
sudo ufw allow ssh
sudo ufw allow http
sudo ufw allow https
sudo ufw --force enable

# Start services
sudo systemctl daemon-reload
sudo systemctl enable genx-trading
sudo systemctl start genx-trading
sudo systemctl restart nginx

echo "GenX Trading Platform setup complete!"
echo "Access your platform at: http://YOUR_VPS_IP/"
'''
        
        with open('namecheap_vps_setup.sh', 'w') as f:
            f.write(setup_script)
        
        print("Generated: namecheap_vps_setup.sh")
        print("Upload this script to your VPS and run: chmod +x namecheap_vps_setup.sh && ./namecheap_vps_setup.sh")

def main():
    """Main deployment function"""
    print("GenX Trading Platform - NameCheap VPS Deployment")
    print("=" * 60)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    deployer = NameCheapVPSDeployer()
    
    # Check credentials
    if not deployer.check_credentials():
        print("\nFailed: Missing NameCheap credentials")
        print("Set credentials with:")
        print('$env:NAMECHEAP_API_USER = "LengNU"')
        print('$env:NAMECHEAP_API_KEY = "your_api_key"')
        print('$env:NAMECHEAP_USERNAME = "LengNU"')
        print('$env:NAMECHEAP_CLIENT_IP = "117.20.115.126"')
        return False
    
    # Test API connection
    if not deployer.test_api_connection():
        print("\nFailed: Could not connect to NameCheap API")
        return False
    
    # Get VPS plans
    deployer.get_available_plans()
    
    # Check domain availability
    deployer.check_domain_availability("genxfx.com")
    
    # Deploy to VPS
    deployer.deploy_to_vps()
    
    print("\nNameCheap deployment process completed!")
    print("Next steps:")
    print("1. Login to NameCheap and deploy VPS manually")
    print("2. Upload and run the generated setup script")
    print("3. Configure domain DNS to point to VPS IP")
    
    return True

if __name__ == "__main__":
    main()