#!/bin/bash

# Simple Final Setup Script for GenX-FX Trading Platform
# Works without virtual environment, uses system Python

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 Setting up GenX-FX Trading Platform (Simple Final Setup)${NC}"

# === GitHub Configuration ===
GITHUB_USERNAME="genxdbxfx1"
GITHUB_REPOSITORY="https://github.com/genxdbxfx1-ctrl/GenX_db_FX-.git"

# === App Credentials ===
MT5_LOGIN="279023502"
MT5_SERVER="Exness-MT5Trial8"
MT5_PASSWORD="Leng12345@#$01"

# === API Keys (placeholders) ===
GEMINI_API_KEY="your_gemini_api_key_here"
ALPHAVANTAGE_API_KEY="your_alpha_api_key_here"
NEWS_API_KEY="your_newsapi_key_here"
NEWSDATA_API_KEY="your_newsdata_key_here"

# === Backend Config ===
ENV="development"
PORT="8080"
DEBUG="true"
DATABASE_URL="sqlite:///./genxdb_fx.db"

# === Security ===
SECRET_KEY=$(openssl rand -hex 32)

# Create environment file
echo -e "${YELLOW}Creating environment file...${NC}"
cat > .env << EOF
# === GitHub ===
GITHUB_USERNAME=$GITHUB_USERNAME
GITHUB_REPOSITORY=$GITHUB_REPOSITORY

# === App Credentials ===
MT5_LOGIN=$MT5_LOGIN
MT5_SERVER=$MT5_SERVER
MT5_PASSWORD=$MT5_PASSWORD

# === API Keys ===
GEMINI_API_KEY=$GEMINI_API_KEY
ALPHAVANTAGE_API_KEY=$ALPHAVANTAGE_API_KEY
NEWS_API_KEY=$NEWS_API_KEY
NEWSDATA_API_KEY=$NEWSDATA_API_KEY

# === Backend Config ===
ENV=$ENV
PORT=$PORT
DEBUG=$DEBUG
DATABASE_URL=$DATABASE_URL

# === Security ===
SECRET_KEY=$SECRET_KEY

# === Heroku ===
HEROKU_TOKEN=HRKU-AAdx7OW4VQYFLAyNbE0_2jze4VpJbaTHK8sxEv1XDN3w_____ws77zaRyPXX
EOF

echo -e "${GREEN}✅ Environment file created${NC}"

# Install Python dependencies using pipx or system pip
echo -e "${YELLOW}Installing Python dependencies...${NC}"
pip3 install --break-system-packages fastapi uvicorn sqlalchemy

# Create database setup script
echo -e "${YELLOW}Creating database setup script...${NC}"
cat > setup_database.py << EOF
#!/usr/bin/env python3
"""
Database Setup Script for GenX-FX Trading Platform
This script initializes the SQLite database with the required tables and schema.
"""

import os
import sys
import logging
import sqlite3
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_database_schema():
    """Create the database schema for the trading platform"""
    
    db_path = "genxdb_fx.db"
    logger.info(f"Creating database: {db_path}")
    
    try:
        # Create database connection
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Create tables
        create_tables(cursor)
        
        # Insert initial data
        insert_initial_data(cursor)
        
        # Commit changes
        conn.commit()
        conn.close()
        
        logger.info("✅ Database schema setup complete!")
        
    except Exception as e:
        logger.error(f"❌ Database error: {e}")
        sys.exit(1)

def create_tables(cursor):
    """Create all required tables"""
    
    # SQL statements to create tables
    tables_sql = [
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,
        
        """
        CREATE TABLE IF NOT EXISTS trading_accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            account_name TEXT NOT NULL,
            broker TEXT NOT NULL,
            account_number TEXT,
            balance REAL DEFAULT 0.00,
            currency TEXT DEFAULT 'USD',
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
        """,
        
        """
        CREATE TABLE IF NOT EXISTS trading_pairs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT UNIQUE NOT NULL,
            base_currency TEXT NOT NULL,
            quote_currency TEXT NOT NULL,
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,
        
        """
        CREATE TABLE IF NOT EXISTS market_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT NOT NULL,
            timestamp TIMESTAMP NOT NULL,
            open_price REAL,
            high_price REAL,
            low_price REAL,
            close_price REAL,
            volume REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,
        
        """
        CREATE TABLE IF NOT EXISTS trading_signals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT NOT NULL,
            signal_type TEXT NOT NULL,
            confidence REAL,
            price REAL,
            timestamp TIMESTAMP NOT NULL,
            model_version TEXT,
            features TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,
        
        """
        CREATE TABLE IF NOT EXISTS trades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            account_id INTEGER,
            symbol TEXT NOT NULL,
            trade_type TEXT NOT NULL,
            quantity REAL NOT NULL,
            price REAL NOT NULL,
            total_amount REAL NOT NULL,
            status TEXT DEFAULT 'PENDING',
            signal_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            executed_at TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (account_id) REFERENCES trading_accounts(id),
            FOREIGN KEY (signal_id) REFERENCES trading_signals(id)
        )
        """,
        
        """
        CREATE TABLE IF NOT EXISTS model_predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT NOT NULL,
            model_name TEXT NOT NULL,
            prediction_type TEXT NOT NULL,
            prediction_value REAL,
            confidence REAL,
            timestamp TIMESTAMP NOT NULL,
            features TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,
        
        """
        CREATE TABLE IF NOT EXISTS system_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            level TEXT NOT NULL,
            message TEXT NOT NULL,
            module TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    ]
    
    for i, sql in enumerate(tables_sql, 1):
        try:
            cursor.execute(sql)
            logger.info(f"✅ Created table {i}/{len(tables_sql)}")
        except Exception as e:
            logger.warning(f"⚠️  Table creation warning (might already exist): {e}")

def insert_initial_data(cursor):
    """Insert initial data into the database"""
    
    initial_data_sql = [
        """
        INSERT OR IGNORE INTO users (username, email, password_hash) VALUES
        ('admin', 'admin@genxdbxfx1.com', 'hashed_password_placeholder')
        """,
        
        """
        INSERT OR IGNORE INTO trading_pairs (symbol, base_currency, quote_currency) VALUES
        ('EUR/USD', 'EUR', 'USD'),
        ('GBP/USD', 'GBP', 'USD'),
        ('USD/JPY', 'USD', 'JPY'),
        ('USD/CHF', 'USD', 'CHF'),
        ('AUD/USD', 'AUD', 'USD'),
        ('USD/CAD', 'USD', 'CAD'),
        ('NZD/USD', 'NZD', 'USD'),
        ('EUR/GBP', 'EUR', 'GBP'),
        ('EUR/JPY', 'EUR', 'JPY'),
        ('GBP/JPY', 'GBP', 'JPY')
        """
    ]
    
    for i, sql in enumerate(initial_data_sql, 1):
        try:
            cursor.execute(sql)
            logger.info(f"✅ Inserted initial data {i}/{len(initial_data_sql)}")
        except Exception as e:
            logger.warning(f"⚠️  Data insertion warning: {e}")

if __name__ == "__main__":
    logger.info("🚀 Setting up GenX-FX Trading Platform Database...")
    create_database_schema()
    logger.info("✅ Database setup complete!")
EOF

echo -e "${GREEN}✅ Database setup script created${NC}"

# Setup database
echo -e "${YELLOW}Setting up database...${NC}"
python3 setup_database.py

# Create startup script
echo -e "${YELLOW}Creating startup script...${NC}"
cat > start_trading_platform.sh << EOF
#!/bin/bash

# Startup Script for GenX-FX Trading Platform

echo "🚀 Starting GenX-FX Trading Platform..."

# Check if database exists
if [ ! -f "genxdb_fx.db" ]; then
    echo "📊 Setting up database..."
    python3 setup_database.py
fi

# Start the API server
echo "🌐 Starting API server on port 8080..."
python3 -m uvicorn api.main:app --host 0.0.0.0 --port 8080 --reload
EOF

chmod +x start_trading_platform.sh

# Create a simple test API
echo -e "${YELLOW}Creating simple test API...${NC}"
mkdir -p api
cat > api/main.py << EOF
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
        "github": "genxdbxfx1",
        "repository": "https://github.com/genxdbxfx1-ctrl/GenX_db_FX-.git"
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
EOF

# Create deployment info file
cat > simple_final_deployment_info.txt << EOF
GenX-FX Trading Platform Simple Final Deployment
===============================================

Deployment Date: $(date)
GitHub Repository: $GITHUB_REPOSITORY

Services:
- SQLite Database: genxdb_fx.db
- API Backend: localhost:8080

Credentials:
- Database: SQLite (genxdb_fx.db)
- Admin User: admin@genxdbxfx1.com

MT5 Credentials:
- Login: $MT5_LOGIN
- Server: $MT5_SERVER
- Password: $MT5_PASSWORD

Useful Commands:
- Start platform: ./start_trading_platform.sh
- View database: sqlite3 genxdb_fx.db
- Test API: curl http://localhost:8080/health
- API docs: http://localhost:8080/docs

API Endpoints:
- Health Check: http://localhost:8080/health
- API Documentation: http://localhost:8080/docs
- Trading Pairs: http://localhost:8080/trading-pairs
- Users: http://localhost:8080/users
- MT5 Info: http://localhost:8080/mt5-info

Database Tables:
- users: User accounts
- trading_accounts: Trading account information
- trading_pairs: Available trading pairs
- market_data: Historical market data
- trading_signals: Trading signals from models
- trades: Executed trades
- model_predictions: ML model predictions
- system_logs: System logs

Next Steps:
1. Start the platform: ./start_trading_platform.sh
2. Access API docs: http://localhost:8080/docs
3. Configure API keys in .env file
4. Set up MT5 connection
EOF

echo -e "${GREEN}✅ Simple final setup complete!${NC}"
echo -e "${GREEN}📝 Deployment information saved to simple_final_deployment_info.txt${NC}"
echo -e "${BLUE}🗄️  Database created: genxdb_fx.db${NC}"
echo -e "${YELLOW}🚀 Start the platform with: ./start_trading_platform.sh${NC}"
echo -e "${BLUE}📚 API documentation will be available at: http://localhost:8080/docs${NC}"