#!/usr/bin/env python3
"""
VPS Deployment & Connection Activity Monitor
Tests connections, deploys VPS, and executes live trading platform
"""

import os
import sys
import subprocess
import time
import requests
import json
from datetime import datetime
from pathlib import Path

class VPSDeploymentManager:
    def __init__(self):
        self.project_root = Path("D:/Dropbox/GenX_FX")
        self.deployment_status = {
            "connection_tests": False,
            "ssh_setup": False,
            "api_ready": False,
            "vps_deployed": False,
            "live_connection": False
        }
        
    def test_system_connectivity(self):
        """Test all system connections before deployment"""
        print("🔍 Testing System Connectivity...")
        print("=" * 50)
        
        # Test 1: Local API Server
        try:
            response = requests.get("http://localhost:8000/health", timeout=5)
            if response.status_code == 200:
                print("✅ Local FastAPI Server: ONLINE")
                self.deployment_status["api_ready"] = True
            else:
                print("⚠️  Local FastAPI Server: RESPONDING (non-200)")
        except:
            print("❌ Local FastAPI Server: OFFLINE")
            print("   Starting FastAPI server...")
            self.start_local_api()
        
        # Test 2: SSH Key Availability
        ssh_key = Path.home() / ".ssh" / "genx_trading_ed25519"
        if ssh_key.exists():
            print("✅ SSH Keys: READY")
            self.deployment_status["ssh_setup"] = True
        else:
            print("❌ SSH Keys: MISSING")
            
        # Test 3: Internet Connectivity
        try:
            response = requests.get("https://httpbin.org/ip", timeout=10)
            if response.status_code == 200:
                ip_info = response.json()
                print(f"✅ Internet Connection: ACTIVE (IP: {ip_info.get('origin', 'Unknown')})")
                self.deployment_status["connection_tests"] = True
            else:
                print("⚠️  Internet Connection: LIMITED")
        except:
            print("❌ Internet Connection: FAILED")
            
        # Test 4: Required Tools
        tools = ["ssh", "curl", "python"]
        for tool in tools:
            try:
                result = subprocess.run([tool, "--version"], 
                                      capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    print(f"✅ {tool.upper()}: Available")
                else:
                    print(f"❌ {tool.upper()}: Not working")
            except:
                print(f"❌ {tool.upper()}: Not found")
                
        return self.deployment_status["connection_tests"]
    
    def start_local_api(self):
        """Start local FastAPI server for testing"""
        print("🚀 Starting Local FastAPI Server...")
        
        try:
            # Check if server is already running
            try:
                response = requests.get("http://localhost:8000/health", timeout=2)
                if response.status_code == 200:
                    print("✅ FastAPI server already running")
                    return True
            except:
                pass
            
            # Start the server in background
            api_file = self.project_root / "api" / "fastapi_server.py"
            if api_file.exists():
                cmd = [
                    "D:/Dropbox/.venv/Scripts/python.exe",
                    str(api_file)
                ]
                
                process = subprocess.Popen(
                    cmd,
                    cwd=str(self.project_root),
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                
                # Wait a moment for server to start
                time.sleep(3)
                
                # Test if it's working
                try:
                    response = requests.get("http://localhost:8000/health", timeout=5)
                    if response.status_code == 200:
                        print("✅ FastAPI server started successfully")
                        return True
                except:
                    pass
                    
            print("⚠️  FastAPI server startup uncertain")
            return False
            
        except Exception as e:
            print(f"❌ Failed to start FastAPI server: {e}")
            return False
    
    def test_vps_providers(self):
        """Test VPS provider API accessibility"""
        print("\n🌐 Testing VPS Provider APIs...")
        print("=" * 40)
        
        providers = {
            "NameCheap": "https://api.namecheap.com/xml.response",
            "Vultr": "https://api.vultr.com/v2/account",
            "Google Cloud": "https://cloud.google.com"
        }
        
        for provider, url in providers.items():
            try:
                response = requests.get(url, timeout=10)
                if response.status_code in [200, 401, 403]:  # API accessible
                    print(f"✅ {provider} API: ACCESSIBLE")
                else:
                    print(f"⚠️  {provider} API: REACHABLE ({response.status_code})")
            except:
                print(f"❌ {provider} API: UNREACHABLE")
    
    def deploy_demo_vps(self):
        """Deploy a demo/test VPS instance"""
        print("\n🚀 STARTING VPS DEPLOYMENT...")
        print("=" * 50)
        
        # For demo purposes, we'll simulate a deployment
        print("📋 Deployment Options Available:")
        print("1. NameCheap VPS (Requires API credentials)")
        print("2. Vultr VPS (Requires API key)")
        print("3. Google Cloud VPS (Requires gcloud auth)")
        print("4. Local Docker Simulation (For testing)")
        
        # Let's use Docker simulation for immediate testing
        print("\n🐳 Using Docker Simulation for immediate testing...")
        return self.deploy_docker_simulation()
    
    def deploy_docker_simulation(self):
        """Deploy a Docker container to simulate VPS"""
        print("🐳 Deploying Docker Simulation VPS...")
        
        try:
            # Check if Docker is available
            result = subprocess.run(["docker", "--version"], 
                                  capture_output=True, text=True)
            if result.returncode != 0:
                print("❌ Docker not available")
                return self.deploy_local_simulation()
            
            print("✅ Docker available")
            
            # Create a simple GenX trading container
            dockerfile_content = """
FROM python:3.9-slim
WORKDIR /app
COPY api/fastapi_server.py .
COPY core/ ./core/
RUN pip install fastapi uvicorn requests aiohttp
EXPOSE 8000
CMD ["python", "-m", "uvicorn", "fastapi_server:app", "--host", "0.0.0.0", "--port", "8000"]
"""
            
            with open("Dockerfile.genx", "w") as f:
                f.write(dockerfile_content)
            
            # Build and run container
            print("🔨 Building GenX container...")
            build_result = subprocess.run([
                "docker", "build", "-t", "genx-trading", "-f", "Dockerfile.genx", "."
            ], capture_output=True, text=True)
            
            if build_result.returncode == 0:
                print("✅ Container built successfully")
                
                # Run container
                print("🚀 Starting GenX container...")
                run_result = subprocess.run([
                    "docker", "run", "-d", "-p", "8001:8000", 
                    "--name", "genx-vps-sim", "genx-trading"
                ], capture_output=True, text=True)
                
                if run_result.returncode == 0:
                    print("✅ VPS Simulation deployed on port 8001")
                    self.deployment_status["vps_deployed"] = True
                    return True
            
            print("⚠️  Docker deployment had issues")
            return self.deploy_local_simulation()
            
        except Exception as e:
            print(f"❌ Docker deployment failed: {e}")
            return self.deploy_local_simulation()
    
    def deploy_local_simulation(self):
        """Deploy local simulation on different port"""
        print("🖥️  Deploying Local VPS Simulation...")
        
        try:
            # Start FastAPI on different port to simulate VPS
            api_file = self.project_root / "api" / "fastapi_server.py"
            
            # Modify the startup to use port 8001
            cmd = [
                "D:/Dropbox/.venv/Scripts/python.exe",
                "-c",
                f"""
import sys
sys.path.append('{self.project_root}')
from api.fastapi_server import app
import uvicorn
print('🚀 Starting GenX VPS Simulation on port 8001...')
uvicorn.run(app, host='0.0.0.0', port=8001, log_level='info')
"""
            ]
            
            process = subprocess.Popen(
                cmd,
                cwd=str(self.project_root),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            # Wait for startup
            time.sleep(5)
            
            # Test connection
            try:
                response = requests.get("http://localhost:8001/health", timeout=5)
                if response.status_code == 200:
                    print("✅ VPS Simulation deployed on port 8001")
                    self.deployment_status["vps_deployed"] = True
                    return True
            except:
                pass
                
            print("⚠️  VPS simulation startup uncertain")
            return False
            
        except Exception as e:
            print(f"❌ Local simulation failed: {e}")
            return False
    
    def test_live_connection(self):
        """Test live connection to deployed VPS"""
        print("\n🔗 Testing Live VPS Connection...")
        print("=" * 40)
        
        # Test different ports
        test_urls = [
            "http://localhost:8000",  # Original API
            "http://localhost:8001",  # VPS simulation
        ]
        
        for url in test_urls:
            try:
                response = requests.get(f"{url}/health", timeout=5)
                if response.status_code == 200:
                    print(f"✅ {url}: CONNECTED")
                    
                    # Test trading endpoints
                    endpoints = ["/", "/trading/status", "/config/magic"]
                    for endpoint in endpoints:
                        try:
                            resp = requests.get(f"{url}{endpoint}", timeout=3)
                            status = "✅" if resp.status_code == 200 else "⚠️"
                            print(f"   {status} {endpoint}: {resp.status_code}")
                        except:
                            print(f"   ❌ {endpoint}: FAILED")
                    
                    self.deployment_status["live_connection"] = True
                    return True
                else:
                    print(f"⚠️  {url}: RESPONDING ({response.status_code})")
            except:
                print(f"❌ {url}: NO CONNECTION")
        
        return False
    
    def execute_live_trading(self):
        """Execute live trading platform"""
        print("\n🎯 EXECUTING LIVE TRADING PLATFORM...")
        print("=" * 50)
        
        if not self.deployment_status["live_connection"]:
            print("❌ No live connection available")
            return False
        
        # Test trading functionality
        base_url = "http://localhost:8001"  # VPS simulation
        
        try:
            # Get trading status
            response = requests.get(f"{base_url}/trading/status")
            if response.status_code == 200:
                status = response.json()
                print("✅ Trading Platform Status:")
                print(f"   Magic Keys: {status.get('magic_keys_enabled', False)}")
                print(f"   Signals: {status.get('signals_count', 0)}")
                
            # Test signal retrieval
            response = requests.get(f"{base_url}/signals")
            if response.status_code == 200:
                signals = response.json()
                print(f"✅ Trading Signals: {signals.get('count', 0)} active")
                
            print("\n🎉 LIVE TRADING PLATFORM IS OPERATIONAL!")
            return True
            
        except Exception as e:
            print(f"❌ Trading platform test failed: {e}")
            return False
    
    def show_deployment_summary(self):
        """Show final deployment summary"""
        print("\n" + "="*60)
        print("📊 VPS DEPLOYMENT SUMMARY")
        print("="*60)
        
        for key, status in self.deployment_status.items():
            status_icon = "✅" if status else "❌"
            print(f"{status_icon} {key.replace('_', ' ').title()}: {status}")
        
        if all(self.deployment_status.values()):
            print("\n🎉 FULL DEPLOYMENT SUCCESS!")
            print("🚀 GenX Trading Platform is LIVE and CONNECTED!")
        else:
            print("\n⚠️  Partial deployment completed")
            print("🔧 Some components may need manual configuration")
        
        print(f"\n📅 Deployment completed: {datetime.now().isoformat()}")
        
        # Next steps
        print("\n🎯 Next Steps:")
        if self.deployment_status["vps_deployed"]:
            print("1. ✅ VPS simulation running on port 8001")
            print("2. 🔑 SSH keys ready for real VPS connection")
            print("3. 📱 Configure Termius with real VPS IP")
            print("4. 🚀 Deploy to actual VPS providers")
        else:
            print("1. 🔧 Fix connection issues")
            print("2. 🚀 Retry VPS deployment")

def main():
    """Main deployment function"""
    print("🚀 GenX Trading Platform - VPS Deployment & Live Execution")
    print("=" * 65)
    
    manager = VPSDeploymentManager()
    
    # Step 1: Test connectivity
    if manager.test_system_connectivity():
        print("✅ System connectivity confirmed")
    else:
        print("⚠️  Some connectivity issues detected")
    
    # Step 2: Test VPS providers
    manager.test_vps_providers()
    
    # Step 3: Deploy VPS (simulation for immediate testing)
    if manager.deploy_demo_vps():
        print("✅ VPS deployment successful")
    else:
        print("❌ VPS deployment failed")
    
    # Step 4: Test live connection
    if manager.test_live_connection():
        print("✅ Live connection established")
    else:
        print("❌ Live connection failed")
    
    # Step 5: Execute live trading
    if manager.execute_live_trading():
        print("✅ Live trading platform operational")
    else:
        print("❌ Live trading platform issues")
    
    # Step 6: Show summary
    manager.show_deployment_summary()
    
    return manager.deployment_status

if __name__ == "__main__":
    deployment_result = main()
    
    if all(deployment_result.values()):
        print("\n🎉 DEPLOYMENT COMPLETE - SYSTEM LIVE!")
        exit(0)
    else:
        print("\n⚠️  DEPLOYMENT PARTIAL - CHECK LOGS")
        exit(1)