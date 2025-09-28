# Firebase Authentication Setup Guide for GenX FX Trading Platform

This guide will help you set up Firebase Authentication for your GenX FX Trading Platform with proper redirect URIs and security configuration.

## 🚀 Quick Setup

### 1. Run the Automated Setup Script

```bash
python3 setup-firebase-auth.py
```

This script will:
- Check and install Firebase CLI if needed
- Login to Firebase
- Get your Firebase configuration
- Create environment files
- Deploy Firestore security rules and indexes

### 2. Manual Configuration Steps

If you prefer to set up manually or need to configure additional settings:

#### Step 1: Firebase Console Configuration

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Select your project: `genx-467217`
3. Navigate to **Authentication > Sign-in method**

#### Step 2: Enable Authentication Providers

Enable and configure the following providers:

##### Email/Password Authentication
- ✅ Enable Email/Password
- ✅ Enable Email link (passwordless sign-in) - Optional

##### Google Authentication
- ✅ Enable Google
- Add these redirect URIs:
  ```
  http://localhost:5173
  http://localhost:3000
  http://localhost:8080
  https://genx-467217.firebaseapp.com
  https://genx-467217.web.app
  https://your-production-domain.com
  ```

##### GitHub Authentication
- ✅ Enable GitHub
- Create a GitHub OAuth App:
  - Homepage URL: `https://genx-467217.firebaseapp.com`
  - Authorization callback URL: `https://genx-467217.firebaseapp.com/__/auth/handler`
- Add the same redirect URIs as Google

#### Step 3: Get Firebase Configuration

1. In Firebase Console, go to **Project Settings**
2. Scroll down to "Your apps" section
3. Click on your web app or create one if it doesn't exist
4. Copy the configuration object

#### Step 4: Update Environment Variables

Create or update `.env` file in your project root:

```env
# Firebase Configuration
VITE_FIREBASE_API_KEY=your_actual_api_key_here
VITE_FIREBASE_AUTH_DOMAIN=genx-467217.firebaseapp.com
VITE_FIREBASE_PROJECT_ID=genx-467217
VITE_FIREBASE_STORAGE_BUCKET=genx-467217.appspot.com
VITE_FIREBASE_MESSAGING_SENDER_ID=your_actual_sender_id_here
VITE_FIREBASE_APP_ID=your_actual_app_id_here
VITE_FIREBASE_MEASUREMENT_ID=your_actual_measurement_id_here

# API Configuration
VITE_API_BASE_URL=http://localhost:8081
VITE_API_V1_BASE_URL=http://localhost:8081/api/v1

# Development
NODE_ENV=development
```

## 🔧 Firebase Configuration Files

### Firestore Security Rules

The project includes comprehensive Firestore security rules in `firestore.rules`:

- **Users**: Can read/write their own profile data
- **Trading Signals**: Readable by all authenticated users, writable by admins only
- **Trade History**: Private to each user
- **System Settings**: Admin access only
- **Notifications**: User-specific access

### Firestore Indexes

Optimized indexes are defined in `firestore.indexes.json` for:
- Trading signals by timestamp and symbol
- Trade history by user and timestamp
- Notifications by user and timestamp

## 🔐 Authentication Features

### Supported Authentication Methods

1. **Email/Password**: Traditional sign-up and sign-in
2. **Google OAuth**: One-click Google authentication
3. **GitHub OAuth**: One-click GitHub authentication

### Security Features

- Email verification for new accounts
- Password reset functionality
- Secure user profile management
- Role-based access control (admin/user)
- Real-time authentication state management

## 🚀 Deployment Configuration

### Development Environment

```bash
# Install dependencies
npm install

# Start development server
npm run dev
```

### Production Deployment

1. **Update Redirect URIs**: Add your production domain to all authentication providers
2. **Environment Variables**: Update `.env` with production Firebase configuration
3. **Deploy Firestore Rules**: 
   ```bash
   firebase deploy --only firestore:rules
   ```
4. **Deploy Indexes**:
   ```bash
   firebase deploy --only firestore:indexes
   ```

## 📱 Client-Side Integration

### Authentication Components

- `AuthProvider`: Context provider for authentication state
- `LoginForm`: Email/password and OAuth sign-in
- `SignupForm`: Account creation with email verification

### Usage Example

```tsx
import { useAuth } from './components/Auth/AuthProvider'

function MyComponent() {
  const { user, signOut, loading } = useAuth()
  
  if (loading) return <div>Loading...</div>
  if (!user) return <div>Please sign in</div>
  
  return (
    <div>
      <h1>Welcome, {user.displayName}!</h1>
      <button onClick={signOut}>Sign Out</button>
    </div>
  )
}
```

## 🔍 Troubleshooting

### Common Issues

1. **Redirect URI Mismatch**
   - Ensure all redirect URIs are added to Firebase Console
   - Check that the domain matches exactly (including protocol)

2. **Firebase Configuration Not Loading**
   - Verify `.env` file exists and has correct variable names
   - Check that variables start with `VITE_` for Vite projects

3. **Authentication Not Working**
   - Check browser console for errors
   - Verify Firebase project settings
   - Ensure authentication providers are enabled

4. **Firestore Permission Denied**
   - Check Firestore security rules
   - Verify user authentication status
   - Ensure proper user claims for admin access

### Debug Commands

```bash
# Check Firebase login status
firebase login:list

# Test Firestore rules
firebase firestore:rules:test

# View project configuration
firebase projects:list

# Check deployed rules
firebase firestore:rules:get
```

## 📚 Additional Resources

- [Firebase Authentication Documentation](https://firebase.google.com/docs/auth)
- [Firestore Security Rules](https://firebase.google.com/docs/firestore/security/get-started)
- [Firebase Hosting Configuration](https://firebase.google.com/docs/hosting)
- [Firebase CLI Reference](https://firebase.google.com/docs/cli)

## 🆘 Support

If you encounter issues:

1. Check the troubleshooting section above
2. Review Firebase Console for error messages
3. Check browser developer console for client-side errors
4. Verify all redirect URIs are properly configured
5. Ensure Firebase project settings are correct

---

**Note**: Remember to keep your Firebase configuration secure and never commit sensitive API keys to version control.