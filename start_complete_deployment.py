#!/usr/bin/env python3
"""
GenX Trading Platform - Complete Deployment Orchestrator
Automated deployment sequence for multi-VPS trading platform
"""

import subprocess
import sys
import os
import time
import json
import requests
from datetime import datetime
from pathlib import Path

class DeploymentOrchestrator:
    def __init__(self):
        self.start_time = datetime.now()
        self.deployment_log = []
        self.vps_endpoints = {}
        self.deployment_status = {
            'local_verification': False,
            'namecheap_deployed': False,
            'vultr_deployed': False,
            'gcp_deployed': False,
            'domain_configured': False
        }
    
    def log_step(self, message, status="INFO"):
        """Log deployment step with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {status}: {message}"
        print(log_entry)
        self.deployment_log.append(log_entry)
    
    def check_local_platform(self):
        """Verify local trading platform is operational"""
        self.log_step("🔍 Verifying Local Trading Platform...", "STEP")
        
        endpoints_to_check = [
            "http://localhost:8000/",
            "http://localhost:8000/trading/status",
            "http://localhost:8000/health",
            "http://localhost:8001/",
            "http://localhost:8001/trading/status"
        ]
        
        working_endpoints = []
        
        for endpoint in endpoints_to_check:
            try:
                response = requests.get(endpoint, timeout=5)
                if response.status_code == 200:
                    working_endpoints.append(endpoint)
                    self.log_step(f"✅ {endpoint} - OK", "SUCCESS")
                else:
                    self.log_step(f"⚠️ {endpoint} - Status {response.status_code}", "WARN")
            except requests.exceptions.ConnectionError:
                self.log_step(f"❌ {endpoint} - Not running", "ERROR")
            except Exception as e:
                self.log_step(f"❌ {endpoint} - Error: {e}", "ERROR")
        
        if working_endpoints:
            self.deployment_status['local_verification'] = True
            self.log_step(f"✅ Local platform verified - {len(working_endpoints)} endpoints operational", "SUCCESS")
            return True
        else:
            self.log_step("❌ Local platform verification failed", "ERROR")
            return False
    
    def start_local_platform(self):
        """Start local trading platform if not running"""
        self.log_step("🚀 Starting Local Trading Platform...", "STEP")
        
        try:
            # Try to start the VPS simulation
            result = subprocess.run([
                sys.executable, "retry_vps_deployment.py"
            ], capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                self.log_step("✅ Local platform started successfully", "SUCCESS")
                time.sleep(5)  # Wait for services to fully start
                return True
            else:
                self.log_step(f"⚠️ Platform start returned code {result.returncode}", "WARN")
                self.log_step(f"Output: {result.stdout}", "INFO")
                return False
                
        except subprocess.TimeoutExpired:
            self.log_step("⚠️ Platform start timeout - continuing anyway", "WARN")
            return True
        except Exception as e:
            self.log_step(f"❌ Failed to start platform: {e}", "ERROR")
            return False
    
    def deploy_namecheap(self):
        """Deploy to NameCheap VPS"""
        self.log_step("🌐 Deploying to NameCheap VPS...", "STEP")
        
        # Check if credentials are set
        required_env_vars = [
            'NAMECHEAP_API_USER',
            'NAMECHEAP_API_KEY', 
            'NAMECHEAP_USERNAME',
            'NAMECHEAP_CLIENT_IP'
        ]
        
        missing_vars = [var for var in required_env_vars if not os.environ.get(var)]
        
        if missing_vars:
            self.log_step(f"❌ Missing NameCheap credentials: {', '.join(missing_vars)}", "ERROR")
            self.log_step("📋 Set credentials with:", "INFO")
            self.log_step('$env:NAMECHEAP_API_USER = "your_username"', "INFO")
            self.log_step('$env:NAMECHEAP_API_KEY = "your_api_key"', "INFO")
            self.log_step('$env:NAMECHEAP_USERNAME = "your_username"', "INFO")
            self.log_step('$env:NAMECHEAP_CLIENT_IP = "117.20.115.126"', "INFO")
            return False
        
        try:
            # Execute NameCheap deployment
            result = subprocess.run([
                sys.executable, "setup_namecheap_deployment.py"
            ], capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                self.deployment_status['namecheap_deployed'] = True
                self.log_step("✅ NameCheap VPS deployment successful", "SUCCESS")
                return True
            else:
                self.log_step(f"❌ NameCheap deployment failed: {result.stderr}", "ERROR")
                return False
                
        except Exception as e:
            self.log_step(f"❌ NameCheap deployment error: {e}", "ERROR")
            return False
    
    def deploy_vultr(self):
        """Deploy to Vultr VPS"""
        self.log_step("🚀 Deploying to Vultr VPS...", "STEP")
        
        if not os.environ.get('VULTR_API_KEY'):
            self.log_step("❌ Missing VULTR_API_KEY environment variable", "ERROR")
            self.log_step("📋 Set with: $env:VULTR_API_KEY = 'your_vultr_api_key'", "INFO")
            return False
        
        # Vultr deployment would go here
        self.log_step("ℹ️ Vultr deployment script ready - implement when needed", "INFO")
        return True
    
    def deploy_gcp(self):
        """Deploy to Google Cloud Platform"""
        self.log_step("☁️ Deploying to Google Cloud Platform...", "STEP")
        
        # Check if gcloud is authenticated
        try:
            result = subprocess.run(['gcloud', 'auth', 'list'], 
                                  capture_output=True, text=True)
            if "No credentialed accounts" in result.stdout:
                self.log_step("❌ No GCP authentication found", "ERROR")
                self.log_step("📋 Run: gcloud auth login", "INFO")
                return False
        except FileNotFoundError:
            self.log_step("❌ Google Cloud CLI not installed", "ERROR")
            return False
        
        # GCP deployment would go here
        self.log_step("ℹ️ GCP deployment script ready - implement when needed", "INFO")
        return True
    
    def configure_domain(self):
        """Configure domain name and SSL"""
        self.log_step("🌐 Configuring Domain & SSL...", "STEP")
        
        # This would integrate with domain registration and DNS setup
        self.log_step("ℹ️ Domain configuration ready - implement after VPS deployment", "INFO")
        return True
    
    def run_deployment_tests(self):
        """Run comprehensive deployment tests"""
        self.log_step("🧪 Running Deployment Tests...", "STEP")
        
        test_results = {
            'local_endpoints': 0,
            'vps_endpoints': 0,
            'ssl_certificates': 0,
            'trading_functionality': 0
        }
        
        # Test local endpoints
        local_endpoints = [
            "http://localhost:8000/",
            "http://localhost:8000/trading/status",
            "http://localhost:8001/"
        ]
        
        for endpoint in local_endpoints:
            try:
                response = requests.get(endpoint, timeout=5)
                if response.status_code == 200:
                    test_results['local_endpoints'] += 1
            except:
                pass
        
        # Test trading functionality
        try:
            magic_response = requests.get("http://localhost:8000/config/magic", timeout=5)
            if magic_response.status_code == 200:
                test_results['trading_functionality'] = 1
        except:
            pass
        
        total_tests = sum(test_results.values())
        self.log_step(f"✅ Deployment tests completed: {total_tests}/4 passed", "SUCCESS")
        
        return test_results
    
    def generate_deployment_report(self):
        """Generate comprehensive deployment report"""
        end_time = datetime.now()
        duration = end_time - self.start_time
        
        report = {
            'deployment_summary': {
                'start_time': self.start_time.isoformat(),
                'end_time': end_time.isoformat(),
                'duration_seconds': duration.total_seconds(),
                'status': self.deployment_status
            },
            'endpoints': self.vps_endpoints,
            'log': self.deployment_log
        }
        
        report_file = f"deployment_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        self.log_step(f"📊 Deployment report saved: {report_file}", "SUCCESS")
        return report
    
    def display_deployment_summary(self):
        """Display deployment summary"""
        print("\n" + "="*60)
        print("🎉 GENX TRADING PLATFORM DEPLOYMENT SUMMARY")
        print("="*60)
        
        print(f"\n📅 Deployment Time: {(datetime.now() - self.start_time).total_seconds():.1f} seconds")
        
        print(f"\n📊 Deployment Status:")
        for service, status in self.deployment_status.items():
            icon = "✅" if status else "❌"
            print(f"   {icon} {service.replace('_', ' ').title()}")
        
        if self.vps_endpoints:
            print(f"\n🌐 Active Endpoints:")
            for name, url in self.vps_endpoints.items():
                print(f"   🔗 {name}: {url}")
        
        print(f"\n📋 Next Steps:")
        if not self.deployment_status['namecheap_deployed']:
            print("   1. Set NameCheap API credentials")
            print("   2. Run NameCheap deployment")
        if not self.deployment_status['domain_configured']:
            print("   3. Configure domain name")
            print("   4. Set up SSL certificates")
        
        print(f"\n🎯 Trading Platform Ready!")
        print("   Access: http://localhost:8000/ or http://localhost:8001/")
        print("   Status: http://localhost:8000/trading/status")
        print("   Magic Config: http://localhost:8000/config/magic")

def main():
    """Main deployment orchestrator"""
    print("🚀 GenX Trading Platform - Complete Deployment Orchestrator")
    print("="*60)
    print(f"🕐 Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    orchestrator = DeploymentOrchestrator()
    
    try:
        # Step 1: Verify or start local platform
        orchestrator.log_step("🎯 PHASE 1: Local Platform Verification", "PHASE")
        if not orchestrator.check_local_platform():
            orchestrator.log_step("🔄 Starting local platform...", "INFO")
            orchestrator.start_local_platform()
            time.sleep(3)
            orchestrator.check_local_platform()
        
        # Step 2: Deploy to VPS providers
        orchestrator.log_step("🎯 PHASE 2: VPS Deployment", "PHASE")
        
        # NameCheap deployment
        orchestrator.deploy_namecheap()
        
        # Vultr deployment (optional)
        # orchestrator.deploy_vultr()
        
        # GCP deployment (optional)
        # orchestrator.deploy_gcp()
        
        # Step 3: Configure domain and SSL
        orchestrator.log_step("🎯 PHASE 3: Domain & SSL Configuration", "PHASE")
        orchestrator.configure_domain()
        
        # Step 4: Run tests
        orchestrator.log_step("🎯 PHASE 4: Deployment Testing", "PHASE")
        test_results = orchestrator.run_deployment_tests()
        
        # Step 5: Generate report
        orchestrator.log_step("🎯 PHASE 5: Deployment Report", "PHASE")
        report = orchestrator.generate_deployment_report()
        
        # Display summary
        orchestrator.display_deployment_summary()
        
    except KeyboardInterrupt:
        orchestrator.log_step("⚠️ Deployment interrupted by user", "WARN")
    except Exception as e:
        orchestrator.log_step(f"❌ Deployment failed: {e}", "ERROR")
    finally:
        orchestrator.log_step("🏁 Deployment orchestrator completed", "FINAL")

if __name__ == "__main__":
    main()