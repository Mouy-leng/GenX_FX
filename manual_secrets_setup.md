# Manual GitHub Secrets Setup Guide

Since the GitHub CLI doesn't have admin permissions to set repository secrets, here's a manual guide to set up all the secrets and environment variables.

## 🔐 GitHub Repository Secrets to Set

### Firebase Configuration
1. Go to: https://github.com/Mouy-leng/GenX_FX/settings/secrets/actions
2. Click "New repository secret" for each of the following:

| Secret Name | Value |
|-------------|-------|
| `FIREBASE_PROJECT_ID` | `genx-firebace` |
| `FIREBASE_PRIVATE_KEY_ID` | `cd773b0c7f9e210f494508859b6874237ea21dd9` |
| `FIREBASE_CLIENT_EMAIL` | `firebase-adminsdk-fbsvc@genx-firebace.iam.gserviceaccount.com` |
| `FIREBASE_CLIENT_ID` | `100615928317007044005` |
| `FIREBASE_AUTH_URI` | `https://accounts.google.com/o/oauth2/auth` |
| `FIREBASE_TOKEN_URI` | `https://oauth2.googleapis.com/token` |
| `FIREBASE_AUTH_PROVIDER_X509_CERT_URL` | `https://www.googleapis.com/oauth2/v1/certs` |
| `FIREBASE_CLIENT_X509_CERT_URL` | `https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-fbsvc%40genx-firebace.iam.gserviceaccount.com` |
| `FIREBASE_UNIVERSE_DOMAIN` | `googleapis.com` |

### Google Cloud Configuration
| Secret Name | Value |
|-------------|-------|
| `GOOGLE_CLOUD_PROJECT_ID` | `flash-student-473123-n2` |
| `GOOGLE_CLOUD_PRIVATE_KEY_ID` | `a0ca3a5d08c3eb7aa0e7147537c16e7d25667af8` |
| `GOOGLE_CLOUD_CLIENT_EMAIL` | `genx-fx-project-yn-901@flash-student-473123-n2.iam.gserviceaccount.com` |
| `GOOGLE_CLOUD_CLIENT_ID` | `116534516340075466625` |
| `GOOGLE_CLOUD_AUTH_URI` | `https://accounts.google.com/o/oauth2/auth` |
| `GOOGLE_CLOUD_TOKEN_URI` | `https://oauth2.googleapis.com/token` |
| `GOOGLE_CLOUD_AUTH_PROVIDER_X509_CERT_URL` | `https://www.googleapis.com/oauth2/v1/certs` |
| `GOOGLE_CLOUD_CLIENT_X509_CERT_URL` | `https://www.googleapis.com/robot/v1/metadata/x509/genx-fx-project-yn-901%40flash-student-473123-n2.iam.gserviceaccount.com` |
| `GOOGLE_CLOUD_UNIVERSE_DOMAIN` | `googleapis.com` |

### Compute Engine Configuration
| Secret Name | Value |
|-------------|-------|
| `COMPUTE_PROJECT_ID` | `sharp-doodad-471511-s5` |
| `COMPUTE_PRIVATE_KEY_ID` | `0b4fd7b7320e4a014bbdc33c99b84a33c22e4049` |
| `COMPUTE_CLIENT_EMAIL` | `236873001744-compute@developer.gserviceaccount.com` |
| `COMPUTE_CLIENT_ID` | `117105304298472220058` |
| `COMPUTE_AUTH_URI` | `https://accounts.google.com/o/oauth2/auth` |
| `COMPUTE_TOKEN_URI` | `https://oauth2.googleapis.com/token` |
| `COMPUTE_AUTH_PROVIDER_X509_CERT_URL` | `https://www.googleapis.com/oauth2/v1/certs` |
| `COMPUTE_CLIENT_X509_CERT_URL` | `https://www.googleapis.com/robot/v1/metadata/x509/236873001744-compute%40developer.gserviceaccount.com` |
| `COMPUTE_UNIVERSE_DOMAIN` | `googleapis.com` |

### Service Account Keys (Full JSON)
For these secrets, copy the entire JSON content from the respective files:

| Secret Name | File Path |
|-------------|-----------|
| `FIREBASE_SERVICE_ACCOUNT_KEY` | `/workspace/drive_content/JSON/genx-firebace-cd773b0c7f9e.json` |
| `GOOGLE_CLOUD_SERVICE_ACCOUNT_KEY` | `/workspace/drive_content/JSON/flash-student-473123-n2-a0ca3a5d08c3.json` |
| `COMPUTE_SERVICE_ACCOUNT_KEY` | `/workspace/drive_content/JSON/sharp-doodad-471511-s5-0b4fd7b7320e.json` |

### SSL Certificates
| Secret Name | File Path |
|-------------|-----------|
| `SSL_CERTIFICATE` | `/workspace/drive_content/JSON/genxfx_org.crt` |
| `SSL_CA_BUNDLE` | `/workspace/drive_content/JSON/genxfx_org.ca-bundle` |
| `SSL_P7B_CERTIFICATE` | `/workspace/drive_content/JSON/genxfx_org.p7b` |

### Repository Configuration
| Secret Name | Value |
|-------------|-------|
| `GITHUB_TOKEN` | `ghs_rhJSLBXTMQJr8lDIovFjnwuWTIwJId359Fxh` |
| `REPOSITORY_NAME` | `GenX_FX` |
| `REPOSITORY_OWNER` | `Mouy-leng` |

## 🌍 Environment Variables

The following environment files have been created:
- `.env` - Development environment variables
- `.env.production` - Production environment variables

## 📋 Summary

✅ **Environment Variables Created:**
- `.env` file with all configuration
- `.env.production` file for production deployment

✅ **Service Account Keys Extracted:**
- Firebase Service Account (genx-firebace)
- Google Cloud Service Account (flash-student-473123-n2)
- Compute Engine Service Account (sharp-doodad-471511-s5)

✅ **SSL Certificates Extracted:**
- genxfx_org.crt
- genxfx_org.ca-bundle
- genxfx_org.p7b

✅ **Additional Files:**
- Docker login credentials
- Git commands documentation
- Gemini API trading bot risks documentation
- Hosting receipt

## 🚀 Next Steps

1. **Set up GitHub Secrets manually** using the table above
2. **Verify environment variables** in `.env` and `.env.production` files
3. **Test the configuration** by running your application
4. **Update CI/CD pipelines** to use the new secrets and variables

## 📁 File Locations

All extracted files are located in:
- `/workspace/drive_content/JSON/` - Service account keys and SSL certificates
- `/workspace/drive_content/Google AI Studio/` - Additional documentation and files
- `/workspace/.env` - Environment variables
- `/workspace/.env.production` - Production environment variables
- `/workspace/SECRETS_SETUP_SUMMARY.md` - Complete setup summary