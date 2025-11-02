#!/usr/bin/env python3
"""
NameCheap Domain Name Checker
Check available domains and manage existing domains
"""

import requests
import xml.etree.ElementTree as ET
import os
from datetime import datetime
import json

class NameCheapDomainChecker:
    def __init__(self):
        self.api_user = os.environ.get('NAMECHEAP_API_USER')
        self.api_key = os.environ.get('NAMECHEAP_API_KEY')
        self.username = os.environ.get('NAMECHEAP_USERNAME')
        self.client_ip = os.environ.get('NAMECHEAP_CLIENT_IP', '117.20.115.126')
        self.sandbox = os.environ.get('NAMECHEAP_SANDBOX', 'false').lower() == 'true'
        
        # API endpoints
        if self.sandbox:
            self.api_url = "https://api.sandbox.namecheap.com/xml.response"
        else:
            self.api_url = "https://api.namecheap.com/xml.response"
    
    def check_credentials(self):
        """Check if NameCheap API credentials are set"""
        print("🔐 Checking NameCheap API Credentials...")
        print("=" * 50)
        
        credentials = {
            'API_USER': self.api_user,
            'API_KEY': self.api_key,
            'USERNAME': self.username,
            'CLIENT_IP': self.client_ip
        }
        
        missing = []
        for key, value in credentials.items():
            if value:
                print(f"✅ {key}: {'*' * (len(value) - 4)}{value[-4:]}")
            else:
                print(f"❌ {key}: NOT SET")
                missing.append(key)
        
        if missing:
            print(f"\n⚠️ Missing credentials: {', '.join(missing)}")
            print("\n📋 To set credentials, run:")
            print('$env:NAMECHEAP_API_USER = "your_username"')
            print('$env:NAMECHEAP_API_KEY = "your_api_key"')
            print('$env:NAMECHEAP_USERNAME = "your_username"')
            print('$env:NAMECHEAP_CLIENT_IP = "117.20.115.126"')
            return False
        
        print("\n✅ All credentials are set!")
        return True
    
    def make_api_request(self, command, params=None):
        """Make API request to NameCheap"""
        if not self.check_credentials():
            return None
        
        base_params = {
            'ApiUser': self.api_user,
            'ApiKey': self.api_key,
            'UserName': self.username,
            'Command': command,
            'ClientIp': self.client_ip
        }
        
        if params:
            base_params.update(params)
        
        try:
            response = requests.get(self.api_url, params=base_params, timeout=30)
            response.raise_for_status()
            
            # Parse XML response
            root = ET.fromstring(response.content)
            
            # Check for API errors
            if root.get('Status') == 'ERROR':
                errors = root.findall('.//Error')
                for error in errors:
                    print(f"❌ API Error: {error.text}")
                return None
            
            return root
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Request failed: {e}")
            return None
        except ET.ParseError as e:
            print(f"❌ XML parsing failed: {e}")
            return None
    
    def check_domain_availability(self, domains):
        """Check if domains are available for registration"""
        print(f"\n🔍 Checking Domain Availability...")
        print("=" * 50)
        
        if isinstance(domains, str):
            domains = [domains]
        
        # NameCheap API supports checking multiple domains at once
        domain_list = ','.join(domains)
        
        params = {
            'DomainList': domain_list
        }
        
        response = self.make_api_request('namecheap.domains.check', params)
        if not response:
            return {}
        
        results = {}
        domain_elements = response.findall('.//DomainCheckResult')
        
        for domain_elem in domain_elements:
            domain = domain_elem.get('Domain')
            available = domain_elem.get('Available', 'false').lower() == 'true'
            premium = domain_elem.get('IsPremiumName', 'false').lower() == 'true'
            error_code = domain_elem.get('ErrorCode')
            
            status = "❌ Not Available"
            if available:
                status = "✅ Available"
                if premium:
                    status += " (Premium)"
            elif error_code:
                status = f"⚠️ Error: {error_code}"
            
            results[domain] = {
                'available': available,
                'premium': premium,
                'status': status,
                'error_code': error_code
            }
            
            print(f"{status}: {domain}")
        
        return results
    
    def get_domain_list(self):
        """Get list of domains owned by the user"""
        print(f"\n📋 Your NameCheap Domains...")
        print("=" * 50)
        
        params = {
            'PageSize': '100',
            'Page': '1'
        }
        
        response = self.make_api_request('namecheap.domains.getList', params)
        if not response:
            return []
        
        domains = []
        domain_elements = response.findall('.//Domain')
        
        if not domain_elements:
            print("ℹ️ No domains found in your account")
            return domains
        
        for domain_elem in domain_elements:
            domain_info = {
                'name': domain_elem.get('Name'),
                'user': domain_elem.get('User'),
                'created': domain_elem.get('Created'),
                'expires': domain_elem.get('Expires'),
                'auto_renew': domain_elem.get('AutoRenew', 'false').lower() == 'true',
                'whois_guard': domain_elem.get('WhoisGuard') == 'ENABLED',
                'is_premium': domain_elem.get('IsPremium', 'false').lower() == 'true'
            }
            domains.append(domain_info)
            
            print(f"🌐 {domain_info['name']}")
            print(f"   Created: {domain_info['created']}")
            print(f"   Expires: {domain_info['expires']}")
            print(f"   Auto-renew: {'✅' if domain_info['auto_renew'] else '❌'}")
            print(f"   WhoisGuard: {'🛡️' if domain_info['whois_guard'] else '🔓'}")
            if domain_info['is_premium']:
                print(f"   💎 Premium Domain")
            print()
        
        return domains
    
    def suggest_domains(self, keyword, tlds=None):
        """Suggest available domains based on keyword"""
        if not tlds:
            tlds = ['.com', '.net', '.org', '.io', '.co', '.ai', '.tech', '.trading', '.fx']
        
        suggestions = []
        base_names = [
            keyword,
            f"{keyword}fx",
            f"{keyword}trade",
            f"{keyword}trading",
            f"genx{keyword}",
            f"{keyword}signals",
            f"{keyword}pro",
            f"my{keyword}",
            f"{keyword}platform"
        ]
        
        for base in base_names:
            for tld in tlds:
                suggestions.append(f"{base.lower()}{tld}")
        
        return suggestions
    
    def generate_trading_domains(self):
        """Generate domain suggestions for trading platform"""
        print(f"\n💡 Domain Suggestions for GenX Trading Platform...")
        print("=" * 50)
        
        trading_keywords = [
            "genxfx", "genxtrading", "genxtrade", "genxsignals",
            "magicfx", "magictrading", "autofx", "smartfx",
            "fxgenx", "tradinggenx", "genxpro", "genxai"
        ]
        
        suggestions = []
        for keyword in trading_keywords:
            suggestions.extend(self.suggest_domains(keyword, ['.com', '.io', '.co', '.ai', '.trading']))
        
        # Remove duplicates and limit to reasonable number
        suggestions = list(dict.fromkeys(suggestions))[:30]
        
        return self.check_domain_availability(suggestions)

def main():
    """Main function"""
    print("🌐 NameCheap Domain Name Checker")
    print("=" * 50)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    checker = NameCheapDomainChecker()
    
    # Check credentials first
    if not checker.check_credentials():
        print("\n❌ Cannot proceed without API credentials")
        print("\n📋 Get your credentials at:")
        print("https://ap.www.namecheap.com/settings/tools/apiaccess/")
        return
    
    print("\n🎯 Choose an option:")
    print("1. Check specific domain")
    print("2. List your domains")
    print("3. Generate trading domain suggestions")
    print("4. All of the above")
    
    try:
        choice = input("\nEnter choice (1-4): ").strip()
        
        if choice == "1" or choice == "4":
            domain = input("Enter domain to check (e.g., genxfx.com): ").strip()
            if domain:
                checker.check_domain_availability([domain])
        
        if choice == "2" or choice == "4":
            checker.get_domain_list()
        
        if choice == "3" or choice == "4":
            results = checker.generate_trading_domains()
            available_domains = [domain for domain, info in results.items() if info['available']]
            
            if available_domains:
                print(f"\n🎉 Found {len(available_domains)} available domains!")
                print("\n🌟 Top recommendations:")
                for domain in available_domains[:10]:
                    print(f"✅ {domain}")
                
                if len(available_domains) > 10:
                    print(f"\n... and {len(available_domains) - 10} more available")
            else:
                print("\n😔 No available domains found in suggestions")
        
        print(f"\n✅ Domain check completed!")
        
    except KeyboardInterrupt:
        print("\n\n👋 Domain check cancelled")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()