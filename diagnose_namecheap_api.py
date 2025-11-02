#!/usr/bin/env python3
"""
NameCheap API Diagnostic Tool
Test API connection and troubleshoot issues
"""

import requests
import xml.etree.ElementTree as ET
import os
from urllib.parse import urlencode

def test_namecheap_api():
    """Test NameCheap API with detailed diagnostics"""
    print("NameCheap API Diagnostic Tool")
    print("=" * 50)
    
    # Get credentials
    api_user = os.environ.get('NAMECHEAP_API_USER')
    api_key = os.environ.get('NAMECHEAP_API_KEY')
    username = os.environ.get('NAMECHEAP_USERNAME')
    client_ip = os.environ.get('NAMECHEAP_CLIENT_IP', '117.20.115.126')
    
    print(f"API User: {api_user}")
    print(f"Username: {username}")
    print(f"Client IP: {client_ip}")
    print(f"API Key: {'*' * 20}{api_key[-8:] if api_key else 'NOT SET'}")
    
    if not all([api_user, api_key, username, client_ip]):
        print("\nERROR: Missing required credentials")
        return False
    
    # Test different API endpoints
    test_endpoints = [
        ("Production API", "https://api.namecheap.com/xml.response"),
        ("Sandbox API", "https://api.sandbox.namecheap.com/xml.response")
    ]
    
    for name, api_url in test_endpoints:
        print(f"\nTesting {name}: {api_url}")
        print("-" * 50)
        
        # Simple API test - get domain list
        params = {
            'ApiUser': api_user,
            'ApiKey': api_key,
            'UserName': username,
            'Command': 'namecheap.domains.getList',
            'ClientIp': client_ip,
            'PageSize': '1',
            'Page': '1'
        }
        
        try:
            print(f"Making request with params: {list(params.keys())}")
            response = requests.get(api_url, params=params, timeout=30)
            print(f"Response status: {response.status_code}")
            print(f"Response headers: {dict(response.headers)}")
            
            if response.status_code == 200:
                try:
                    root = ET.fromstring(response.content)
                    status = root.get('Status')
                    print(f"API Response Status: {status}")
                    
                    if status == 'OK':
                        print("SUCCESS: API connection working!")
                        
                        # Check for domain list
                        domains = root.findall('.//Domain')
                        print(f"Found {len(domains)} domains in account")
                        
                        return True
                        
                    elif status == 'ERROR':
                        errors = root.findall('.//Error')
                        for error in errors:
                            error_num = error.get('Number')
                            error_text = error.text
                            print(f"API Error {error_num}: {error_text}")
                    
                except ET.ParseError as e:
                    print(f"XML Parse Error: {e}")
                    print(f"Raw response: {response.text[:500]}")
            else:
                print(f"HTTP Error: {response.status_code}")
                print(f"Response: {response.text[:500]}")
                
        except requests.exceptions.RequestException as e:
            print(f"Request Exception: {e}")
        except Exception as e:
            print(f"Unexpected Error: {e}")
    
    return False

def check_ip_whitelist():
    """Check current IP and whitelist status"""
    print("\nChecking IP Address...")
    print("=" * 30)
    
    try:
        # Get current public IP
        ip_response = requests.get('https://api.ipify.org', timeout=10)
        current_ip = ip_response.text.strip()
        print(f"Your current IP: {current_ip}")
        
        configured_ip = os.environ.get('NAMECHEAP_CLIENT_IP', '117.20.115.126')
        print(f"Configured IP: {configured_ip}")
        
        if current_ip != configured_ip:
            print("WARNING: Current IP doesn't match configured IP!")
            print("You may need to update the whitelist in NameCheap")
            print("Go to: https://ap.www.namecheap.com/settings/tools/apiaccess/")
        else:
            print("OK: IP addresses match")
            
    except Exception as e:
        print(f"Could not check IP: {e}")

def manual_vps_instructions():
    """Provide manual VPS deployment instructions"""
    print("\n" + "=" * 60)
    print("MANUAL VPS DEPLOYMENT INSTRUCTIONS")
    print("=" * 60)
    
    print("\nStep 1: Create NameCheap VPS")
    print("1. Go to: https://www.namecheap.com/hosting/vps/")
    print("2. Choose 'Stellar Plus' plan ($19.98/month)")
    print("   - 2 vCPU cores")
    print("   - 6GB RAM") 
    print("   - 120GB SSD")
    print("   - 3TB bandwidth")
    print("3. Select Ubuntu 22.04 LTS operating system")
    print("4. Choose Phoenix, AZ datacenter")
    print("5. Complete purchase and wait for VPS setup")
    
    print("\nStep 2: Get VPS Details")
    print("1. Check email for VPS login details")
    print("2. Note your VPS IP address")
    print("3. Note root password")
    
    print("\nStep 3: Connect to VPS")
    print("1. Use SSH: ssh root@YOUR_VPS_IP")
    print("2. Or use NameCheap VPS console")
    
    print("\nStep 4: Deploy GenX Trading Platform")
    print("1. Upload the setup script to your VPS")
    print("2. Run: chmod +x namecheap_vps_setup.sh")
    print("3. Run: ./namecheap_vps_setup.sh")
    
    print("\nStep 5: Configure Domain (Optional)")
    print("1. Point domain to VPS IP in DNS settings")
    print("2. Wait for DNS propagation (24-48 hours)")
    print("3. Access: http://yourdomain.com")

def main():
    """Main diagnostic function"""
    test_namecheap_api()
    check_ip_whitelist()
    manual_vps_instructions()
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print("If API connection failed:")
    print("1. Check API is enabled: https://ap.www.namecheap.com/settings/tools/apiaccess/")
    print("2. Verify IP whitelist includes your current IP")
    print("3. Ensure API key is correct")
    print("4. Try manual VPS deployment instead")
    
    print("\nFor immediate deployment:")
    print("1. Your local trading platform is working (localhost:8000)")
    print("2. Manual VPS deployment is straightforward")
    print("3. All setup scripts are ready")

if __name__ == "__main__":
    main()