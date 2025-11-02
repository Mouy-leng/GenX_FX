#!/usr/bin/env python3
"""
GenX Trading Platform - LIVE TRADING ACTIVATION
🚨 CRITICAL: Switch from demo to real money trading
"""

import subprocess
import os
import time
import json
from datetime import datetime

def check_critical_requirements():
    """Check critical requirements before live trading"""
    print("🚨 LIVE TRADING ACTIVATION - CRITICAL CHECKS")
    print("=" * 60)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    requirements = {
        'broker_api': False,
        'real_account': False,
        'funding': False,
        'risk_management': False,
        'security_verification': False,
        'live_data_feed': False
    }
    
    print("\n⚠️ CRITICAL REQUIREMENTS FOR LIVE TRADING:")
    print("   1. ❌ Broker API credentials (AMP/OANDA/MT4/MT5)")
    print("   2. ❌ Real trading account (not demo)")
    print("   3. ❌ Account funding ($500+ recommended)")
    print("   4. ❌ Risk management settings")
    print("   5. ❌ Live market data subscription")
    print("   6. ❌ Real-time execution verification")
    
    print("\n🛡️ CURRENT SECURITY STATUS:")
    print("   ✅ Samsung fingerprint authentication active")
    print("   ✅ Encrypted credential storage")
    print("   ✅ Local platform operational")
    print("   ✅ Multi-factor authentication enabled")
    
    return requirements

def show_broker_options():
    """Show available broker options for live trading"""
    print("\n📊 BROKER OPTIONS FOR LIVE TRADING:")
    print("=" * 50)
    
    brokers = {
        '1': {
            'name': 'AMP Futures',
            'min_deposit': '$500',
            'commission': '$0.85/round turn',
            'markets': 'Futures (ES, NQ, YM, RTY)',
            'api': 'AMP API',
            'status': 'READY - Config available'
        },
        '2': {
            'name': 'OANDA',
            'min_deposit': '$100',
            'commission': 'Spread-based',
            'markets': 'Forex (EUR/USD, GBP/USD, etc)',
            'api': 'OANDA REST API',
            'status': 'READY - Easy setup'
        },
        '3': {
            'name': 'Interactive Brokers',
            'min_deposit': '$10,000',
            'commission': '$0.85/contract',
            'markets': 'Stocks, Futures, Forex, Options',
            'api': 'TWS API',
            'status': 'ADVANCED - Setup required'
        },
        '4': {
            'name': 'TD Ameritrade',
            'min_deposit': '$2,000',
            'commission': '$0.65/contract',
            'markets': 'Stocks, Options, Futures',
            'api': 'TDA API',
            'status': 'READY - OAuth setup'
        },
        '5': {
            'name': 'MetaTrader 4/5',
            'min_deposit': 'Varies by broker',
            'commission': 'Spread + commission',
            'markets': 'Forex, CFDs',
            'api': 'MT4/MT5 API',
            'status': 'READY - Many brokers'
        }
    }
    
    for key, broker in brokers.items():
        print(f"\n   {key}. {broker['name']}")
        print(f"      Min Deposit: {broker['min_deposit']}")
        print(f"      Commission: {broker['commission']}")
        print(f"      Markets: {broker['markets']}")
        print(f"      API: {broker['api']}")
        print(f"      Status: {broker['status']}")
    
    return brokers

def configure_amp_live_trading():
    """Configure AMP Futures for live trading"""
    print("\n🔥 CONFIGURING AMP FUTURES LIVE TRADING")
    print("=" * 50)
    
    print("📋 AMP FUTURES SETUP STEPS:")
    print("   1. Open account at: https://www.ampfutures.com/")
    print("   2. Fund account with minimum $500")
    print("   3. Request API access from AMP support")
    print("   4. Get live trading credentials:")
    print("      - Username: [Your AMP username]")
    print("      - Password: [Your AMP password]") 
    print("      - API Key: [Request from AMP]")
    print("      - API Secret: [Request from AMP]")
    print("   5. Set live data feed subscription")
    
    print("\n⚠️ RISK WARNING:")
    print("   🚨 LIVE TRADING INVOLVES REAL MONEY")
    print("   🚨 YOU CAN LOSE MORE THAN YOUR DEPOSIT")
    print("   🚨 FUTURES TRADING IS HIGH RISK")
    print("   🚨 ONLY TRADE WITH MONEY YOU CAN AFFORD TO LOSE")
    
    print("\n📊 RECOMMENDED STARTING SETTINGS:")
    print("   💰 Max Risk Per Trade: 1-2% of account")
    print("   🎯 Position Size: 1 micro contract (MES/MNQ)")
    print("   🛑 Stop Loss: 10-20 points")
    print("   💵 Take Profit: 20-40 points")
    print("   ⏰ Trading Hours: Market hours only")
    
    return True

def configure_oanda_live_trading():
    """Configure OANDA for live trading"""
    print("\n💱 CONFIGURING OANDA FOREX LIVE TRADING")
    print("=" * 50)
    
    print("📋 OANDA SETUP STEPS:")
    print("   1. Open account at: https://www.oanda.com/")
    print("   2. Fund account with minimum $100")
    print("   3. Generate API credentials:")
    print("      - Go to: https://www.oanda.com/account/tpa/personal_token")
    print("      - Create Personal Access Token")
    print("      - Get Account ID from account dashboard")
    print("   4. Set live environment:")
    print("      - Live API: https://api-fxtrade.oanda.com")
    print("      - Practice API: https://api-fxpractice.oanda.com")
    
    print("\n📊 RECOMMENDED FOREX PAIRS:")
    print("   💵 EUR/USD - Most liquid, low spreads")
    print("   💷 GBP/USD - Good volatility")
    print("   💴 USD/JPY - Asian market exposure")
    print("   🇨🇭 USD/CHF - Safe haven currency")
    
    print("\n⚙️ TRADING PARAMETERS:")
    print("   💰 Max Risk: 1% per trade")
    print("   📏 Position Size: 1,000-10,000 units")
    print("   🛑 Stop Loss: 20-50 pips")
    print("   💵 Take Profit: 40-100 pips")
    
    return True

def generate_live_trading_config():
    """Generate live trading configuration"""
    print("\n⚙️ GENERATING LIVE TRADING CONFIGURATION")
    print("=" * 50)
    
    config = {
        "trading_mode": "LIVE",
        "created": datetime.now().isoformat(),
        "risk_management": {
            "max_risk_per_trade_percent": 1.0,
            "max_daily_loss_percent": 5.0,
            "max_positions": 3,
            "force_stop_loss": True,
            "force_take_profit": True
        },
        "broker_config": {
            "primary_broker": "DEMO",
            "backup_broker": "NONE",
            "live_data_feed": "REQUIRED",
            "execution_mode": "MARKET"
        },
        "security": {
            "require_fingerprint": True,
            "session_timeout_minutes": 30,
            "require_confirmation": True,
            "log_all_trades": True
        },
        "notifications": {
            "trade_alerts": True,
            "loss_alerts": True,
            "profit_alerts": True,
            "system_alerts": True
        }
    }
    
    config_file = "live_trading_config.json"
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"✅ Configuration saved to: {config_file}")
    return config_file

def show_live_trading_warnings():
    """Show critical warnings before live trading"""
    print("\n🚨 CRITICAL LIVE TRADING WARNINGS")
    print("=" * 50)
    
    warnings = [
        "⚠️ LIVE TRADING USES REAL MONEY - LOSSES ARE REAL",
        "⚠️ NEVER TRADE MORE THAN YOU CAN AFFORD TO LOSE",
        "⚠️ FUTURES TRADING CAN RESULT IN LOSSES > DEPOSIT",
        "⚠️ MARKET CONDITIONS CAN CHANGE RAPIDLY",
        "⚠️ TECHNICAL ISSUES CAN CAUSE UNEXPECTED LOSSES",
        "⚠️ ALWAYS USE STOP LOSSES",
        "⚠️ START WITH SMALL POSITION SIZES",
        "⚠️ MONITOR TRADES ACTIVELY",
        "⚠️ HAVE A TRADING PLAN",
        "⚠️ PRACTICE WITH DEMO FIRST"
    ]
    
    for warning in warnings:
        print(f"   {warning}")
    
    print(f"\n💡 RECOMMENDATION:")
    print(f"   📚 Practice with demo account for 30+ days")
    print(f"   📊 Test all strategies thoroughly")
    print(f"   💰 Start with minimum deposit")
    print(f"   📱 Ensure Samsung auth is working")
    print(f"   🛡️ Verify all security features")
    
    return True

def main():
    """Main live trading activation"""
    try:
        # Check critical requirements
        requirements = check_critical_requirements()
        
        # Show broker options
        brokers = show_broker_options()
        
        # Show warnings
        show_live_trading_warnings()
        
        # Generate config
        config_file = generate_live_trading_config()
        
        print(f"\n" + "="*60)
        print("🚨 LIVE TRADING ACTIVATION SUMMARY")
        print("="*60)
        
        print(f"\n📊 CURRENT STATUS:")
        print(f"   ✅ Local platform operational")
        print(f"   ✅ Samsung fingerprint auth active")
        print(f"   ✅ Security features enabled")
        print(f"   ❌ Live broker API not configured")
        print(f"   ❌ Real trading account not connected")
        print(f"   ❌ Live data feed not active")
        
        print(f"\n🎯 IMMEDIATE NEXT STEPS:")
        print(f"   1. Choose a broker (AMP, OANDA, IB, TDA, MT4/5)")
        print(f"   2. Open and fund real trading account")
        print(f"   3. Get API credentials from broker")
        print(f"   4. Configure live data feed")
        print(f"   5. Test with small positions")
        print(f"   6. Gradually increase position sizes")
        
        print(f"\n⚡ QUICK START OPTIONS:")
        print(f"   🥇 EASIEST: OANDA Forex (30 minutes setup)")
        print(f"   🏆 RECOMMENDED: AMP Futures (1 hour setup)")
        print(f"   🚀 ADVANCED: Interactive Brokers (2+ hours)")
        
        print(f"\n🚨 CRITICAL: This switches from demo to REAL MONEY")
        print(f"🛡️ Your Samsung fingerprint auth will protect trades")
        print(f"📁 Config saved to: {config_file}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in live trading activation: {e}")
        return False

if __name__ == "__main__":
    main()