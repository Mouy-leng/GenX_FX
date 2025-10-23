#!/bin/bash
# Install GenX FX Trading Platform service on VPS

# Copy files to appropriate locations
sudo mkdir -p /opt/genx_fx
sudo cp start_trading_vps.sh /opt/genx_fx/
sudo cp docker-compose.yml /opt/genx_fx/
sudo chmod +x /opt/genx_fx/start_trading_vps.sh

# Copy and enable systemd service
sudo cp genx-fx.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable genx-fx
sudo systemctl start genx-fx

# Check status
echo "Service status:"
sudo systemctl status genx-fx

echo "You can check logs with:"
echo "tail -f /var/log/genx_fx/startup.log"
echo "tail -f /var/log/genx_fx/service.log"