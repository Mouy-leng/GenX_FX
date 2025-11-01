#!/usr/bin/env python3
"""
GenX Frontend Server - Port 5173
Simple HTTP server for mobile-optimized trading dashboard
"""

import http.server
import socketserver
import logging
from pathlib import Path
import sys
import json
from datetime import datetime
import urllib.request
import urllib.error

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from utils.logger_setup import setup_logging

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

class GenXFrontendHandler(http.server.SimpleHTTPRequestHandler):
    """Custom handler for GenX frontend"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(Path(__file__).parent / "static"), **kwargs)
    
    def do_GET(self):
        """Handle GET requests"""
        if self.path == '/':
            self.path = '/index.html'
        elif self.path == '/api/status':
            self.send_api_status()
            return
        elif self.path == '/api/signals':
            self.send_api_signals()
            return
        elif self.path == '/api/health':
            self.send_health_check()
            return
            
        super().do_GET()
    
    def send_api_status(self):
        """Send API status"""
        try:
            # Check all services
            services = {
                "main_api": self.check_service("http://localhost:8080/health"),
                "fastapi": self.check_service("http://localhost:8000/health"), 
                "ea_server": self.check_service("http://localhost:9091/health")
            }
            
            response = {
                "status": "operational",
                "services": services,
                "timestamp": datetime.now().isoformat()
            }
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            logger.error(f"Error getting API status: {e}")
            self.send_error(500)
    
    def send_api_signals(self):
        """Send trading signals"""
        try:
            # Try to get signals from FastAPI
            try:
                with urllib.request.urlopen("http://localhost:8000/signals", timeout=5) as response:
                    data = json.loads(response.read().decode())
                    
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(data).encode())
                return
            except:
                pass
                
            # Fallback to mock data
            mock_signals = {
                "signals": [
                    {
                        "pair": "EURUSD",
                        "direction": "BUY",
                        "confidence": 0.85,
                        "entry_price": 1.0950,
                        "timestamp": datetime.now().isoformat()
                    }
                ],
                "source": "frontend_mock"
            }
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json') 
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(mock_signals).encode())
            
        except Exception as e:
            logger.error(f"Error getting signals: {e}")
            self.send_error(500)
    
    def send_health_check(self):
        """Send health check"""
        response = {
            "status": "healthy",
            "service": "genx-frontend-server",
            "timestamp": datetime.now().isoformat()
        }
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())
    
    def check_service(self, url):
        """Check if a service is running"""
        try:
            with urllib.request.urlopen(url, timeout=3) as response:
                return {"status": "online", "code": response.getcode()}
        except Exception as e:
            return {"status": "offline", "error": str(e)}

def create_static_files():
    """Create static HTML files for mobile dashboard"""
    static_dir = Path(__file__).parent / "static"
    static_dir.mkdir(exist_ok=True)
    
    # Create index.html
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GenX Trading Dashboard</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Arial, sans-serif;
            background: linear-gradient(135deg, #1e3c72, #2a5298);
            color: white;
            min-height: 100vh;
            padding: 20px;
        }
        .header { text-align: center; margin-bottom: 30px; }
        .header h1 { font-size: 2rem; margin-bottom: 10px; }
        .status-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-bottom: 30px; }
        .status-card { 
            background: rgba(255,255,255,0.1); 
            border-radius: 15px; 
            padding: 20px; 
            border: 1px solid rgba(255,255,255,0.2);
            backdrop-filter: blur(10px);
        }
        .status-card h3 { margin-bottom: 15px; color: #FFD700; }
        .signal-item { 
            background: rgba(0,255,0,0.1); 
            border-radius: 10px; 
            padding: 15px; 
            margin: 10px 0;
            border-left: 4px solid #00FF00;
        }
        .signal-item.sell { 
            background: rgba(255,0,0,0.1); 
            border-left-color: #FF4444;
        }
        .status-online { color: #00FF00; }
        .status-offline { color: #FF4444; }
        .refresh-btn {
            background: #FFD700;
            color: #1e3c72;
            border: none;
            padding: 12px 30px;
            border-radius: 25px;
            font-weight: bold;
            cursor: pointer;
            margin: 10px;
            font-size: 16px;
        }
        .timestamp { font-size: 0.8rem; opacity: 0.7; margin-top: 10px; }
        @media (max-width: 768px) {
            .status-grid { grid-template-columns: 1fr; }
            .header h1 { font-size: 1.5rem; }
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🚀 GenX Trading Dashboard</h1>
        <p>Mobile-Optimized Trading Control Center</p>
        <button class="refresh-btn" onclick="refreshData()">🔄 Refresh Data</button>
    </div>
    
    <div class="status-grid">
        <div class="status-card">
            <h3>📊 System Status</h3>
            <div id="system-status">Loading...</div>
        </div>
        
        <div class="status-card">
            <h3>📈 Trading Signals</h3>
            <div id="trading-signals">Loading...</div>
        </div>
        
        <div class="status-card">
            <h3>🔧 API Services</h3>
            <div id="api-services">Loading...</div>
        </div>
        
        <div class="status-card">
            <h3>📱 Quick Actions</h3>
            <button class="refresh-btn" onclick="testTelegram()">📱 Test Telegram Bot</button>
            <button class="refresh-btn" onclick="viewDocs()">📖 API Docs</button>
        </div>
    </div>

    <script>
        let lastUpdate = new Date();
        
        async function refreshData() {
            try {
                await Promise.all([
                    updateSystemStatus(),
                    updateTradingSignals(),
                    updateApiServices()
                ]);
                lastUpdate = new Date();
                console.log('Data refreshed successfully');
            } catch (error) {
                console.error('Error refreshing data:', error);
            }
        }
        
        async function updateSystemStatus() {
            try {
                const response = await fetch('/api/status');
                const data = await response.json();
                
                const statusHtml = `
                    <div><strong>Status:</strong> <span class="status-online">${data.status}</span></div>
                    <div><strong>Services Online:</strong> ${Object.values(data.services).filter(s => s.status === 'online').length}/3</div>
                    <div class="timestamp">Last Update: ${new Date(data.timestamp).toLocaleTimeString()}</div>
                `;
                
                document.getElementById('system-status').innerHTML = statusHtml;
            } catch (error) {
                document.getElementById('system-status').innerHTML = '<span class="status-offline">Error loading status</span>';
            }
        }
        
        async function updateTradingSignals() {
            try {
                const response = await fetch('/api/signals');
                const data = await response.json();
                
                let signalsHtml = '';
                if (data.signals && data.signals.length > 0) {
                    data.signals.forEach(signal => {
                        const direction = signal.direction || signal.action;
                        const cssClass = direction === 'SELL' ? 'sell' : '';
                        signalsHtml += `
                            <div class="signal-item ${cssClass}">
                                <strong>${signal.pair}</strong> - ${direction}<br>
                                <small>Confidence: ${Math.round((signal.confidence || 0.8) * 100)}%</small>
                            </div>
                        `;
                    });
                } else {
                    signalsHtml = '<div>No signals available</div>';
                }
                
                document.getElementById('trading-signals').innerHTML = signalsHtml;
            } catch (error) {
                document.getElementById('trading-signals').innerHTML = '<span class="status-offline">Error loading signals</span>';
            }
        }
        
        async function updateApiServices() {
            try {
                const response = await fetch('/api/status');
                const data = await response.json();
                
                let servicesHtml = '';
                Object.entries(data.services).forEach(([name, service]) => {
                    const statusClass = service.status === 'online' ? 'status-online' : 'status-offline';
                    servicesHtml += `
                        <div><strong>${name}:</strong> <span class="${statusClass}">${service.status}</span></div>
                    `;
                });
                
                document.getElementById('api-services').innerHTML = servicesHtml;
            } catch (error) {
                document.getElementById('api-services').innerHTML = '<span class="status-offline">Error loading services</span>';
            }
        }
        
        function testTelegram() {
            alert('Open Telegram and search for @GenX_FX_bot to test the bot!');
        }
        
        function viewDocs() {
            window.open('http://' + window.location.hostname + ':8000/docs', '_blank');
        }
        
        // Auto-refresh every 30 seconds
        setInterval(refreshData, 30000);
        
        // Initial load
        refreshData();
    </script>
</body>
</html>"""
    
    with open(static_dir / "index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    
    logger.info("Static files created successfully")

if __name__ == "__main__":
    # Create static files
    create_static_files()
    
    PORT = 5173
    
    with socketserver.TCPServer(("", PORT), GenXFrontendHandler) as httpd:
        logger.info(f"Starting GenX Frontend Server on port {PORT}...")
        logger.info(f"Access dashboard at: http://localhost:{PORT}")
        logger.info(f"Mobile access at: http://10.124.54.249:{PORT}")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            logger.info("Frontend server stopped")
            httpd.shutdown()