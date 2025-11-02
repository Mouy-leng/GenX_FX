"""
Enhanced FastAPI Trading Server with Magic Key Integration
Real-time signal API with encrypted authentication and multi-broker support
"""

from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import Dict, List, Optional, Any
import json
import logging
from datetime import datetime
import uvicorn
import asyncio
import os
import sys

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import magic key system
try:
    from core.magic_key_config import (
        magic_keys,
        validate_trading_permission,
        verify_trading_signal,
        get_trading_config,
        MAGIC_KEY_CONFIG
    )
    MAGIC_KEYS_AVAILABLE = True
except ImportError as e:
    MAGIC_KEYS_AVAILABLE = False
    print(f"Magic key system not available: {e}")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI with magic key integration
app = FastAPI(
    title="GenX Magic Trading API",
    description="Enhanced Trading Signal API with Magic Key Authentication",
    version="2.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Pydantic models
class TradingSignal(BaseModel):
    symbol: str
    signal_type: str  # BUY, SELL, HOLD
    confidence: float
    price: float
    timestamp: str
    broker: Optional[str] = "Exness"
    magic_number: Optional[int] = None

class EncryptedSignal(BaseModel):
    data: Dict[str, Any]
    signature: str
    timestamp: str
    key_type: str

class APIResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Dict] = None
    timestamp: str = datetime.now().isoformat()

# Global storage for signals
live_signals = []
signal_history = []

# Authentication dependency
async def verify_api_key(x_api_key: Optional[str] = Header(None)):
    """Verify API key using magic key system"""
    if not MAGIC_KEYS_AVAILABLE:
        logger.warning("Magic key system not available, allowing request")
        return True
        
    if not x_api_key:
        raise HTTPException(status_code=401, detail="API key required")
        
    if not validate_trading_permission(x_api_key):
        raise HTTPException(status_code=403, detail="Invalid API key")
        
    return True

# Root endpoint with magic key info
@app.get("/", response_model=APIResponse)
async def root():
    """Root endpoint with system information"""
    if MAGIC_KEYS_AVAILABLE:
        magic_config = get_trading_config()
        return APIResponse(
            success=True,
            message="GenX Magic Trading API - Live and Ready",
            data={
                "service": "GenX Magic Trading API",
                "version": "2.0.0",
                "magic_keys_enabled": True,
                "live_trading": magic_config["permissions"]["live_trading"],
                "endpoints": [
                    "/health",
                    "/signals/live",
                    "/signals/history", 
                    "/config/magic",
                    "/trading/status"
                ]
            }
        )
    else:
        return APIResponse(
            success=True,
            message="GenX Trading API - Basic Mode",
            data={
                "service": "GenX Trading API", 
                "version": "2.0.0",
                "magic_keys_enabled": False
            }
        )

# Health check
@app.get("/health", response_model=APIResponse)
async def health_check():
    """Health check endpoint"""
    return APIResponse(
        success=True,
        message="Service healthy",
        data={"status": "healthy", "magic_keys": MAGIC_KEYS_AVAILABLE}
    )

# Magic key configuration endpoint
@app.get("/config/magic", response_model=APIResponse)
async def get_magic_config(authenticated: bool = Depends(verify_api_key)):
    """Get magic key configuration (authenticated)"""
    if not MAGIC_KEYS_AVAILABLE:
        raise HTTPException(status_code=503, detail="Magic key system not available")
        
    config = get_trading_config()
    
    # Remove sensitive keys for API response
    safe_config = {
        "magic_numbers": {k: v for k, v in config["magic_numbers"].items() if isinstance(v, int)},
        "permissions": config["permissions"],
        "expires_at": config["expires_at"],
        "created_at": config["created_at"]
    }
    
    return APIResponse(
        success=True,
        message="Magic configuration retrieved",
        data=safe_config
    )

# Live signals endpoint
@app.post("/signals/live", response_model=APIResponse)
async def receive_live_signal(
    signal: EncryptedSignal,
    background_tasks: BackgroundTasks,
    authenticated: bool = Depends(verify_api_key)
):
    """Receive and process encrypted live trading signal"""
    try:
        if MAGIC_KEYS_AVAILABLE:
            # Verify signal integrity
            if not verify_trading_signal(signal.dict()):
                raise HTTPException(status_code=400, detail="Invalid signal signature")
                
        # Store signal
        live_signals.append(signal.dict())
        signal_history.append(signal.dict())
        
        # Keep only last 100 live signals
        if len(live_signals) > 100:
            live_signals.pop(0)
            
        # Keep only last 1000 historical signals
        if len(signal_history) > 1000:
            signal_history.pop(0)
            
        logger.info(f"Received live signal for {signal.data.get('symbol', 'unknown')}")
        
        return APIResponse(
            success=True,
            message="Live signal received and processed",
            data={"signal_id": len(signal_history), "symbol": signal.data.get("symbol")}
        )
        
    except Exception as e:
        logger.error(f"Error processing live signal: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Get live signals
@app.get("/signals/live", response_model=APIResponse)
async def get_live_signals(
    limit: int = 10,
    symbol: Optional[str] = None,
    authenticated: bool = Depends(verify_api_key)
):
    """Get recent live signals"""
    try:
        signals = live_signals[-limit:] if not symbol else [
            s for s in live_signals[-limit:] 
            if s.get("data", {}).get("symbol") == symbol
        ]
        
        return APIResponse(
            success=True,
            message=f"Retrieved {len(signals)} live signals",
            data={"signals": signals, "total": len(signals)}
        )
        
    except Exception as e:
        logger.error(f"Error retrieving live signals: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Signal history
@app.get("/signals/history", response_model=APIResponse)
async def get_signal_history(
    limit: int = 50,
    symbol: Optional[str] = None,
    authenticated: bool = Depends(verify_api_key)
):
    """Get signal history"""
    try:
        signals = signal_history[-limit:] if not symbol else [
            s for s in signal_history[-limit:]
            if s.get("data", {}).get("symbol") == symbol
        ]
        
        return APIResponse(
            success=True,
            message=f"Retrieved {len(signals)} historical signals",
            data={"signals": signals, "total": len(signals)}
        )
        
    except Exception as e:
        logger.error(f"Error retrieving signal history: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Trading status
@app.get("/trading/status", response_model=APIResponse)
async def get_trading_status(authenticated: bool = Depends(verify_api_key)):
    """Get current trading status"""
    try:
        status = {
            "live_signals_count": len(live_signals),
            "total_signals_count": len(signal_history),
            "magic_keys_enabled": MAGIC_KEYS_AVAILABLE,
            "last_signal_time": signal_history[-1]["timestamp"] if signal_history else None,
            "server_time": datetime.now().isoformat()
        }
        
        if MAGIC_KEYS_AVAILABLE:
            config = get_trading_config()
            status.update({
                "live_trading_enabled": config["permissions"]["live_trading"],
                "api_access_enabled": config["permissions"]["api_access"],
                "magic_numbers": {k: v for k, v in config["magic_numbers"].items() if isinstance(v, int)}
            })
            
        return APIResponse(
            success=True,
            message="Trading status retrieved",
            data=status
        )
        
    except Exception as e:
        logger.error(f"Error retrieving trading status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Clear signals (admin only)
@app.delete("/signals/clear", response_model=APIResponse)
async def clear_signals(
    signal_type: str = "live",  # "live", "history", "all"
    authenticated: bool = Depends(verify_api_key)
):
    """Clear signals (admin endpoint)"""
    try:
        if signal_type == "live":
            live_signals.clear()
            cleared = "live signals"
        elif signal_type == "history":
            signal_history.clear()
            cleared = "signal history"
        elif signal_type == "all":
            live_signals.clear()
            signal_history.clear()
            cleared = "all signals"
        else:
            raise HTTPException(status_code=400, detail="Invalid signal_type")
            
        return APIResponse(
            success=True,
            message=f"Cleared {cleared}",
            data={"cleared": signal_type}
        )
        
    except Exception as e:
        logger.error(f"Error clearing signals: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Startup event
@app.on_event("startup")
async def startup_event():
    """Startup event handler"""
    logger.info("GenX Magic Trading API starting up...")
    
    if MAGIC_KEYS_AVAILABLE:
        logger.info("Magic key system initialized")
        config = get_trading_config()
        logger.info(f"Live trading enabled: {config['permissions']['live_trading']}")
    else:
        logger.warning("Running in basic mode without magic keys")
        
    logger.info("GenX Magic Trading API ready!")

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown event handler"""
    logger.info("GenX Magic Trading API shutting down...")

if __name__ == "__main__":
    # Display magic configuration if available
    if MAGIC_KEYS_AVAILABLE:
        print("\n" + "="*60)
        print("GENX MAGIC TRADING API")
        print("="*60)
        from core.magic_key_config import display_magic_keys
        display_magic_keys()
        print("\nStarting Enhanced API Server with Magic Key Integration...")
        print("="*60)
    else:
        print("Starting GenX Trading API in Basic Mode...")
        
    # Start the server
    uvicorn.run(
        "magic_fastapi_server:app",
        host="0.0.0.0", 
        port=8000,
        reload=False,
        log_level="info"
    )