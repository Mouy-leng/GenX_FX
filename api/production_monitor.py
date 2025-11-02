#!/usr/bin/env python3
"""
GenX Production Monitor & Health Dashboard
Comprehensive monitoring for all GenX trading services
"""

import asyncio
import aiohttp
import json
import time
from datetime import datetime, timedelta
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="GenX Production Monitor",
    description="Comprehensive monitoring dashboard for GenX Trading Platform",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Service endpoints to monitor
SERVICES = {
    "main_trading": "http://localhost:8080/health",
    "fastapi_server": "http://localhost:8000/health", 
    "websocket_server": "ws://localhost:8765",
    "external_fastapi": "http://10.124.54.249:8000/health",
    "external_websocket": "ws://10.124.54.249:8765"
}

# Global monitoring data
monitoring_data = {
    "services": {},
    "alerts": [],
    "uptime_start": datetime.now(),
    "last_check": None,
    "total_checks": 0
}

async def check_http_service(name: str, url: str) -> dict:
    """Check HTTP/HTTPS service health"""
    try:
        start_time = time.time()
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=5) as response:
                response_time = (time.time() - start_time) * 1000  # Convert to ms
                
                if response.status == 200:
                    data = await response.json()
                    return {
                        "status": "healthy",
                        "response_time": round(response_time, 2),
                        "details": data,
                        "last_check": datetime.now().isoformat()
                    }
                else:
                    return {
                        "status": "unhealthy",
                        "response_time": round(response_time, 2),
                        "error": f"HTTP {response.status}",
                        "last_check": datetime.now().isoformat()
                    }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "last_check": datetime.now().isoformat()
        }

async def check_websocket_service(name: str, url: str) -> dict:
    """Check WebSocket service health"""
    try:
        # For WebSocket, we'll try to connect to the HTTP equivalent or ping
        http_url = url.replace("ws://", "http://").replace(":8765", ":8000/health")
        return await check_http_service(name, http_url)
    except Exception as e:
        return {
            "status": "error", 
            "error": str(e),
            "last_check": datetime.now().isoformat()
        }

async def monitor_services():
    """Monitor all services continuously"""
    while True:
        try:
            monitoring_data["total_checks"] += 1
            
            for service_name, service_url in SERVICES.items():
                if service_url.startswith("ws://"):
                    result = await check_websocket_service(service_name, service_url)
                else:
                    result = await check_http_service(service_name, service_url)
                
                monitoring_data["services"][service_name] = result
                
                # Generate alerts for unhealthy services
                if result["status"] != "healthy":
                    alert = {
                        "service": service_name,
                        "status": result["status"],
                        "error": result.get("error", "Unknown error"),
                        "timestamp": datetime.now().isoformat()
                    }
                    monitoring_data["alerts"].append(alert)
                    
                    # Keep only last 50 alerts
                    if len(monitoring_data["alerts"]) > 50:
                        monitoring_data["alerts"] = monitoring_data["alerts"][-50:]
            
            monitoring_data["last_check"] = datetime.now().isoformat()
            logger.info(f"Health check #{monitoring_data['total_checks']} completed")
            
        except Exception as e:
            logger.error(f"Error in monitoring loop: {e}")
        
        # Wait 30 seconds before next check
        await asyncio.sleep(30)

@app.get("/")
async def dashboard():
    """Production monitoring dashboard"""
    uptime_str = str(datetime.now() - monitoring_data['uptime_start'])
    healthy_count = len([s for s in monitoring_data['services'].values() if s.get('status') == 'healthy'])
    unhealthy_count = len([s for s in monitoring_data['services'].values() if s.get('status') != 'healthy'])
    alerts_count = len(monitoring_data['alerts'])
    last_check_str = monitoring_data.get('last_check', 'Never')
    
    dashboard_html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GenX Production Monitor</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            min-height: 100vh;
            padding: 20px;
        }}
        .header {{ text-align: center; margin-bottom: 30px; }}
        .header h1 {{ font-size: 2.5rem; margin-bottom: 10px; }}
        .stats-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-bottom: 30px; }}
        .stat-card {{ 
            background: rgba(255,255,255,0.1);
            border-radius: 15px;
            padding: 20px;
            border: 1px solid rgba(255,255,255,0.2);
            backdrop-filter: blur(10px);
        }}
        .service-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }}
        .service-card {{
            background: rgba(255,255,255,0.1);
            border-radius: 15px;
            padding: 20px;
            border: 1px solid rgba(255,255,255,0.2);
        }}
        .status-healthy {{ color: #4ade80; }}
        .status-unhealthy {{ color: #f87171; }}
        .status-error {{ color: #fbbf24; }}
        .refresh-btn {{
            background: #10b981;
            color: white;
            border: none;
            padding: 12px 30px;
            border-radius: 25px;
            font-weight: bold;
            cursor: pointer;
            margin: 10px;
            font-size: 16px;
        }}
        .alert {{ 
            background: rgba(248, 113, 113, 0.2);
            border: 1px solid #f87171;
            border-radius: 10px;
            padding: 15px;
            margin: 10px 0;
        }}
        @media (max-width: 768px) {{
            .stats-grid, .service-grid {{ grid-template-columns: 1fr; }}
            .header h1 {{ font-size: 1.8rem; }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🚀 GenX Production Monitor</h1>
        <p>Real-time monitoring of all trading platform services</p>
        <button class="refresh-btn" onclick="location.reload()">🔄 Refresh Dashboard</button>
    </div>
    
    <div class="stats-grid">
        <div class="stat-card">
            <h3>📊 System Overview</h3>
            <div><strong>Uptime:</strong> {uptime_str}</div>
            <div><strong>Total Checks:</strong> {monitoring_data['total_checks']}</div>
            <div><strong>Last Check:</strong> {last_check_str}</div>
        </div>
        
        <div class="stat-card">
            <h3>🟢 Healthy Services</h3>
            <div><strong>Count:</strong> {healthy_count}</div>
        </div>
        
        <div class="stat-card">
            <h3>🔴 Issues Detected</h3>
            <div><strong>Count:</strong> {unhealthy_count}</div>
        </div>
        
        <div class="stat-card">
            <h3>⚠️ Recent Alerts</h3>
            <div><strong>Count:</strong> {alerts_count}</div>
        </div>
    </div>
    
    <div class="service-grid" id="services">
        <!-- Services will be populated by JavaScript -->
    </div>
    
    <script>
        // JavaScript for dynamic updates
    </script>
</body>
</html>
"""
    return HTMLResponse(content=dashboard_html)

@app.get("/api/status")
async def get_status():
    """Get current monitoring status"""
    return {
        "timestamp": datetime.now().isoformat(),
        "services": monitoring_data["services"],
        "alerts": monitoring_data["alerts"][-10:],  # Last 10 alerts
        "uptime": str(datetime.now() - monitoring_data["uptime_start"]),
        "total_checks": monitoring_data["total_checks"]
    }

@app.get("/health")
async def health():
    """Monitor health endpoint"""
    healthy_services = len([s for s in monitoring_data["services"].values() if s.get("status") == "healthy"])
    total_services = len(monitoring_data["services"])
    
    return {
        "status": "healthy" if healthy_services == total_services else "degraded",
        "services_healthy": f"{healthy_services}/{total_services}",
        "last_check": monitoring_data.get("last_check"),
        "uptime": str(datetime.now() - monitoring_data["uptime_start"])
    }

@app.on_event("startup")
async def startup_event():
    """Start monitoring on startup"""
    asyncio.create_task(monitor_services())
    logger.info("GenX Production Monitor started")

if __name__ == "__main__":
    logger.info("Starting GenX Production Monitor on port 8888...")
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8888,
        log_level="info",
        reload=False
    )