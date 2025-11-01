#!/usr/bin/env python3
"""
GenX Simple EA Server - Standalone version
Handles communication between Expert Advisors and the trading system
"""

import asyncio
import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import aiohttp

# Configure basic logging
logging.basicConfig(level=logging.INFO)
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
                async with session.get("http://localhost:8000/signals", timeout=3) as response:
                    if response.status == 200:
                        data = await response.json()
                        # Convert format for EA consumption
                        ea_signals = []
                        for signal in data.get("signals", []):
                            ea_signals.append({
                                "pair": signal.get("pair"),
                                "action": signal.get("direction", signal.get("action")),
                                "confidence": int((signal.get("confidence", 0.8) * 100)),
                                "entry": signal.get("entry_price", signal.get("entry", 0)),
                                "sl": signal.get("stop_loss", signal.get("sl", 0)),
                                "tp": signal.get("take_profit", signal.get("tp", 0)),
                                "lot_size": 0.1,
                                "timestamp": signal.get("timestamp", datetime.now().isoformat())
                            })
                        
                        return {
                            "status": "success",
                            "signals": ea_signals,
                            "source": "fastapi_server",
                            "timestamp": datetime.now().isoformat()
                        }
            except Exception as e:
                logger.warning(f"Failed to get signals from FastAPI: {e}")
                
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
            },
            {
                "pair": "GBPUSD",
                "action": "SELL", 
                "confidence": 78,
                "entry": 1.2650,
                "sl": 1.2680,
                "tp": 1.2600,
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
    recent = trade_confirmations[-50:] if len(trade_confirmations) > 50 else trade_confirmations
    return {
        "confirmations": recent,
        "count": len(recent),
        "total": len(trade_confirmations),
        "timestamp": datetime.now().isoformat()
    }

@app.delete("/ea/{ea_id}")
async def disconnect_ea(ea_id: str):
    """Disconnect an EA"""
    if ea_id in ea_connections:
        del ea_connections[ea_id]
        logger.info(f"EA disconnected: {ea_id}")
        return {"status": "disconnected"}
    else:
        raise HTTPException(status_code=404, detail="EA not found")

if __name__ == "__main__":
    logger.info("Starting GenX Simple EA Communication Server on port 9091...")
    uvicorn.run(
        app,
        host="0.0.0.0", 
        port=9091,
        log_level="info",
        reload=False
    )