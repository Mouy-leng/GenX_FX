#!/bin/bash
# GenX Trading Platform - SSH Key Setup for Termius
# This script generates SSH keys and configures Termius connection

set -e

echo "🔑 GenX Trading Platform - SSH Key Setup for Termius"
echo "=================================================="

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Configuration
SSH_KEY_NAME="genx_trading_ed25519"
SSH_KEY_PATH="$HOME/.ssh/$SSH_KEY_NAME"
SSH_EMAIL="genxapitrading@gmail.com"
SSH_PORT="8080"

# Your existing public key from Termius link
EXISTING_PUBLIC_KEY="ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAICw9/G//98IiSdsfAyn2tYS0ip9rE5wB6UAV1iue4dFm genxapitrading@gmail.com"

echo -e "${YELLOW}Setting up SSH keys for Termius connection...${NC}"

# Create .ssh directory if it doesn't exist
mkdir -p "$HOME/.ssh"
chmod 700 "$HOME/.ssh"

# Check if SSH key already exists
if [ -f "$SSH_KEY_PATH" ]; then
    echo -e "${YELLOW}SSH key already exists at $SSH_KEY_PATH${NC}"
    echo "Do you want to:"
    echo "1. Use existing key"
    echo "2. Generate new key (will backup existing)"
    read -p "Choose option (1 or 2): " choice
    
    if [ "$choice" = "2" ]; then
        echo -e "${YELLOW}Backing up existing key...${NC}"
        mv "$SSH_KEY_PATH" "$SSH_KEY_PATH.backup.$(date +%Y%m%d_%H%M%S)"
        mv "$SSH_KEY_PATH.pub" "$SSH_KEY_PATH.pub.backup.$(date +%Y%m%d_%H%M%S)"
    else
        echo -e "${GREEN}Using existing SSH key${NC}"
    fi
fi

# Generate new SSH key if needed
if [ ! -f "$SSH_KEY_PATH" ]; then
    echo -e "${YELLOW}Generating new ED25519 SSH key...${NC}"
    ssh-keygen -t ed25519 -C "$SSH_EMAIL" -f "$SSH_KEY_PATH" -N ""
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ SSH key generated successfully${NC}"
    else
        echo -e "${RED}❌ Failed to generate SSH key${NC}"
        exit 1
    fi
fi

# Set proper permissions
chmod 600 "$SSH_KEY_PATH"
chmod 644 "$SSH_KEY_PATH.pub"

# Display public key
echo -e "${GREEN}📋 Your SSH Public Key:${NC}"
echo "----------------------------------------"
cat "$SSH_KEY_PATH.pub"
echo "----------------------------------------"

# Create SSH config entry
SSH_CONFIG="$HOME/.ssh/config"
echo -e "${YELLOW}Updating SSH config...${NC}"

# Backup existing config
if [ -f "$SSH_CONFIG" ]; then
    cp "$SSH_CONFIG" "$SSH_CONFIG.backup.$(date +%Y%m%d_%H%M%S)"
fi

# Add GenX Trading VPS configuration
cat >> "$SSH_CONFIG" << EOF

# GenX Trading VPS Configuration
Host genx-trading-vps
    HostName [VPS_IP_TO_BE_UPDATED]
    Port $SSH_PORT
    User root
    IdentityFile $SSH_KEY_PATH
    IdentitiesOnly yes
    ServerAliveInterval 60
    ServerAliveCountMax 3
    StrictHostKeyChecking no
    UserKnownHostsFile /dev/null

# NameCheap VPS
Host genx-namecheap
    HostName [NAMECHEAP_VPS_IP]
    Port $SSH_PORT
    User root
    IdentityFile $SSH_KEY_PATH
    IdentitiesOnly yes

# Vultr VPS  
Host genx-vultr
    HostName [VULTR_VPS_IP]
    Port $SSH_PORT
    User root
    IdentityFile $SSH_KEY_PATH
    IdentitiesOnly yes

# Google Cloud VPS
Host genx-gcp
    HostName [GCP_VPS_IP]
    Port $SSH_PORT
    User root
    IdentityFile $SSH_KEY_PATH
    IdentitiesOnly yes
EOF

echo -e "${GREEN}✅ SSH config updated${NC}"

# Create Termius import file
TERMIUS_CONFIG="./termius_genx_config.json"
echo -e "${YELLOW}Creating Termius configuration file...${NC}"

cat > "$TERMIUS_CONFIG" << EOF
{
  "version": "1.0",
  "hosts": [
    {
      "label": "GenX Trading VPS",
      "address": "[VPS_IP_TO_BE_UPDATED]",
      "port": $SSH_PORT,
      "username": "root",
      "ssh_key": "$SSH_KEY_NAME",
      "tags": ["genx", "trading", "production"]
    },
    {
      "label": "GenX NameCheap VPS",
      "address": "[NAMECHEAP_VPS_IP]",
      "port": $SSH_PORT,
      "username": "root", 
      "ssh_key": "$SSH_KEY_NAME",
      "tags": ["genx", "namecheap", "trading"]
    },
    {
      "label": "GenX Vultr VPS",
      "address": "[VULTR_VPS_IP]",
      "port": $SSH_PORT,
      "username": "root",
      "ssh_key": "$SSH_KEY_NAME", 
      "tags": ["genx", "vultr", "trading"]
    },
    {
      "label": "GenX Google Cloud VPS",
      "address": "[GCP_VPS_IP]",
      "port": $SSH_PORT,
      "username": "root",
      "ssh_key": "$SSH_KEY_NAME",
      "tags": ["genx", "gcp", "trading"]
    }
  ],
  "ssh_keys": [
    {
      "name": "$SSH_KEY_NAME",
      "private_key_path": "$SSH_KEY_PATH",
      "public_key_path": "$SSH_KEY_PATH.pub"
    }
  ]
}
EOF

echo -e "${GREEN}✅ Termius configuration created: $TERMIUS_CONFIG${NC}"

# Create PowerShell script for Windows users
POWERSHELL_SCRIPT="./setup_ssh_windows.ps1"
echo -e "${YELLOW}Creating PowerShell setup script...${NC}"

cat > "$POWERSHELL_SCRIPT" << 'EOF'
# GenX Trading Platform - SSH Setup for Windows/Termius
Write-Host "🔑 GenX Trading Platform - SSH Setup for Windows" -ForegroundColor Green

# Create .ssh directory
$sshDir = "$env:USERPROFILE\.ssh"
if (-not (Test-Path $sshDir)) {
    New-Item -ItemType Directory -Path $sshDir -Force
    Write-Host "✅ Created .ssh directory" -ForegroundColor Green
}

# Generate SSH key
$keyPath = "$sshDir\genx_trading_ed25519"
if (-not (Test-Path $keyPath)) {
    Write-Host "Generating SSH key..." -ForegroundColor Yellow
    ssh-keygen -t ed25519 -C "genxapitrading@gmail.com" -f $keyPath -N '""'
    Write-Host "✅ SSH key generated" -ForegroundColor Green
}

# Display public key
Write-Host "`n📋 Your SSH Public Key:" -ForegroundColor Cyan
Write-Host "----------------------------------------" -ForegroundColor Gray
Get-Content "$keyPath.pub"
Write-Host "----------------------------------------" -ForegroundColor Gray

# Create SSH config
$configContent = @"

# GenX Trading VPS Configuration
Host genx-trading-vps
    HostName [VPS_IP_TO_BE_UPDATED]
    Port 8080
    User root
    IdentityFile $keyPath
    IdentitiesOnly yes
    ServerAliveInterval 60
    ServerAliveCountMax 3
"@

$configPath = "$sshDir\config"
Add-Content -Path $configPath -Value $configContent
Write-Host "✅ SSH config updated" -ForegroundColor Green

Write-Host "`n🚀 Next Steps:" -ForegroundColor Yellow
Write-Host "1. Deploy VPS using our deployment scripts" -ForegroundColor White
Write-Host "2. Update VPS IP in SSH config and Termius" -ForegroundColor White
Write-Host "3. Import SSH key to Termius app" -ForegroundColor White
Write-Host "4. Connect via Termius" -ForegroundColor White
EOF

echo -e "${GREEN}✅ PowerShell script created: $POWERSHELL_SCRIPT${NC}"

# Create instructions file
INSTRUCTIONS_FILE="./TERMIUS_CONNECTION_GUIDE.md"
echo -e "${YELLOW}Creating connection guide...${NC}"

cat > "$INSTRUCTIONS_FILE" << EOF
# Termius Connection Guide for GenX Trading Platform

## 📱 Termius App Setup

### Step 1: Install Termius
- **Mobile**: Download from App Store/Google Play
- **Desktop**: Download from https://termius.com/

### Step 2: Import SSH Key
1. Open Termius app
2. Go to **Settings** → **Keys**
3. Click **+** to add new key
4. **Import** or **Create** key:
   - Name: \`genx_trading_ed25519\`
   - Import private key file: \`$SSH_KEY_PATH\`

### Step 3: Add Hosts
For each VPS (after deployment):

1. **Add New Host**:
   - Label: "GenX Trading VPS"
   - Address: [VPS IP from deployment]
   - Port: 8080
   - Username: root

2. **Authentication**:
   - Select SSH Key
   - Choose: \`genx_trading_ed25519\`

3. **Save & Connect**

## 🔗 VPS Deployment Integration

### After VPS Deployment
When you deploy VPS using our scripts, you'll get IP addresses:

\`\`\`bash
# NameCheap VPS
./deploy_namecheap_vps.sh
# Output: VPS IP: xxx.xxx.xxx.xxx

# Vultr VPS  
./deploy_vultr_vps.sh
# Output: VPS IP: yyy.yyy.yyy.yyy

# Google Cloud VPS
./deploy_gcp_multi_account.sh
# Output: VPS IPs: zzz.zzz.zzz.zzz (3 instances)
\`\`\`

### Update SSH Config
Replace placeholders in \`~/.ssh/config\`:
\`\`\`bash
# Update VPS IP addresses
sed -i 's/\[VPS_IP_TO_BE_UPDATED\]/ACTUAL_VPS_IP/g' ~/.ssh/config
\`\`\`

### Update Termius
1. Edit each host in Termius
2. Update IP address 
3. Test connection

## 🚀 Quick Connect

### Via SSH (Terminal)
\`\`\`bash
# Connect to deployed VPS
ssh genx-trading-vps

# Port forward GenX API
ssh -L 8000:localhost:8000 genx-trading-vps
\`\`\`

### Via Termius
1. Select host from list
2. Click connect
3. Monitor GenX trading platform

## 🔧 Troubleshooting

### Common Issues:
- **Connection refused**: Check VPS is running
- **Permission denied**: Verify SSH key permissions
- **Port blocked**: Check firewall settings

### Debug Commands:
\`\`\`bash
# Test SSH connection
ssh -v genx-trading-vps

# Check key fingerprint
ssh-keygen -lf $SSH_KEY_PATH.pub
\`\`\`

## 📊 Integration with GenX Platform

### After Connection:
1. **Monitor Logs**: \`tail -f /var/log/genx-trading.log\`
2. **Check Status**: \`systemctl status genx-trading\`
3. **API Access**: \`curl http://localhost:8000/health\`
4. **Trading Signals**: \`curl http://localhost:8000/signals\`

---

**🔑 SSH Public Key**: 
\`$(cat "$SSH_KEY_PATH.pub")\`

**📱 Ready for Termius!** Import the private key and add hosts with VPS IPs.
EOF

echo -e "${GREEN}✅ Connection guide created: $INSTRUCTIONS_FILE${NC}"

echo ""
echo -e "${GREEN}🎉 SSH Setup Complete!${NC}"
echo ""
echo -e "${YELLOW}📋 Summary:${NC}"
echo "✅ SSH key pair generated: $SSH_KEY_PATH"
echo "✅ SSH config updated: $SSH_CONFIG"  
echo "✅ Termius config created: $TERMIUS_CONFIG"
echo "✅ PowerShell script: $POWERSHELL_SCRIPT"
echo "✅ Connection guide: $INSTRUCTIONS_FILE"
echo ""
echo -e "${YELLOW}🚀 Next Steps:${NC}"
echo "1. Deploy VPS using our deployment scripts"
echo "2. Update VPS IP in SSH config and Termius"
echo "3. Import SSH key to Termius app"
echo "4. Connect and monitor GenX trading platform"
echo ""
echo -e "${GREEN}📱 Your SSH Public Key (for VPS deployment):${NC}"
echo "----------------------------------------"
cat "$SSH_KEY_PATH.pub"
echo "----------------------------------------"