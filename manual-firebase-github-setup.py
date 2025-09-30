#!/usr/bin/env python3
"""
Manual Firebase GitHub Secrets & Variables Setup
Generates comprehensive setup instructions for Firebase integration
"""

import json
from pathlib import Path

class FirebaseGitHubSetup:
    def __init__(self):
        self.project_id = "genx-467217"
        self.auth_domain = f"{self.project_id}.firebaseapp.com"
        self.repo_owner = "Mouy-leng"
        self.repo_name = "GenX_FX"

    def get_firebase_secrets(self):
        """Get Firebase secrets that need to be added"""
        return {
            # Firebase Configuration Secrets
            "FIREBASE_API_KEY": "your_firebase_api_key_here",
            "FIREBASE_AUTH_DOMAIN": self.auth_domain,
            "FIREBASE_PROJECT_ID": self.project_id,
            "FIREBASE_STORAGE_BUCKET": f"{self.project_id}.appspot.com",
            "FIREBASE_MESSAGING_SENDER_ID": "your_messaging_sender_id_here",
            "FIREBASE_APP_ID": "your_firebase_app_id_here",
            "FIREBASE_MEASUREMENT_ID": "your_measurement_id_here",

            # Firebase Service Account (for server-side operations)
            "FIREBASE_SERVICE_ACCOUNT_KEY": "your_firebase_service_account_json_here",

            # Firebase Admin SDK
            "FIREBASE_ADMIN_SDK_KEY": "your_firebase_admin_sdk_key_here",

            # Additional Firebase secrets
            "FIREBASE_AUTH_UID": "your_auth_uid_here",
            "FIREBASE_WEB_API_KEY": "your_web_api_key_here",
        }

    def get_firebase_variables(self):
        """Get Firebase variables that need to be added"""
        return {
            # Firebase Configuration Variables
            "FIREBASE_PROJECT_ID": self.project_id,
            "FIREBASE_AUTH_DOMAIN": self.auth_domain,
            "FIREBASE_STORAGE_BUCKET": f"{self.project_id}.appspot.com",
            "FIREBASE_DATABASE_URL": f"https://{self.project_id}-default-rtdb.firebaseio.com/",

            # Firebase Environment
            "FIREBASE_ENV": "production",
            "FIREBASE_REGION": "us-central1",

            # Firebase Hosting
            "FIREBASE_HOSTING_URL": f"https://{self.project_id}.web.app",
            "FIREBASE_HOSTING_ALT_URL": f"https://{self.project_id}.firebaseapp.com",

            # API Configuration
            "API_BASE_URL": "https://api.genx-fx.com",
            "API_V1_BASE_URL": "https://api.genx-fx.com/api/v1",

            # Authentication Configuration
            "AUTH_REDIRECT_URL": f"https://{self.project_id}.web.app/auth/callback",
            "AUTH_DOMAIN": self.auth_domain,
        }

    def create_github_secrets_json(self):
        """Create JSON file with all GitHub secrets"""
        secrets = self.get_firebase_secrets()

        # Add existing secrets
        existing_secrets = {
            "AMP_TOKEN": "sgamp_user_01K1B28JVS8XWZQ3CEWJP8E5GN_97969aa27077d9e44e82ad554b337f2bda14a5e3eccf15165b1a09c24872495e",
            "DOCKER_USERNAME": "keamouyleng",
            "DOCKER_PASSWORD": "your_docker_hub_token_here",
            "AWS_ACCESS_KEY_ID": "your_aws_access_key_here",
            "AWS_SECRET_ACCESS_KEY": "your_aws_secret_key_here",
            "POSTGRES_PASSWORD": "Hz67QFj6P5RSxB6EZv7xT+S/3EXLDksUo1X/EVOAu3M=",
            "REDIS_PASSWORD": "w1W7BMXPYbG5lsH2/aND6VvNxxU1aAgA/sFWDyU/5bQ=",
        }

        secrets.update(existing_secrets)

        with open("github-secrets.json", "w") as f:
            json.dump(secrets, f, indent=2)

        print("📄 Created github-secrets.json with all secrets")

    def create_github_variables_json(self):
        """Create JSON file with all GitHub variables"""
        variables = self.get_firebase_variables()

        # Add existing variables
        existing_variables = {
            "AMP_ENV": "production",
            "DOCKER_IMAGE": "keamouyleng/genx-fx",
            "AWS_REGION": "us-east-1",
            "EC2_INSTANCE_TYPE": "t2.micro",
        }

        variables.update(existing_variables)

        with open("github-variables.json", "w") as f:
            json.dump(variables, f, indent=2)

        print("📄 Created github-variables.json with all variables")

    def create_comprehensive_guide(self):
        """Create comprehensive setup guide"""
        guide_content = f"""# 🔥 Complete Firebase GitHub Secrets & Variables Setup

## 🎯 **Repository: {self.repo_owner}/{self.repo_name}**
**Settings URL**: https://github.com/{self.repo_owner}/{self.repo_name}/settings/secrets/actions

## 📋 **All Secrets & Variables (Copy & Paste Ready)**

### 🔐 **Repository Secrets** (Settings → Secrets and variables → Actions → Secrets)

#### **🔥 NEW: Firebase Secrets**
```
Name: FIREBASE_API_KEY
Value: [Get from Firebase Console → Project Settings → Web App Config]
```

```
Name: FIREBASE_AUTH_DOMAIN
Value: {self.auth_domain}
```

```
Name: FIREBASE_PROJECT_ID
Value: {self.project_id}
```

```
Name: FIREBASE_STORAGE_BUCKET
Value: {self.project_id}.appspot.com
```

```
Name: FIREBASE_MESSAGING_SENDER_ID
Value: [Get from Firebase Console → Project Settings → Web App Config]
```

```
Name: FIREBASE_APP_ID
Value: [Get from Firebase Console → Project Settings → Web App Config]
```

```
Name: FIREBASE_MEASUREMENT_ID
Value: [Get from Firebase Console → Project Settings → Web App Config]
```

```
Name: FIREBASE_SERVICE_ACCOUNT_KEY
Value: [Get from Firebase Console → Project Settings → Service Accounts → Generate New Private Key]
```

```
Name: FIREBASE_ADMIN_SDK_KEY
Value: [Get from Firebase Console → Project Settings → Service Accounts → Admin SDK Config]
```

```
Name: FIREBASE_AUTH_UID
Value: [Your Firebase Auth UID]
```

```
Name: FIREBASE_WEB_API_KEY
Value: [Get from Firebase Console → Project Settings → Web App Config]
```

#### **✅ EXISTING: Already Configured Secrets**
```
Name: AMP_TOKEN
Value: sgamp_user_01K1B28JVS8XWZQ3CEWJP8E5GN_97969aa27077d9e44e82ad554b337f2bda14a5e3eccf15165b1a09c24872495e
```

```
Name: DOCKER_USERNAME
Value: keamouyleng
```

```
Name: DOCKER_PASSWORD
Value: [Your Docker Hub Access Token]
```

```
Name: AWS_ACCESS_KEY_ID
Value: [Your AWS Access Key ID]
```

```
Name: AWS_SECRET_ACCESS_KEY
Value: [Your AWS Secret Access Key]
```

```
Name: POSTGRES_PASSWORD
Value: Hz67QFj6P5RSxB6EZv7xT+S/3EXLDksUo1X/EVOAu3M=
```

```
Name: REDIS_PASSWORD
Value: w1W7BMXPYbG5lsH2/aND6VvNxxU1aAgA/sFWDyU/5bQ=
```

### 📊 **Repository Variables** (Settings → Secrets and variables → Actions → Variables)

#### **🔥 NEW: Firebase Variables**
```
Name: FIREBASE_PROJECT_ID
Value: {self.project_id}
```

```
Name: FIREBASE_AUTH_DOMAIN
Value: {self.auth_domain}
```

```
Name: FIREBASE_STORAGE_BUCKET
Value: {self.project_id}.appspot.com
```

```
Name: FIREBASE_DATABASE_URL
Value: https://{self.project_id}-default-rtdb.firebaseio.com/
```

```
Name: FIREBASE_ENV
Value: production
```

```
Name: FIREBASE_REGION
Value: us-central1
```

```
Name: FIREBASE_HOSTING_URL
Value: https://{self.project_id}.web.app
```

```
Name: FIREBASE_HOSTING_ALT_URL
Value: https://{self.project_id}.firebaseapp.com
```

```
Name: API_BASE_URL
Value: https://api.genx-fx.com
```

```
Name: API_V1_BASE_URL
Value: https://api.genx-fx.com/api/v1
```

```
Name: AUTH_REDIRECT_URL
Value: https://{self.project_id}.web.app/auth/callback
```

```
Name: AUTH_DOMAIN
Value: {self.auth_domain}
```

#### **✅ EXISTING: Already Configured Variables**
```
Name: AMP_ENV
Value: production
```

```
Name: DOCKER_IMAGE
Value: keamouyleng/genx-fx
```

```
Name: AWS_REGION
Value: us-east-1
```

```
Name: EC2_INSTANCE_TYPE
Value: t2.micro
```

## 🚀 **Step-by-Step Setup Instructions**

### **Step 1: Access GitHub Repository Settings**
1. Go to: **https://github.com/{self.repo_owner}/{self.repo_name}/settings/secrets/actions**
2. You'll see two tabs: **"Secrets"** and **"Variables"**

### **Step 2: Add Firebase Secrets**
1. Click **"Secrets"** tab
2. Click **"New repository secret"** for each Firebase secret above
3. Copy the exact Name and Value pairs

### **Step 3: Add Firebase Variables**
1. Click **"Variables"** tab
2. Click **"New repository variable"** for each Firebase variable above
3. Copy the exact Name and Value pairs

## 🔑 **How to Get Firebase Configuration Values**

### **Firebase Console Setup**
1. Go to: **https://console.firebase.google.com/project/{self.project_id}**
2. Click **"Project Settings"** (gear icon)
3. Scroll down to **"Your apps"** section

### **Get Web App Configuration**
1. If you don't have a web app, click **"Add app"** → **"Web"**
2. Register your app with name: `GenX FX Trading Platform`
3. Copy these values from the configuration object:
   - `apiKey` → `FIREBASE_API_KEY`
   - `authDomain` → `FIREBASE_AUTH_DOMAIN`
   - `projectId` → `FIREBASE_PROJECT_ID`
   - `storageBucket` → `FIREBASE_STORAGE_BUCKET`
   - `messagingSenderId` → `FIREBASE_MESSAGING_SENDER_ID`
   - `appId` → `FIREBASE_APP_ID`
   - `measurementId` → `FIREBASE_MEASUREMENT_ID`

### **Get Service Account Key**
1. In Firebase Console → **Project Settings** → **Service Accounts**
2. Click **"Generate new private key"**
3. Download the JSON file
4. Copy the entire JSON content for `FIREBASE_SERVICE_ACCOUNT_KEY`

## 🔧 **Firebase Authentication Configuration**

### **Required Redirect URIs**
Add these to your Firebase Authentication providers:

```
http://localhost:5173
http://localhost:3000
http://localhost:8080
https://{self.project_id}.firebaseapp.com
https://{self.project_id}.web.app
https://your-production-domain.com
```

### **Authentication Providers Setup**
1. Go to **Authentication** → **Sign-in method**
2. Enable these providers:
   - ✅ **Email/Password**
   - ✅ **Google OAuth** (with redirect URIs above)
   - ✅ **GitHub OAuth** (with redirect URIs above)

## 📋 **Complete Checklist**

### **🔥 NEW Firebase Secrets (Must Add)**
- [ ] `FIREBASE_API_KEY`
- [ ] `FIREBASE_AUTH_DOMAIN` = `{self.auth_domain}`
- [ ] `FIREBASE_PROJECT_ID` = `{self.project_id}`
- [ ] `FIREBASE_STORAGE_BUCKET` = `{self.project_id}.appspot.com`
- [ ] `FIREBASE_MESSAGING_SENDER_ID`
- [ ] `FIREBASE_APP_ID`
- [ ] `FIREBASE_MEASUREMENT_ID`
- [ ] `FIREBASE_SERVICE_ACCOUNT_KEY`
- [ ] `FIREBASE_ADMIN_SDK_KEY`
- [ ] `FIREBASE_AUTH_UID`
- [ ] `FIREBASE_WEB_API_KEY`

### **🔥 NEW Firebase Variables (Must Add)**
- [ ] `FIREBASE_PROJECT_ID` = `{self.project_id}`
- [ ] `FIREBASE_AUTH_DOMAIN` = `{self.auth_domain}`
- [ ] `FIREBASE_STORAGE_BUCKET` = `{self.project_id}.appspot.com`
- [ ] `FIREBASE_DATABASE_URL` = `https://{self.project_id}-default-rtdb.firebaseio.com/`
- [ ] `FIREBASE_ENV` = `production`
- [ ] `FIREBASE_REGION` = `us-central1`
- [ ] `FIREBASE_HOSTING_URL` = `https://{self.project_id}.web.app`
- [ ] `FIREBASE_HOSTING_ALT_URL` = `https://{self.project_id}.firebaseapp.com`
- [ ] `API_BASE_URL` = `https://api.genx-fx.com`
- [ ] `API_V1_BASE_URL` = `https://api.genx-fx.com/api/v1`
- [ ] `AUTH_REDIRECT_URL` = `https://{self.project_id}.web.app/auth/callback`
- [ ] `AUTH_DOMAIN` = `{self.auth_domain}`

### **✅ EXISTING Secrets (Already Configured)**
- [x] `AMP_TOKEN`
- [x] `DOCKER_USERNAME`
- [x] `DOCKER_PASSWORD`
- [x] `AWS_ACCESS_KEY_ID`
- [x] `AWS_SECRET_ACCESS_KEY`
- [x] `POSTGRES_PASSWORD`
- [x] `REDIS_PASSWORD`

### **✅ EXISTING Variables (Already Configured)**
- [x] `AMP_ENV`
- [x] `DOCKER_IMAGE`
- [x] `AWS_REGION`
- [x] `EC2_INSTANCE_TYPE`

## 🎯 **GitHub Actions Integration**

### **Environment Variables Available**
Your workflows can now use:
- `${{ secrets.FIREBASE_API_KEY }}`
- `${{ secrets.FIREBASE_PROJECT_ID }}`
- `${{ secrets.FIREBASE_SERVICE_ACCOUNT_KEY }}`
- `${{ vars.FIREBASE_HOSTING_URL }}`
- `${{ vars.API_BASE_URL }}`

### **Example Usage in GitHub Actions**
```yaml
- name: Deploy to Firebase
  run: |
    echo "${{ secrets.FIREBASE_SERVICE_ACCOUNT_KEY }}" > firebase-service-account.json
    firebase deploy --project ${{ vars.FIREBASE_PROJECT_ID }}
```

## 🔗 **Important Links**

- **GitHub Settings**: https://github.com/{self.repo_owner}/{self.repo_name}/settings/secrets/actions
- **Firebase Console**: https://console.firebase.google.com/project/{self.project_id}
- **Authentication Setup**: https://console.firebase.google.com/project/{self.project_id}/authentication
- **Firestore Rules**: https://console.firebase.google.com/project/{self.project_id}/firestore

## 🎉 **What You Get After Setup**

- ✅ **Firebase Authentication** fully integrated with GitHub Actions
- ✅ **Automated Firebase deployments** via GitHub Actions
- ✅ **Secure Firebase configuration** in repository secrets
- ✅ **Production-ready authentication** with OAuth providers
- ✅ **Firestore security rules** and database indexes
- ✅ **Complete trading platform** with user authentication

---

**Status**: 🔥 Firebase configuration ready for GitHub repository
**Next**: Add the new Firebase secrets and variables listed above
"""

        with open("COMPLETE_FIREBASE_GITHUB_SETUP.md", "w") as f:
            f.write(guide_content)

        print("📄 Created COMPLETE_FIREBASE_GITHUB_SETUP.md")

    def run_setup(self):
        """Run the complete Firebase GitHub setup"""
        print("🔥 Firebase GitHub Secrets & Variables Setup")
        print("=" * 60)
        print(f"Repository: {self.repo_owner}/{self.repo_name}")
        print(f"Project ID: {self.project_id}")
        print(f"Auth Domain: {self.auth_domain}")
        print("=" * 60)

        # Create JSON files
        self.create_github_secrets_json()
        self.create_github_variables_json()

        # Create comprehensive guide
        self.create_comprehensive_guide()

        print("\n" + "=" * 60)
        print("✅ Firebase GitHub Secrets & Variables Setup Complete!")
        print("\n📋 Files Created:")
        print("   • github-secrets.json - All secrets in JSON format")
        print("   • github-variables.json - All variables in JSON format")
        print("   • COMPLETE_FIREBASE_GITHUB_SETUP.md - Comprehensive setup guide")

        print("\n📋 Next Steps:")
        print("1. Go to GitHub repository settings")
        print("2. Add the new Firebase secrets and variables")
        print("3. Get actual Firebase configuration values from Firebase Console")
        print("4. Update placeholder values with real Firebase config")
        print("5. Configure Firebase Authentication providers")

        print(f"\n🔗 Important Links:")
        print(f"   • GitHub Settings: https://github.com/{self.repo_owner}/{self.repo_name}/settings/secrets/actions")
        print(f"   • Firebase Console: https://console.firebase.google.com/project/{self.project_id}")
        print(f"   • Setup Guide: COMPLETE_FIREBASE_GITHUB_SETUP.md")

        return True

def main():
    """Main execution function"""
    setup = FirebaseGitHubSetup()
    success = setup.run_setup()

    if success:
        print("\n🎉 Firebase GitHub setup completed successfully!")
        return 0
    else:
        print("\n❌ Firebase GitHub setup failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    import sys
    sys.exit(main())