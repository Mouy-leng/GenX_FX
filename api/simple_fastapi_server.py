#!/usr/bin/env python3
"""
GenX Simple FastAPI Server - Standalone version
Provides REST endpoints without complex dependencies
"""

import asyncio
import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from datetime import datetime
from typing import List, Dict, Optional
import aiohttp

# Configure basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="GenX Trading API",
    description="Advanced AI-powered Forex trading signals and portfolio management",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global state
trading_signals = [
    {
        "pair": "EURUSD",
        "direction": "BUY",
        "confidence": 0.85,
        "entry_price": 1.0950,
        "stop_loss": 1.0920,
        "take_profit": 1.1000,
        "timestamp": datetime.now().isoformat()
    },
    {
        "pair": "GBPUSD", 
        "direction": "SELL",
        "confidence": 0.78,
        "entry_price": 1.2650,
        "stop_loss": 1.2680,
        "take_profit": 1.2600,
        "timestamp": datetime.now().isoformat()
    },
    {
        "pair": "USDJPY",
        "direction": "BUY", 
        "confidence": 0.82,
        "entry_price": 149.25,
        "stop_loss": 148.90,
        "take_profit": 149.80,
        "timestamp": datetime.now().isoformat()
    }
]

portfolio_status = {
    "balance": 10000.0,
    "equity": 10247.50,
    "margin": 156.30,
    "free_margin": 10091.20,
    "margin_level": 6555.2,
    "active_trades": 3,
    "total_trades": 127,
    "profit": 247.50,
    "last_updated": datetime.now().isoformat()
}

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "service": "GenX Trading API",
        "version": "2.0.0",
        "status": "operational",
        "endpoints": {
            "health": "/health",
            "signals": "/signals",
            "portfolio": "/portfolio",
            "analysis": "/analysis",
            "docs": "/docs"
        },
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "genx-fastapi-server",
        "timestamp": datetime.now().isoformat(),
        "uptime": "operational",
        "signals_available": len(trading_signals)
    }

@app.get("/signals")
async def get_trading_signals():
    """Get current trading signals"""
    try:
        return {
            "signals": trading_signals,
            "count": len(trading_signals),
            "last_updated": datetime.now().isoformat(),
            "source": "genx_trading_system"
        }
    except Exception as e:
        logger.error(f"Error getting signals: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving signals")

@app.get("/portfolio")
async def get_portfolio_status():
    """Get current portfolio status"""
    return {
        "status": "success",
        "data": portfolio_status,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/analysis")
async def get_market_analysis():
    """Get current market analysis"""
    analysis = {
        "trends": {
            "EURUSD": "bullish",
            "GBPUSD": "bearish", 
            "USDJPY": "bullish"
        },
        "volatility": {
            "overall": "medium",
            "major_pairs": "low",
            "cross_pairs": "high"
        },
        "support_resistance": {
            "EURUSD": {"support": 1.0920, "resistance": 1.1000},
            "GBPUSD": {"support": 1.2600, "resistance": 1.2680}
        },
        "last_updated": datetime.now().isoformat()
    }
    
    return {
        "status": "success", 
        "data": analysis,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/pairs")
async def get_currency_pairs():
    """Get available currency pairs"""
    pairs = [
        "EURUSD", "GBPUSD", "USDJPY", "USDCAD",
        "AUDUSD", "NZDUSD", "USDCHF", "EURJPY",
        "GBPJPY", "EURGBP", "AUDCAD", "CADCHF"
    ]
    return {
        "pairs": pairs,
        "count": len(pairs),
        "timestamp": datetime.now().isoformat()
    }

@app.get("/stats")
async def get_trading_stats():
    """Get trading statistics"""
    return {
        "daily_trades": 12,
        "weekly_profit": 247.50,
        "monthly_profit": 1156.75,
        "win_rate": 73.2,
        "avg_profit": 45.30,
        "max_drawdown": 2.1,
        "sharpe_ratio": 1.85,
        "timestamp": datetime.now().isoformat()
    }

@app.post("/signals/update")
async def update_signals(signals: List[dict]):
    """Update trading signals"""
    global trading_signals
    trading_signals = signals
    return {
        "status": "updated",
        "count": len(signals),
        "timestamp": datetime.now().isoformat()
    }

@app.get("/server/status")
async def get_server_status():
    """Get server and system status"""
    try:
        # Check main trading system
        main_system_status = "unknown"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get("http://localhost:8080/health", timeout=3) as response:
                    if response.status == 200:
                        main_system_status = "online"
        except:
            main_system_status = "offline"
        
        return {
            "fastapi_server": "online",
            "main_trading_system": main_system_status,
            "signals_count": len(trading_signals),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting server status: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving server status")

if __name__ == "__main__":
    logger.info("Starting GenX Simple FastAPI Server on port 8000...")
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info",
        reload=False
    )