#!/usr/bin/env python3
"""
GenX EA Communication Server - Port 9090
Handles communication between Expert Advisors and the trading system
"""

import asyncio
import logging
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from pathlib import Path
import sys
import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import aiohttp
import websockets
from threading import Thread

# Add project root to path  
sys.path.append(str(Path(__file__).parent.parent))

from utils.logger_setup import setup_logging

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="GenX EA Communication Server", 
    description="Expert Advisor communication hub for MT4/MT5 integration",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)

# Global state for EA connections
ea_connections = {}
signal_queue = []
trade_confirmations = []

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "GenX EA Communication Server",
        "version": "1.0.0", 
        "status": "operational",
        "connected_eas": len(ea_connections),
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "genx-ea-server",
        "connected_eas": len(ea_connections),
        "signal_queue_size": len(signal_queue),
        "timestamp": datetime.now().isoformat()
    }

@app.post("/ea/register")
async def register_ea(ea_data: dict):
    """Register a new EA connection"""
    ea_id = ea_data.get("ea_id", f"ea_{len(ea_connections)}")
    ea_connections[ea_id] = {
        "id": ea_id,
        "name": ea_data.get("name", "Unknown EA"),
        "version": ea_data.get("version", "1.0"),
        "account": ea_data.get("account", "Unknown"),
        "broker": ea_data.get("broker", "Unknown"),
        "connected_at": datetime.now().isoformat(),
        "last_heartbeat": datetime.now().isoformat(),
        "status": "connected"
    }
    
    logger.info(f"EA registered: {ea_id}")
    return {
        "status": "registered",
        "ea_id": ea_id,
        "timestamp": datetime.now().isoformat()
    }

@app.post("/ea/{ea_id}/heartbeat")
async def ea_heartbeat(ea_id: str):
    """Update EA heartbeat"""
    if ea_id in ea_connections:
        ea_connections[ea_id]["last_heartbeat"] = datetime.now().isoformat()
        ea_connections[ea_id]["status"] = "connected"
        return {"status": "acknowledged"}
    else:
        raise HTTPException(status_code=404, detail="EA not found")

@app.get("/ea/list")
async def list_eas():
    """List all connected EAs"""
    return {
        "eas": list(ea_connections.values()),
        "count": len(ea_connections),
        "timestamp": datetime.now().isoformat()
    }

@app.get("/signals/latest")
async def get_latest_signals():
    """Get latest trading signals for EAs"""
    try:
        # Try to get signals from FastAPI server
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get("http://localhost:8000/signals") as response:
                    if response.status == 200:
                        data = await response.json()
                        return {
                            "status": "success",
                            "signals": data.get("signals", []),
                            "source": "fastapi_server",
                            "timestamp": datetime.now().isoformat()
                        }
            except:
                pass
                
        # Return mock signals if FastAPI not available
        mock_signals = [
            {
                "pair": "EURUSD",
                "action": "BUY",
                "confidence": 85,
                "entry": 1.0950,
                "sl": 1.0920,
                "tp": 1.1000,
                "lot_size": 0.1,
                "timestamp": datetime.now().isoformat()
            }
        ]
        
        return {
            "status": "success",
            "signals": mock_signals,
            "source": "mock_data", 
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error getting signals: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving signals")

@app.post("/trades/confirmation")
async def trade_confirmation(trade_data: dict):
    """Receive trade confirmation from EA"""
    confirmation = {
        "ea_id": trade_data.get("ea_id"),
        "ticket": trade_data.get("ticket"),
        "pair": trade_data.get("pair"),
        "action": trade_data.get("action"),
        "volume": trade_data.get("volume"),
        "open_price": trade_data.get("open_price"),
        "status": trade_data.get("status", "opened"),
        "timestamp": datetime.now().isoformat()
    }
    
    trade_confirmations.append(confirmation)
    logger.info(f"Trade confirmation received: {confirmation}")
    
    return {
        "status": "confirmed",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/trades/confirmations")
async def get_trade_confirmations():
    """Get recent trade confirmations"""
    # Return last 50 confirmations
    recent = trade_confirmations[-50:] if len(trade_confirmations) > 50 else trade_confirmations
    return {
        "confirmations": recent,
        "count": len(recent),
        "total": len(trade_confirmations),
        "timestamp": datetime.now().isoformat()
    }

@app.post("/ea/{ea_id}/status")
async def update_ea_status(ea_id: str, status_data: dict):
    """Update EA status"""
    if ea_id in ea_connections:
        ea_connections[ea_id].update(status_data)
        ea_connections[ea_id]["last_update"] = datetime.now().isoformat()
        return {"status": "updated"}
    else:
        raise HTTPException(status_code=404, detail="EA not found")

@app.delete("/ea/{ea_id}")
async def disconnect_ea(ea_id: str):
    """Disconnect an EA"""
    if ea_id in ea_connections:
        del ea_connections[ea_id]
        logger.info(f"EA disconnected: {ea_id}")
        return {"status": "disconnected"}
    else:
        raise HTTPException(status_code=404, detail="EA not found")

# Background task to clean up stale connections
async def cleanup_stale_connections():
    """Remove EAs that haven't sent heartbeat in 5 minutes"""
    while True:
        try:
            current_time = datetime.now()
            stale_eas = []
            
            for ea_id, ea_data in ea_connections.items():
                last_heartbeat = datetime.fromisoformat(ea_data["last_heartbeat"])
                if (current_time - last_heartbeat).total_seconds() > 300:  # 5 minutes
                    stale_eas.append(ea_id)
                    
            for ea_id in stale_eas:
                ea_connections[ea_id]["status"] = "disconnected"
                logger.warning(f"EA marked as stale: {ea_id}")
                
        except Exception as e:
            logger.error(f"Error in cleanup task: {e}")
            
        await asyncio.sleep(60)  # Check every minute

@app.on_event("startup")
async def startup_event():
    """Start background tasks"""
    asyncio.create_task(cleanup_stale_connections())
    logger.info("GenX EA Communication Server started on port 9090")

if __name__ == "__main__":
    logger.info("Starting GenX EA Communication Server on port 9090...")
    uvicorn.run(
        app,
        host="0.0.0.0", 
        port=9090,
        log_level="info",
        reload=False
    )