#!/bin/bash

# GenX_FX Deployment Script for Google VM
# Run this script on your VM to deploy the backend

set -e

echo "🚀 Starting GenX_FX Deployment..."

# --- Helper Functions ---
print_status() {
    echo "🔵 $1"
}

print_success() {
    echo "✅ $1"
}

print_warning() {
    echo "⚠️  $1"
}

print_error() {
    echo "❌ $1" >&2
    exit 1
}


# --- Pre-flight Check ---
print_status "Checking for required environment variables..."
required_vars=(
    "DOCKER_USERNAME" "DOCKER_PASSWORD" "GEMINI_API_KEY" "TELEGRAM_BOT_TOKEN"
    "GMAIL_USER" "GMAIL_PASSWORD" "REDDIT_CLIENT_ID" "REDDIT_CLIENT_SECRET"
    "REDDIT_USERNAME" "REDDIT_PASSWORD" "FXCM_USERNAME" "FXCM_PASSWORD" "JWT_SECRET_KEY"
)
missing_vars=()
for var in "${required_vars[@]}"; do
    if [ -z "${!var}" ]; then
        missing_vars+=("$var")
    fi
done

if [ ${#missing_vars[@]} -ne 0 ]; then
    print_error "The following required environment variables are not set: ${missing_vars[*]}"
    echo "Please export them before running this script. Example: export DOCKER_USERNAME='your_user'"
    exit 1
fi
print_success "All required environment variables are present."


# --- System Setup ---
print_status "📦 Installing dependencies..."
sudo apt update
sudo apt install -y docker.io docker-compose curl wget git nginx certbot python3-certbot-nginx

print_status "🐳 Setting up Docker..."
sudo systemctl enable docker
sudo systemctl start docker
sudo usermod -aG docker $USER


# --- Project Setup ---
print_status "📁 Setting up project directory..."
mkdir -p ~/GenX_FX
cd ~/GenX_FX

print_status "🔧 Creating .env file from environment variables..."
cat > .env << EOF
# === Docker Registry Credentials ===
DOCKER_USERNAME=${DOCKER_USERNAME}
DOCKER_PASSWORD=${DOCKER_PASSWORD}
DOCKER_IMAGE=${DOCKER_IMAGE:-"keamouyleng/genx_docker"}
DOCKER_TAG=${DOCKER_TAG:-"latest"}

# === API Keys ===
GEMINI_API_KEY=${GEMINI_API_KEY}
VANTAGE_ALPHAVANTAGE_API_KEY=${VANTAGE_ALPHAVANTAGE_API_KEY}
NEWS_API_KEY=${NEWS_API_KEY}
NEWSDATA_API_KEY=${NEWSDATA_API_KEY}
FINNHUB_API_KEY=${FINNHUB_API_KEY}

# === Telegram Credentials ===
TELEGRAM_BOT_TOKEN=${TELEGRAM_BOT_TOKEN}
TELEGRAM_USER_ID=${TELEGRAM_USER_ID}

# === Gmail Credentials ===
GMAIL_USER=${GMAIL_USER}
GMAIL_PASSWORD=${GMAIL_PASSWORD}
GMAIL_APP_API_KEY=${GMAIL_APP_API_KEY}

# === Reddit Credentials ===
REDDIT_CLIENT_ID=${REDDIT_CLIENT_ID}
REDDIT_CLIENT_SECRET=${REDDIT_CLIENT_SECRET}
REDDIT_USERNAME=${REDDIT_USERNAME}
REDDIT_PASSWORD=${REDDIT_PASSWORD}
REDDIT_USER_AGENT=${REDDIT_USER_AGENT:-"GenX-Trading-Bot/1.0"}

# === FXCM Credentials ===
FXCM_USERNAME=${FXCM_USERNAME}
FXCM_PASSWORD=${FXCM_PASSWORD}
FXCM_CONNECTION_TYPE=${FXCM_CONNECTION_TYPE:-"Demo"}
FXCM_URL=${FXCM_URL:-"www.fxcorporate.com/Hosts.jsp"}

# === Security Keys ===
JWT_SECRET_KEY=${JWT_SECRET_KEY}

# === Feature Flags ===
ENABLE_NEWS_ANALYSIS=${ENABLE_NEWS_ANALYSIS:-"true"}
ENABLE_REDDIT_ANALYSIS=${ENABLE_REDDIT_ANALYSIS:-"true"}
ENABLE_WEBSOCKET_FEED=${ENABLE_WEBSOCKET_FEED:-"true"}
API_PROVIDER=${API_PROVIDER:-"gemini"}
EOF
print_success ".env file created successfully."


# --- Source Code ---
print_status "📥 Cloning GenX_FX repository..."
if [ -d "temp_genx" ]; then
    rm -rf temp_genx
fi
git clone https://github.com/Mouy-leng/GenX_FX.git temp_genx
# Use rsync to avoid issues with hidden files and permissions
rsync -a --exclude='.git' temp_genx/ .
rm -rf temp_genx
print_success "Repository cloned."


# --- Docker and Nginx Configuration ---
print_status "🐳 Creating Docker Compose configuration..."
cat > docker-compose.production.yml << 'EOF'
version: '3.8'

services:
  genx-backend:
    build: .
    container_name: genx-backend
    restart: unless-stopped
    ports:
      - "8080:8080"
    environment:
      - NODE_ENV=production
    env_file:
      - .env
    volumes:
      - ./expert-advisors:/app/expert-advisors
      - ./scripts:/app/scripts
      - ./logs:/app/logs
    networks:
      - genx-network

  nginx:
    image: nginx:alpine
    container_name: genx-nginx
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - genx-backend
    networks:
      - genx-network

networks:
  genx-network:
    driver: bridge

volumes:
  logs:
EOF
print_success "Docker Compose file created."

print_status "🌐 Creating Nginx configuration..."
cat > nginx.conf << 'EOF'
events {
    worker_connections 1024;
}

http {
    upstream genx_backend {
        server genx-backend:8080;
    }

    # HTTP to HTTPS redirect
    server {
        listen 80;
        server_name _;
        return 301 https://$host$request_uri;
    }

    # HTTPS server
    server {
        listen 443 ssl;
        server_name _;

        # Self-signed certificate (replace with Let's Encrypt for production)
        ssl_certificate /etc/nginx/ssl/nginx.crt;
        ssl_certificate_key /etc/nginx/ssl/nginx.key;

        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers HIGH:!aNULL:!MD5;

        location / {
            proxy_pass http://genx_backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        location /ws {
            proxy_pass http://genx_backend;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            proxy_set_header Host $host;
        }
    }
}
EOF
print_success "Nginx configuration created."

print_status "🔒 Setting up SSL certificate..."
mkdir -p ssl
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout ssl/nginx.key -out ssl/nginx.crt \
    -subj "/C=US/ST=State/L=City/O=GenX/CN=localhost"

# Set proper permissions
chmod 600 ssl/nginx.key
chmod 644 ssl/nginx.crt
print_success "Self-signed SSL certificate generated."
print_warning "This is a self-signed certificate, not suitable for production. Use Certbot for a trusted certificate."

# --- Build and Run ---
print_status "🏗️ Building and starting containers..."
sudo docker-compose -f docker-compose.production.yml up -d --build

print_status "⏳ Waiting for containers to start..."
sleep 30

# --- Post-deployment ---
print_status "📊 Container status:"
sudo docker ps

print_status "📋 Recent logs:"
sudo docker-compose -f docker-compose.production.yml logs --tail=20

print_success "✅ Deployment completed!"
echo "🌐 Your GenX_FX backend is now running on:"
echo "   - HTTPS: https://$(curl -s ifconfig.me)"
print_warning "You may need to accept the self-signed certificate in your browser."

echo "🔧 To view logs: sudo docker-compose -f docker-compose.production.yml logs -f"
echo "🔧 To stop: sudo docker-compose -f docker-compose.production.yml down"
echo "🔧 To restart: sudo docker-compose -f docker-compose.production.yml restart"