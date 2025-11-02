#!/usr/bin/env python3
"""
Mock Trading Engine for GenX Platform
"""

import asyncio
import logging
from datetime import datetime
import random

logger = logging.getLogger(__name__)

class TradingEngine:
    def __init__(self):
        self.is_running = False
        
    async def start(self):
        """Start the trading engine"""
        logger.info("Starting GenX Trading Engine...")
        self.is_running = True
        
        # Start signal generation loop
        asyncio.create_task(self._signal_generation_loop())
        
    async def stop(self):
        """Stop the trading engine"""
        logger.info("Stopping GenX Trading Engine...")
        self.is_running = False
        
    async def _signal_generation_loop(self):
        """Main signal generation loop"""
        while self.is_running:
            try:
                # Generate mock trading signals
                await self._generate_signals()
                await asyncio.sleep(60)  # Generate signals every minute
            except Exception as e:
                logger.error(f"Error in signal generation: {e}")
                await asyncio.sleep(10)
    
    async def _generate_signals(self):
        """Generate mock trading signals"""
        symbols = ['EURUSD', 'GBPUSD', 'USDJPY']
        
        for symbol in symbols:
            signal_type = random.choice(['BUY', 'SELL', 'HOLD'])
            confidence = random.uniform(0.6, 0.95)
            price = random.uniform(1.0500, 1.1200) if symbol == 'EURUSD' else random.uniform(1.2000, 1.3000)
            
            logger.info(f"[SIGNAL] {symbol}: {signal_type} @ {price:.5f} (confidence: {confidence:.3f})")
            
            # Save to CSV (mock)
            await self._save_signal_to_csv(symbol, signal_type, price, confidence)
    
    async def _save_signal_to_csv(self, symbol, signal_type, price, confidence):
        """Save signal to CSV file"""
        import csv
        from pathlib import Path
        
        # Create output directory
        output_dir = Path('signal_output')
        output_dir.mkdir(exist_ok=True)
        
        # Save to MT4 signals file
        mt4_file = output_dir / 'MT4_Signals.csv'
        with open(mt4_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                symbol,
                signal_type,
                price,
                confidence
            ])
        
        logger.info(f"Signal saved to {mt4_file}")
    
    async def force_signal_generation(self, symbols):
        """Force generate signals for testing"""
        signals = []
        for symbol in symbols:
            signal = {
                'symbol': symbol,
                'signal_type': random.choice(['BUY', 'SELL']),
                'entry_price': random.uniform(1.0500, 1.1200),
                'confidence': random.uniform(0.7, 0.95)
            }
            signals.append(type('Signal', (), signal)())
        return signals