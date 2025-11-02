"""
Enhanced Live Signal Generator with Magic Key Integration
Real-time trading signals for Exness MT5 and FBS MT4 with encrypted authentication
"""

import MetaTrader5 as mt5
import asyncio
import json
import time
import logging
from datetime import datetime
from typing import Dict, List, Optional
import websockets
import httpx
import numpy as np
from magic_key_config import (
    magic_keys, 
    get_magic_number, 
    encrypt_trading_signal,
    get_trading_config,
    MAGIC_KEY_CONFIG
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('live_signal_generator_magic.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class MagicLiveSignalGenerator:
    def __init__(self):
        self.is_running = False
        self.mt5_connected = False
        self.magic_config = get_trading_config()
        
        # Trading configuration with magic keys
        self.exness_config = {
            "login": 1039533005,
            "password": "Leng12345@#$01",
            "server": "Exness-MT5real15",
            "magic_number": get_magic_number("exness"),
            "broker": "Exness",
            "platform": "MT5"
        }
        
        self.fbs_config = {
            "magic_number": get_magic_number("fbs"),
            "broker": "FBS", 
            "platform": "MT4"
        }
        
        # API endpoints
        self.api_base = "http://localhost:8000"
        self.websocket_url = "ws://localhost:8765"
        
        # Signal parameters with magic enhancement
        self.symbols = ["EURUSD", "GBPUSD", "USDJPY", "AUDUSD"]
        self.timeframes = [mt5.TIMEFRAME_M5, mt5.TIMEFRAME_M15]
        
    async def initialize_mt5(self):
        """Initialize MT5 connection with magic key authentication"""
        try:
            logger.info("Initializing MT5 with magic key authentication...")
            
            if not mt5.initialize():
                logger.error("Failed to initialize MT5")
                return False
                
            logger.info("Attempting login with Exness credentials...")
            login_result = mt5.login(
                login=self.exness_config["login"],
                password=self.exness_config["password"], 
                server=self.exness_config["server"]
            )
            
            if login_result:
                account_info = mt5.account_info()
                if account_info:
                    logger.info(f"MT5 connected successfully!")
                    logger.info(f"Account: {account_info.login}")
                    logger.info(f"Server: {account_info.server}")
                    logger.info(f"Balance: ${account_info.balance}")
                    logger.info(f"Magic Number: {self.exness_config['magic_number']}")
                    self.mt5_connected = True
                    return True
                    
            error = mt5.last_error()
            logger.error(f"MT5 login failed: {error}")
            return False
            
        except Exception as e:
            logger.error(f"MT5 initialization error: {e}")
            return False
            
    def get_market_data(self, symbol: str, timeframe: int, count: int = 100) -> Optional[np.ndarray]:
        """Get market data for analysis"""
        try:
            rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, count)
            if rates is not None and len(rates) > 0:
                return rates
            return None
        except Exception as e:
            logger.error(f"Failed to get market data for {symbol}: {e}")
            return None
            
    def calculate_indicators(self, rates: np.ndarray) -> Dict:
        """Calculate technical indicators with magic enhancement"""
        try:
            closes = rates['close']
            
            # Simple Moving Averages
            sma_20 = np.mean(closes[-20:])
            sma_50 = np.mean(closes[-50:])
            
            # RSI calculation
            deltas = np.diff(closes)
            gains = np.where(deltas > 0, deltas, 0)
            losses = np.where(deltas < 0, -deltas, 0)
            
            avg_gains = np.mean(gains[-14:])
            avg_losses = np.mean(losses[-14:])
            
            if avg_losses == 0:
                rsi = 100
            else:
                rs = avg_gains / avg_losses
                rsi = 100 - (100 / (1 + rs))
                
            # Magic-enhanced confidence calculation
            confidence = self.calculate_magic_confidence(sma_20, sma_50, rsi, closes[-1])
            
            return {
                "sma_20": sma_20,
                "sma_50": sma_50,
                "rsi": rsi,
                "current_price": closes[-1],
                "confidence": confidence,
                "magic_validated": confidence >= MAGIC_KEY_CONFIG["MIN_CONFIDENCE"]
            }
            
        except Exception as e:
            logger.error(f"Failed to calculate indicators: {e}")
            return {}
            
    def calculate_magic_confidence(self, sma_20: float, sma_50: float, rsi: float, current_price: float) -> float:
        """Calculate signal confidence with magic key enhancement"""
        try:
            # Base confidence from technical indicators
            base_confidence = 0.5
            
            # SMA trend confidence
            if sma_20 > sma_50:
                base_confidence += 0.2  # Uptrend
            else:
                base_confidence -= 0.1  # Downtrend
                
            # RSI momentum confidence
            if 30 <= rsi <= 70:
                base_confidence += 0.15  # Neutral RSI
            elif rsi < 30:
                base_confidence += 0.25  # Oversold
            elif rsi > 70:
                base_confidence += 0.25  # Overbought
                
            # Magic key validation bonus
            if self.magic_config["permissions"]["live_trading"]:
                base_confidence += 0.1
                
            return min(max(base_confidence, 0.0), 1.0)
            
        except Exception as e:
            logger.error(f"Failed to calculate magic confidence: {e}")
            return 0.5
            
    def generate_signal(self, symbol: str, indicators: Dict) -> Optional[Dict]:
        """Generate trading signal with magic key encryption"""
        try:
            if not indicators.get("magic_validated", False):
                return None
                
            signal_type = "HOLD"
            action = "WAIT"
            
            current_price = indicators["current_price"]
            sma_20 = indicators["sma_20"]
            sma_50 = indicators["sma_50"]
            rsi = indicators["rsi"]
            confidence = indicators["confidence"]
            
            # Signal generation logic
            if current_price > sma_20 > sma_50 and rsi < 70:
                signal_type = "BUY"
                action = "LONG"
            elif current_price < sma_20 < sma_50 and rsi > 30:
                signal_type = "SELL"
                action = "SHORT"
                
            if signal_type == "HOLD":
                return None
                
            # Create signal with magic key integration
            signal = {
                "symbol": symbol,
                "signal_type": signal_type,
                "action": action,
                "price": current_price,
                "confidence": confidence,
                "indicators": {
                    "sma_20": sma_20,
                    "sma_50": sma_50,
                    "rsi": rsi
                },
                "magic_number": get_magic_number("exness", "signal"),
                "broker": "Exness",
                "platform": "MT5",
                "timestamp": datetime.now().isoformat(),
                "risk_percent": MAGIC_KEY_CONFIG["MAX_RISK_PERCENT"],
                "stop_loss_pips": MAGIC_KEY_CONFIG["STOP_LOSS_PIPS"],
                "take_profit_pips": MAGIC_KEY_CONFIG["TAKE_PROFIT_PIPS"]
            }
            
            # Encrypt signal with magic key
            encrypted_signal = encrypt_trading_signal(signal)
            
            if encrypted_signal:
                logger.info(f"Generated encrypted {signal_type} signal for {symbol} (Confidence: {confidence:.2f})")
                return encrypted_signal
                
            return None
            
        except Exception as e:
            logger.error(f"Failed to generate signal for {symbol}: {e}")
            return None
            
    async def send_signal_to_api(self, signal: Dict):
        """Send encrypted signal to FastAPI server"""
        try:
            async with httpx.AsyncClient() as client:
                headers = {
                    "X-API-Key": self.magic_config["keys"]["api_key"],
                    "X-Trading-Key": self.magic_config["keys"]["trading_key"],
                    "Content-Type": "application/json"
                }
                
                response = await client.post(
                    f"{self.api_base}/signals/live",
                    json=signal,
                    headers=headers,
                    timeout=5.0
                )
                
                if response.status_code == 200:
                    logger.info(f"Signal sent successfully to API")
                else:
                    logger.warning(f"API response: {response.status_code}")
                    
        except Exception as e:
            logger.error(f"Failed to send signal to API: {e}")
            
    async def broadcast_signal(self, signal: Dict):
        """Broadcast encrypted signal via WebSocket"""
        try:
            async with websockets.connect(self.websocket_url) as websocket:
                await websocket.send(json.dumps(signal))
                logger.info(f"Signal broadcasted via WebSocket")
                
        except Exception as e:
            logger.error(f"Failed to broadcast signal: {e}")
            
    async def run_signal_generation(self):
        """Main signal generation loop with magic key integration"""
        logger.info("Starting Magic Live Signal Generation...")
        
        # Initialize MT5
        if not await self.initialize_mt5():
            logger.error("Failed to initialize MT5. Exiting...")
            return
            
        self.is_running = True
        signal_count = 0
        
        try:
            while self.is_running:
                logger.info(f"Signal generation cycle {signal_count + 1}...")
                
                for symbol in self.symbols:
                    try:
                        # Get market data
                        rates = self.get_market_data(symbol, mt5.TIMEFRAME_M5)
                        
                        if rates is not None:
                            # Calculate indicators
                            indicators = self.calculate_indicators(rates)
                            
                            if indicators:
                                # Generate signal
                                signal = self.generate_signal(symbol, indicators)
                                
                                if signal:
                                    # Send to API and broadcast
                                    await self.send_signal_to_api(signal)
                                    await self.broadcast_signal(signal)
                                    
                                    logger.info(f"Processed signal for {symbol}")
                                    
                    except Exception as e:
                        logger.error(f"Error processing {symbol}: {e}")
                        continue
                        
                signal_count += 1
                
                # Wait before next cycle
                await asyncio.sleep(30)  # 30-second intervals
                
        except KeyboardInterrupt:
            logger.info("Signal generation stopped by user")
        except Exception as e:
            logger.error(f"Signal generation error: {e}")
        finally:
            self.is_running = False
            if self.mt5_connected:
                mt5.shutdown()
                logger.info("MT5 connection closed")
                
    def stop(self):
        """Stop signal generation"""
        self.is_running = False
        logger.info("Stopping signal generation...")

# CLI interface
async def main():
    """Main entry point for magic signal generator"""
    generator = MagicLiveSignalGenerator()
    
    try:
        # Display magic configuration
        logger.info("GENX MAGIC LIVE SIGNAL GENERATOR")
        logger.info("=" * 50)
        logger.info(f"Magic Numbers: Exness={generator.exness_config['magic_number']}")
        logger.info(f"API Key: {generator.magic_config['keys']['api_key'][:16]}...")
        logger.info(f"Live Trading: {generator.magic_config['permissions']['live_trading']}")
        logger.info("=" * 50)
        
        # Start signal generation
        await generator.run_signal_generation()
        
    except Exception as e:
        logger.error(f"Main execution error: {e}")

if __name__ == "__main__":
    # Run the magic signal generator
    asyncio.run(main())