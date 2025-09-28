#!/bin/bash

# Quick AMP System GCS Deployment
# Simplified deployment script for rapid deployment

set -e

# Configuration
PROJECT_ID="${PROJECT_ID:-fortress-notes-omrjz}"
REGION="${REGION:-us-central1}"
SERVICE_NAME="${SERVICE_NAME:-amp-trading-system}"
BUCKET_NAME="${BUCKET_NAME:-amp-trading-system-data}"

# Check for .env.secrets and source it if it exists
if [ -f .env.secrets ]; then
    echo "🔑 Sourcing secrets from .env.secrets..."
    set -a
    source .env.secrets
    set +a
else
    echo "⚠️ .env.secrets file not found. Please create it with your credentials."
    echo "Example .env.secrets:"
    echo "export AMP_TOKEN='your_amp_token'"
    echo "export GITHUB_TOKEN='your_github_token'"
    echo "export SERVICE_ACCOUNT_KEY_JSON='{\"type\": \"service_account\", ...}'"
    exit 1
fi

# Verify that all required secrets are set
required_secrets=(
    AMP_TOKEN GITHUB_TOKEN SERVICE_ACCOUNT_KEY_JSON
)

for secret in "${required_secrets[@]}"; do
    if [ -z "${!secret}" ]; then
        echo "❌ Error: Environment variable $secret is not set." >&2
        exit 1
    fi
done

echo "🚀 Quick AMP System GCS Deployment"
echo "=================================="

# Create service account key from environment variable
if [ -z "$SERVICE_ACCOUNT_KEY_JSON" ]; then
    echo "❌ SERVICE_ACCOUNT_KEY_JSON environment variable not set."
    exit 1
fi
echo "$SERVICE_ACCOUNT_KEY_JSON" > service-account-key.json

echo "✅ Service account key created"

# Install gcloud if not available
if ! command -v gcloud &> /dev/null; then
    echo "📥 Installing Google Cloud CLI..."
    curl https://sdk.cloud.google.com | bash
    exec -l $SHELL
    source ~/.bashrc
fi

echo "✅ Google Cloud CLI ready"

# Authenticate and set project
gcloud config set project $PROJECT_ID
gcloud auth activate-service-account --key-file=service-account-key.json

echo "✅ Authenticated with Google Cloud"

# Create GCS bucket
gsutil mb -p $PROJECT_ID -c STANDARD -l $REGION gs://$BUCKET_NAME 2>/dev/null || echo "ℹ️  Bucket already exists"

echo "✅ GCS bucket ready"

# Create deployment package
tar -czf amp-system.tar.gz \
    amp_cli.py \
    amp_config.json \
    amp_auth.json \
    amp-plugins/ \
    requirements-amp.txt \
    docker-compose.amp.yml \
    --exclude='*.pyc' \
    --exclude='__pycache__'

echo "✅ Deployment package created"

# Upload to GCS
gsutil cp amp-system.tar.gz gs://$BUCKET_NAME/
gsutil cp amp_config.json gs://$BUCKET_NAME/
gsutil cp amp_auth.json gs://$BUCKET_NAME/

echo "✅ Files uploaded to GCS"

# Create Dockerfile for Cloud Run
cat > Dockerfile << 'EOF'
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements-amp.txt .
RUN pip install -r requirements-amp.txt

# Copy application files
COPY amp_cli.py .
COPY amp_config.json .
COPY amp_auth.json .
COPY amp-plugins/ ./amp-plugins/

# Create startup script
RUN echo '#!/bin/bash\npython3 amp_cli.py status' > start.sh && chmod +x start.sh

# Expose port
EXPOSE 8080

# Start the application
CMD ["python3", "amp_cli.py", "status"]
EOF

echo "✅ Dockerfile created"

# Deploy to Cloud Run
gcloud run deploy $SERVICE_NAME \
    --source . \
    --platform managed \
    --region $REGION \
    --allow-unauthenticated \
    --memory 1Gi \
    --cpu 1 \
    --max-instances 10 \
    --set-env-vars "AMP_TOKEN=$AMP_TOKEN,GITHUB_TOKEN=$GITHUB_TOKEN,PROJECT_ID=$PROJECT_ID,BUCKET_NAME=$BUCKET_NAME"

echo "✅ Deployed to Cloud Run"

# Get service URL
SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --region=$REGION --format="value(status.url)" 2>/dev/null || echo "Service URL will be available after deployment completes")

echo ""
echo "🎉 AMP System GCS Deployment Complete!"
echo "======================================"
echo "GCS Bucket: gs://$BUCKET_NAME"
echo "Cloud Run Service: $SERVICE_NAME"
echo "Region: $REGION"
echo "Service URL: $SERVICE_URL"
echo ""
echo "📋 Next Steps:"
echo "1. Monitor: gcloud run services describe $SERVICE_NAME --region=$REGION"
echo "2. Logs: gcloud logs tail --service=$SERVICE_NAME"
echo "3. Access: gcloud run services call $SERVICE_NAME --region=$REGION"