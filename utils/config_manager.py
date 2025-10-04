"""
Configuration Manager for GenX FX Trading System
Handles configuration loading and management
"""

import json
import logging
import os
from typing import Dict, Any
from pathlib import Path

logger = logging.getLogger(__name__)

class ConfigManager:
    """Configuration manager for the trading system"""
    
    def __init__(self, config_path: str):
        self.config_path = config_path
        self.config = {}
        self.load_config()
        
    def load_config(self):
        """Load configuration from file and override with environment variables."""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r') as f:
                    self.config = json.load(f)
                logger.info(f"Configuration loaded from {self.config_path}")
            else:
                logger.warning(f"Config file {self.config_path} not found, using defaults")
                self.config = self.get_default_config()

            # Override with environment variables for secrets
            logger.info("Overriding configuration with environment variables for secrets...")
            if 'fxcm' in self.config:
                self.config['fxcm']['access_token'] = os.getenv('FXCM_API_TOKEN', self.config['fxcm'].get('access_token'))

            if 'notifications' in self.config:
                if 'slack' in self.config['notifications']:
                    self.config['notifications']['slack']['webhook_url'] = os.getenv('SLACK_WEBHOOK_URL', self.config['notifications']['slack'].get('webhook_url'))
                if 'telegram' in self.config['notifications']:
                    self.config['notifications']['telegram']['bot_token'] = os.getenv('TELEGRAM_BOT_TOKEN', self.config['notifications']['telegram'].get('bot_token'))
                    self.config['notifications']['telegram']['chat_id'] = os.getenv('TELEGRAM_CHAT_ID', self.config['notifications']['telegram'].get('chat_id'))
                if 'email' in self.config['notifications']:
                    self.config['notifications']['email']['smtp_server'] = os.getenv('SMTP_SERVER', self.config['notifications']['email'].get('smtp_server'))
                    self.config['notifications']['email']['smtp_port'] = int(os.getenv('SMTP_PORT', self.config['notifications']['email'].get('smtp_port', 587)))
                    self.config['notifications']['email']['username'] = os.getenv('SMTP_USERNAME', self.config['notifications']['email'].get('username'))
                    self.config['notifications']['email']['password'] = os.getenv('SMTP_PASSWORD', self.config['notifications']['email'].get('password'))
                    recipients_str = os.getenv('EMAIL_RECIPIENTS')
                    if recipients_str:
                        self.config['notifications']['email']['recipients'] = [e.strip() for e in recipients_str.split(',')]
                    elif 'recipients' not in self.config['notifications']['email']:
                        self.config['notifications']['email']['recipients'] = []

        except Exception as e:
            logger.error(f"Error loading config: {e}")
            self.config = self.get_default_config()
            
    def get_config(self) -> Dict[str, Any]:
        """Get the current configuration"""
        return self.config
        
    def get_default_config(self) -> Dict[str, Any]:
        """Get default configuration"""
        return {
            "broker": "exness",
            "symbols": ["EURUSD", "GBPUSD", "USDJPY"],
            "timeframes": ["H1", "H4", "D1"],
            "risk_percentage": 2.0,
            "max_positions": 5,
            "stop_loss_pips": 50,
            "take_profit_pips": 100
        }