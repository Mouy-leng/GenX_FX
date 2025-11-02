"""
🚀 LIVE MT5/MT4 Real-Time Signal Generator
Generates live trading signals for Exness MT5 and FBS MT4 accounts with real money
"""

import MetaTrader5 as mt5
import time
import json
import asyncio
import aiohttp
from datetime import datetime
import logging
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('live_trading_signals.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Account configurations
EXNESS_MT5_CONFIG = {
    "account": 1039533005,
    "password": "Leng12345@#$01",
    "server": "Exness-MT5real15",
    "platform": "MT5",
    "broker": "Exness"
}

FBS_MT4_CONFIG = {
    "account": None,  # Will be set when available
    "password": "Leng12345@#$01", 
    "server": "FBS-Real",  # Standard FBS server
    "platform": "MT4",
    "broker": "FBS"
}

# Trading pairs to monitor
TRADING_PAIRS = [
    "EURUSD", "GBPUSD", "USDJPY", "USDCHF", "AUDUSD",
    "NZDUSD", "USDCAD", "EURJPY", "GBPJPY", "XAUUSD"
]

class LiveSignalGenerator:
    def __init__(self):
        self.mt5_connected = False
        self.mt4_connected = False
        self.running = False
        self.signals = []
        
    async def connect_mt5(self):
        """Connect to Exness MT5 real account"""
        logger.info("🔗 Connecting to Exness MT5 live account...")
        
        if not mt5.initialize():
            logger.error("❌ MT5 initialization failed")
            return False
            
        # Login to Exness account
        if not mt5.login(
            login=EXNESS_MT5_CONFIG["account"],
            password=EXNESS_MT5_CONFIG["password"], 
            server=EXNESS_MT5_CONFIG["server"]
        ):
            logger.error(f"❌ Failed to login to Exness MT5: {mt5.last_error()}")
            return False
            
        # Verify connection
        account_info = mt5.account_info()
        if account_info is None:
            logger.error("❌ Failed to get account info")
            return False
            
        logger.info(f"✅ Connected to Exness MT5!")
        logger.info(f"   Account: {account_info.login}")
        logger.info(f"   Balance: ${account_info.balance}")
        logger.info(f"   Equity: ${account_info.equity}")
        logger.info(f"   Server: {account_info.server}")
        
        self.mt5_connected = True
        return True
        
    def get_live_market_data(self, symbol):
        """Get real-time market data for symbol"""
        if not self.mt5_connected:
            return None
            
        # Get current tick
        tick = mt5.symbol_info_tick(symbol)
        if tick is None:
            return None
            
        # Get recent price data
        rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M1, 0, 100)
        if rates is None or len(rates) == 0:
            return None
            
        return {
            "symbol": symbol,
            "bid": tick.bid,
            "ask": tick.ask,
            "last": tick.last,
            "volume": tick.volume,
            "time": datetime.fromtimestamp(tick.time),
            "rates": rates[-20:]  # Last 20 minutes
        }
        
    def analyze_signal(self, market_data):
        """Analyze market data and generate trading signal"""
        if not market_data or len(market_data["rates"]) < 10:
            return None
            
        symbol = market_data["symbol"]
        rates = market_data["rates"]
        current_price = market_data["bid"]
        
        # Simple moving average strategy
        prices = [rate[4] for rate in rates]  # Close prices
        sma_short = sum(prices[-5:]) / 5  # 5-period SMA
        sma_long = sum(prices[-20:]) / 20  # 20-period SMA
        
        # RSI calculation (simplified)
        changes = [prices[i] - prices[i-1] for i in range(1, len(prices))]
        gains = [change if change > 0 else 0 for change in changes]
        losses = [-change if change < 0 else 0 for change in changes]
        
        avg_gain = sum(gains[-14:]) / 14 if len(gains) >= 14 else sum(gains) / len(gains)
        avg_loss = sum(losses[-14:]) / 14 if len(losses) >= 14 else sum(losses) / len(losses)
        
        rs = avg_gain / avg_loss if avg_loss != 0 else 100
        rsi = 100 - (100 / (1 + rs))
        
        # Generate signal
        signal = None
        confidence = 0.5
        
        if sma_short > sma_long and rsi < 70:
            signal = "BUY"
            confidence = min(0.95, 0.6 + (sma_short - sma_long) / current_price * 100)
        elif sma_short < sma_long and rsi > 30:
            signal = "SELL"
            confidence = min(0.95, 0.6 + (sma_long - sma_short) / current_price * 100)
            
        if signal and confidence > 0.65:  # Only high-confidence signals
            # Calculate entry, SL, and TP
            if symbol == "USDJPY":
                pip_size = 0.01
            else:
                pip_size = 0.0001
                
            if signal == "BUY":
                entry = market_data["ask"]
                stop_loss = entry - (30 * pip_size)
                take_profit = entry + (50 * pip_size)
            else:
                entry = market_data["bid"]
                stop_loss = entry + (30 * pip_size)
                take_profit = entry - (50 * pip_size)
                
            return {
                "symbol": symbol,
                "signal": signal,
                "confidence": round(confidence, 3),
                "entry_price": round(entry, 5 if symbol != "USDJPY" else 3),
                "stop_loss": round(stop_loss, 5 if symbol != "USDJPY" else 3),
                "take_profit": round(take_profit, 5 if symbol != "USDJPY" else 3),
                "timestamp": datetime.now().isoformat(),
                "broker": "Exness",
                "account": EXNESS_MT5_CONFIG["account"],
                "rsi": round(rsi, 2),
                "sma_short": round(sma_short, 5),
                "sma_long": round(sma_long, 5)
            }
            
        return None
        
    async def send_signal_to_api(self, signal):
        """Send generated signal to FastAPI server"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    "http://localhost:8000/signals/live",
                    json=signal,
                    timeout=aiohttp.ClientTimeout(total=5)
                ) as response:
                    if response.status == 200:
                        logger.info(f"✅ Signal sent to API: {signal['symbol']} {signal['signal']}")
                    else:
                        logger.warning(f"⚠️ API response: {response.status}")
        except Exception as e:
            logger.error(f"❌ Failed to send signal to API: {e}")
            
    async def generate_live_signals(self):
        """Main loop for generating live trading signals"""
        logger.info("🚀 Starting live signal generation...")
        self.running = True
        
        while self.running:
            try:
                active_signals = []
                
                for symbol in TRADING_PAIRS:
                    # Get live market data
                    market_data = self.get_live_market_data(symbol)
                    if market_data is None:
                        continue
                        
                    # Analyze and generate signal
                    signal = self.analyze_signal(market_data)
                    if signal:
                        active_signals.append(signal)
                        logger.info(f"📈 NEW SIGNAL: {signal['symbol']} {signal['signal']} @ {signal['entry_price']} (Confidence: {signal['confidence']*100:.1f}%)")
                        
                        # Send to API
                        await self.send_signal_to_api(signal)
                        
                # Update signals list
                self.signals = active_signals
                
                # Save signals to file
                with open('live_signals.json', 'w') as f:
                    json.dump({
                        "timestamp": datetime.now().isoformat(),
                        "signals": active_signals,
                        "account": EXNESS_MT5_CONFIG["account"],
                        "broker": "Exness"
                    }, f, indent=2)
                    
                logger.info(f"📊 Generated {len(active_signals)} live signals")
                
                # Wait before next analysis
                await asyncio.sleep(30)  # Check every 30 seconds
                
            except Exception as e:
                logger.error(f"❌ Error in signal generation: {e}")
                await asyncio.sleep(60)  # Wait longer on error
                
    def stop(self):
        """Stop signal generation"""
        logger.info("🛑 Stopping live signal generation...")
        self.running = False
        if self.mt5_connected:
            mt5.shutdown()
            
async def main():
    """Main function to start live signal generation"""
    logger.info("🚀 GenX Live Signal Generator Starting...")
    logger.info("💰 REAL MONEY TRADING MODE ACTIVATED")
    
    generator = LiveSignalGenerator()
    
    # Connect to MT5
    if not await generator.connect_mt5():
        logger.error("❌ Failed to connect to MT5. Exiting...")
        return
        
    try:
        # Start live signal generation
        await generator.generate_live_signals()
    except KeyboardInterrupt:
        logger.info("⏹️ Signal generation stopped by user")
    finally:
        generator.stop()
        
if __name__ == "__main__":
    asyncio.run(main())