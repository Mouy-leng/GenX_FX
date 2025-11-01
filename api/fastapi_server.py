#!/usr/bin/env python3
"""
GenX FastAPI Server - Advanced Trading API
Provides REST endpoints for trading signals, portfolio management, and market analysis
"""

import asyncio
import logging
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
import uvicorn
from pathlib import Path
import sys
import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import aiohttp

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from core.config import config
from utils.logger_setup import setup_logging

# Setup logging
setup_logging()
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

# Security
security = HTTPBearer()

# Global state
trading_signals = []
portfolio_status = {
    "balance": 10000.0,
    "equity": 10000.0,
    "margin": 0.0,
    "free_margin": 10000.0,
    "margin_level": 0.0,
    "active_trades": 0,
    "total_trades": 0,
    "profit": 0.0,
    "last_updated": datetime.now().isoformat()
}

market_analysis = {
    "trends": {},
    "volatility": {},
    "support_resistance": {},
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
        "uptime": "operational"
    }

@app.get("/signals")
async def get_trading_signals():
    """Get current trading signals"""
    try:
        # Try to get signals from main trading system
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get("http://localhost:8080/health") as response:
                    if response.status == 200:
                        # Main system is running, get real signals
                        return {
                            "signals": trading_signals,
                            "count": len(trading_signals),
                            "last_updated": datetime.now().isoformat(),
                            "source": "live_system"
                        }
            except:
                pass
        
        # Return mock signals if main system not available
        mock_signals = [
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
            }
        ]
        
        return {
            "signals": mock_signals,
            "count": len(mock_signals),
            "last_updated": datetime.now().isoformat(),
            "source": "mock_data"
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
    return {
        "status": "success", 
        "data": market_analysis,
        "timestamp": datetime.now().isoformat()
    }

@app.post("/signals/update")
async def update_signals(signals: List[dict]):
    """Update trading signals (internal use)"""
    global trading_signals
    trading_signals = signals
    return {
        "status": "updated",
        "count": len(signals),
        "timestamp": datetime.now().isoformat()
    }

@app.post("/portfolio/update")
async def update_portfolio(data: dict):
    """Update portfolio status (internal use)"""
    global portfolio_status
    portfolio_status.update(data)
    portfolio_status["last_updated"] = datetime.now().isoformat()
    return {
        "status": "updated",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/pairs")
async def get_currency_pairs():
    """Get available currency pairs"""
    pairs = [
        "EURUSD", "GBPUSD", "USDJPY", "USDCAD",
        "AUDUSD", "NZDUSD", "USDCHF", "EURJPY",
        "GBPJPY", "EURGBP", "AUDCAD", "CADCHF",
        "EURAUD", "EURCHF", "GBPAUD", "GBPCAD"
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
        "weekly_profit": 156.50,
        "monthly_profit": 623.75,
        "win_rate": 73.2,
        "avg_profit": 45.30,
        "max_drawdown": 2.1,
        "sharpe_ratio": 1.85,
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    logger.info("Starting GenX FastAPI Server on port 8000...")
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info",
        reload=False
    )