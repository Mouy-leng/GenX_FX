#!/bin/bash
# Vultr VPS MT4 FBS Deployment Script
# Ubuntu 22.04 LTS with Wine for MT4

echo "Starting MT4 FBS deployment on Vultr VPS..."
echo "Timestamp: $(date)"

# Update system
echo "Updating system packages..."
apt update && apt upgrade -y

# Install Wine for MT4
echo "Installing Wine for MetaTrader 4..."
dpkg --add-architecture i386
wget -O - https://dl.winehq.org/wine-builds/winehq.key | apt-key add -
echo "deb https://dl.winehq.org/wine-builds/ubuntu/ $(lsb_release -cs) main" >> /etc/apt/sources.list
apt update
apt install -y winehq-stable

# Install additional dependencies
echo "Installing dependencies..."
apt install -y curl wget unzip xvfb python3 python3-pip nginx git

# Create trading user
echo "Creating trading user..."
useradd -m -s /bin/bash trader
usermod -aG sudo trader

# Download MT4 from FBS
echo "Downloading MetaTrader 4..."
cd /home/trader
wget -O mt4setup.exe "https://download.metatrader.com/cdn/web/fbs.inc/mt4/fbsmt4setup.exe"

# Install MT4 with Wine
echo "Installing MT4..."
sudo -u trader DISPLAY=:99 wine mt4setup.exe /S

# Setup Xvfb for headless operation
echo "Setting up virtual display..."
cat > /etc/systemd/system/xvfb.service << EOF
[Unit]
Description=Virtual Frame Buffer X Server
After=network.target

[Service]
Type=simple
User=trader
ExecStart=/usr/bin/Xvfb :99 -screen 0 1024x768x24
Restart=always

[Install]
WantedBy=multi-user.target
EOF

systemctl enable xvfb
systemctl start xvfb

# Install Python packages
echo "Installing Python packages..."
pip3 install fastapi uvicorn pandas numpy requests websockets

# Create MT4 bridge script
cat > /home/trader/genx_mt4_bridge.py << 'BRIDGE_EOF'
#!/usr/bin/env python3
"""
GenX MT4 Bridge - Connect MT4 to GenX Platform
"""
import time
import requests
import json
from datetime import datetime

class GenXMT4Bridge:
    def __init__(self):
        self.genx_url = "http://localhost:8000"
        self.mt4_path = "/home/trader/.wine/drive_c/Program Files (x86)/FBS MetaTrader 4/"
        
    def start_bridge(self):
        print("GenX MT4 Bridge starting...")
        while True:
            try:
                # Check GenX platform status
                response = requests.get(f"{self.genx_url}/health", timeout=5)
                if response.status_code == 200:
                    print(f"GenX platform online - {datetime.now()}")
                else:
                    print(f"GenX platform issues - {response.status_code}")
                
                # MT4 bridge logic here
                time.sleep(30)
                
            except Exception as e:
                print(f"Bridge error: {e}")
                time.sleep(60)

if __name__ == "__main__":
    bridge = GenXMT4Bridge()
    bridge.start_bridge()
BRIDGE_EOF

chmod +x /home/trader/genx_mt4_bridge.py

# Setup MT4 service
cat > /etc/systemd/system/mt4.service << EOF
[Unit]
Description=MetaTrader 4 Service
After=xvfb.service
Requires=xvfb.service

[Service]
Type=simple
User=trader
Environment=DISPLAY=:99
WorkingDirectory=/home/trader
ExecStart=/usr/bin/wine /home/trader/.wine/drive_c/Program Files (x86)/FBS MetaTrader 4/terminal.exe
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Clone GenX platform
echo "Setting up GenX platform..."
cd /home/trader
git clone https://github.com/A6-9V/GenX_FX.git || echo "Repo clone failed, manual setup required"
cd GenX_FX

# Create systemd service for GenX
cat > /etc/systemd/system/genx.service << EOF
[Unit]
Description=GenX Trading Platform
After=network.target

[Service]
Type=simple
User=trader
WorkingDirectory=/home/trader/GenX_FX
ExecStart=/usr/bin/python3 -m uvicorn app:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Enable services
systemctl enable mt4
systemctl enable genx
systemctl daemon-reload

# Setup firewall
echo "Configuring firewall..."
ufw allow 22    # SSH
ufw allow 80    # HTTP
ufw allow 443   # HTTPS
ufw allow 8000  # GenX API
ufw allow 8001  # GenX Admin
ufw --force enable

# Setup basic nginx
echo "Setting up nginx..."
cat > /etc/nginx/sites-available/genx << EOF
server {
    listen 80;
    server_name _;
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
    }
}
EOF

ln -sf /etc/nginx/sites-available/genx /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default
systemctl enable nginx
systemctl restart nginx

echo "MT4 FBS deployment complete!"
echo "Next steps:"
echo "  1. Configure FBS account in MT4"
echo "  2. Install Expert Advisors"
echo "  3. Start services: systemctl start mt4 genx"
echo "  4. Access GenX at: http://YOUR_VPS_IP"
