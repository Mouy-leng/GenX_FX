"""
Trading Engine - Core trading logic and signal generation
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any

from .config import config
from .data_sources.fxcm_provider import FXCMDataProvider, MockFXCMProvider
from .signal_types import SignalType, TradingSignal
from ai_models.ensemble_predictor import EnsemblePredictor
from .spreadsheet_manager import SpreadsheetManager

logger = logging.getLogger(__name__)

class TradingEngine:
    """Main trading engine for signal generation and execution"""
    
    def __init__(self):
        self.data_provider = None
        self.ensemble_predictor = None
        self.spreadsheet_manager = None
        self.is_running = False
        self.last_signal_time = {}
        
        logger.info("Trading Engine initialized")
    
    async def initialize(self):
        """Initialize all components"""
        try:
            # Initialize data provider
            if config.fxcm.use_mock:
                self.data_provider = MockFXCMProvider(config.fxcm.dict())
            else:
                self.data_provider = FXCMDataProvider(config.fxcm.dict())
            
            await self.data_provider.connect()
            logger.info("✅ Data provider connected")
            
            # Initialize AI predictor
            self.ensemble_predictor = EnsemblePredictor(config.ai_models.dict())
            await self.ensemble_predictor.initialize()
            logger.info("✅ AI predictor initialized")
            
            # Initialize spreadsheet manager
            self.spreadsheet_manager = SpreadsheetManager(config.spreadsheet.dict())
            await self.spreadsheet_manager.initialize()
            logger.info("✅ Spreadsheet manager initialized")
            
        except Exception as e:
            logger.error(f"Failed to initialize trading engine: {e}")
            raise
    
    async def start(self):
        """Start the trading engine"""
        if not self.data_provider or not self.ensemble_predictor:
            await self.initialize()
        
        self.is_running = True
        logger.info("🚀 Trading Engine started")
        
        # Start signal generation loop
        asyncio.create_task(self._signal_generation_loop())
    
    async def stop(self):
        """Stop the trading engine"""
        self.is_running = False
        
        if self.data_provider:
            await self.data_provider.disconnect()
        
        logger.info("🛑 Trading Engine stopped")
    
    async def _signal_generation_loop(self):
        """Main signal generation loop"""
        while self.is_running:
            try:
                await self._generate_signals_for_symbols()
                await asyncio.sleep(config.trading.signal_generation_interval)
            except Exception as e:
                logger.error(f"Error in signal generation loop: {e}")
                await asyncio.sleep(60)  # Wait before retrying
    
    async def _generate_signals_for_symbols(self):
        """Generate signals for all configured symbols"""
        symbols = config.trading.symbols
        
        for symbol in symbols:
            try:
                # Check if enough time has passed since last signal
                if self._should_generate_signal(symbol):
                    signal = await self._generate_signal_for_symbol(symbol)
                    if signal:
                        await self._process_signal(signal)
                        self.last_signal_time[symbol] = datetime.now()
            except Exception as e:
                logger.error(f"Error generating signal for {symbol}: {e}")
    
    def _should_generate_signal(self, symbol: str) -> bool:
        """Check if enough time has passed since last signal"""
        if symbol not in self.last_signal_time:
            return True
        
        time_since_last = datetime.now() - self.last_signal_time[symbol]
        return time_since_last.total_seconds() >= config.trading.signal_generation_interval
    
    async def _generate_signal_for_symbol(self, symbol: str) -> Optional[TradingSignal]:
        """Generate a trading signal for a specific symbol"""
        try:
            # Get historical data
            data = await self.data_provider.get_historical_data(
                symbol, 
                config.trading.primary_timeframe, 
                100
            )
            
            if len(data) < 50:
                logger.warning(f"Insufficient data for {symbol}")
                return None
            
            # Get AI prediction
            prediction = await self.ensemble_predictor.predict(symbol, data)
            
            if prediction['confidence'] < config.ai_models.confidence_threshold:
                logger.info(f"Low confidence for {symbol}: {prediction['confidence']:.3f}")
                return None
            
            # Generate signal
            signal = self._create_signal(symbol, prediction, data)
            return signal
            
        except Exception as e:
            logger.error(f"Error generating signal for {symbol}: {e}")
            return None
    
    def _create_signal(self, symbol: str, prediction: Dict[str, Any], data: List[Dict]) -> TradingSignal:
        """Create a trading signal from prediction and data"""
        current_price = data[-1]['close']
        confidence = prediction['confidence']
        direction = prediction['direction']
        
        # Calculate stop loss and take profit
        atr = self._calculate_atr(data, 14)
        stop_distance = atr * config.risk_management.stop_loss_multiplier
        take_profit_distance = stop_distance * config.risk_management.take_profit_multiplier
        
        if direction > 0:  # Buy signal
            signal_type = SignalType.BUY
            entry_price = current_price
            stop_loss = entry_price - stop_distance
            take_profit = entry_price + take_profit_distance
        else:  # Sell signal
            signal_type = SignalType.SELL
            entry_price = current_price
            stop_loss = entry_price + stop_distance
            take_profit = entry_price - take_profit_distance
        
        return TradingSignal(
            symbol=symbol,
            signal_type=signal_type,
            entry_price=entry_price,
            stop_loss=stop_loss,
            take_profit=take_profit,
            confidence=confidence,
            timestamp=datetime.now(),
            timeframe=config.trading.primary_timeframe,
            risk_reward_ratio=config.risk_management.take_profit_multiplier
        )
    
    def _calculate_atr(self, data: List[Dict], period: int = 14) -> float:
        """Calculate Average True Range"""
        if len(data) < period:
            return 0.001  # Default small value
        
        true_ranges = []
        for i in range(1, len(data)):
            high = data[i]['high']
            low = data[i]['low']
            prev_close = data[i-1]['close']
            
            tr = max(
                high - low,
                abs(high - prev_close),
                abs(low - prev_close)
            )
            true_ranges.append(tr)
        
        return sum(true_ranges[-period:]) / period
    
    async def _process_signal(self, signal: TradingSignal):
        """Process and save a trading signal"""
        try:
            # Save to spreadsheet
            await self.spreadsheet_manager.add_signal(signal)
            
            logger.info(f"📊 Signal generated: {signal.symbol} {signal.signal_type.value} "
                       f"@ {signal.entry_price:.5f} (confidence: {signal.confidence:.3f})")
            
        except Exception as e:
            logger.error(f"Error processing signal: {e}")
    
    async def force_signal_generation(self, symbols: List[str]) -> List[TradingSignal]:
        """Force signal generation for specific symbols (for testing)"""
        signals = []
        
        # Initialize components if not already done
        if not self.data_provider:
            if config.fxcm.use_mock:
                self.data_provider = MockFXCMProvider(config.fxcm.dict())
            else:
                self.data_provider = FXCMDataProvider(config.fxcm.dict())
            await self.data_provider.connect()
        
        if not self.ensemble_predictor:
            self.ensemble_predictor = EnsemblePredictor(config.ai_models.dict())
            await self.ensemble_predictor.initialize()
        
        for symbol in symbols:
            try:
                signal = await self._generate_signal_for_symbol(symbol)
                if signal:
                    signals.append(signal)
            except Exception as e:
                logger.error(f"Error generating signal for {symbol}: {e}")
        
        return signals
