# VPS Deployment Credentials Setup for GenX Trading Platform

## 🌐 VPS Providers Configuration

### 1. NameCheap VPS Credentials

```bash
# NameCheap VPS API Configuration
NAMECHEAP_API_USER=""          # Your NameCheap username
NAMECHEAP_API_KEY=""           # Generate from: https://ap.www.namecheap.com/settings/tools/apiaccess/
NAMECHEAP_USERNAME=""          # Account username
NAMECHEAP_CLIENT_IP=""         # Your IP address (whitelist required)

# VPS Specifications
NAMECHEAP_VPS_PLAN="Stellar Plus"  # 2 vCPU, 6GB RAM, 120GB SSD
NAMECHEAP_VPS_OS="Ubuntu 22.04"
NAMECHEAP_VPS_LOCATION="Phoenix, AZ"
```

### 2. Vultr VPS Credentials

```bash
# Vultr API Configuration
VULTR_API_KEY=""               # Generate from: https://my.vultr.com/settings/#settingsapi
VULTR_REGION="ewr"             # New York (ewr), London (lhr), Tokyo (nrt)
VULTR_PLAN="vc2-2c-4gb"        # 2 vCPU, 4GB RAM, 80GB SSD, $12/month
VULTR_OS_ID="387"              # Ubuntu 22.04 LTS x64

# Optional Vultr Features
VULTR_ENABLE_BACKUPS="true"
VULTR_ENABLE_DDOS_PROTECTION="true"
VULTR_ENABLE_PRIVATE_NETWORK="false"
```

### 3. Google Cloud Credentials (3 Accounts)

```bash
# Account 1: Primary Trading Account
GCP_ACCOUNT_1_EMAIL=""         # Gmail account 1
GCP_PROJECT_1_ID=""            # Project ID for account 1
GCP_SERVICE_ACCOUNT_1_KEY=""   # Service account JSON key path

# Account 2: Backup Trading Account  
GCP_ACCOUNT_2_EMAIL=""         # Gmail account 2
GCP_PROJECT_2_ID=""            # Project ID for account 2
GCP_SERVICE_ACCOUNT_2_KEY=""   # Service account JSON key path

# Account 3: Development/Testing Account
GCP_ACCOUNT_3_EMAIL=""         # Gmail account 3
GCP_PROJECT_3_ID=""            # Project ID for account 3
GCP_SERVICE_ACCOUNT_3_KEY=""   # Service account JSON key path

# Google Cloud Configuration
GCP_REGION="us-central1"       # Or us-east1, europe-west1
GCP_ZONE="us-central1-a"
GCP_MACHINE_TYPE="e2-medium"   # 2 vCPUs, 4GB RAM (~$24/month, but covered by $300 credit)
GCP_DISK_SIZE="50"             # GB
GCP_IMAGE_FAMILY="ubuntu-2204-lts"
GCP_IMAGE_PROJECT="ubuntu-os-cloud"
```

## 🎯 Free Tier Eligibility Check for Google Cloud

### Google Cloud $300 Free Trial Requirements

1. **New Google Account**: Each account must be new to Google Cloud
2. **Credit Card Required**: For identity verification (won't be charged)
3. **One Free Trial Per Person**: Only one trial per person/household
4. **12-Month Duration**: $300 credit expires after 12 months
5. **Always Free Tier**: Some services remain free after trial

### Estimated Costs with $300 Credit

- **e2-medium instance**: ~$24/month × 12 months = $288 (within credit)
- **Network egress**: ~$5-10/month
- **Storage**: ~$2-5/month
- **Total per account**: ~$300-350/year (mostly covered by credit)

## 🚀 Quick Setup Commands

### NameCheap VPS Setup

```bash
# Get your API credentials
echo "1. Login to NameCheap: https://www.namecheap.com/myaccount/login/"
echo "2. Go to API Access: https://ap.www.namecheap.com/settings/tools/apiaccess/"
echo "3. Enable API and whitelist your IP"
echo "4. Copy API key and username"
```

### Vultr VPS Setup

```bash
# Get your API credentials
echo "1. Login to Vultr: https://my.vultr.com/"
echo "2. Go to API: https://my.vultr.com/settings/#settingsapi"
echo "3. Generate API key"
echo "4. Copy API key"
```

### Google Cloud Setup (Per Account)

```bash
# Setup for each of the 3 accounts
echo "1. Create new Gmail account (if needed)"
echo "2. Go to Google Cloud Console: https://console.cloud.google.com/"
echo "3. Activate $300 free trial"
echo "4. Create new project"
echo "5. Enable Compute Engine API"
echo "6. Create service account and download JSON key"
```

## 📋 Credential Collection Checklist

### ✅ NameCheap Requirements

- [ ] NameCheap account created
- [ ] API access enabled
- [ ] IP address whitelisted
- [ ] API key generated
- [ ] Username confirmed

### ✅ Vultr Requirements

- [ ] Vultr account created
- [ ] Payment method added
- [ ] API key generated
- [ ] Region selected
- [ ] Plan confirmed

### ✅ Google Cloud Requirements (×3)

- [ ] Gmail Account 1 - Free trial activated
- [ ] Gmail Account 2 - Free trial activated  
- [ ] Gmail Account 3 - Free trial activated
- [ ] All projects created
- [ ] Service accounts configured
- [ ] JSON keys downloaded
- [ ] Compute Engine APIs enabled

## 🔧 Next Steps After Credentials

1. **Fill in credentials** in the sections above
2. **Run deployment scripts** (will be created)
3. **Configure DNS** for domain names
4. **Setup SSL certificates** for HTTPS
5. **Deploy GenX Magic Trading Platform**
6. **Start live trading operations**

## 💰 Cost Estimates

### NameCheap VPS

- **Stellar Plus**: $18.88/month
- **Total Year 1**: ~$226

### Vultr VPS

- **2 vCPU, 4GB RAM**: $12/month
- **Total Year 1**: ~$144

### Google Cloud (3 accounts)

- **Account 1**: $300 credit (12 months free)
- **Account 2**: $300 credit (12 months free)
- **Account 3**: $300 credit (12 months free)
- **Total Year 1**: $0 (covered by credits)

**Grand Total Year 1**: ~$370 for 5 VPS instances (3 essentially free!)

---

## 🎯 Ready to Deploy?

Once you provide the credentials above, I'll create automated deployment scripts for all providers and execute live deployment of the GenX Magic Trading Platform!
