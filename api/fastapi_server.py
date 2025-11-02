#!/usr/bin/env python3
"""
GenX FastAPI Server - Trading API with Magic Key Integration
"""

import logging
from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from pathlib import Path
import sys
from datetime import datetime
from typing import List, Optional
import aiohttp

sys.path.append(str(Path(__file__).parent.parent))

try:
    from core.magic_key_config import validate_trading_permission, get_trading_config
    from utils.logger_setup import setup_logging
    setup_logging()
    MAGIC_KEYS_AVAILABLE = True
except ImportError:
    MAGIC_KEYS_AVAILABLE = False

logger = logging.getLogger(__name__)

app = FastAPI(
    title="GenX Trading API",
    description="Forex trading signals and portfolio management",
    version="2.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

async def verify_api_key(x_api_key: Optional[str] = Header(None)):
    if not MAGIC_KEYS_AVAILABLE or not x_api_key:
        return True
    if not validate_trading_permission(x_api_key):
        raise HTTPException(status_code=403, detail="Invalid API key")
    return True

trading_signals = []
portfolio_status = {
    "balance": 10000.0,
    "equity": 10000.0,
    "active_trades": 0,
    "profit": 0.0,
    "last_updated": datetime.now().isoformat()
}

market_analysis = {
    "trends": {},
    "volatility": {},
    "last_updated": datetime.now().isoformat()
}

@app.get("/")
async def root():
    return {
        "service": "GenX Trading API",
        "version": "2.1.0",
        "status": "operational",
        "magic_keys_enabled": MAGIC_KEYS_AVAILABLE,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.get("/config/magic")
async def get_magic_config(authenticated: bool = Depends(verify_api_key)):
    if not MAGIC_KEYS_AVAILABLE:
        raise HTTPException(status_code=503, detail="Magic key system not available")
    
    config = get_trading_config()
    return {
        "magic_numbers": {k: v for k, v in config["magic_numbers"].items() if isinstance(v, int)},
        "permissions": config["permissions"],
        "timestamp": datetime.now().isoformat()
    }

@app.get("/trading/status")
async def get_trading_status(authenticated: bool = Depends(verify_api_key)):
    return {
        "signals_count": len(trading_signals),
        "magic_keys_enabled": MAGIC_KEYS_AVAILABLE,
        "portfolio": portfolio_status,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/signals")
async def get_trading_signals(authenticated: bool = Depends(verify_api_key)):
    try:
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get("http://localhost:8080/health") as response:
                    if response.status == 200:
                        return {
                            "signals": trading_signals,
                            "count": len(trading_signals),
                            "source": "live_system",
                            "timestamp": datetime.now().isoformat()
                        }
            except:
                pass
        
        mock_signals = [
            {
                "pair": "EURUSD",
                "direction": "BUY",
                "confidence": 0.85,
                "entry_price": 1.0950,
                "timestamp": datetime.now().isoformat()
            }
        ]
        
        return {
            "signals": mock_signals,
            "count": len(mock_signals),
            "source": "mock_data",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error getting signals: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving signals")

@app.get("/portfolio")
async def get_portfolio_status():
    return {
        "data": portfolio_status,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/analysis")
async def get_market_analysis():
    return {
        "data": market_analysis,
        "timestamp": datetime.now().isoformat()
    }

@app.post("/signals/update")
async def update_signals(signals: List[dict]):
    global trading_signals
    trading_signals = signals
    return {"count": len(signals), "timestamp": datetime.now().isoformat()}

@app.post("/portfolio/update")
async def update_portfolio(data: dict):
    global portfolio_status
    portfolio_status.update(data)
    portfolio_status["last_updated"] = datetime.now().isoformat()
    return {"timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    logger.info("Starting GenX FastAPI Server on port 8000...")
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info",
        reload=False
    )