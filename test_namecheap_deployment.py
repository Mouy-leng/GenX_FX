#!/usr/bin/env python3
"""
NameCheap VPS Deployment Test Script
Tests API connectivity and validates deployment prerequisites
"""

import os
import sys
import requests
import json
from pathlib import Path

def test_namecheap_api():
    """Test NameCheap API connectivity"""
    print("🧪 Testing NameCheap API Connectivity...")
    
    # Check environment variables
    required_vars = [
        'NAMECHEAP_API_USER',
        'NAMECHEAP_API_KEY', 
        'NAMECHEAP_USERNAME',
        'NAMECHEAP_CLIENT_IP'
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
        print("\nSet them using:")
        for var in missing_vars:
            print(f"$env:{var} = 'your_value'")
        return False
    
    # Test API connection
    api_user = os.getenv('NAMECHEAP_API_USER')
    api_key = os.getenv('NAMECHEAP_API_KEY')
    username = os.getenv('NAMECHEAP_USERNAME')
    client_ip = os.getenv('NAMECHEAP_CLIENT_IP')
    
    # NameCheap API test call
    url = "https://api.namecheap.com/xml.response"
    params = {
        'ApiUser': api_user,
        'ApiKey': api_key,
        'UserName': username,
        'Command': 'namecheap.domains.getList',
        'ClientIp': client_ip
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        print(f"✅ API Response Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ NameCheap API connection successful!")
            return True
        else:
            print(f"❌ API Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

def validate_deployment_files():
    """Validate deployment files exist"""
    print("\n🔍 Validating Deployment Files...")
    
    required_files = [
        'deploy_namecheap_vps.sh',
        'api/fastapi_server.py',
        'core/magic_key_config.py'
    ]
    
    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
        else:
            print(f"✅ Found: {file}")
    
    if missing_files:
        print(f"❌ Missing files: {', '.join(missing_files)}")
        return False
    
    return True

def test_magic_keys():
    """Test magic key system"""
    print("\n🔑 Testing Magic Key System...")
    
    try:
        sys.path.append(str(Path.cwd()))
        from core.magic_key_config import validate_trading_permission, get_trading_config
        
        # Test magic key validation
        test_key = "test_key_123"
        result = validate_trading_permission(test_key)
        print(f"✅ Magic key system operational")
        return True
        
    except Exception as e:
        print(f"❌ Magic key system error: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 GenX Trading Platform - NameCheap VPS Deployment Test")
    print("=" * 60)
    
    # Run all tests
    tests = [
        ("API Connectivity", test_namecheap_api),
        ("Deployment Files", validate_deployment_files),
        ("Magic Key System", test_magic_keys)
    ]
    
    results = {}
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ {test_name} failed: {e}")
            results[test_name] = False
        print()
    
    # Summary
    print("📊 Test Results Summary:")
    print("-" * 30)
    passed = 0
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nTests Passed: {passed}/{len(tests)}")
    
    if passed == len(tests):
        print("\n🎉 All tests passed! Ready for deployment!")
        print("Run: ./deploy_namecheap_vps.sh to start deployment")
        return True
    else:
        print("\n⚠️ Some tests failed. Fix issues before deployment.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)