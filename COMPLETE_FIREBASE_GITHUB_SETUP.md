# 🔥 Complete Firebase GitHub Secrets & Variables Setup

## 🎯 **Repository: Mouy-leng/GenX_FX**
**Settings URL**: https://github.com/Mouy-leng/GenX_FX/settings/secrets/actions

## 📋 **All Secrets & Variables (Copy & Paste Ready)**

### 🔐 **Repository Secrets** (Settings → Secrets and variables → Actions → Secrets)

#### **🔥 NEW: Firebase Secrets**
```
Name: FIREBASE_API_KEY
Value: [Get from Firebase Console → Project Settings → Web App Config]
```

```
Name: FIREBASE_AUTH_DOMAIN
Value: genx-467217.firebaseapp.com
```

```
Name: FIREBASE_PROJECT_ID
Value: genx-467217
```

```
Name: FIREBASE_STORAGE_BUCKET
Value: genx-467217.appspot.com
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
Value: genx-467217
```

```
Name: FIREBASE_AUTH_DOMAIN
Value: genx-467217.firebaseapp.com
```

```
Name: FIREBASE_STORAGE_BUCKET
Value: genx-467217.appspot.com
```

```
Name: FIREBASE_DATABASE_URL
Value: https://genx-467217-default-rtdb.firebaseio.com/
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
Value: https://genx-467217.web.app
```

```
Name: FIREBASE_HOSTING_ALT_URL
Value: https://genx-467217.firebaseapp.com
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
Value: https://genx-467217.web.app/auth/callback
```

```
Name: AUTH_DOMAIN
Value: genx-467217.firebaseapp.com
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
1. Go to: **https://github.com/Mouy-leng/GenX_FX/settings/secrets/actions**
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
1. Go to: **https://console.firebase.google.com/project/genx-467217**
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
https://genx-467217.firebaseapp.com
https://genx-467217.web.app
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
- [ ] `FIREBASE_AUTH_DOMAIN` = `genx-467217.firebaseapp.com`
- [ ] `FIREBASE_PROJECT_ID` = `genx-467217`
- [ ] `FIREBASE_STORAGE_BUCKET` = `genx-467217.appspot.com`
- [ ] `FIREBASE_MESSAGING_SENDER_ID`
- [ ] `FIREBASE_APP_ID`
- [ ] `FIREBASE_MEASUREMENT_ID`
- [ ] `FIREBASE_SERVICE_ACCOUNT_KEY`
- [ ] `FIREBASE_ADMIN_SDK_KEY`
- [ ] `FIREBASE_AUTH_UID`
- [ ] `FIREBASE_WEB_API_KEY`

### **🔥 NEW Firebase Variables (Must Add)**
- [ ] `FIREBASE_PROJECT_ID` = `genx-467217`
- [ ] `FIREBASE_AUTH_DOMAIN` = `genx-467217.firebaseapp.com`
- [ ] `FIREBASE_STORAGE_BUCKET` = `genx-467217.appspot.com`
- [ ] `FIREBASE_DATABASE_URL` = `https://genx-467217-default-rtdb.firebaseio.com/`
- [ ] `FIREBASE_ENV` = `production`
- [ ] `FIREBASE_REGION` = `us-central1`
- [ ] `FIREBASE_HOSTING_URL` = `https://genx-467217.web.app`
- [ ] `FIREBASE_HOSTING_ALT_URL` = `https://genx-467217.firebaseapp.com`
- [ ] `API_BASE_URL` = `https://api.genx-fx.com`
- [ ] `API_V1_BASE_URL` = `https://api.genx-fx.com/api/v1`
- [ ] `AUTH_REDIRECT_URL` = `https://genx-467217.web.app/auth/callback`
- [ ] `AUTH_DOMAIN` = `genx-467217.firebaseapp.com`

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
- `${ secrets.FIREBASE_API_KEY }`
- `${ secrets.FIREBASE_PROJECT_ID }`
- `${ secrets.FIREBASE_SERVICE_ACCOUNT_KEY }`
- `${ vars.FIREBASE_HOSTING_URL }`
- `${ vars.API_BASE_URL }`

### **Example Usage in GitHub Actions**
```yaml
- name: Deploy to Firebase
  run: |
    echo "${ secrets.FIREBASE_SERVICE_ACCOUNT_KEY }" > firebase-service-account.json
    firebase deploy --project ${ vars.FIREBASE_PROJECT_ID }
```

## 🔗 **Important Links**

- **GitHub Settings**: https://github.com/Mouy-leng/GenX_FX/settings/secrets/actions
- **Firebase Console**: https://console.firebase.google.com/project/genx-467217
- **Authentication Setup**: https://console.firebase.google.com/project/genx-467217/authentication
- **Firestore Rules**: https://console.firebase.google.com/project/genx-467217/firestore

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
