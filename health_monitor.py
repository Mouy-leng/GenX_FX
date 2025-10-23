#!/usr/bin/env python3
"""
GenX FX Trading Platform Health Monitor
Monitors all system components and provides detailed health status
"""

import os
import sys
import time
import json
import logging
import psutil
import docker
import requests
from datetime import datetime
import mysql.connector
import redis
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler('logs/health_monitor.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class HealthMonitor:
    def __init__(self):
        self.docker_client = docker.from_env()
        self.health_data = {
            'timestamp': '',
            'overall_status': 'healthy',
            'containers': {},
            'services': {},
            'system': {},
            'trading': {}
        }

    def check_container_health(self):
        """Check health of all Docker containers"""
        try:
            containers = self.docker_client.containers.list()
            for container in containers:
                name = container.name
                status = {
                    'status': container.status,
                    'health': 'unknown'
                }
                
                # Get container health status if available
                if hasattr(container.attrs['State'], 'Health'):
                    status['health'] = container.attrs['State']['Health']['Status']
                
                # Get container metrics
                stats = container.stats(stream=False)
                status['memory_usage'] = stats['memory_stats'].get('usage', 0)
                status['cpu_usage'] = stats['cpu_stats'].get('cpu_usage', {}).get('total_usage', 0)
                
                self.health_data['containers'][name] = status
                
                if container.status != 'running' or status['health'] == 'unhealthy':
                    self.health_data['overall_status'] = 'degraded'
                    logger.warning(f"Container {name} is not healthy: {status}")
        except Exception as e:
            logger.error(f"Error checking container health: {e}")
            self.health_data['overall_status'] = 'degraded'

    def check_system_health(self):
        """Check system resources"""
        try:
            self.health_data['system'] = {
                'cpu_percent': psutil.cpu_percent(),
                'memory_percent': psutil.virtual_memory().percent,
                'disk_usage': psutil.disk_usage('/').percent,
                'load_average': os.getloadavg() if sys.platform != 'win32' else None
            }
            
            # Alert on high resource usage
            if self.health_data['system']['cpu_percent'] > 90 or \
               self.health_data['system']['memory_percent'] > 90 or \
               self.health_data['system']['disk_usage'] > 90:
                self.health_data['overall_status'] = 'degraded'
                logger.warning("High system resource usage detected")
        except Exception as e:
            logger.error(f"Error checking system health: {e}")
            self.health_data['overall_status'] = 'degraded'

    def check_service_health(self):
        """Check health of various services"""
        # Check API health
        try:
            response = requests.get('http://localhost:8080/health')
            self.health_data['services']['api'] = {
                'status': 'healthy' if response.status_code == 200 else 'unhealthy',
                'response_time': response.elapsed.total_seconds()
            }
        except Exception as e:
            logger.error(f"Error checking API health: {e}")
            self.health_data['services']['api'] = {'status': 'unhealthy', 'error': str(e)}
            self.health_data['overall_status'] = 'degraded'

        # Check MySQL health
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="genx_user",
                password="genx_password",
                database="genxdb_fx_db"
            )
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            cursor.fetchone()
            cursor.close()
            conn.close()
            self.health_data['services']['mysql'] = {'status': 'healthy'}
        except Exception as e:
            logger.error(f"Error checking MySQL health: {e}")
            self.health_data['services']['mysql'] = {'status': 'unhealthy', 'error': str(e)}
            self.health_data['overall_status'] = 'degraded'

        # Check Redis health
        try:
            r = redis.Redis(host='localhost', port=6379, db=0)
            r.ping()
            self.health_data['services']['redis'] = {'status': 'healthy'}
        except Exception as e:
            logger.error(f"Error checking Redis health: {e}")
            self.health_data['services']['redis'] = {'status': 'unhealthy', 'error': str(e)}
            self.health_data['overall_status'] = 'degraded'

    def check_trading_health(self):
        """Check trading-specific components"""
        # Check if trading bot process is running
        try:
            trading_bot_running = False
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                if 'python' in proc.info['name'] and 'main.py' in ' '.join(proc.info['cmdline']):
                    trading_bot_running = True
                    break
            
            self.health_data['trading']['bot_status'] = 'running' if trading_bot_running else 'stopped'
            if not trading_bot_running:
                self.health_data['overall_status'] = 'degraded'
                logger.warning("Trading bot is not running")
        except Exception as e:
            logger.error(f"Error checking trading bot status: {e}")
            self.health_data['trading']['bot_status'] = 'unknown'
            self.health_data['overall_status'] = 'degraded'

    def run_health_check(self):
        """Run all health checks and return results"""
        self.health_data['timestamp'] = datetime.now().isoformat()
        self.health_data['overall_status'] = 'healthy'  # Reset status

        self.check_container_health()
        self.check_system_health()
        self.check_service_health()
        self.check_trading_health()

        # Save health data to file
        health_file = Path('data/health_status.json')
        health_file.parent.mkdir(parents=True, exist_ok=True)
        with health_file.open('w') as f:
            json.dump(self.health_data, f, indent=2)

        return self.health_data

def main():
    """Main function to run health checks periodically"""
    monitor = HealthMonitor()
    check_interval = 60  # seconds

    while True:
        try:
            health_data = monitor.run_health_check()
            status = health_data['overall_status']
            logger.info(f"Health check completed. Overall status: {status}")
            
            if status != 'healthy':
                logger.warning("System is in degraded state. Check logs for details.")
            
            time.sleep(check_interval)
        except KeyboardInterrupt:
            logger.info("Health monitor shutting down...")
            break
        except Exception as e:
            logger.error(f"Error in health monitor: {e}")
            time.sleep(check_interval)

if __name__ == "__main__":
    main()