#!/usr/bin/env python3
"""
NameCheap VPS Deployment Setup
Step-by-step guide to get NameCheap API credentials and deploy GenX Trading Platform
"""

import os
import sys
import requests
import json
from datetime import datetime
from pathlib import Path

class NameCheapDeployment:
    def __init__(self):
        self.api_base = "https://api.namecheap.com/xml.response"
        self.credentials = {
            "api_user": os.getenv("NAMECHEAP_API_USER"),
            "api_key": os.getenv("NAMECHEAP_API_KEY"),
            "username": os.getenv("NAMECHEAP_USERNAME"),
            "client_ip": os.getenv("NAMECHEAP_CLIENT_IP", "117.20.115.126")
        }
        
    def show_credential_setup(self):
        """Show how to get NameCheap API credentials"""
        print("🔐 NAMECHEAP API CREDENTIALS SETUP")
        print("=" * 50)
        
        print("\n📋 Step 1: Enable API Access")
        print("1. Login to your NameCheap account")
        print("2. Go to Profile → Tools → Business & Dev Tools → API Access")
        print("3. Enable API access for your account")
        print("4. Note down your credentials")
        
        print("\n📋 Step 2: Whitelist Your IP Address")
        print(f"Your current IP: {self.credentials['client_ip']}")
        print("1. In API Access settings, add this IP to whitelist")
        print("2. Save the IP whitelist settings")
        
        print("\n📋 Step 3: Get Your Credentials")
        print("You'll need these 4 values:")
        print("• API User (your NameCheap username)")
        print("• API Key (generated in API settings)")
        print("• Username (same as API User)")
        print("• Client IP (your whitelisted IP)")
        
        print("\n🔗 NameCheap API Access URL:")
        print("https://ap.www.namecheap.com/settings/tools/apiaccess/")
        
    def check_credentials(self):
        """Check if credentials are set"""
        print("\n🔍 Checking Current Credentials...")
        
        missing = []
        for key, value in self.credentials.items():
            if value:
                print(f"✅ {key.upper()}: Set")
            else:
                print(f"❌ {key.upper()}: Missing")
                missing.append(key)
        
        return len(missing) == 0
    
    def set_credentials_interactive(self):
        """Interactive credential setup"""
        print("\n💻 INTERACTIVE CREDENTIAL SETUP")
        print("=" * 40)
        
        # Get credentials from user
        api_user = input("Enter your NameCheap API User: ").strip()
        api_key = input("Enter your NameCheap API Key: ").strip()
        username = input("Enter your NameCheap Username (usually same as API User): ").strip() or api_user
        client_ip = input(f"Enter your Client IP [{self.credentials['client_ip']}]: ").strip() or self.credentials['client_ip']
        
        # Set environment variables
        os.environ["NAMECHEAP_API_USER"] = api_user
        os.environ["NAMECHEAP_API_KEY"] = api_key
        os.environ["NAMECHEAP_USERNAME"] = username
        os.environ["NAMECHEAP_CLIENT_IP"] = client_ip
        
        # Update credentials
        self.credentials = {
            "api_user": api_user,
            "api_key": api_key,
            "username": username,
            "client_ip": client_ip
        }
        
        print("\n✅ Credentials set in environment")
        
        # Create PowerShell commands for future use
        ps_commands = f"""
# NameCheap API Credentials - Save these commands
$env:NAMECHEAP_API_USER = "{api_user}"
$env:NAMECHEAP_API_KEY = "{api_key}"
$env:NAMECHEAP_USERNAME = "{username}"
$env:NAMECHEAP_CLIENT_IP = "{client_ip}"
"""
        
        with open("namecheap_credentials.ps1", "w") as f:
            f.write(ps_commands)
        
        print("💾 Credentials saved to: namecheap_credentials.ps1")
        
    def test_api_connection(self):
        """Test NameCheap API connection"""
        print("\n🧪 Testing NameCheap API Connection...")
        
        if not self.check_credentials():
            print("❌ Cannot test - credentials missing")
            return False
        
        # Test API call - get domain list
        params = {
            'ApiUser': self.credentials['api_user'],
            'ApiKey': self.credentials['api_key'],
            'UserName': self.credentials['username'],
            'Command': 'namecheap.domains.getList',
            'ClientIp': self.credentials['client_ip']
        }
        
        try:
            print("🔄 Making API test call...")
            response = requests.get(self.api_base, params=params, timeout=15)
            
            print(f"📡 Response Status: {response.status_code}")
            
            if response.status_code == 200:
                print("✅ API Connection: SUCCESS")
                
                # Basic XML parsing to check for errors
                if "ApiResponse Status=\"ERROR\"" in response.text:
                    print("⚠️  API Error in response:")
                    # Extract error message
                    if "Error Number" in response.text:
                        print(f"   Check your credentials and IP whitelist")
                    print("   Full response available for debugging")
                    return False
                else:
                    print("✅ API Authentication: SUCCESS")
                    print("🎉 Ready for VPS deployment!")
                    return True
            else:
                print(f"❌ API Connection Failed: HTTP {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ API Test Failed: {e}")
            return False
    
    def show_vps_options(self):
        """Show NameCheap VPS options"""
        print("\n🖥️  NAMECHEAP VPS OPTIONS")
        print("=" * 40)
        
        vps_plans = [
            {
                "name": "Stellar Plus",
                "cpu": "2 vCPU",
                "ram": "6GB RAM", 
                "storage": "120GB SSD",
                "bandwidth": "3TB",
                "price": "$19.98/month",
                "recommended": True
            },
            {
                "name": "Stellar Business",
                "cpu": "4 vCPU",
                "ram": "8GB RAM",
                "storage": "200GB SSD", 
                "bandwidth": "4TB",
                "price": "$29.98/month",
                "recommended": False
            }
        ]
        
        for plan in vps_plans:
            status = "⭐ RECOMMENDED" if plan["recommended"] else ""
            print(f"\n📦 {plan['name']} {status}")
            print(f"   💻 {plan['cpu']}, {plan['ram']}")
            print(f"   💾 {plan['storage']}")
            print(f"   🌐 {plan['bandwidth']} bandwidth")
            print(f"   💰 {plan['price']}")
    
    def deploy_to_namecheap(self):
        """Execute NameCheap VPS deployment"""
        print("\n🚀 DEPLOYING TO NAMECHEAP VPS")
        print("=" * 40)
        
        if not self.test_api_connection():
            print("❌ Cannot deploy - API connection failed")
            return False
        
        print("✅ API connection verified")
        print("🚀 Executing deployment script...")
        
        # Run the actual deployment script
        deployment_script = Path("deploy_namecheap_vps.sh")
        
        if deployment_script.exists():
            print(f"📋 Found deployment script: {deployment_script}")
            
            # For Windows, we'll need to adapt the bash script
            print("🔄 Adapting deployment for Windows...")
            
            # Create Python version of deployment
            self.create_python_deployment()
            
            return True
        else:
            print("❌ Deployment script not found")
            return False
    
    def create_python_deployment(self):
        """Create Python version of NameCheap deployment"""
        print("🐍 Creating Python deployment script...")
        
        deployment_code = '''
#!/usr/bin/env python3
"""
NameCheap VPS Deployment - Python Version
"""
import requests
import time
import os

def deploy_namecheap_vps():
    print("🚀 Starting NameCheap VPS Deployment...")
    
    # VPS Configuration
    config = {
        "hostname": f"genx-trading-{int(time.time())}",
        "plan": "stellar-plus",
        "os": "ubuntu-22-04",
        "location": "phoenix-az"
    }
    
    # For now, we'll simulate the deployment process
    print("📋 VPS Configuration:")
    for key, value in config.items():
        print(f"   {key}: {value}")
    
    print("\\n🎯 Next Steps:")
    print("1. ✅ API credentials verified")
    print("2. 🔄 VPS creation would happen here")
    print("3. 📦 GenX platform deployment")
    print("4. 🔐 SSH key installation")
    print("5. 🌐 Domain/IP configuration")
    
    print("\\n💡 This is a simulation - real deployment requires:")
    print("• NameCheap VPS API (currently in beta)")
    print("• Manual VPS creation through NameCheap panel")
    print("• SSH deployment of GenX platform")
    
    return True

if __name__ == "__main__":
    deploy_namecheap_vps()
'''
        
        with open("deploy_namecheap_python.py", "w") as f:
            f.write(deployment_code)
        
        print("✅ Python deployment script created")
        
        # Execute the deployment
        os.system("python deploy_namecheap_python.py")

def main():
    """Main function"""
    print("🚀 GenX Trading Platform - NameCheap VPS Deployment")
    print("=" * 55)
    
    deployment = NameCheapDeployment()
    
    # Step 1: Show credential setup
    deployment.show_credential_setup()
    
    # Step 2: Check current credentials
    if deployment.check_credentials():
        print("✅ Credentials already set")
        
        # Test API connection
        if deployment.test_api_connection():
            print("✅ Ready for deployment")
        else:
            print("❌ API connection issues")
            return False
    else:
        print("⚠️  Credentials missing")
        
        # Ask if user wants to set credentials now
        choice = input("\nWould you like to set credentials now? (y/n): ").lower()
        if choice == 'y':
            deployment.set_credentials_interactive()
            
            # Test after setting
            if deployment.test_api_connection():
                print("✅ Credentials working!")
            else:
                print("❌ Credential test failed")
                return False
        else:
            print("📋 Set credentials manually using the instructions above")
            return False
    
    # Step 3: Show VPS options
    deployment.show_vps_options()
    
    # Step 4: Deploy
    deploy_choice = input("\nDeploy to NameCheap VPS now? (y/n): ").lower()
    if deploy_choice == 'y':
        return deployment.deploy_to_namecheap()
    else:
        print("📋 Deployment ready when you are!")
        print("Run: python deploy_namecheap_python.py")
        return True

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎉 NameCheap deployment setup complete!")
    else:
        print("\n⚠️  Please resolve issues and try again")