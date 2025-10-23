"""
Spreadsheet Manager - Handle Excel and CSV output for trading signals
"""

import asyncio
import logging
import pandas as pd
import xlsxwriter
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional
import json

from .signal_types import TradingSignal

logger = logging.getLogger(__name__)

class SpreadsheetManager:
    """Manages Excel and CSV output for trading signals"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.output_dir = Path(config.get('output_directory', 'signal_output'))
        self.signals = []
        
        # Create output directory
        self.output_dir.mkdir(exist_ok=True)
        
        logger.info(f"Spreadsheet Manager initialized - Output: {self.output_dir}")
    
    async def initialize(self):
        """Initialize the spreadsheet manager"""
        try:
            # Create output directory if it doesn't exist
            self.output_dir.mkdir(parents=True, exist_ok=True)
            logger.info("✅ Spreadsheet Manager initialized")
        except Exception as e:
            logger.error(f"Failed to initialize spreadsheet manager: {e}")
            raise
    
    async def add_signal(self, signal: TradingSignal):
        """Add a new trading signal"""
        try:
            self.signals.append(signal)
            await self._update_output_files()
            logger.info(f"Signal added: {signal.symbol} {signal.signal_type.value}")
        except Exception as e:
            logger.error(f"Error adding signal: {e}")
    
    async def update_signals(self, signals: List[TradingSignal]):
        """Update with multiple signals"""
        try:
            self.signals.extend(signals)
            await self._update_output_files()
            logger.info(f"Updated with {len(signals)} signals")
        except Exception as e:
            logger.error(f"Error updating signals: {e}")
    
    async def _update_output_files(self):
        """Update all output files"""
        try:
            # Update Excel file
            await self._update_excel_file()
            
            # Update CSV files
            await self._update_csv_files()
            
            # Update JSON file
            await self._update_json_file()
            
        except Exception as e:
            logger.error(f"Error updating output files: {e}")
    
    async def _update_excel_file(self):
        """Update Excel dashboard"""
        try:
            excel_file = self.output_dir / self.config.get('excel_filename', 'genx_signals.xlsx')
            
            # Create workbook
            workbook = xlsxwriter.Workbook(str(excel_file))
            
            # Add formats
            header_format = workbook.add_format({
                'bold': True,
                'bg_color': '#4472C4',
                'font_color': 'white',
                'border': 1
            })
            
            signal_format = workbook.add_format({'border': 1})
            buy_format = workbook.add_format({'bg_color': '#C6EFCE', 'border': 1})
            sell_format = workbook.add_format({'bg_color': '#FFC7CE', 'border': 1})
            
            # Create signals worksheet
            signals_ws = workbook.add_worksheet('Trading Signals')
            
            # Headers
            headers = ['Timestamp', 'Symbol', 'Signal', 'Entry Price', 'Stop Loss', 
                      'Take Profit', 'Confidence', 'Timeframe', 'Risk/Reward']
            
            for col, header in enumerate(headers):
                signals_ws.write(0, col, header, header_format)
            
            # Add signals data
            for row, signal in enumerate(self.signals, 1):
                signals_ws.write(row, 0, signal.timestamp.strftime('%Y-%m-%d %H:%M:%S'))
                signals_ws.write(row, 1, signal.symbol)
                signals_ws.write(row, 2, signal.signal_type.value)
                signals_ws.write(row, 3, f"{signal.entry_price:.5f}")
                signals_ws.write(row, 4, f"{signal.stop_loss:.5f}")
                signals_ws.write(row, 5, f"{signal.take_profit:.5f}")
                signals_ws.write(row, 6, f"{signal.confidence:.3f}")
                signals_ws.write(row, 7, signal.timeframe)
                signals_ws.write(row, 8, f"{signal.risk_reward_ratio:.2f}")
                
                # Color coding for signal type
                if signal.signal_type.value == 'BUY':
                    for col in range(len(headers)):
                        signals_ws.write(row, col, None, buy_format)
                elif signal.signal_type.value == 'SELL':
                    for col in range(len(headers)):
                        signals_ws.write(row, col, None, sell_format)
            
            # Auto-fit columns
            for col in range(len(headers)):
                signals_ws.set_column(col, col, 15)
            
            # Create summary worksheet
            summary_ws = workbook.add_worksheet('Summary')
            
            # Summary statistics
            total_signals = len(self.signals)
            buy_signals = len([s for s in self.signals if s.signal_type.value == 'BUY'])
            sell_signals = len([s for s in self.signals if s.signal_type.value == 'SELL'])
            avg_confidence = sum(s.confidence for s in self.signals) / len(self.signals) if self.signals else 0
            
            summary_data = [
                ['Total Signals', total_signals],
                ['BUY Signals', buy_signals],
                ['SELL Signals', sell_signals],
                ['Average Confidence', f"{avg_confidence:.3f}"],
                ['Last Update', datetime.now().strftime('%Y-%m-%d %H:%M:%S')]
            ]
            
            for row, (label, value) in enumerate(summary_data):
                summary_ws.write(row, 0, label, header_format)
                summary_ws.write(row, 1, value)
            
            workbook.close()
            logger.info(f"Excel file updated: {excel_file}")
            
        except Exception as e:
            logger.error(f"Error updating Excel file: {e}")
    
    async def _update_csv_files(self):
        """Update CSV files for MT4/MT5"""
        try:
            # MT4 CSV
            mt4_file = self.output_dir / self.config.get('mt4_filename', 'MT4_Signals.csv')
            await self._create_mt4_csv(mt4_file)
            
            # MT5 CSV
            mt5_file = self.output_dir / self.config.get('mt5_filename', 'MT5_Signals.csv')
            await self._create_mt5_csv(mt5_file)
            
        except Exception as e:
            logger.error(f"Error updating CSV files: {e}")
    
    async def _create_mt4_csv(self, file_path: Path):
        """Create MT4 compatible CSV"""
        try:
            with open(file_path, 'w') as f:
                f.write("Symbol,Signal,Entry,StopLoss,TakeProfit,Confidence,Timeframe\n")
                
                for signal in self.signals:
                    f.write(f"{signal.symbol},{signal.signal_type.value},"
                           f"{signal.entry_price:.5f},{signal.stop_loss:.5f},"
                           f"{signal.take_profit:.5f},{signal.confidence:.3f},"
                           f"{signal.timeframe}\n")
            
            logger.info(f"MT4 CSV updated: {file_path}")
            
        except Exception as e:
            logger.error(f"Error creating MT4 CSV: {e}")
    
    async def _create_mt5_csv(self, file_path: Path):
        """Create MT5 compatible CSV"""
        try:
            with open(file_path, 'w') as f:
                f.write("Symbol,Signal,Entry,StopLoss,TakeProfit,Confidence,Timeframe,Timestamp\n")
                
                for signal in self.signals:
                    f.write(f"{signal.symbol},{signal.signal_type.value},"
                           f"{signal.entry_price:.5f},{signal.stop_loss:.5f},"
                           f"{signal.take_profit:.5f},{signal.confidence:.3f},"
                           f"{signal.timeframe},{signal.timestamp.isoformat()}\n")
            
            logger.info(f"MT5 CSV updated: {file_path}")
            
        except Exception as e:
            logger.error(f"Error creating MT5 CSV: {e}")
    
    async def _update_json_file(self):
        """Update JSON file for API access"""
        try:
            json_file = self.output_dir / 'genx_signals.json'
            
            signals_data = []
            for signal in self.signals:
                signals_data.append({
                    'symbol': signal.symbol,
                    'signal_type': signal.signal_type.value,
                    'entry_price': signal.entry_price,
                    'stop_loss': signal.stop_loss,
                    'take_profit': signal.take_profit,
                    'confidence': signal.confidence,
                    'timestamp': signal.timestamp.isoformat(),
                    'timeframe': signal.timeframe,
                    'risk_reward_ratio': signal.risk_reward_ratio
                })
            
            with open(json_file, 'w') as f:
                json.dump({
                    'signals': signals_data,
                    'total_count': len(signals_data),
                    'last_updated': datetime.now().isoformat()
                }, f, indent=2)
            
            logger.info(f"JSON file updated: {json_file}")
            
        except Exception as e:
            logger.error(f"Error updating JSON file: {e}")
