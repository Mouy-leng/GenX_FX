#!/usr/bin/env python3
"""
Firebase Authentication Setup Script for GenX FX Trading Platform
This script helps configure Firebase Authentication with proper redirect URIs
"""

import os
import json
import subprocess
import sys
from pathlib import Path

class FirebaseAuthSetup:
    def __init__(self):
        self.project_id = "genx-467217"
        self.auth_domain = f"{self.project_id}.firebaseapp.com"
        
    def check_firebase_cli(self):
        """Check if Firebase CLI is installed"""
        try:
            result = subprocess.run(['firebase', '--version'], 
                                  capture_output=True, text=True, check=True)
            print(f"✅ Firebase CLI found: {result.stdout.strip()}")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("❌ Firebase CLI not found. Installing...")
            return self.install_firebase_cli()
    
    def install_firebase_cli(self):
        """Install Firebase CLI"""
        try:
            subprocess.run(['npm', 'install', '-g', 'firebase-tools'], 
                         check=True)
            print("✅ Firebase CLI installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install Firebase CLI: {e}")
            return False
    
    def login_firebase(self):
        """Login to Firebase"""
        try:
            print("🔐 Logging into Firebase...")
            subprocess.run(['firebase', 'login'], check=True)
            print("✅ Successfully logged into Firebase")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to login to Firebase: {e}")
            return False
    
    def setup_auth_providers(self):
        """Configure authentication providers with redirect URIs"""
        print("\n🔧 Setting up authentication providers...")
        
        # Common redirect URIs for development and production
        redirect_uris = [
            "http://localhost:5173",
            "http://localhost:3000", 
            "http://localhost:8080",
            f"https://{self.auth_domain}",
            f"https://{self.project_id}.web.app",
            f"https://{self.project_id}.firebaseapp.com"
        ]
        
        print("📋 Recommended redirect URIs:")
        for uri in redirect_uris:
            print(f"   • {uri}")
        
        print("\n⚠️  IMPORTANT: You need to configure these redirect URIs in Firebase Console:")
        print("   1. Go to https://console.firebase.google.com/")
        print(f"   2. Select project: {self.project_id}")
        print("   3. Go to Authentication > Sign-in method")
        print("   4. For each provider (Google, GitHub), add the redirect URIs above")
        print("   5. Make sure to add your production domain when you deploy")
        
        return True
    
    def create_env_file(self):
        """Create environment file with Firebase configuration"""
        env_content = f"""# Firebase Configuration
VITE_FIREBASE_API_KEY=your_firebase_api_key_here
VITE_FIREBASE_AUTH_DOMAIN={self.auth_domain}
VITE_FIREBASE_PROJECT_ID={self.project_id}
VITE_FIREBASE_STORAGE_BUCKET={self.project_id}.appspot.com
VITE_FIREBASE_MESSAGING_SENDER_ID=your_messaging_sender_id_here
VITE_FIREBASE_APP_ID=your_firebase_app_id_here
VITE_FIREBASE_MEASUREMENT_ID=your_measurement_id_here

# API Configuration
VITE_API_BASE_URL=http://localhost:8081
VITE_API_V1_BASE_URL=http://localhost:8081/api/v1

# Development
NODE_ENV=development
"""
        
        env_file = Path(".env")
        if not env_file.exists():
            with open(env_file, 'w') as f:
                f.write(env_content)
            print(f"✅ Created {env_file}")
        else:
            print(f"⚠️  {env_file} already exists. Please update it manually with the Firebase config.")
        
        return True
    
    def get_firebase_config(self):
        """Get Firebase configuration from project"""
        try:
            print("\n🔍 Getting Firebase configuration...")
            result = subprocess.run(['firebase', 'apps:list'], 
                                  capture_output=True, text=True, check=True)
            
            print("📱 Firebase Apps:")
            print(result.stdout)
            
            # Try to get web app config
            try:
                config_result = subprocess.run(['firebase', 'apps:sdkconfig', 'web'], 
                                             capture_output=True, text=True, check=True)
                config_data = json.loads(config_result.stdout)
                
                print("\n🔧 Firebase Web App Configuration:")
                print(f"   API Key: {config_data.get('apiKey', 'Not found')}")
                print(f"   Auth Domain: {config_data.get('authDomain', 'Not found')}")
                print(f"   Project ID: {config_data.get('projectId', 'Not found')}")
                print(f"   Storage Bucket: {config_data.get('storageBucket', 'Not found')}")
                print(f"   Messaging Sender ID: {config_data.get('messagingSenderId', 'Not found')}")
                print(f"   App ID: {config_data.get('appId', 'Not found')}")
                
                return config_data
                
            except subprocess.CalledProcessError:
                print("⚠️  Could not get web app configuration. You may need to create a web app in Firebase Console.")
                return None
                
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to get Firebase configuration: {e}")
            return None
    
    def deploy_firestore_rules(self):
        """Deploy Firestore security rules"""
        try:
            print("\n🚀 Deploying Firestore security rules...")
            subprocess.run(['firebase', 'deploy', '--only', 'firestore:rules'], 
                         check=True)
            print("✅ Firestore rules deployed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to deploy Firestore rules: {e}")
            return False
    
    def deploy_firestore_indexes(self):
        """Deploy Firestore indexes"""
        try:
            print("\n🚀 Deploying Firestore indexes...")
            subprocess.run(['firebase', 'deploy', '--only', 'firestore:indexes'], 
                         check=True)
            print("✅ Firestore indexes deployed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to deploy Firestore indexes: {e}")
            return False
    
    def run_setup(self):
        """Run the complete setup process"""
        print("🚀 Starting Firebase Authentication Setup for GenX FX")
        print("=" * 60)
        
        # Check Firebase CLI
        if not self.check_firebase_cli():
            print("❌ Setup failed: Firebase CLI not available")
            return False
        
        # Login to Firebase
        if not self.login_firebase():
            print("❌ Setup failed: Could not login to Firebase")
            return False
        
        # Setup auth providers
        self.setup_auth_providers()
        
        # Get Firebase configuration
        config = self.get_firebase_config()
        
        # Create environment file
        self.create_env_file()
        
        # Deploy Firestore rules and indexes
        print("\n📋 Deploying Firestore configuration...")
        self.deploy_firestore_rules()
        self.deploy_firestore_indexes()
        
        print("\n" + "=" * 60)
        print("✅ Firebase Authentication Setup Complete!")
        print("\n📋 Next Steps:")
        print("1. Update .env file with your actual Firebase configuration values")
        print("2. Configure authentication providers in Firebase Console with redirect URIs")
        print("3. Test authentication in your application")
        print("\n🔗 Useful Links:")
        print(f"   • Firebase Console: https://console.firebase.google.com/project/{self.project_id}")
        print("   • Authentication: https://console.firebase.google.com/project/genx-467217/authentication")
        print("   • Firestore: https://console.firebase.google.com/project/genx-467217/firestore")
        
        return True

if __name__ == "__main__":
    setup = FirebaseAuthSetup()
    success = setup.run_setup()
    
    if success:
        print("\n🎉 Setup completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Setup failed. Please check the errors above.")
        sys.exit(1)