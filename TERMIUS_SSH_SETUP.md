# Termius SSH Configuration for GenX Trading Platform

# Remote Host Connection Setup

## 🔑 SSH Key Information

**SSH Key Type**: ssh-ed25519
**Public Key**: AAAAC3NzaC1lZDI1NTE5AAAAICw9/G//98IiSdsfAyn2tYS0ip9rE5wB6UAV1iue4dFm
**Email**: <genxapitrading@gmail.com>
**Port**: 8080

## 📋 Termius Host Configuration

### Host Details

- **Host Name**: GenX Trading VPS
- **Hostname/IP**: [TO BE CONFIGURED AFTER VPS DEPLOYMENT]
- **Port**: 8080
- **Username**: root (or ubuntu)
- **Authentication**: SSH Key

### SSH Key Setup

1. **Key Type**: ED25519
2. **Public Key**: ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAICw9/G//98IiSdsfAyn2tYS0ip9rE5wB6UAV1iue4dFm <genxapitrading@gmail.com>
3. **Private Key**: [REQUIRED - Generate matching private key]

## 🛠️ Setup Steps

### Step 1: Generate SSH Key Pair

```bash
# Generate new ED25519 key pair for GenX Trading
ssh-keygen -t ed25519 -C "genxapitrading@gmail.com" -f ~/.ssh/genx_trading_ed25519

# This will create:
# ~/.ssh/genx_trading_ed25519 (private key)
# ~/.ssh/genx_trading_ed25519.pub (public key)
```

### Step 2: Configure SSH Config

```bash
# Add to ~/.ssh/config
Host genx-trading-vps
    HostName [VPS_IP_ADDRESS]
    Port 8080
    User root
    IdentityFile ~/.ssh/genx_trading_ed25519
    IdentitiesOnly yes
    ServerAliveInterval 60
    ServerAliveCountMax 3
```

### Step 3: Termius Configuration

1. **Open Termius App**
2. **Add New Host**:
   - Label: "GenX Trading VPS"
   - Address: [VPS IP from deployment]
   - Port: 8080
   - Username: root
3. **Add SSH Key**:
   - Import private key: genx_trading_ed25519
   - Assign to host
4. **Connect**

## 🔗 Integration with VPS Deployment

### NameCheap VPS Integration

When deploying via our NameCheap script, the SSH key will be automatically configured:

```bash
# In deploy_namecheap_vps.sh
SSH_PUBLIC_KEY="ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAICw9/G//98IiSdsfAyn2tYS0ip9rE5wB6UAV1iue4dFm genxapitrading@gmail.com"
SSH_PORT=8080
```

### Vultr VPS Integration

```bash
# In deploy_vultr_vps.sh
VULTR_SSH_KEY_NAME="genx-trading-key"
VULTR_SSH_PORT=8080
```

### Google Cloud Integration

```bash
# In deploy_gcp_multi_account.sh
GCP_SSH_KEY_PATH="~/.ssh/genx_trading_ed25519.pub"
GCP_SSH_PORT=8080
```

## 🔐 Security Configuration

### SSH Hardening (Applied automatically in deployment)

```bash
# /etc/ssh/sshd_config modifications
Port 8080
PermitRootLogin prohibit-password
PasswordAuthentication no
PubkeyAuthentication yes
AuthorizedKeysFile .ssh/authorized_keys
MaxAuthTries 3
MaxSessions 2
ClientAliveInterval 300
ClientAliveCountMax 2
```

### Firewall Rules

```bash
# UFW configuration (auto-applied)
ufw allow 8080/tcp   # SSH
ufw allow 8000/tcp   # GenX API
ufw allow 443/tcp    # HTTPS
ufw allow 80/tcp     # HTTP
ufw enable
```

## 📱 Termius Mobile/Desktop Setup

### Mobile App Configuration

1. **Download Termius**: iOS/Android app store
2. **Account Setup**: Create Termius account
3. **Import Configuration**:
   - Use sharing link format
   - Import SSH keys
   - Sync across devices

### Desktop Application

1. **Download**: <https://termius.com/>
2. **Import Keys**: Drag-drop private key file
3. **Host Configuration**: Same as mobile

## 🚀 Quick Connect Commands

### Direct SSH (Terminal)

```bash
# Connect to VPS once deployed
ssh -p 8080 -i ~/.ssh/genx_trading_ed25519 root@[VPS_IP]

# Port forward GenX API
ssh -p 8080 -L 8000:localhost:8000 -i ~/.ssh/genx_trading_ed25519 root@[VPS_IP]
```

### Termius Command Line

```bash
# Install Termius CLI
npm install -g @termius/cli

# Connect via Termius
termius connect genx-trading-vps
```

## 🔧 Troubleshooting

### Common Issues

1. **Port 8080 blocked**: Check VPS firewall
2. **Key permission error**: `chmod 600 ~/.ssh/genx_trading_ed25519`
3. **Connection timeout**: Verify VPS is running
4. **Authentication failed**: Check public key in authorized_keys

### Debug Commands

```bash
# Test SSH connection with verbose output
ssh -v -p 8080 -i ~/.ssh/genx_trading_ed25519 root@[VPS_IP]

# Check SSH key fingerprint
ssh-keygen -lf ~/.ssh/genx_trading_ed25519.pub
```

## 📊 Next Steps

1. **Complete VPS Deployment**: Use NameCheap/Vultr/GCP scripts
2. **Get VPS IP Address**: From deployment output
3. **Update Termius Configuration**: With actual IP
4. **Test Connection**: Verify SSH access
5. **Deploy GenX Platform**: Access via Termius for monitoring

---

**Note**: The Termius sharing link appears to have formatting issues. The SSH key and email are extracted, but you'll need to:

1. Generate the corresponding private key
2. Get the actual VPS IP from deployment
3. Update Termius with correct connection details
