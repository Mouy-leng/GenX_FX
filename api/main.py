from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import os
from datetime import datetime
app = FastAPI(
    title="GenX-FX Trading Platform API",
    description="Trading platform with ML-powered predictions",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "GenX-FX Trading Platform API",
        "version": "1.0.0",
        "status": "running",
        "github": "Mouy-leng",
        "repository": "https://github.com/Mouy-leng/GenX_FX.git"
    }

@app.get("/health")
async def health_check():
    try:
        # Test database connection
        conn = sqlite3.connect("genxdb_fx.db")
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        conn.close()
        
        return {
            "status": "healthy",
            "database": "connected",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

@app.get("/api/v1/health")
async def api_health_check():
    return {
        "status": "healthy",
        "services": {
            "ml_service": "active",
            "data_service": "active"
        },
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/v1/predictions")
async def get_predictions():
    return {
        "predictions": [],
        "status": "ready",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/trading-pairs")
async def get_trading_pairs():
    try:
        conn = sqlite3.connect("genxdb_fx.db")
        cursor = conn.cursor()
        cursor.execute("SELECT symbol, base_currency, quote_currency FROM trading_pairs WHERE is_active = 1")
        pairs = cursor.fetchall()
        conn.close()
        
        return {
            "trading_pairs": [
                {
                    "symbol": pair[0],
                    "base_currency": pair[1],
                    "quote_currency": pair[2]
                }
                for pair in pairs
            ]
        }
    except Exception as e:
        return {"error": str(e)}

@app.get("/users")
async def get_users():
    try:
        conn = sqlite3.connect("genxdb_fx.db")
        cursor = conn.cursor()
        cursor.execute("SELECT username, email, is_active FROM users")
        users = cursor.fetchall()
        conn.close()
        
        return {
            "users": [
                {
                    "username": user[0],
                    "email": user[1],
                    "is_active": bool(user[2])
                }
                for user in users
            ]
        }
    except Exception as e:
        return {"error": str(e)}

@app.get("/mt5-info")
async def get_mt5_info():
    return {
        "login": "279023502",
        "server": "Exness-MT5Trial8",
        "status": "configured"
    }

from fastapi.responses import StreamingResponse
import pandas as pd
import io
from datetime import datetime
import random

@app.get("/api/signals")
async def get_live_signals_csv():
    """
    Generates simulated live trading signals and returns them in CSV format.
    """
    # Simulate live data by adding a timestamp and randomizing values slightly
    now = datetime.utcnow()
    signals = [
        {
            "timestamp": now.isoformat(),
            "symbol": "EURUSD",
            "entry": round(1.0850 + random.uniform(-0.0005, 0.0005), 5),
            "target": round(1.0900 + random.uniform(-0.0005, 0.0005), 5),
            "stop_loss": round(1.0800 + random.uniform(-0.0005, 0.0005), 5),
            "confidence": round(random.uniform(0.65, 0.85), 2)
        },
        {
            "timestamp": now.isoformat(),
            "symbol": "GBPUSD",
            "entry": round(1.2700 + random.uniform(-0.0005, 0.0005), 5),
            "target": round(1.2750 + random.uniform(-0.0005, 0.0005), 5),
            "stop_loss": round(1.2650 + random.uniform(-0.0005, 0.0005), 5),
            "confidence": round(random.uniform(0.60, 0.80), 2)
        }
    ]

    df = pd.DataFrame(signals)
    stream = io.StringIO()
    # Reorder columns to have symbol first
    df = df[['timestamp', 'symbol', 'entry', 'target', 'stop_loss', 'confidence']]
    df.to_csv(stream, index=False)

    response = StreamingResponse(iter([stream.getvalue()]),
                                 media_type="text/csv")

    response.headers["Content-Disposition"] = "attachment; filename=signals.csv"

    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
