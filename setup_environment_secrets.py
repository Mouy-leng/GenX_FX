#!/usr/bin/env python3
"""
Setup GitHub Repository Secrets and Environment Variables
Based on information extracted from Google Drive folders
"""

import json
import os
import subprocess
import sys
from pathlib import Path

def run_command(cmd, description=""):
    """Run a command and return the result"""
    try:
        print(f"Running: {description}")
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✓ Success: {description}")
            return result.stdout.strip()
        else:
            print(f"✗ Error: {description}")
            print(f"Error: {result.stderr}")
            return None
    except Exception as e:
        print(f"✗ Exception: {description} - {e}")
        return None

def setup_github_secrets():
    """Set up GitHub repository secrets"""
    
    # Check for GitHub token
    github_token = os.getenv("GITHUB_TOKEN")
    if not github_token:
        print("✗ Error: GITHUB_TOKEN environment variable not set.")
        print("Please set the GITHUB_TOKEN environment variable with a valid GitHub personal access token.")
        sys.exit(1)
    os.environ['GITHUB_TOKEN'] = github_token
    
    print("🔐 Setting up GitHub Repository Secrets...")
    print("=" * 50)
    
    # Firebase Service Account
    firebase_key_path = "/workspace/drive_content/JSON/genx-firebace-cd773b0c7f9e.json"
    if os.path.exists(firebase_key_path):
        with open(firebase_key_path, 'r') as f:
            firebase_data = json.load(f)
        
        # Set Firebase secrets
        run_command(f'gh secret set FIREBASE_PROJECT_ID --body "{firebase_data["project_id"]}"', "Firebase Project ID")
        run_command(f'gh secret set FIREBASE_PRIVATE_KEY_ID --body "{firebase_data["private_key_id"]}"', "Firebase Private Key ID")
        run_command(f'gh secret set FIREBASE_PRIVATE_KEY --body "{firebase_data["private_key"]}"', "Firebase Private Key")
        run_command(f'gh secret set FIREBASE_CLIENT_EMAIL --body "{firebase_data["client_email"]}"', "Firebase Client Email")
        run_command(f'gh secret set FIREBASE_CLIENT_ID --body "{firebase_data["client_id"]}"', "Firebase Client ID")
        run_command(f'gh secret set FIREBASE_AUTH_URI --body "{firebase_data["auth_uri"]}"', "Firebase Auth URI")
        run_command(f'gh secret set FIREBASE_TOKEN_URI --body "{firebase_data["token_uri"]}"', "Firebase Token URI")
        run_command(f'gh secret set FIREBASE_AUTH_PROVIDER_X509_CERT_URL --body "{firebase_data["auth_provider_x509_cert_url"]}"', "Firebase Auth Provider X509 Cert URL")
        run_command(f'gh secret set FIREBASE_CLIENT_X509_CERT_URL --body "{firebase_data["client_x509_cert_url"]}"', "Firebase Client X509 Cert URL")
        run_command(f'gh secret set FIREBASE_UNIVERSE_DOMAIN --body "{firebase_data["universe_domain"]}"', "Firebase Universe Domain")
        
        # Set the entire Firebase service account as a secret
        run_command(f'gh secret set FIREBASE_SERVICE_ACCOUNT_KEY --body "$(cat {firebase_key_path})"', "Firebase Service Account Key")
    
    # Google Cloud Service Account (Flash Student)
    flash_key_path = "/workspace/drive_content/JSON/flash-student-473123-n2-a0ca3a5d08c3.json"
    if os.path.exists(flash_key_path):
        with open(flash_key_path, 'r') as f:
            flash_data = json.load(f)
        
        # Set Google Cloud secrets
        run_command(f'gh secret set GOOGLE_CLOUD_PROJECT_ID --body "{flash_data["project_id"]}"', "Google Cloud Project ID")
        run_command(f'gh secret set GOOGLE_CLOUD_PRIVATE_KEY_ID --body "{flash_data["private_key_id"]}"', "Google Cloud Private Key ID")
        run_command(f'gh secret set GOOGLE_CLOUD_PRIVATE_KEY --body "{flash_data["private_key"]}"', "Google Cloud Private Key")
        run_command(f'gh secret set GOOGLE_CLOUD_CLIENT_EMAIL --body "{flash_data["client_email"]}"', "Google Cloud Client Email")
        run_command(f'gh secret set GOOGLE_CLOUD_CLIENT_ID --body "{flash_data["client_id"]}"', "Google Cloud Client ID")
        run_command(f'gh secret set GOOGLE_CLOUD_AUTH_URI --body "{flash_data["auth_uri"]}"', "Google Cloud Auth URI")
        run_command(f'gh secret set GOOGLE_CLOUD_TOKEN_URI --body "{flash_data["token_uri"]}"', "Google Cloud Token URI")
        run_command(f'gh secret set GOOGLE_CLOUD_AUTH_PROVIDER_X509_CERT_URL --body "{flash_data["auth_provider_x509_cert_url"]}"', "Google Cloud Auth Provider X509 Cert URL")
        run_command(f'gh secret set GOOGLE_CLOUD_CLIENT_X509_CERT_URL --body "{flash_data["client_x509_cert_url"]}"', "Google Cloud Client X509 Cert URL")
        run_command(f'gh secret set GOOGLE_CLOUD_UNIVERSE_DOMAIN --body "{flash_data["universe_domain"]}"', "Google Cloud Universe Domain")
        
        # Set the entire Google Cloud service account as a secret
        run_command(f'gh secret set GOOGLE_CLOUD_SERVICE_ACCOUNT_KEY --body "$(cat {flash_key_path})"', "Google Cloud Service Account Key")
    
    # Compute Engine Service Account (Sharp Doodad)
    compute_key_path = "/workspace/drive_content/JSON/sharp-doodad-471511-s5-0b4fd7b7320e.json"
    if os.path.exists(compute_key_path):
        with open(compute_key_path, 'r') as f:
            compute_data = json.load(f)
        
        # Set Compute Engine secrets
        run_command(f'gh secret set COMPUTE_PROJECT_ID --body "{compute_data["project_id"]}"', "Compute Project ID")
        run_command(f'gh secret set COMPUTE_PRIVATE_KEY_ID --body "{compute_data["private_key_id"]}"', "Compute Private Key ID")
        run_command(f'gh secret set COMPUTE_PRIVATE_KEY --body "{compute_data["private_key"]}"', "Compute Private Key")
        run_command(f'gh secret set COMPUTE_CLIENT_EMAIL --body "{compute_data["client_email"]}"', "Compute Client Email")
        run_command(f'gh secret set COMPUTE_CLIENT_ID --body "{compute_data["client_id"]}"', "Compute Client ID")
        run_command(f'gh secret set COMPUTE_AUTH_URI --body "{compute_data["auth_uri"]}"', "Compute Auth URI")
        run_command(f'gh secret set COMPUTE_TOKEN_URI --body "{compute_data["token_uri"]}"', "Compute Token URI")
        run_command(f'gh secret set COMPUTE_AUTH_PROVIDER_X509_CERT_URL --body "{compute_data["auth_provider_x509_cert_url"]}"', "Compute Auth Provider X509 Cert URL")
        run_command(f'gh secret set COMPUTE_CLIENT_X509_CERT_URL --body "{compute_data["client_x509_cert_url"]}"', "Compute Client X509 Cert URL")
        run_command(f'gh secret set COMPUTE_UNIVERSE_DOMAIN --body "{compute_data["universe_domain"]}"', "Compute Universe Domain")
        
        # Set the entire Compute service account as a secret
        run_command(f'gh secret set COMPUTE_SERVICE_ACCOUNT_KEY --body "$(cat {compute_key_path})"', "Compute Service Account Key")
    
    # SSL Certificate secrets
    ssl_cert_path = "/workspace/drive_content/JSON/genxfx_org.crt"
    ssl_bundle_path = "/workspace/drive_content/JSON/genxfx_org.ca-bundle"
    ssl_p7b_path = "/workspace/drive_content/JSON/genxfx_org.p7b"
    
    if os.path.exists(ssl_cert_path):
        run_command(f'gh secret set SSL_CERTIFICATE --body "$(cat {ssl_cert_path})"', "SSL Certificate")
    
    if os.path.exists(ssl_bundle_path):
        run_command(f'gh secret set SSL_CA_BUNDLE --body "$(cat {ssl_bundle_path})"', "SSL CA Bundle")
    
    if os.path.exists(ssl_p7b_path):
        run_command(f'gh secret set SSL_P7B_CERTIFICATE --body "$(cat {ssl_p7b_path})"', "SSL P7B Certificate")
    
    # Additional secrets
    run_command(f'gh secret set GITHUB_TOKEN --body "{github_token}"', "GitHub Token")
    run_command('gh secret set REPOSITORY_NAME --body "GenX_FX"', "Repository Name")
    run_command('gh secret set REPOSITORY_OWNER --body "Mouy-leng"', "Repository Owner")
    
    print("\n✅ GitHub Secrets setup completed!")

def setup_environment_variables():
    """Set up environment variables"""
    
    print("\n🌍 Setting up Environment Variables...")
    print("=" * 50)
    
    # Create .env file with all environment variables
    env_content = """# GenX FX Environment Variables
# Generated from Google Drive folder extraction

# Firebase Configuration
FIREBASE_PROJECT_ID=genx-firebace
FIREBASE_CLIENT_EMAIL=firebase-adminsdk-fbsvc@genx-firebace.iam.gserviceaccount.com
FIREBASE_AUTH_URI=https://accounts.google.com/o/oauth2/auth
FIREBASE_TOKEN_URI=https://oauth2.googleapis.com/token
FIREBASE_AUTH_PROVIDER_X509_CERT_URL=https://www.googleapis.com/oauth2/v1/certs
FIREBASE_CLIENT_X509_CERT_URL=https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-fbsvc%40genx-firebace.iam.gserviceaccount.com
FIREBASE_UNIVERSE_DOMAIN=googleapis.com

# Google Cloud Configuration
GOOGLE_CLOUD_PROJECT_ID=flash-student-473123-n2
GOOGLE_CLOUD_CLIENT_EMAIL=genx-fx-project-yn-901@flash-student-473123-n2.iam.gserviceaccount.com
GOOGLE_CLOUD_AUTH_URI=https://accounts.google.com/o/oauth2/auth
GOOGLE_CLOUD_TOKEN_URI=https://oauth2.googleapis.com/token
GOOGLE_CLOUD_AUTH_PROVIDER_X509_CERT_URL=https://www.googleapis.com/oauth2/v1/certs
GOOGLE_CLOUD_CLIENT_X509_CERT_URL=https://www.googleapis.com/robot/v1/metadata/x509/genx-fx-project-yn-901%40flash-student-473123-n2.iam.gserviceaccount.com
GOOGLE_CLOUD_UNIVERSE_DOMAIN=googleapis.com

# Compute Engine Configuration
COMPUTE_PROJECT_ID=sharp-doodad-471511-s5
COMPUTE_CLIENT_EMAIL=236873001744-compute@developer.gserviceaccount.com
COMPUTE_AUTH_URI=https://accounts.google.com/o/oauth2/auth
COMPUTE_TOKEN_URI=https://oauth2.googleapis.com/token
COMPUTE_AUTH_PROVIDER_X509_CERT_URL=https://www.googleapis.com/oauth2/v1/certs
COMPUTE_CLIENT_X509_CERT_URL=https://www.googleapis.com/robot/v1/metadata/x509/236873001744-compute%40developer.gserviceaccount.com
COMPUTE_UNIVERSE_DOMAIN=googleapis.com

# Repository Configuration
REPOSITORY_NAME=GenX_FX
REPOSITORY_OWNER=Mouy-leng
REPOSITORY_URL=https://github.com/Mouy-leng/GenX_FX

# SSL Certificate Paths
SSL_CERT_PATH=/workspace/drive_content/JSON/genxfx_org.crt
SSL_CA_BUNDLE_PATH=/workspace/drive_content/JSON/genxfx_org.ca-bundle
SSL_P7B_PATH=/workspace/drive_content/JSON/genxfx_org.p7b

# Service Account Key Paths
FIREBASE_SERVICE_ACCOUNT_KEY_PATH=/workspace/drive_content/JSON/genx-firebace-cd773b0c7f9e.json
GOOGLE_CLOUD_SERVICE_ACCOUNT_KEY_PATH=/workspace/drive_content/JSON/flash-student-473123-n2-a0ca3a5d08c3.json
COMPUTE_SERVICE_ACCOUNT_KEY_PATH=/workspace/drive_content/JSON/sharp-doodad-471511-s5-0b4fd7b7320e.json

# Application Configuration
NODE_ENV=production
PYTHON_ENV=production
APP_NAME=GenX_FX
APP_VERSION=1.0.0
APP_DESCRIPTION=Trading Platform with AI Integration

# Database Configuration (if needed)
DB_HOST=localhost
DB_PORT=5432
DB_NAME=genx_fx
DB_USER=genx_user

# API Configuration
API_PORT=3000
API_HOST=0.0.0.0
API_BASE_URL=https://api.genxfx.org

# Trading Configuration
TRADING_ENABLED=true
TRADING_MODE=production
RISK_MANAGEMENT=true

# Monitoring Configuration
MONITORING_ENABLED=true
LOG_LEVEL=info
METRICS_ENABLED=true
"""
    
    # Write .env file
    with open('/workspace/.env', 'w') as f:
        f.write(env_content)
    
    print("✅ Environment variables written to .env file")
    
    # Also create a production .env file
    with open('/workspace/.env.production', 'w') as f:
        f.write(env_content)
    
    print("✅ Production environment variables written to .env.production file")

def create_secrets_summary():
    """Create a summary of all secrets and variables"""
    
    summary_content = """# GenX FX Environment Secrets and Variables Summary

## GitHub Repository Secrets Set:
- FIREBASE_PROJECT_ID
- FIREBASE_PRIVATE_KEY_ID
- FIREBASE_PRIVATE_KEY
- FIREBASE_CLIENT_EMAIL
- FIREBASE_CLIENT_ID
- FIREBASE_AUTH_URI
- FIREBASE_TOKEN_URI
- FIREBASE_AUTH_PROVIDER_X509_CERT_URL
- FIREBASE_CLIENT_X509_CERT_URL
- FIREBASE_UNIVERSE_DOMAIN
- FIREBASE_SERVICE_ACCOUNT_KEY

- GOOGLE_CLOUD_PROJECT_ID
- GOOGLE_CLOUD_PRIVATE_KEY_ID
- GOOGLE_CLOUD_PRIVATE_KEY
- GOOGLE_CLOUD_CLIENT_EMAIL
- GOOGLE_CLOUD_CLIENT_ID
- GOOGLE_CLOUD_AUTH_URI
- GOOGLE_CLOUD_TOKEN_URI
- GOOGLE_CLOUD_AUTH_PROVIDER_X509_CERT_URL
- GOOGLE_CLOUD_CLIENT_X509_CERT_URL
- GOOGLE_CLOUD_UNIVERSE_DOMAIN
- GOOGLE_CLOUD_SERVICE_ACCOUNT_KEY

- COMPUTE_PROJECT_ID
- COMPUTE_PRIVATE_KEY_ID
- COMPUTE_PRIVATE_KEY
- COMPUTE_CLIENT_EMAIL
- COMPUTE_CLIENT_ID
- COMPUTE_AUTH_URI
- COMPUTE_TOKEN_URI
- COMPUTE_AUTH_PROVIDER_X509_CERT_URL
- COMPUTE_CLIENT_X509_CERT_URL
- COMPUTE_UNIVERSE_DOMAIN
- COMPUTE_SERVICE_ACCOUNT_KEY

- SSL_CERTIFICATE
- SSL_CA_BUNDLE
- SSL_P7B_CERTIFICATE
- GITHUB_TOKEN
- REPOSITORY_NAME
- REPOSITORY_OWNER

## Environment Variables Created:
- .env (development)
- .env.production (production)

## Source Files:
- Firebase Service Account: genx-firebace-cd773b0c7f9e.json
- Google Cloud Service Account: flash-student-473123-n2-a0ca3a5d08c3.json
- Compute Engine Service Account: sharp-doodad-471511-s5-0b4fd7b7320e.json
- SSL Certificates: genxfx_org.crt, genxfx_org.ca-bundle, genxfx_org.p7b

## Generated on: $(date)
## Repository: Mouy-leng/GenX_FX
"""
    
    with open('/workspace/SECRETS_SETUP_SUMMARY.md', 'w') as f:
        f.write(summary_content)
    
    print("✅ Secrets summary written to SECRETS_SETUP_SUMMARY.md")

def main():
    """Main function to set up all secrets and variables"""
    
    print("🚀 GenX FX Environment Setup")
    print("=" * 50)
    print("Setting up GitHub repository secrets and environment variables")
    print("Based on information extracted from Google Drive folders")
    print("=" * 50)
    
    # Set up GitHub secrets
    setup_github_secrets()
    
    # Set up environment variables
    setup_environment_variables()
    
    # Create summary
    create_secrets_summary()
    
    print("\n🎉 Setup completed successfully!")
    print("=" * 50)
    print("All secrets and environment variables have been configured.")
    print("Check SECRETS_SETUP_SUMMARY.md for a complete overview.")

if __name__ == "__main__":
    main()