#!/bin/bash

# Quick AMP System GCS Deployment
# Simplified deployment script for rapid deployment

set -e

# --- Configuration ---
# IMPORTANT: Replace these placeholders with your actual project details,
# or set them as environment variables before running the script.
PROJECT_ID="${PROJECT_ID:-"your-gcp-project-id"}"
REGION="${REGION:-"us-central1"}"
SERVICE_NAME="amp-trading-system"
BUCKET_NAME="${BUCKET_NAME:-"your-gcs-bucket-name"}"

# IMPORTANT: These tokens should be managed securely, for example, via environment variables or a secret manager.
# DO NOT hardcode them in production scripts.
AMP_TOKEN="${AMP_TOKEN:-"your_amp_token_here"}"
GITHUB_TOKEN="${GITHUB_TOKEN:-"your_github_token_here"}"

echo "🚀 Quick AMP System GCS Deployment"
echo "=================================="

# --- Pre-flight checks ---
if [ "$PROJECT_ID" = "your-gcp-project-id" ] || [ "$BUCKET_NAME" = "your-gcs-bucket-name" ]; then
    echo "❌ Error: PROJECT_ID and BUCKET_NAME must be set. Please edit the script or set them as environment variables."
    exit 1
fi

# --- Authentication ---
echo "🔐 Authenticating with Google Cloud..."
# This script assumes you have authenticated with the gcloud CLI.
# For automated environments, it is HIGHLY recommended to use a service account:
# 1. Create a service account with necessary permissions (e.g., Storage Admin, Cloud Run Admin).
# 2. Download the JSON key file for the service account.
# 3. Authenticate using the key file. You can either:
#    a) Set the GOOGLE_APPLICATION_CREDENTIALS environment variable:
#       export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"
#    b) Or activate it directly for this session:
#       gcloud auth activate-service-account --key-file=/path/to/your/keyfile.json
#
# This script will proceed assuming you have already logged in via `gcloud auth login` or a service account.
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q .; then
    echo "🔵 Not authenticated with gcloud. Please run 'gcloud auth login' or configure a service account."
    gcloud auth login
fi

gcloud config set project $PROJECT_ID
echo "✅ Authenticated and project set to '$PROJECT_ID'."

# Install gcloud if not available
if ! command -v gcloud &> /dev/null; then
    echo "📥 Installing Google Cloud CLI..."
    curl https://sdk.cloud.google.com | bash
    exec -l $SHELL
    source ~/.bashrc
fi

echo "✅ Google Cloud CLI ready"

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