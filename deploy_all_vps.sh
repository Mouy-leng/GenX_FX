#!/bin/bash
# Master VPS Deployment Script for GenX Magic Trading Platform
# Deploys across NameCheap, Vultr, and Google Cloud (3 accounts)

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

echo -e "${PURPLE}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${PURPLE}║                GenX Magic Trading Platform                   ║${NC}"
echo -e "${PURPLE}║              MASTER VPS DEPLOYMENT SCRIPT                    ║${NC}"
echo -e "${PURPLE}║                                                              ║${NC}"
echo -e "${PURPLE}║  Deploys to: NameCheap + Vultr + Google Cloud (3 accounts)  ║${NC}"
echo -e "${PURPLE}╚══════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Deployment configuration
DEPLOY_NAMECHEAP="${DEPLOY_NAMECHEAP:-true}"
DEPLOY_VULTR="${DEPLOY_VULTR:-true}"
DEPLOY_GOOGLE_CLOUD="${DEPLOY_GOOGLE_CLOUD:-true}"

echo -e "${YELLOW}📋 Deployment Configuration:${NC}"
echo "NameCheap VPS: $([ "$DEPLOY_NAMECHEAP" = "true" ] && echo "✅ Enabled" || echo "❌ Disabled")"
echo "Vultr VPS: $([ "$DEPLOY_VULTR" = "true" ] && echo "✅ Enabled" || echo "❌ Disabled")"
echo "Google Cloud: $([ "$DEPLOY_GOOGLE_CLOUD" = "true" ] && echo "✅ Enabled" || echo "❌ Disabled")"
echo ""

# Function to check prerequisites
check_prerequisites() {
    echo -e "${BLUE}🔍 Checking prerequisites...${NC}"
    
    local missing_tools=()
    
    # Check required tools
    command -v curl >/dev/null 2>&1 || missing_tools+=("curl")
    command -v python3 >/dev/null 2>&1 || missing_tools+=("python3")
    command -v ssh >/dev/null 2>&1 || missing_tools+=("ssh")
    command -v rsync >/dev/null 2>&1 || missing_tools+=("rsync")
    
    if [ ${#missing_tools[@]} -ne 0 ]; then
        echo -e "${RED}❌ Missing required tools: ${missing_tools[*]}${NC}"
        echo "Please install the missing tools and run again."
        exit 1
    fi
    
    # Check Python packages
    python3 -c "import requests" 2>/dev/null || {
        echo -e "${YELLOW}⚠️ Installing Python requests library...${NC}"
        pip3 install requests || pip install requests
    }
    
    echo -e "${GREEN}✅ Prerequisites check passed${NC}"
}

# Function to validate credentials
validate_credentials() {
    echo -e "${BLUE}🔐 Validating credentials...${NC}"
    
    local credentials_valid=true
    
    # Check NameCheap credentials
    if [ "$DEPLOY_NAMECHEAP" = "true" ]; then
        if [ -z "$NAMECHEAP_API_USER" ] || [ -z "$NAMECHEAP_API_KEY" ]; then
            echo -e "${RED}❌ NameCheap credentials missing${NC}"
            credentials_valid=false
        else
            echo -e "${GREEN}✅ NameCheap credentials found${NC}"
        fi
    fi
    
    # Check Vultr credentials
    if [ "$DEPLOY_VULTR" = "true" ]; then
        if [ -z "$VULTR_API_KEY" ]; then
            echo -e "${RED}❌ Vultr API key missing${NC}"
            credentials_valid=false
        else
            echo -e "${GREEN}✅ Vultr credentials found${NC}"
        fi
    fi
    
    # Check Google Cloud credentials
    if [ "$DEPLOY_GOOGLE_CLOUD" = "true" ]; then
        if command -v gcloud >/dev/null 2>&1; then
            if gcloud auth list --filter=status:ACTIVE --format="value(account)" | head -1 > /dev/null 2>&1; then
                echo -e "${GREEN}✅ Google Cloud authentication found${NC}"
            else
                echo -e "${RED}❌ Google Cloud authentication missing${NC}"
                credentials_valid=false
            fi
        else
            echo -e "${RED}❌ Google Cloud SDK not installed${NC}"
            credentials_valid=false
        fi
    fi
    
    if [ "$credentials_valid" = "false" ]; then
        echo -e "${RED}❌ Credential validation failed${NC}"
        echo "Please refer to VPS_DEPLOYMENT_CREDENTIALS.md for setup instructions"
        exit 1
    fi
    
    echo -e "${GREEN}✅ All credentials validated${NC}"
}

# Function to deploy to NameCheap
deploy_namecheap() {
    echo ""
    echo -e "${BLUE}🚀 Deploying to NameCheap VPS...${NC}"
    echo "================================================"
    
    if [ ! -f "./deploy_namecheap_vps.sh" ]; then
        echo -e "${RED}❌ NameCheap deployment script not found${NC}"
        return 1
    fi
    
    chmod +x ./deploy_namecheap_vps.sh
    
    if ./deploy_namecheap_vps.sh; then
        echo -e "${GREEN}✅ NameCheap deployment completed${NC}"
        return 0
    else
        echo -e "${RED}❌ NameCheap deployment failed${NC}"
        return 1
    fi
}

# Function to deploy to Vultr
deploy_vultr() {
    echo ""
    echo -e "${BLUE}🚀 Deploying to Vultr VPS...${NC}"
    echo "============================================"
    
    if [ ! -f "./deploy_vultr_vps.sh" ]; then
        echo -e "${RED}❌ Vultr deployment script not found${NC}"
        return 1
    fi
    
    chmod +x ./deploy_vultr_vps.sh
    
    if ./deploy_vultr_vps.sh; then
        echo -e "${GREEN}✅ Vultr deployment completed${NC}"
        return 0
    else
        echo -e "${RED}❌ Vultr deployment failed${NC}"
        return 1
    fi
}

# Function to deploy to Google Cloud
deploy_google_cloud() {
    echo ""
    echo -e "${BLUE}🚀 Deploying to Google Cloud (3 accounts)...${NC}"
    echo "====================================================="
    
    if [ ! -f "./deploy_gcp_multi_account.sh" ]; then
        echo -e "${RED}❌ Google Cloud deployment script not found${NC}"
        return 1
    fi
    
    chmod +x ./deploy_gcp_multi_account.sh
    
    if ./deploy_gcp_multi_account.sh; then
        echo -e "${GREEN}✅ Google Cloud deployment completed${NC}"
        return 0
    else
        echo -e "${RED}❌ Google Cloud deployment failed${NC}"
        return 1
    fi
}

# Function to generate deployment summary
generate_summary() {
    echo ""
    echo -e "${PURPLE}╔══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${PURPLE}║                    DEPLOYMENT SUMMARY                        ║${NC}"
    echo -e "${PURPLE}╚══════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    
    local total_deployments=0
    local successful_deployments=0
    
    # Count NameCheap
    if [ "$DEPLOY_NAMECHEAP" = "true" ]; then
        total_deployments=$((total_deployments + 1))
        if [ -f "namecheap_instance.json" ]; then
            successful_deployments=$((successful_deployments + 1))
            echo -e "${GREEN}✅ NameCheap VPS: DEPLOYED${NC}"
        else
            echo -e "${RED}❌ NameCheap VPS: FAILED${NC}"
        fi
    fi
    
    # Count Vultr
    if [ "$DEPLOY_VULTR" = "true" ]; then
        total_deployments=$((total_deployments + 1))
        if [ -f "vultr_instance.json" ]; then
            successful_deployments=$((successful_deployments + 1))
            echo -e "${GREEN}✅ Vultr VPS: DEPLOYED${NC}"
        else
            echo -e "${RED}❌ Vultr VPS: FAILED${NC}"
        fi
    fi
    
    # Count Google Cloud
    if [ "$DEPLOY_GOOGLE_CLOUD" = "true" ]; then
        local gcp_count=0
        for i in {1..3}; do
            total_deployments=$((total_deployments + 1))
            if [ -f "gcp-instance-$i.json" ]; then
                successful_deployments=$((successful_deployments + 1))
                gcp_count=$((gcp_count + 1))
            fi
        done
        echo -e "${GREEN}✅ Google Cloud VPS: $gcp_count/3 DEPLOYED${NC}"
    fi
    
    echo ""
    echo -e "${YELLOW}📊 Overall Success Rate: $successful_deployments/$total_deployments${NC}"
    
    if [ $successful_deployments -gt 0 ]; then
        echo ""
        echo -e "${GREEN}🎉 LIVE TRADING PLATFORMS:${NC}"
        echo "================================="
        
        # List NameCheap instances
        if [ -f "namecheap_instance.json" ]; then
            echo "🔹 NameCheap VPS:"
            echo "   Provider: NameCheap"
            echo "   Plan: Stellar Plus (2 vCPU, 6GB RAM)"
            echo "   Cost: ~$18.88/month"
        fi
        
        # List Vultr instances
        if [ -f "vultr_instance.json" ]; then
            vultr_ip=$(jq -r '.main_ip' vultr_instance.json 2>/dev/null || echo "N/A")
            echo "🔹 Vultr VPS:"
            echo "   IP: $vultr_ip"
            echo "   Plan: 2 vCPU, 4GB RAM"
            echo "   Cost: ~$12/month"
            echo "   URL: https://$vultr_ip"
        fi
        
        # List Google Cloud instances
        for i in {1..3}; do
            if [ -f "gcp-instance-$i.json" ]; then
                gcp_ip=$(jq -r '.external_ip' gcp-instance-$i.json 2>/dev/null || echo "N/A")
                gcp_account=$(jq -r '.account' gcp-instance-$i.json 2>/dev/null || echo "Account $i")
                echo "🔹 Google Cloud VPS $i:"
                echo "   Account: $gcp_account"
                echo "   IP: $gcp_ip"
                echo "   Plan: e2-medium (2 vCPU, 4GB RAM)"
                echo "   Cost: FREE ($300 credit)"
                echo "   URL: http://$gcp_ip"
            fi
        done
        
        echo ""
        echo -e "${YELLOW}💰 ESTIMATED COSTS (Year 1):${NC}"
        echo "NameCheap: ~$226/year"
        echo "Vultr: ~$144/year"
        echo "Google Cloud: $0/year (3 × $300 credits)"
        echo "Total: ~$370/year for up to 5 VPS instances!"
        
        echo ""
        echo -e "${GREEN}🔑 MAGIC KEY CONFIGURATION:${NC}"
        echo "All platforms deployed with magic key authentication"
        echo "Exness Magic Number: 123456789"
        echo "FBS Magic Number: 987654321"
        echo "Signal Magic Number: 555666777"
    fi
    
    echo ""
    echo -e "${BLUE}📋 NEXT STEPS:${NC}"
    echo "1. Test all deployed platforms"
    echo "2. Configure domain names (optional)"
    echo "3. Setup SSL certificates"
    echo "4. Start live trading operations"
    echo "5. Monitor performance across all platforms"
    
    echo ""
    if [ $successful_deployments -eq $total_deployments ]; then
        echo -e "${GREEN}🎯 ALL DEPLOYMENTS SUCCESSFUL! Ready for live trading! 🎯${NC}"
    elif [ $successful_deployments -gt 0 ]; then
        echo -e "${YELLOW}⚠️ Partial deployment success. Some platforms are ready for trading.${NC}"
    else
        echo -e "${RED}❌ All deployments failed. Please check credentials and try again.${NC}"
    fi
}

# Main execution flow
main() {
    echo -e "${YELLOW}🚀 Starting GenX Magic Trading Platform deployment...${NC}"
    echo ""
    
    # Run prerequisite checks
    check_prerequisites
    
    # Validate credentials
    validate_credentials
    
    echo ""
    echo -e "${BLUE}🎯 Beginning multi-provider deployment...${NC}"
    
    # Deploy to each provider
    local deployment_success=true
    
    if [ "$DEPLOY_NAMECHEAP" = "true" ]; then
        deploy_namecheap || deployment_success=false
    fi
    
    if [ "$DEPLOY_VULTR" = "true" ]; then
        deploy_vultr || deployment_success=false
    fi
    
    if [ "$DEPLOY_GOOGLE_CLOUD" = "true" ]; then
        deploy_google_cloud || deployment_success=false
    fi
    
    # Generate final summary
    generate_summary
    
    if [ "$deployment_success" = "true" ]; then
        exit 0
    else
        exit 1
    fi
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --skip-namecheap)
            DEPLOY_NAMECHEAP=false
            shift
            ;;
        --skip-vultr)
            DEPLOY_VULTR=false
            shift
            ;;
        --skip-gcp)
            DEPLOY_GOOGLE_CLOUD=false
            shift
            ;;
        --help)
            echo "GenX Magic Trading Platform - Master VPS Deployment"
            echo ""
            echo "Usage: $0 [options]"
            echo ""
            echo "Options:"
            echo "  --skip-namecheap    Skip NameCheap VPS deployment"
            echo "  --skip-vultr        Skip Vultr VPS deployment"
            echo "  --skip-gcp          Skip Google Cloud deployment"
            echo "  --help              Show this help message"
            echo ""
            echo "Environment Variables Required:"
            echo "  NAMECHEAP_API_USER, NAMECHEAP_API_KEY"
            echo "  VULTR_API_KEY"
            echo "  GCP authentication via gcloud"
            echo ""
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

# Run main function
main