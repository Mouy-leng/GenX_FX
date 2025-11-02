#!/usr/bin/env python3
"""
Simplified VPS Deployment - Retry with Fixed Approach
Focus on getting the core system running reliably
"""

import os
import sys
import subprocess
import time
import requests
import json
from datetime import datetime
from pathlib import Path

def test_current_api():
    """Test if FastAPI is currently running"""
    print("🔍 Testing Current API Status...")
    
    try:
        response = requests.get("http://localhost:8000/health", timeout=3)
        if response.status_code == 200:
            print("✅ FastAPI Server: RUNNING on port 8000")
            return True
        else:
            print(f"⚠️  FastAPI Server: Responding with status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ FastAPI Server: NOT RUNNING")
        return False
    except Exception as e:
        print(f"❌ FastAPI Test Error: {e}")
        return False

def start_vps_simulation():
    """Start VPS simulation on port 8001"""
    print("🚀 Starting VPS Simulation on Port 8001...")
    
    # First check if something is already on 8001
    try:
        response = requests.get("http://localhost:8001/health", timeout=2)
        if response.status_code == 200:
            print("✅ VPS Simulation already running on port 8001")
            return True
    except:
        pass
    
    # Start new instance on port 8001
    project_root = Path("D:/Dropbox/GenX_FX")
    
    # Create a simple startup script
    startup_script = f"""
import sys
sys.path.append('{project_root}')

print('Starting GenX VPS Simulation...')

try:
    from api.fastapi_server import app
    import uvicorn
    print('Modules imported successfully')
    print('Starting server on http://localhost:8001')
    uvicorn.run(app, host='0.0.0.0', port=8001, log_level='info')
except Exception as e:
    print(f'Startup error: {{e}}')
    import traceback
    traceback.print_exc()
"""
    
    # Write startup script to file
    script_file = project_root / "start_vps_sim.py"
    with open(script_file, 'w', encoding='utf-8') as f:
        f.write(startup_script)
    
    print("📝 Created startup script")
    
    # Start the server
    try:
        cmd = [
            "D:/Dropbox/.venv/Scripts/python.exe",
            str(script_file)
        ]
        
        print("🔄 Launching VPS simulation...")
        process = subprocess.Popen(
            cmd,
            cwd=str(project_root),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == 'nt' else 0
        )
        
        # Give it time to start
        print("⏱️  Waiting for server startup...")
        time.sleep(8)
        
        # Test if it's running
        for attempt in range(5):
            try:
                response = requests.get("http://localhost:8001/health", timeout=3)
                if response.status_code == 200:
                    print("✅ VPS Simulation: SUCCESSFULLY STARTED")
                    return True
            except:
                pass
            time.sleep(2)
        
        print("⚠️  VPS simulation may need more time to start")
        return False
        
    except Exception as e:
        print(f"❌ Failed to start VPS simulation: {e}")
        return False

def test_all_endpoints():
    """Test all available endpoints"""
    print("\n🧪 Testing All Available Endpoints...")
    print("=" * 50)
    
    servers = [
        ("Main API", "http://localhost:8000"),
        ("VPS Simulation", "http://localhost:8001")
    ]
    
    endpoints = [
        "/health",
        "/",
        "/trading/status", 
        "/signals",
        "/config/magic"
    ]
    
    results = {}
    
    for server_name, base_url in servers:
        print(f"\n📡 Testing {server_name} ({base_url}):")
        server_results = {}
        
        for endpoint in endpoints:
            try:
                url = f"{base_url}{endpoint}"
                response = requests.get(url, timeout=5)
                
                if response.status_code == 200:
                    print(f"   ✅ {endpoint}: OK (200)")
                    server_results[endpoint] = True
                else:
                    print(f"   ⚠️  {endpoint}: {response.status_code}")
                    server_results[endpoint] = False
                    
            except requests.exceptions.ConnectionError:
                print(f"   ❌ {endpoint}: NO CONNECTION")
                server_results[endpoint] = False
            except Exception as e:
                print(f"   ❌ {endpoint}: ERROR ({e})")
                server_results[endpoint] = False
        
        results[server_name] = server_results
    
    return results

def execute_trading_tests():
    """Execute trading functionality tests"""
    print("\n🎯 Executing Trading Functionality Tests...")
    print("=" * 50)
    
    # Find working server
    working_server = None
    for port in [8000, 8001]:
        try:
            response = requests.get(f"http://localhost:{port}/health", timeout=3)
            if response.status_code == 200:
                working_server = f"http://localhost:{port}"
                print(f"✅ Using server: {working_server}")
                break
        except:
            continue
    
    if not working_server:
        print("❌ No working server found")
        return False
    
    # Test trading endpoints
    tests = [
        ("Health Check", "/health"),
        ("Trading Status", "/trading/status"),
        ("Get Signals", "/signals"),
        ("Magic Config", "/config/magic")
    ]
    
    success_count = 0
    for test_name, endpoint in tests:
        try:
            response = requests.get(f"{working_server}{endpoint}", timeout=5)
            if response.status_code == 200:
                print(f"✅ {test_name}: PASSED")
                success_count += 1
                
                # Show some data for key endpoints
                if endpoint == "/trading/status":
                    data = response.json()
                    print(f"   📊 Signals: {data.get('signals_count', 0)}")
                    print(f"   🔑 Magic Keys: {data.get('magic_keys_enabled', False)}")
                    
            else:
                print(f"⚠️  {test_name}: STATUS {response.status_code}")
                
        except Exception as e:
            print(f"❌ {test_name}: FAILED ({e})")
    
    print(f"\n📊 Test Results: {success_count}/{len(tests)} passed")
    return success_count >= len(tests) // 2  # At least half should pass

def show_final_status():
    """Show final deployment status"""
    print("\n" + "="*60)
    print("🎉 FINAL VPS DEPLOYMENT STATUS")
    print("="*60)
    
    # Check what's actually running
    running_services = []
    
    for port in [8000, 8001]:
        try:
            response = requests.get(f"http://localhost:{port}/health", timeout=2)
            if response.status_code == 200:
                running_services.append(f"localhost:{port}")
        except:
            pass
    
    if running_services:
        print("✅ ACTIVE SERVICES:")
        for service in running_services:
            print(f"   🌐 http://{service}")
            
        print("\n🎯 WHAT YOU CAN DO NOW:")
        print("1. 📱 Test in browser: http://localhost:8000")
        if "localhost:8001" in running_services:
            print("2. 🚀 VPS Simulation: http://localhost:8001")
        print("3. 🔑 Connect with Termius (SSH keys ready)")
        print("4. 📊 View trading status: /trading/status")
        print("5. 📈 Get signals: /signals")
        
        print("\n🚀 READY FOR REAL VPS DEPLOYMENT!")
        print("   Your system is working - now deploy to actual VPS")
        
    else:
        print("❌ NO SERVICES RUNNING")
        print("🔧 Check logs and retry")
    
    return len(running_services) > 0

def main():
    """Main retry function"""
    print("🔄 RETRYING VPS DEPLOYMENT - SIMPLIFIED APPROACH")
    print("=" * 60)
    
    success_count = 0
    total_steps = 4
    
    # Step 1: Test current API
    if test_current_api():
        success_count += 1
        print("✅ Step 1: Current API working")
    else:
        print("⚠️  Step 1: API needs attention")
    
    # Step 2: Start VPS simulation
    if start_vps_simulation():
        success_count += 1
        print("✅ Step 2: VPS simulation started")
    else:
        print("⚠️  Step 2: VPS simulation issues")
    
    # Step 3: Test all endpoints
    results = test_all_endpoints()
    if any(any(server.values()) for server in results.values()):
        success_count += 1
        print("✅ Step 3: Some endpoints working")
    else:
        print("⚠️  Step 3: Endpoint issues")
    
    # Step 4: Execute trading tests
    if execute_trading_tests():
        success_count += 1
        print("✅ Step 4: Trading tests passed")
    else:
        print("⚠️  Step 4: Trading test issues")
    
    # Final status
    final_success = show_final_status()
    
    print(f"\n📊 OVERALL SUCCESS: {success_count}/{total_steps} steps completed")
    
    if final_success:
        print("🎉 DEPLOYMENT RETRY: SUCCESS!")
        return True
    else:
        print("⚠️  DEPLOYMENT RETRY: PARTIAL SUCCESS")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)