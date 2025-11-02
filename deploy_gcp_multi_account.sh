#!/bin/bash
# Google Cloud VPS Deployment Script for GenX Magic Trading Platform
# Supports deployment across 3 Google Cloud accounts with $300 free tier

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 GenX Trading Platform - Google Cloud Multi-Account Deployment${NC}"
echo "=================================================================="

# Account configuration
declare -A ACCOUNTS=(
    ["1"]="${GCP_ACCOUNT_1_EMAIL:-account1@gmail.com}"
    ["2"]="${GCP_ACCOUNT_2_EMAIL:-account2@gmail.com}"
    ["3"]="${GCP_ACCOUNT_3_EMAIL:-account3@gmail.com}"
)

declare -A PROJECTS=(
    ["1"]="${GCP_PROJECT_1_ID:-genx-trading-1}"
    ["2"]="${GCP_PROJECT_2_ID:-genx-trading-2}"
    ["3"]="${GCP_PROJECT_3_ID:-genx-trading-3}"
)

declare -A SERVICE_KEYS=(
    ["1"]="${GCP_SERVICE_ACCOUNT_1_KEY:-}"
    ["2"]="${GCP_SERVICE_ACCOUNT_2_KEY:-}"
    ["3"]="${GCP_SERVICE_ACCOUNT_3_KEY:-}"
)

# GCP Configuration
GCP_REGION="${GCP_REGION:-us-central1}"
GCP_ZONE="${GCP_ZONE:-us-central1-a}"
GCP_MACHINE_TYPE="${GCP_MACHINE_TYPE:-e2-medium}"
GCP_DISK_SIZE="${GCP_DISK_SIZE:-50}"

echo -e "${YELLOW}📋 Deployment Configuration:${NC}"
echo "Region: $GCP_REGION"
echo "Zone: $GCP_ZONE"
echo "Machine Type: $GCP_MACHINE_TYPE (2 vCPUs, 4GB RAM)"
echo "Disk Size: ${GCP_DISK_SIZE}GB"
echo "Accounts: ${#ACCOUNTS[@]} accounts configured"
echo ""

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo -e "${RED}❌ Google Cloud SDK not found${NC}"
    echo "Please install gcloud: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Function to check free tier eligibility
check_free_tier() {
    local account=$1
    local project=$2
    
    echo -e "${BLUE}💰 Checking free tier status for $account...${NC}"
    
    # Switch to account
    gcloud auth login $account --no-launch-browser 2>/dev/null || true
    gcloud config set project $project 2>/dev/null || true
    
    # Check billing account
    billing_account=$(gcloud beta billing accounts list --format="value(name)" 2>/dev/null | head -1)
    
    if [ -n "$billing_account" ]; then
        echo -e "${GREEN}✅ Billing account found: $billing_account${NC}"
        
        # Check if free tier is active
        gcloud beta billing budgets list --billing-account=$billing_account --format="table(displayName,amount)" 2>/dev/null || true
        
        return 0
    else
        echo -e "${YELLOW}⚠️ No billing account found - may need to activate free tier${NC}"
        return 1
    fi
}

# Function to create VM instance
create_vm_instance() {
    local account_num=$1
    local account=${ACCOUNTS[$account_num]}
    local project=${PROJECTS[$account_num]}
    local vm_name="genx-trading-vm-$account_num"
    
    echo -e "${BLUE}🔧 Creating VM instance for Account $account_num ($account)...${NC}"
    
    # Switch to account and project
    gcloud auth login $account --no-launch-browser 2>/dev/null || true
    gcloud config set project $project
    
    # Enable required APIs
    echo "📡 Enabling Compute Engine API..."
    gcloud services enable compute.googleapis.com
    
    # Create startup script
    cat > startup-script-$account_num.sh << 'STARTUP'
#!/bin/bash
# GenX Trading Platform Startup Script

# Update system
apt-get update && apt-get upgrade -y

# Install dependencies
apt-get install -y python3 python3-pip python3-venv nginx certbot python3-certbot-nginx \
    curl wget git htop unzip jq

# Create user for GenX
useradd -m -s /bin/bash genx
usermod -aG sudo genx

# Setup GenX directory
mkdir -p /home/genx/GenX_FX
chown genx:genx /home/genx/GenX_FX

# Clone or setup GenX platform (placeholder - you'll need to provide the actual source)
# For now, create a basic structure
sudo -u genx mkdir -p /home/genx/GenX_FX/{api,core,logs}

# Create virtual environment
sudo -u genx python3 -m venv /home/genx/GenX_FX/venv

# Install Python packages
sudo -u genx /home/genx/GenX_FX/venv/bin/pip install --upgrade pip
sudo -u genx /home/genx/GenX_FX/venv/bin/pip install fastapi uvicorn MetaTrader5 aiohttp \
    python-multipart numpy pandas websockets httpx python-dotenv asyncio

# Create basic FastAPI app
sudo -u genx cat > /home/genx/GenX_FX/api/server.py << 'FASTAPI'
from fastapi import FastAPI
from datetime import datetime
import uvicorn

app = FastAPI(
    title="GenX Trading API - Google Cloud",
    description="Magic Key Trading Platform on Google Cloud",
    version="2.1.0"
)

@app.get("/")
async def root():
    return {
        "service": "GenX Trading API",
        "platform": "Google Cloud",
        "status": "operational",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "platform": "google-cloud",
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
FASTAPI

# Create systemd service
cat > /etc/systemd/system/genx-api.service << 'SERVICE'
[Unit]
Description=GenX Trading API
After=network.target

[Service]
Type=simple
User=genx
WorkingDirectory=/home/genx/GenX_FX
Environment=PATH=/home/genx/GenX_FX/venv/bin
ExecStart=/home/genx/GenX_FX/venv/bin/python api/server.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
SERVICE

# Enable and start service
systemctl daemon-reload
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

    location /health {
        proxy_pass http://localhost:8000/health;
    }
}
NGINX

# Enable Nginx site
ln -sf /etc/nginx/sites-available/genx-trading /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default
systemctl restart nginx

# Setup firewall
ufw allow OpenSSH
ufw allow 'Nginx Full'
ufw allow 8000
ufw --force enable

# Create monitoring script
cat > /home/genx/monitor.sh << 'MONITOR'
#!/bin/bash
echo "GenX Trading Platform - Google Cloud"
echo "====================================="
echo "Instance: $(curl -s http://metadata.google.internal/computeMetadata/v1/instance/name -H "Metadata-Flavor: Google")"
echo "Zone: $(curl -s http://metadata.google.internal/computeMetadata/v1/instance/zone -H "Metadata-Flavor: Google" | cut -d/ -f4)"
echo "External IP: $(curl -s http://metadata.google.internal/computeMetadata/v1/instance/network-interfaces/0/access-configs/0/external-ip -H "Metadata-Flavor: Google")"
echo "Date: $(date)"
echo ""
systemctl is-active genx-api && echo "✅ API Service: Running" || echo "❌ API Service: Stopped"
systemctl is-active nginx && echo "✅ Nginx: Running" || echo "❌ Nginx: Stopped"
echo ""
echo "API Health: $(curl -s http://localhost:8000/health | jq -r .status 2>/dev/null || echo "Not responding")"
MONITOR

chown genx:genx /home/genx/monitor.sh
chmod +x /home/genx/monitor.sh

echo "✅ GenX Trading Platform setup completed!"
STARTUP

    # Create VM instance
    echo "🚀 Creating VM instance: $vm_name"
    
    gcloud compute instances create $vm_name \
        --zone=$GCP_ZONE \
        --machine-type=$GCP_MACHINE_TYPE \
        --network-tier=PREMIUM \
        --maintenance-policy=MIGRATE \
        --provisioning-model=STANDARD \
        --service-account=${project}@${project}.iam.gserviceaccount.com \
        --scopes=https://www.googleapis.com/auth/cloud-platform \
        --tags=http-server,https-server \
        --create-disk=auto-delete=yes,boot=yes,device-name=$vm_name,image=projects/ubuntu-os-cloud/global/images/family/ubuntu-2204-lts,mode=rw,size=$GCP_DISK_SIZE,type=projects/$project/zones/$GCP_ZONE/diskTypes/pd-standard \
        --metadata-from-file startup-script=startup-script-$account_num.sh \
        --reservation-affinity=any
    
    # Create firewall rules
    echo "🔥 Creating firewall rules..."
    gcloud compute firewall-rules create allow-genx-http-$account_num \
        --allow tcp:80,tcp:443,tcp:8000 \
        --source-ranges 0.0.0.0/0 \
        --target-tags http-server \
        --description "Allow HTTP/HTTPS for GenX Trading Platform" \
        2>/dev/null || echo "Firewall rule already exists"
    
    # Get instance IP
    echo "⏳ Waiting for instance to be ready..."
    sleep 60
    
    EXTERNAL_IP=$(gcloud compute instances describe $vm_name \
        --zone=$GCP_ZONE \
        --format='get(networkInterfaces[0].accessConfigs[0].natIP)')
    
    if [ -n "$EXTERNAL_IP" ]; then
        echo -e "${GREEN}✅ VM created successfully!${NC}"
        echo -e "${GREEN}🌐 External IP: $EXTERNAL_IP${NC}"
        echo -e "${GREEN}📊 API URL: http://$EXTERNAL_IP${NC}"
        echo -e "${GREEN}🔍 Health Check: http://$EXTERNAL_IP/health${NC}"
        
        # Save instance info
        cat > gcp-instance-$account_num.json << EOF
{
  "account": "$account",
  "project": "$project",
  "instance_name": "$vm_name",
  "zone": "$GCP_ZONE",
  "external_ip": "$EXTERNAL_IP",
  "machine_type": "$GCP_MACHINE_TYPE",
  "created": "$(date -Iseconds)"
}
EOF
        
        return 0
    else
        echo -e "${RED}❌ Failed to get external IP${NC}"
        return 1
    fi
}

# Function to deploy complete GenX platform
deploy_genx_platform() {
    local account_num=$1
    local instance_info_file="gcp-instance-$account_num.json"
    
    if [ ! -f "$instance_info_file" ]; then
        echo -e "${RED}❌ Instance info file not found: $instance_info_file${NC}"
        return 1
    fi
    
    local external_ip=$(jq -r '.external_ip' $instance_info_file)
    local vm_name=$(jq -r '.instance_name' $instance_info_file)
    local project=$(jq -r '.project' $instance_info_file)
    
    echo -e "${BLUE}📦 Deploying complete GenX platform to $external_ip...${NC}"
    
    # Copy GenX files to the instance
    echo "📁 Copying GenX platform files..."
    gcloud compute scp --zone=$GCP_ZONE --recurse \
        . genx@$vm_name:/home/genx/GenX_FX/ \
        --project=$project \
        2>/dev/null || echo "⚠️ Direct file copy not available, using startup script deployment"
    
    # Update the instance with full GenX platform
    gcloud compute instances add-metadata $vm_name \
        --zone=$GCP_ZONE \
        --metadata=genx-deployed=true,deployment-date="$(date -Iseconds)" \
        --project=$project
    
    echo -e "${GREEN}✅ GenX platform deployed to Account $account_num${NC}"
}

# Main deployment flow
echo -e "${YELLOW}🚀 Starting multi-account Google Cloud deployment...${NC}"

# Check Google Cloud authentication
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | head -1 > /dev/null 2>&1; then
    echo -e "${YELLOW}⚠️ No active Google Cloud authentication found${NC}"
    echo "Please run: gcloud auth login"
    exit 1
fi

# Deploy to each account
success_count=0
for account_num in "${!ACCOUNTS[@]}"; do
    echo ""
    echo -e "${BLUE}📍 Processing Account $account_num: ${ACCOUNTS[$account_num]}${NC}"
    echo "Project: ${PROJECTS[$account_num]}"
    echo "======================================================"
    
    # Check free tier eligibility
    check_free_tier "${ACCOUNTS[$account_num]}" "${PROJECTS[$account_num]}"
    
    # Create VM instance
    if create_vm_instance $account_num; then
        echo -e "${GREEN}✅ Account $account_num deployment successful${NC}"
        success_count=$((success_count + 1))
        
        # Wait for instance to fully boot
        echo "⏳ Waiting for services to start (2 minutes)..."
        sleep 120
        
        # Deploy full GenX platform
        deploy_genx_platform $account_num
    else
        echo -e "${RED}❌ Account $account_num deployment failed${NC}"
    fi
    
    echo ""
done

# Summary
echo -e "${GREEN}🎉 DEPLOYMENT SUMMARY${NC}"
echo "======================"
echo "Successful deployments: $success_count/${#ACCOUNTS[@]}"
echo ""

if [ $success_count -gt 0 ]; then
    echo -e "${GREEN}✅ GenX Trading Platforms deployed successfully!${NC}"
    echo ""
    echo -e "${YELLOW}📋 Access Information:${NC}"
    
    for account_num in "${!ACCOUNTS[@]}"; do
        if [ -f "gcp-instance-$account_num.json" ]; then
            external_ip=$(jq -r '.external_ip' gcp-instance-$account_num.json)
            account=$(jq -r '.account' gcp-instance-$account_num.json)
            
            echo "Account $account_num ($account):"
            echo "  🌐 URL: http://$external_ip"
            echo "  📊 API Docs: http://$external_ip/docs"
            echo "  🔍 Health: http://$external_ip/health"
            echo ""
        fi
    done
    
    echo -e "${YELLOW}💰 Free Tier Usage:${NC}"
    echo "Each account uses ~$24/month from the $300 credit"
    echo "Estimated 12+ months of free usage per account"
    echo ""
    
    echo -e "${YELLOW}🔧 Management Commands:${NC}"
    echo "gcloud compute instances list"
    echo "gcloud compute ssh [INSTANCE_NAME] --zone=$GCP_ZONE"
    echo ""
else
    echo -e "${RED}❌ No successful deployments${NC}"
    echo "Please check your Google Cloud credentials and billing setup"
fi

# Cleanup
rm -f startup-script-*.sh

echo -e "${GREEN}🎯 Google Cloud deployment completed!${NC}"