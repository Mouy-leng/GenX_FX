#!/usr/bin/env python3
"""
NameCheap VPS Quick Deploy Script
Run this after setting your NameCheap API credentials
"""

import os
import subprocess
import sys

def quick_deploy_namecheap():
    print("🚀 NameCheap VPS Quick Deploy")
    print("=" * 30)
    
    # Check credentials
    required_vars = [
        "NAMECHEAP_API_USER",
        "NAMECHEAP_API_KEY", 
        "NAMECHEAP_USERNAME",
        "NAMECHEAP_CLIENT_IP"
    ]
    
    missing = []
    for var in required_vars:
        if not os.getenv(var):
            missing.append(var)
        else:
            print(f"✅ {var}: Set")
    
    if missing:
        print(f"\n❌ Missing credentials: {', '.join(missing)}")
        print("\nSet them first:")
        for var in missing:
            print(f'$env:{var} = "your_value"')
        return False
    
    print("\n✅ All credentials set!")
    
    # Run the setup
    print("🔄 Running NameCheap deployment setup...")
    try:
        result = subprocess.run([
            "D:/Dropbox/.venv/Scripts/python.exe",
            "setup_namecheap_deployment.py"
        ], check=True, capture_output=True, text=True)
        
        print("✅ Deployment setup completed!")
        print(result.stdout)
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Deployment failed: {e}")
        print(e.stdout)
        print(e.stderr)
        return False

if __name__ == "__main__":
    success = quick_deploy_namecheap()
    sys.exit(0 if success else 1)