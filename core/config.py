"""
Configuration management for GenX FX Trading System
"""

import os
import yaml
from pathlib import Path
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field

class TradingConfig(BaseModel):
    """Trading configuration"""
    symbols: list = Field(default=['EURUSD', 'GBPUSD', 'USDJPY', 'AUDUSD', 'USDCAD'])
    timeframes: list = Field(default=['H1', 'H4', 'D1'])
    primary_timeframe: str = Field(default='H1')
    signal_generation_interval: int = Field(default=300)  # seconds

class AIModelsConfig(BaseModel):
    """AI Models configuration"""
    ensemble_size: int = Field(default=5)
    confidence_threshold: float = Field(default=0.75)
    retrain_interval: int = Field(default=86400)  # seconds

class RiskManagementConfig(BaseModel):
    """Risk management configuration"""
    max_risk_per_trade: float = Field(default=0.02)  # 2%
    max_daily_risk: float = Field(default=0.05)  # 5%
    stop_loss_multiplier: float = Field(default=1.5)
    take_profit_multiplier: float = Field(default=2.0)

class FXCMConfig(BaseModel):
    """FXCM configuration"""
    use_mock: bool = Field(default=True)
    username: Optional[str] = None
    password: Optional[str] = None
    environment: str = Field(default='demo')

class SpreadsheetConfig(BaseModel):
    """Spreadsheet configuration"""
    output_directory: str = Field(default='signal_output')
    excel_filename: str = Field(default='genx_signals.xlsx')
    mt4_filename: str = Field(default='MT4_Signals.csv')
    mt5_filename: str = Field(default='MT5_Signals.csv')

class SystemConfig(BaseModel):
    """System configuration"""
    name: str = Field(default='GenX FX Trading System')
    version: str = Field(default='1.0.0')
    log_level: str = Field(default='INFO')

class Config:
    """Main configuration class"""
    
    def __init__(self, config_file: str = None):
        self.config_file = config_file or 'config.yaml'
        self._config_data = self._load_config()
        
        # Initialize configuration sections
        self.trading = TradingConfig(**self._config_data.get('trading', {}))
        self.ai_models = AIModelsConfig(**self._config_data.get('ai_models', {}))
        self.risk_management = RiskManagementConfig(**self._config_data.get('risk_management', {}))
        self.fxcm = FXCMConfig(**self._config_data.get('fxcm', {}))
        self.spreadsheet = SpreadsheetConfig(**self._config_data.get('spreadsheet', {}))
        self.system = SystemConfig(**self._config_data.get('system', {}))
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file or environment"""
        config_data = {}
        
        # Try to load from config file
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    config_data = yaml.safe_load(f) or {}
            except Exception as e:
                print(f"Warning: Could not load config file {self.config_file}: {e}")
        
        # Override with environment variables
        config_data.update({
            'trading': {
                'symbols': os.getenv('TRADING_SYMBOLS', config_data.get('trading', {}).get('symbols', ['EURUSD', 'GBPUSD'])).split(',') if os.getenv('TRADING_SYMBOLS') else config_data.get('trading', {}).get('symbols', ['EURUSD', 'GBPUSD']),
                'timeframes': os.getenv('TRADING_TIMEFRAMES', config_data.get('trading', {}).get('timeframes', ['H1', 'H4'])).split(',') if os.getenv('TRADING_TIMEFRAMES') else config_data.get('trading', {}).get('timeframes', ['H1', 'H4']),
                'primary_timeframe': os.getenv('PRIMARY_TIMEFRAME', config_data.get('trading', {}).get('primary_timeframe', 'H1')),
                'signal_generation_interval': int(os.getenv('SIGNAL_INTERVAL', config_data.get('trading', {}).get('signal_generation_interval', 300)))
            },
            'fxcm': {
                'use_mock': os.getenv('FXCM_USE_MOCK', 'true').lower() == 'true',
                'username': os.getenv('FXCM_USERNAME', config_data.get('fxcm', {}).get('username')),
                'password': os.getenv('FXCM_PASSWORD', config_data.get('fxcm', {}).get('password')),
                'environment': os.getenv('FXCM_ENVIRONMENT', config_data.get('fxcm', {}).get('environment', 'demo'))
            },
            'ai_models': {
                'ensemble_size': int(os.getenv('AI_ENSEMBLE_SIZE', config_data.get('ai_models', {}).get('ensemble_size', 5))),
                'confidence_threshold': float(os.getenv('AI_CONFIDENCE_THRESHOLD', config_data.get('ai_models', {}).get('confidence_threshold', 0.75))),
                'retrain_interval': int(os.getenv('AI_RETRAIN_INTERVAL', config_data.get('ai_models', {}).get('retrain_interval', 86400)))
            },
            'risk_management': {
                'max_risk_per_trade': float(os.getenv('MAX_RISK_PER_TRADE', config_data.get('risk_management', {}).get('max_risk_per_trade', 0.02))),
                'max_daily_risk': float(os.getenv('MAX_DAILY_RISK', config_data.get('risk_management', {}).get('max_daily_risk', 0.05))),
                'stop_loss_multiplier': float(os.getenv('STOP_LOSS_MULTIPLIER', config_data.get('risk_management', {}).get('stop_loss_multiplier', 1.5))),
                'take_profit_multiplier': float(os.getenv('TAKE_PROFIT_MULTIPLIER', config_data.get('risk_management', {}).get('take_profit_multiplier', 2.0)))
            },
            'spreadsheet': {
                'output_directory': os.getenv('OUTPUT_DIRECTORY', config_data.get('spreadsheet', {}).get('output_directory', 'signal_output')),
                'excel_filename': os.getenv('EXCEL_FILENAME', config_data.get('spreadsheet', {}).get('excel_filename', 'genx_signals.xlsx')),
                'mt4_filename': os.getenv('MT4_FILENAME', config_data.get('spreadsheet', {}).get('mt4_filename', 'MT4_Signals.csv')),
                'mt5_filename': os.getenv('MT5_FILENAME', config_data.get('spreadsheet', {}).get('mt5_filename', 'MT5_Signals.csv'))
            },
            'system': {
                'name': os.getenv('SYSTEM_NAME', config_data.get('system', {}).get('name', 'GenX FX Trading System')),
                'version': os.getenv('SYSTEM_VERSION', config_data.get('system', {}).get('version', '1.0.0')),
                'log_level': os.getenv('LOG_LEVEL', config_data.get('system', {}).get('log_level', 'INFO'))
            }
        })
        
        return config_data
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by key (dot notation)"""
        keys = key.split('.')
        value = self._config_data
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    def save(self, filename: str = None) -> None:
        """Save current configuration to file"""
        filename = filename or self.config_file
        
        # Convert to dict for YAML serialization
        config_dict = {
            'trading': self.trading.dict(),
            'ai_models': self.ai_models.dict(),
            'risk_management': self.risk_management.dict(),
            'fxcm': self.fxcm.dict(),
            'spreadsheet': self.spreadsheet.dict(),
            'system': self.system.dict()
        }
        
        with open(filename, 'w') as f:
            yaml.dump(config_dict, f, default_flow_style=False)

# Global config instance
config = Config()
