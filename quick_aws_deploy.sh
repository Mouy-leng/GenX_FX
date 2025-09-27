#!/bin/bash

# Quick AWS Deployment Script for AMP System
# This script helps you deploy your AMP system to AWS quickly.
# It has been updated to remove hardcoded credentials.

set -e

# --- Helper Functions ---
# (Color definitions and print functions remain the same)
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}
print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}
print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}
print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# --- Core Functions ---
check_credentials() {
    if aws sts get-caller-identity &> /dev/null; then
        print_success "AWS credentials are configured!"
        aws sts get-caller-identity
        return 0
    else
        return 1
    fi
}

setup_credentials_manual() {
    print_status "Setting up AWS credentials manually..."
    
    echo ""
    echo "📋 To get your AWS credentials, follow these general steps:"
    echo "=========================================================="
    echo ""
    echo "1. 🌐 Log in to your AWS Management Console:"
    echo "   https://console.aws.amazon.com"
    echo ""
    echo "2. 👤 Navigate to the IAM (Identity and Access Management) service."
    echo ""
    echo "3. 🔑 Go to 'Users', select your user, and then go to the 'Security credentials' tab."
    echo ""
    echo "4. 🔐 In the 'Access keys' section, click 'Create access key'."
    echo ""
    echo "5. ✅ Choose 'Command Line Interface (CLI)' as the use case."
    echo ""
    echo "6. 📋 Follow the steps to create and download your Access Key ID and Secret Access Key."
    echo "   (Store them securely!)"
    echo ""
    
    read -p "Press Enter when you have your credentials ready..."
    
    echo ""
    echo "🔧 Now, let's configure your credentials locally:"
    echo "============================================="
    
    aws configure
    
    print_success "Credentials configured!"
    
    if check_credentials; then
        print_success "Credentials are working!"
        return 0
    else
        print_error "Credentials test failed. Please check your credentials and try again."
        return 1
    fi
}

deploy_to_aws() {
    print_status "Starting AWS deployment..."
    
    if ! check_credentials; then
        print_error "AWS credentials not configured."
        setup_credentials_manual
    fi
    
    print_status "Deploying AMP system to AWS..."
    
    if [ -f "aws/amp-deploy.sh" ]; then
        cd aws/
        ./amp-deploy.sh
    else
        print_error "Deployment script 'aws/amp-deploy.sh' not found."
    fi
}

show_info() {
    echo ""
    echo "🎯 What will be deployed:"
    echo "========================"
    echo "✅ EC2 Instance (t2.micro - free tier)"
    echo "✅ VPC & Security Groups"
    echo "✅ S3 Bucket (5GB free storage)"
    echo "✅ DynamoDB Table (25GB free)"
    echo "✅ CloudWatch Logs"
    echo "✅ AMP Trading System (Docker)"
    echo ""
    echo "🔗 After deployment, you'll get:"
    echo "   - An API endpoint URL."
    echo "   - An SSH command to access the EC2 instance."
    echo ""
}

main() {
    print_status "Checking current setup..."
    
    if ! command -v aws &> /dev/null; then
        print_error "AWS CLI not found. Please install it first."
        exit 1
    fi
    print_success "AWS CLI is installed."
    
    show_info
    
    if check_credentials; then
        read -p "🚀 Ready to deploy. Press Enter to start..."
        deploy_to_aws
    else
        print_warning "AWS credentials need to be configured."
        setup_credentials_manual
        if check_credentials; then
            read -p "🚀 Ready to deploy. Press Enter to start..."
            deploy_to_aws
        fi
    fi
}

# --- Argument Handling ---
case "${1:-}" in
    "deploy")
        deploy_to_aws
        ;;
    "setup")
        setup_credentials_manual
        ;;
    "check")
        check_credentials
        ;;
    "help"|"-h"|"--help")
        echo "Quick AWS Deployment Script"
        echo "Usage: $0 [command]"
        echo "Commands:"
        echo "  (no args)  - Run the interactive setup and deployment."
        echo "  deploy     - Deploy to AWS (requires pre-configured credentials)."
        echo "  setup      - Interactively set up AWS credentials."
        echo "  check      - Check if AWS credentials are configured."
        echo "  help       - Show this help message."
        ;;
    *)
        main
        ;;
esac