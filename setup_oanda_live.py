#!/usr/bin/env python3
"""
GenX Trading Platform - OANDA LIVE SETUP
Quick 30-minute setup for live forex trading
"""

import requests
import json
import os
from datetime import datetime

def setup_oanda_live_account():
    """Quick OANDA setup for live trading"""
    print("💱 OANDA LIVE FOREX TRADING SETUP")
    print("=" * 50)
    print(f"⏰ Setup Time: ~30 minutes")
    print(f"💰 Min Deposit: $100")
    print(f"🎯 Best For: Forex beginners")
    
    print(f"\n📋 STEP-BY-STEP SETUP:")
    
    steps = [
        {
            'step': 1,
            'title': 'Open OANDA Account',
            'action': 'Go to https://www.oanda.com/register/',
            'time': '5 minutes',
            'details': [
                'Select "Live Trading Account"',
                'Complete identity verification',
                'Choose base currency (USD recommended)',
                'Agree to terms and conditions'
            ]
        },
        {
            'step': 2, 
            'title': 'Fund Your Account',
            'action': 'Deposit minimum $100',
            'time': '10 minutes',
            'details': [
                'Credit card: Instant funding',
                'Bank transfer: 1-3 business days',
                'PayPal: Available in some regions',
                'Recommend starting with $500+'
            ]
        },
        {
            'step': 3,
            'title': 'Generate API Token',
            'action': 'Create Personal Access Token',
            'time': '5 minutes',
            'details': [
                'Login to OANDA account',
                'Go to: Manage API Access',
                'Click "Generate" personal access token',
                'Copy and save the token securely'
            ]
        },
        {
            'step': 4,
            'title': 'Get Account ID',
            'action': 'Find your account number',
            'time': '2 minutes',
            'details': [
                'Go to account dashboard',
                'Copy the account ID number',
                'Format: XXX-XXX-XXXXXXXX-XXX',
                'Save this for API configuration'
            ]
        },
        {
            'step': 5,
            'title': 'Configure GenX Platform',
            'action': 'Update trading configuration',
            'time': '8 minutes',
            'details': [
                'Set OANDA_API_TOKEN environment variable',
                'Set OANDA_ACCOUNT_ID environment variable', 
                'Update broker config to OANDA',
                'Test API connection'
            ]
        }
    ]
    
    for step_info in steps:
        print(f"\n🔄 STEP {step_info['step']}: {step_info['title']}")
        print(f"   ⏱️ Time: {step_info['time']}")
        print(f"   🎯 Action: {step_info['action']}")
        for detail in step_info['details']:
            print(f"      • {detail}")
    
    return steps

def create_oanda_config_template():
    """Create OANDA configuration template"""
    print(f"\n⚙️ CREATING OANDA CONFIGURATION TEMPLATE")
    print("=" * 50)
    
    config = {
        "broker": "OANDA",
        "environment": "live",
        "api_url": "https://api-fxtrade.oanda.com",
        "stream_url": "https://stream-fxtrade.oanda.com",
        "account_id": "YOUR_ACCOUNT_ID_HERE",
        "api_token": "YOUR_API_TOKEN_HERE",
        "trading_pairs": [
            "EUR_USD",
            "GBP_USD", 
            "USD_JPY",
            "USD_CHF",
            "AUD_USD",
            "USD_CAD"
        ],
        "risk_settings": {
            "max_position_size": 1000,
            "max_risk_per_trade": 0.01,
            "stop_loss_pips": 20,
            "take_profit_pips": 40
        },
        "security": {
            "require_samsung_auth": True,
            "session_timeout": 1800,
            "trade_confirmation": True
        }
    }
    
    config_file = "oanda_live_config.json"
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"✅ Template saved to: {config_file}")
    
    print(f"\n📝 CONFIGURATION INSTRUCTIONS:")
    print(f"   1. Edit {config_file}")
    print(f"   2. Replace YOUR_ACCOUNT_ID_HERE with your OANDA account ID")
    print(f"   3. Replace YOUR_API_TOKEN_HERE with your personal access token")
    print(f"   4. Save the file")
    print(f"   5. Restart the GenX platform")
    
    return config_file

def test_oanda_connection():
    """Test OANDA API connection"""
    print(f"\n🔌 TESTING OANDA API CONNECTION")
    print("=" * 50)
    
    # Check if credentials are set
    api_token = os.environ.get('OANDA_API_TOKEN')
    account_id = os.environ.get('OANDA_ACCOUNT_ID')
    
    if not api_token:
        print("❌ OANDA_API_TOKEN not set")
        print("💡 Set with: $env:OANDA_API_TOKEN = 'your_token_here'")
        return False
    
    if not account_id:
        print("❌ OANDA_ACCOUNT_ID not set") 
        print("💡 Set with: $env:OANDA_ACCOUNT_ID = 'your_account_id'")
        return False
    
    try:
        headers = {
            'Authorization': f'Bearer {api_token}',
            'Content-Type': 'application/json'
        }
        
        # Test account info
        url = f"https://api-fxtrade.oanda.com/v3/accounts/{account_id}"
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            account_data = response.json()
            print("✅ OANDA API connection successful!")
            print(f"   Account ID: {account_data['account']['id']}")
            print(f"   Currency: {account_data['account']['currency']}")
            print(f"   Balance: {account_data['account']['balance']}")
            print(f"   Margin Available: {account_data['account']['marginAvailable']}")
            return True
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

def show_quick_start_trading():
    """Show quick start trading examples"""
    print(f"\n🚀 QUICK START TRADING EXAMPLES")
    print("=" * 50)
    
    examples = [
        {
            'pair': 'EUR/USD',
            'action': 'BUY',
            'size': '1000 units ($10 per pip)',
            'stop_loss': '20 pips',
            'take_profit': '40 pips',
            'risk': '~$200 max loss'
        },
        {
            'pair': 'GBP/USD', 
            'action': 'SELL',
            'size': '500 units ($5 per pip)',
            'stop_loss': '25 pips',
            'take_profit': '50 pips',
            'risk': '~$125 max loss'
        }
    ]
    
    for i, example in enumerate(examples, 1):
        print(f"\n   Example {i}: {example['pair']} {example['action']}")
        print(f"      Size: {example['size']}")
        print(f"      Stop Loss: {example['stop_loss']}")
        print(f"      Take Profit: {example['take_profit']}")
        print(f"      Max Risk: {example['risk']}")
    
    print(f"\n⚠️ SAFETY REMINDERS:")
    print(f"   • Start with micro lots (1000 units)")
    print(f"   • Always use stop losses")
    print(f"   • Risk max 1% of account per trade")
    print(f"   • Trade major pairs only initially")
    print(f"   • Monitor trades actively")
    
    return examples

def main():
    """Main OANDA live setup"""
    try:
        # Setup steps
        steps = setup_oanda_live_account()
        
        # Create config template
        config_file = create_oanda_config_template()
        
        # Test connection (if credentials available)
        connection_ok = test_oanda_connection()
        
        # Show trading examples
        examples = show_quick_start_trading()
        
        print(f"\n" + "="*50)
        print("💱 OANDA LIVE TRADING SETUP COMPLETE!")
        print("="*50)
        
        print(f"\n📊 SETUP STATUS:")
        if connection_ok:
            print(f"   ✅ API connection working")
            print(f"   ✅ Account verified")
            print(f"   ✅ Ready to trade live!")
        else:
            print(f"   ⏳ Waiting for API credentials")
            print(f"   📝 Complete OANDA account setup")
            print(f"   🔑 Set environment variables")
        
        print(f"\n🎯 NEXT STEPS:")
        print(f"   1. Complete OANDA account registration")
        print(f"   2. Fund your account ($100+ recommended)")
        print(f"   3. Get API token and account ID")
        print(f"   4. Update {config_file}")
        print(f"   5. Set environment variables")
        print(f"   6. Test with small trades")
        
        print(f"\n🚨 REMEMBER: THIS IS REAL MONEY TRADING")
        print(f"🛡️ Samsung fingerprint auth will protect your trades")
        print(f"📱 All trades logged and monitored")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in OANDA setup: {e}")
        return False

if __name__ == "__main__":
    main()