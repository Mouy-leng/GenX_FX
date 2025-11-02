#!/usr/bin/env python3
"""
Domain Name Suggestions for GenX Trading Platform
Generate domain ideas without requiring API credentials
"""

import requests
import json
from datetime import datetime
import time

class DomainSuggester:
    def __init__(self):
        self.trading_keywords = [
            "genxfx", "genxtrading", "genxtrade", "genxsignals",
            "magicfx", "magictrading", "autofx", "smartfx",
            "fxgenx", "tradinggenx", "genxpro", "genxai",
            "genxbot", "fxmagic", "tradingbot", "fxsignals"
        ]
        
        self.tlds = [
            '.com', '.net', '.org', '.io', '.co', '.ai', 
            '.tech', '.trading', '.fx', '.pro', '.biz',
            '.app', '.dev', '.online', '.site', '.live'
        ]
    
    def generate_domain_suggestions(self):
        """Generate domain suggestions for trading platform"""
        print("💡 Domain Name Suggestions for GenX Trading Platform")
        print("=" * 60)
        
        suggestions = []
        
        # Base combinations
        for keyword in self.trading_keywords:
            for tld in self.tlds:
                suggestions.append(f"{keyword}{tld}")
        
        # Additional creative combinations
        creative_combinations = [
            "genx-fx.com", "genx-trading.com", "genx-signals.com",
            "my-genx.com", "genx-platform.io", "genx-bot.ai",
            "trade-genx.co", "genx-magic.com", "genx-auto.com",
            "genx-pro.trading", "genx-fx.live", "genx-signals.app"
        ]
        
        suggestions.extend(creative_combinations)
        
        return suggestions
    
    def categorize_suggestions(self, suggestions):
        """Categorize domain suggestions by type"""
        categories = {
            'Premium (.com)': [],
            'Tech (.io, .ai, .tech)': [],
            'Trading Specific (.trading, .fx, .pro)': [],
            'Alternative (.co, .net, .org)': [],
            'Modern (.app, .dev, .live)': []
        }
        
        for domain in suggestions:
            if domain.endswith('.com'):
                categories['Premium (.com)'].append(domain)
            elif any(domain.endswith(ext) for ext in ['.io', '.ai', '.tech']):
                categories['Tech (.io, .ai, .tech)'].append(domain)
            elif any(domain.endswith(ext) for ext in ['.trading', '.fx', '.pro']):
                categories['Trading Specific (.trading, .fx, .pro)'].append(domain)
            elif any(domain.endswith(ext) for ext in ['.co', '.net', '.org']):
                categories['Alternative (.co, .net, .org)'].append(domain)
            elif any(domain.endswith(ext) for ext in ['.app', '.dev', '.live']):
                categories['Modern (.app, .dev, .live)'].append(domain)
        
        return categories
    
    def check_basic_availability(self, domain):
        """Basic domain availability check using DNS lookup"""
        import socket
        try:
            socket.gethostbyname(domain)
            return False  # Domain exists (has DNS record)
        except socket.gaierror:
            return True   # Domain might be available (no DNS record)
        except Exception:
            return None   # Cannot determine
    
    def display_suggestions(self):
        """Display categorized domain suggestions"""
        suggestions = self.generate_domain_suggestions()
        categories = self.categorize_suggestions(suggestions)
        
        print(f"\n🎯 Generated {len(suggestions)} domain suggestions")
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        for category, domains in categories.items():
            if domains:
                print(f"\n📂 {category}")
                print("-" * 40)
                
                # Show top 8 from each category
                for domain in domains[:8]:
                    print(f"   🌐 {domain}")
                
                if len(domains) > 8:
                    print(f"   ... and {len(domains) - 8} more in this category")
        
        print(f"\n💰 Domain Pricing Guide:")
        print("   .com domains: $8.88 - $12.98/year")
        print("   .io domains: $32.88 - $39.98/year") 
        print("   .ai domains: $49.98 - $89.98/year")
        print("   .trading domains: $19.98 - $29.98/year")
        print("   .co domains: $28.88 - $32.88/year")
        
        print(f"\n🎯 Top Recommendations:")
        top_picks = [
            "genxfx.com", "genxtrading.com", "genx-fx.io",
            "genxsignals.com", "magicfx.com", "genxpro.trading",
            "genx-platform.io", "tradinggenx.co"
        ]
        
        for pick in top_picks:
            print(f"   ⭐ {pick}")
        
        return suggestions

def check_whois_basic(domain):
    """Basic WHOIS check to see if domain might be available"""
    try:
        import subprocess
        result = subprocess.run(['nslookup', domain], 
                              capture_output=True, text=True, timeout=5)
        if "can't find" in result.stderr.lower() or "nxdomain" in result.stderr.lower():
            return "Possibly Available ✅"
        else:
            return "Likely Taken ❌"
    except:
        return "Unknown ❓"

def main():
    """Main function"""
    print("🌐 GenX Trading Platform - Domain Name Generator")
    print("=" * 60)
    
    suggester = DomainSuggester()
    
    print("🎯 Generating domain suggestions...")
    suggestions = suggester.display_suggestions()
    
    print("\n" + "=" * 60)
    print("📋 NEXT STEPS:")
    print("1. Choose 3-5 favorite domains from the suggestions")
    print("2. Get NameCheap API credentials:")
    print("   https://ap.www.namecheap.com/settings/tools/apiaccess/")
    print("3. Run check_namecheap_domains.py to verify availability")
    print("4. Register your chosen domain")
    print("5. Point domain to your VPS after deployment")
    
    print(f"\n🔧 For VPS deployment with custom domain:")
    print("   • Domain will point to your VPS IP")
    print("   • SSL certificate will be auto-generated")
    print("   • Access your platform at https://yourdomain.com")
    
    print(f"\n💡 Pro Tips:")
    print("   • .com domains are most trusted")
    print("   • .io domains are popular for tech platforms")
    print("   • Keep it short and memorable")
    print("   • Avoid hyphens if possible")
    print("   • Consider brandability over keywords")

if __name__ == "__main__":
    main()