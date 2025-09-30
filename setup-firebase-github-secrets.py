#!/usr/bin/env python3
"""
Firebase GitHub Secrets & Variables Setup Script
Adds Firebase configuration to GitHub repository secrets and variables
"""

import os
import requests
import base64
import json
from pathlib import Path
from nacl import encoding, public

# Configuration
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
REPO_OWNER = "Mouy-leng"
REPO_NAME = "GenX_FX"
BASE_URL = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}"

class FirebaseGitHubSecretsManager:
    def __init__(self):
        self.headers = {
            "Authorization": f"token {GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3+json"
        }
        self.project_id = "genx-467217"
        self.auth_domain = f"{self.project_id}.firebaseapp.com"

    def get_public_key(self):
        """Get repository public key for encryption"""
        response = requests.get(f"{BASE_URL}/actions/secrets/public-key", headers=self.headers)
        if response.status_code == 200:
            return response.json()
        raise Exception(f"Failed to get public key: {response.text}")

    def encrypt_secret(self, public_key_b64, secret_value):
        """Encrypt secret using repository public key"""
        public_key = public.PublicKey(public_key_b64.encode("utf-8"), encoding.Base64Encoder())
        box = public.SealedBox(public_key)
        encrypted = box.encrypt(secret_value.encode("utf-8"))
        return base64.b64encode(encrypted).decode("utf-8")

    def set_secret(self, name, value):
        """Set a repository secret"""
        key_data = self.get_public_key()
        encrypted_value = self.encrypt_secret(key_data["key"], value)

        data = {
            "encrypted_value": encrypted_value,
            "key_id": key_data["key_id"]
        }

        response = requests.put(f"{BASE_URL}/actions/secrets/{name}",
                              headers=self.headers, json=data)
        return response.status_code in [201, 204]

    def set_variable(self, name, value):
        """Set repository variable"""
        data = {"name": name, "value": value}
        response = requests.post(f"{BASE_URL}/actions/variables",
                               headers=self.headers, json=data)
        return response.status_code in [201, 204]

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

    def setup_firebase_secrets(self):
        """Setup Firebase secrets"""
        print("🔐 Setting up Firebase Secrets...")
        secrets = self.get_firebase_secrets()

        for name, value in secrets.items():
            try:
                success = self.set_secret(name, value)
                status = "✅ [OK]" if success else "❌ [ERROR]"
                print(f"   {status} {name}")
            except Exception as e:
                print(f"   ❌ [ERROR] {name}: {str(e)}")

    def setup_firebase_variables(self):
        """Setup Firebase variables"""
        print("\n📊 Setting up Firebase Variables...")
        variables = self.get_firebase_variables()

        for name, value in variables.items():
            try:
                success = self.set_variable(name, value)
                status = "✅ [OK]" if success else "❌ [ERROR]"
                print(f"   {status} {name} = {value}")
            except Exception as e:
                print(f"   ❌ [ERROR] {name}: {str(e)}")

    def create_firebase_guide(self):
        """Create comprehensive Firebase setup guide"""
        guide_content = f"""# 🔥 Firebase GitHub Secrets & Variables Setup

## 🎯 **Repository: {REPO_OWNER}/{REPO_NAME}**
**Settings URL**: https://github.com/{REPO_OWNER}/{REPO_NAME}/settings/secrets/actions

## 🔐 **Firebase Secrets Added**

### **✅ Firebase Configuration Secrets**
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

### **✅ Firebase Service Secrets**
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

## 📊 **Firebase Variables Added**

### **✅ Firebase Configuration Variables**
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

## 🚀 **How to Get Firebase Configuration Values**

### **Step 1: Access Firebase Console**
1. Go to: https://console.firebase.google.com/project/{self.project_id}
2. Click on **"Project Settings"** (gear icon)
3. Scroll down to **"Your apps"** section

### **Step 2: Get Web App Configuration**
1. If you don't have a web app, click **"Add app"** → **"Web"**
2. Register your app with name: `GenX FX Trading Platform`
3. Copy the configuration object values

### **Step 3: Get Service Account Key**
1. In Firebase Console → **Project Settings** → **Service Accounts**
2. Click **"Generate new private key"**
3. Download the JSON file
4. Copy the entire JSON content for `FIREBASE_SERVICE_ACCOUNT_KEY`

### **Step 4: Update GitHub Secrets**
1. Go to: https://github.com/{REPO_OWNER}/{REPO_NAME}/settings/secrets/actions
2. Update each secret with actual values from Firebase Console
3. Keep the placeholder values for now if you don't have the actual values yet

## 🔧 **Firebase Authentication Setup**

### **Required Redirect URIs for OAuth Providers**
Add these to your Firebase Authentication providers:

```
http://localhost:5173
http://localhost:3000
http://localhost:8080
https://{self.project_id}.firebaseapp.com
https://{self.project_id}.web.app
https://your-production-domain.com
```

### **Authentication Providers to Enable**
1. **Email/Password**: Enable in Firebase Console → Authentication → Sign-in method
2. **Google OAuth**: Enable and configure with redirect URIs above
3. **GitHub OAuth**: Enable and configure with redirect URIs above

## 🎯 **GitHub Actions Integration**

Your Firebase configuration is now ready for GitHub Actions workflows:

### **Environment Variables Available**
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

## ✅ **Next Steps**

1. **Get Firebase Configuration**: Visit Firebase Console and get actual values
2. **Update Secrets**: Replace placeholder values with real Firebase config
3. **Enable Authentication**: Configure OAuth providers with redirect URIs
4. **Deploy Firestore Rules**: `firebase deploy --only firestore:rules`
5. **Test Authentication**: Verify login/signup functionality

## 🔗 **Important Links**

- **Firebase Console**: https://console.firebase.google.com/project/{self.project_id}
- **GitHub Settings**: https://github.com/{REPO_OWNER}/{REPO_NAME}/settings/secrets/actions
- **Authentication Setup**: https://console.firebase.google.com/project/{self.project_id}/authentication
- **Firestore Rules**: https://console.firebase.google.com/project/{self.project_id}/firestore

---

**Status**: ✅ Firebase GitHub secrets and variables configured
**Ready for**: Firebase Console configuration and testing
"""

        with open("FIREBASE_GITHUB_SECRETS_GUIDE.md", "w") as f:
            f.write(guide_content)

        print(f"\n📋 Created FIREBASE_GITHUB_SECRETS_GUIDE.md")

    def run_setup(self):
        """Run the complete Firebase GitHub setup"""
        print("🔥 Firebase GitHub Secrets & Variables Setup")
        print("=" * 60)
        print(f"Repository: {REPO_OWNER}/{REPO_NAME}")
        print(f"Project ID: {self.project_id}")
        print(f"Auth Domain: {self.auth_domain}")
        print("=" * 60)

        if not GITHUB_TOKEN:
            print("❌ GITHUB_TOKEN environment variable not set")
            print("Please set GITHUB_TOKEN with a valid GitHub token")
            return False

        try:
            # Setup Firebase secrets
            self.setup_firebase_secrets()

            # Setup Firebase variables
            self.setup_firebase_variables()

            # Create comprehensive guide
            self.create_firebase_guide()

            print("\n" + "=" * 60)
            print("✅ Firebase GitHub Secrets & Variables Setup Complete!")
            print("\n📋 Next Steps:")
            print("1. Get actual Firebase configuration values from Firebase Console")
            print("2. Update GitHub secrets with real values")
            print("3. Configure Firebase Authentication providers")
            print("4. Deploy Firestore security rules")
            print("5. Test the complete authentication flow")

            print(f"\n🔗 Important Links:")
            print(f"   • GitHub Settings: https://github.com/{REPO_OWNER}/{REPO_NAME}/settings/secrets/actions")
            print(f"   • Firebase Console: https://console.firebase.google.com/project/{self.project_id}")
            print(f"   • Setup Guide: FIREBASE_GITHUB_SECRETS_GUIDE.md")

            return True

        except Exception as e:
            print(f"❌ Setup failed: {str(e)}")
            return False

def main():
    """Main execution function"""
    setup = FirebaseGitHubSecretsManager()
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