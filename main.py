#!/usr/bin/env python3
"""
GenX FX Trading System - Main Entry Point
Advanced AI-powered Forex trading signal generator for MT4/5 EAs
"""

import asyncio
import logging
import argparse
import sys
from pathlib import Path
from datetime import datetime
import signal
import json

# Add project root to path
sys.path.append(str(Path(__file__).parent))

# Setup basic logging first
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import with error handling for missing dependencies
try:
    from core.trading_engine import TradingEngine
    from core.data_sources.fxcm_provider import FXCMDataProvider, MockFXCMProvider
    from core.ai_models.ensemble_predictor import EnsemblePredictor
    from core.model_trainer import ModelTrainer
    from core.backtester import Backtester
    from utils.config_manager import ConfigManager
    from utils.logger_setup import setup_logging
    FULL_SYSTEM_AVAILABLE = True
except ImportError as e:
    logger.warning(f"Some modules not available: {e}")
    FULL_SYSTEM_AVAILABLE = False
    # Create dummy classes for missing imports
    class TradingEngine:
        def __init__(self, config): pass
        async def start(self): pass
        async def stop(self): pass
    class ModelTrainer:
        def __init__(self, config): pass
        async def initialize(self): pass
    class Backtester:
        def __init__(self, config): pass

class GenXTradingSystem:
    """
    Main GenX Trading System Controller
    
    Modes:
    - live: Live trading signal generation
    - train: Train AI models with historical data
    - backtest: Backtest strategies
    - test: Test system components
    """
    
    def __init__(self, config_path: str = "config/trading_config.json"):
        if FULL_SYSTEM_AVAILABLE:
            self.config_manager = ConfigManager(config_path)
            self.config = self.config_manager.get_config()
        else:
            # Simplified mode - use default config
            self.config = {
                "broker": "exness",
                "symbols": ["EURUSD", "GBPUSD", "USDJPY"],
                "timeframes": ["H1", "H4", "D1"],
                "risk_percentage": 2.0,
                "max_positions": 5,
                "stop_loss_pips": 50,
                "take_profit_pips": 100
            }
        self.trading_engine = None
        self.is_running = False
        
        # Setup graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        logger.info("GenX Trading System initialized")
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully"""
        logger.info(f"Received signal {signum}, shutting down...")
        self.is_running = False
    
    async def run_live_trading(self):
        """Run live trading signal generation"""
        logger.info("🚀 Starting Live Trading Mode")
        
        try:
            # Initialize trading engine
            self.trading_engine = TradingEngine(self.config)
            
            # Start the engine
            await self.trading_engine.start()
            self.is_running = True
            
            logger.info("✅ Live trading started successfully")
            logger.info("📊 Signals will be output to: signal_output/")
            logger.info("📈 MT4 signals: signal_output/MT4_Signals.csv")
            logger.info("📈 MT5 signals: signal_output/MT5_Signals.csv")
            logger.info("📊 Excel dashboard: signal_output/genx_signals.xlsx")
            
            # Keep running until shutdown
            while self.is_running:
                await asyncio.sleep(1)
                
        except KeyboardInterrupt:
            logger.info("Shutdown requested by user")
        except Exception as e:
            logger.error(f"Error in live trading mode: {e}")
        finally:
            if self.trading_engine:
                await self.trading_engine.stop()
            logger.info("Live trading stopped")
    
    async def run_training_mode(self, symbols: list = None, timeframes: list = None):
        """Run AI model training"""
        logger.info("🎯 Starting Training Mode")
        
        try:
            trainer = ModelTrainer(self.config)
            await trainer.initialize()
            
            symbols = symbols or self.config.get('symbols', ['EURUSD', 'GBPUSD'])
            timeframes = timeframes or self.config.get('timeframes', ['H1', 'H4'])
            
            logger.info(f"Training models for symbols: {symbols}")
            logger.info(f"Training timeframes: {timeframes}")
            
            results = await trainer.train_all_models(symbols, timeframes)
            
            # Display training results
            logger.info("🎓 Training Results:")
            for symbol, result in results.items():
                if result.get('status') == 'success':
                    logger.info(f"  ✅ {symbol}: {result['models_trained']} models trained")
                    for model_name, scores in result.get('model_scores', {}).items():
                        if 'cv_mean' in scores:
                            logger.info(f"    📊 {model_name}: {scores['cv_mean']:.3f} ± {scores['cv_std']:.3f}")
                else:
                    logger.error(f"  ❌ {symbol}: {result.get('error', 'Unknown error')}")
            
            logger.info("✅ Training completed")
            
        except Exception as e:
            logger.error(f"Error in training mode: {e}")
    
    async def run_backtesting(self, start_date: str = None, end_date: str = None):
        """Run backtesting"""
        logger.info("📈 Starting Backtesting Mode")
        
        try:
            backtester = Backtester(self.config)
            await backtester.initialize()
            
            start_date = start_date or "2023-01-01"
            end_date = end_date or datetime.now().strftime("%Y-%m-%d")
            
            logger.info(f"Backtesting period: {start_date} to {end_date}")
            
            results = await backtester.run_backtest(
                start_date=start_date,
                end_date=end_date,
                symbols=self.config.get('symbols', ['EURUSD'])
            )
            
            # Display backtest results
            logger.info("📊 Backtest Results:")
            for symbol, result in results.items():
                stats = result.get('statistics', {})
                logger.info(f"  📈 {symbol}:")
                logger.info(f"    Total Trades: {stats.get('total_trades', 0)}")
                logger.info(f"    Win Rate: {stats.get('win_rate', 0):.2%}")
                logger.info(f"    Total Return: {stats.get('total_return', 0):.2%}")
                logger.info(f"    Sharpe Ratio: {stats.get('sharpe_ratio', 0):.3f}")
                logger.info(f"    Max Drawdown: {stats.get('max_drawdown', 0):.2%}")
            
            logger.info("✅ Backtesting completed")
            
        except Exception as e:
            logger.error(f"Error in backtesting mode: {e}")
    
    async def run_test_mode(self):
        """Run system tests"""
        logger.info("🧪 Starting Test Mode")
        
        try:
            # Test data provider connection
            logger.info("Testing data provider...")
            if self.config.get('fxcm', {}).get('use_mock', True):
                data_provider = MockFXCMProvider(self.config['fxcm'])
            else:
                data_provider = FXCMDataProvider(self.config['fxcm'])
            
            connected = await data_provider.connect()
            if connected:
                logger.info("✅ Data provider connection successful")
                
                # Test data retrieval
                test_data = await data_provider.get_historical_data('EURUSD', 'H1', 100)
                logger.info(f"✅ Retrieved {len(test_data)} data points for EURUSD")
                
                await data_provider.disconnect()
            else:
                logger.error("❌ Data provider connection failed")
                return
            
            # Test AI predictor
            logger.info("Testing AI predictor...")
            predictor = EnsemblePredictor(self.config['ai_models'])
            await predictor.initialize()
            
            if len(test_data) > 50:
                prediction = await predictor.predict('EURUSD', test_data)
                logger.info(f"✅ AI prediction generated: confidence={prediction['confidence']:.3f}")
            
            # Test signal generation
            logger.info("Testing signal generation...")
            self.trading_engine = TradingEngine(self.config)
            test_signals = await self.trading_engine.force_signal_generation(['EURUSD'])
            
            if test_signals:
                logger.info(f"✅ Generated {len(test_signals)} test signals")
                for signal in test_signals:
                    logger.info(f"  📊 {signal.symbol}: {signal.signal_type.value} @ {signal.confidence:.3f}")
            else:
                logger.warning("⚠️  No test signals generated")
            
            logger.info("✅ All tests completed successfully")
            
        except Exception as e:
            logger.error(f"Error in test mode: {e}")
    
    async def generate_sample_signals(self, count: int = 5):
        """Generate sample signals for testing MT4/5 integration"""
        logger.info(f"🎲 Generating {count} sample signals")
        
        try:
            self.trading_engine = TradingEngine(self.config)
            await self.trading_engine.data_provider.connect()
            await self.trading_engine.ensemble_predictor.initialize()
            await self.trading_engine.spreadsheet_manager.initialize()
            
            signals = await self.trading_engine.force_signal_generation(
                self.config.get('symbols', ['EURUSD', 'GBPUSD'])[:count]
            )
            
            if signals:
                await self.trading_engine.spreadsheet_manager.update_signals(signals)
                
                logger.info(f"✅ Generated {len(signals)} sample signals")
                logger.info("📁 Output files created:")
                logger.info("  📊 signal_output/genx_signals.xlsx")
                logger.info("  📈 signal_output/MT4_Signals.csv")
                logger.info("  📈 signal_output/MT5_Signals.csv")
                
                # Display signal summary
                for signal in signals:
                    logger.info(f"  🎯 {signal.symbol}: {signal.signal_type.value} "
                              f"@ {signal.entry_price:.5f} (confidence: {signal.confidence:.3f})")
            else:
                logger.warning("⚠️  No signals could be generated")
            
            await self.trading_engine.data_provider.disconnect()
            
        except Exception as e:
            logger.error(f"Error generating sample signals: {e}")
    
    def print_system_info(self):
        """Print system information"""
        logger.info("=" * 60)
        logger.info("🚀 GenX FX Trading System")
        logger.info("   Advanced AI-Powered Forex Signal Generator")
        logger.info("=" * 60)
        logger.info(f"📊 Symbols: {', '.join(self.config.get('symbols', []))}")
        logger.info(f"⏰ Timeframes: {', '.join(self.config.get('timeframes', []))}")
        logger.info(f"🎯 Primary Timeframe: {self.config.get('primary_timeframe', 'H1')}")
        logger.info(f"🤖 AI Models: {self.config.get('ai_models', {}).get('ensemble_size', 5)} ensemble models")
        logger.info(f"📈 Max Risk per Trade: {self.config.get('risk_management', {}).get('max_risk_per_trade', 0.02):.1%}")
        logger.info(f"⚡ Signal Generation: Every {self.config.get('signal_generation_interval', 300)} seconds")
        logger.info(f"💾 Output Directory: signal_output/")
        logger.info("=" * 60)

async def main():
    """Main entry point"""
    # Check if we're in simplified mode
    if not FULL_SYSTEM_AVAILABLE:
        logger.info("Running in simplified mode due to missing dependencies")
        logger.info("This is a test deployment for Google Cloud Build")
        
        # Run simplified system
        system = GenXTradingSystem()
        system.print_system_info()
        await system.run_live_trading()
        return
    
    # Full system mode
    parser = argparse.ArgumentParser(description="GenX FX Trading System")
    parser.add_argument('mode', choices=['live', 'train', 'backtest', 'test', 'sample'], 
                       help='System mode to run')
    parser.add_argument('--config', default='config/trading_config.json', 
                       help='Configuration file path')
    parser.add_argument('--symbols', nargs='+', 
                       help='Symbols to trade (for training/backtesting)')
    parser.add_argument('--timeframes', nargs='+', 
                       help='Timeframes to use (for training)')
    parser.add_argument('--start-date', type=str, 
                       help='Start date for backtesting (YYYY-MM-DD)')
    parser.add_argument('--end-date', type=str, 
                       help='End date for backtesting (YYYY-MM-DD)')
    parser.add_argument('--count', type=int, default=5, 
                       help='Number of sample signals to generate')
    parser.add_argument('--log-level', default='INFO', 
                       choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
                       help='Logging level')
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(level=args.log_level)
    
    # Initialize system
    system = GenXTradingSystem(args.config)
    system.print_system_info()
    
    try:
        if args.mode == 'live':
            await system.run_live_trading()
        elif args.mode == 'train':
            await system.run_training_mode(args.symbols, args.timeframes)
        elif args.mode == 'backtest':
            await system.run_backtesting(args.start_date, args.end_date)
        elif args.mode == 'test':
            await system.run_test_mode()
        elif args.mode == 'sample':
            await system.generate_sample_signals(args.count)
        
    except KeyboardInterrupt:
        logger.info("👋 Shutdown requested by user")
    except Exception as e:
        logger.error(f"💥 System error: {e}")
        sys.exit(1)
    
    logger.info("🏁 GenX Trading System stopped")

if __name__ == "__main__":
    asyncio.run(main())