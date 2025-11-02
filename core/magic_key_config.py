"""
Magic Key Configuration System for GenX Trading Platform
Provides enhanced authentication, signal encryption, and advanced trading features
"""

import os
import json
import hashlib
import secrets
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import logging

# Configure logging
logger = logging.getLogger(__name__)

class MagicKeyManager:
    def __init__(self):
        self.config_file = "magic_key_config.json"
        self.keys = {}
        self.load_config()
        
    def load_config(self):
        """Load magic key configuration"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    self.keys = json.load(f)
                logger.info("Magic key configuration loaded")
            else:
                self.generate_default_keys()
                logger.info("Generated new magic key configuration")
        except Exception as e:
            logger.error(f"Failed to load magic key config: {e}")
            self.generate_default_keys()
            
    def generate_default_keys(self):
        """Generate default magic keys for the system"""
        self.keys = {
            "master_key": self.generate_secure_key(),
            "api_key": self.generate_secure_key(),
            "signal_key": self.generate_secure_key(),
            "trading_key": self.generate_secure_key(),
            "exness_key": self.generate_secure_key(),
            "fbs_key": self.generate_secure_key(),
            "created_at": datetime.now().isoformat(),
            "expires_at": (datetime.now() + timedelta(days=365)).isoformat(),
            "permissions": {
                "live_trading": True,
                "signal_generation": True,
                "api_access": True,
                "admin_access": True
            }
        }
        self.save_config()
        
    def generate_secure_key(self, length=32):
        """Generate a cryptographically secure key"""
        return secrets.token_hex(length)
        
    def save_config(self):
        """Save magic key configuration"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.keys, f, indent=2)
            logger.info("Magic key configuration saved")
        except Exception as e:
            logger.error(f"Failed to save magic key config: {e}")
            
    def validate_key(self, key_type: str, provided_key: str) -> bool:
        """Validate a provided key against stored keys"""
        if key_type not in self.keys:
            return False
            
        stored_key = self.keys.get(key_type)
        return secrets.compare_digest(stored_key, provided_key)
        
    def get_key(self, key_type: str) -> Optional[str]:
        """Get a specific key by type"""
        return self.keys.get(key_type)
        
    def encrypt_signal(self, signal_data: Dict, key_type: str = "signal_key") -> str:
        """Encrypt signal data using magic key"""
        try:
            key = self.get_key(key_type)
            if not key:
                return None
                
            # Simple encryption for signals
            signal_json = json.dumps(signal_data)
            encrypted = hashlib.sha256((signal_json + key).encode()).hexdigest()
            
            return {
                "data": signal_data,
                "signature": encrypted,
                "timestamp": datetime.now().isoformat(),
                "key_type": key_type
            }
        except Exception as e:
            logger.error(f"Failed to encrypt signal: {e}")
            return None
            
    def verify_signal(self, encrypted_signal: Dict, key_type: str = "signal_key") -> bool:
        """Verify encrypted signal integrity"""
        try:
            key = self.get_key(key_type)
            if not key:
                return False
                
            signal_json = json.dumps(encrypted_signal["data"])
            expected_signature = hashlib.sha256((signal_json + key).encode()).hexdigest()
            
            return secrets.compare_digest(encrypted_signal["signature"], expected_signature)
        except Exception as e:
            logger.error(f"Failed to verify signal: {e}")
            return False

# Global magic key manager instance
magic_keys = MagicKeyManager()

# Magic Key Configuration for Trading
MAGIC_KEY_CONFIG = {
    "EXNESS_MAGIC": 123456789,  # Unique identifier for Exness trades
    "FBS_MAGIC": 987654321,     # Unique identifier for FBS trades
    "SIGNAL_MAGIC": 555666777,  # Magic number for signal trades
    "AUTO_MAGIC": 111222333,    # Magic number for automated trades
    "MANUAL_MAGIC": 444555666,  # Magic number for manual trades
    
    # Advanced configurations
    "MAX_RISK_PERCENT": 2.0,    # Maximum risk per trade
    "MAX_TRADES": 10,           # Maximum concurrent trades
    "MIN_CONFIDENCE": 0.75,     # Minimum signal confidence
    "STOP_LOSS_PIPS": 30,       # Default stop loss in pips
    "TAKE_PROFIT_PIPS": 50,     # Default take profit in pips
    
    # API Keys
    "API_SECRET": magic_keys.get_key("api_key"),
    "MASTER_SECRET": magic_keys.get_key("master_key"),
    "TRADING_SECRET": magic_keys.get_key("trading_key")
}

def get_magic_number(broker: str, trade_type: str = "signal") -> int:
    """Get appropriate magic number for trade identification"""
    if broker.lower() == "exness":
        return MAGIC_KEY_CONFIG["EXNESS_MAGIC"]
    elif broker.lower() == "fbs":
        return MAGIC_KEY_CONFIG["FBS_MAGIC"]
    elif trade_type == "auto":
        return MAGIC_KEY_CONFIG["AUTO_MAGIC"]
    elif trade_type == "manual":
        return MAGIC_KEY_CONFIG["MANUAL_MAGIC"]
    else:
        return MAGIC_KEY_CONFIG["SIGNAL_MAGIC"]

def validate_trading_permission(api_key: str) -> bool:
    """Validate if API key has trading permissions"""
    return magic_keys.validate_key("api_key", api_key) or magic_keys.validate_key("master_key", api_key)

def encrypt_trading_signal(signal: Dict) -> Dict:
    """Encrypt trading signal with magic key"""
    return magic_keys.encrypt_signal(signal, "signal_key")

def verify_trading_signal(encrypted_signal: Dict) -> bool:
    """Verify trading signal integrity"""
    return magic_keys.verify_signal(encrypted_signal, "signal_key")

def get_trading_config() -> Dict:
    """Get complete trading configuration with magic keys"""
    return {
        "magic_numbers": MAGIC_KEY_CONFIG,
        "keys": {
            "api_key": magic_keys.get_key("api_key"),
            "trading_key": magic_keys.get_key("trading_key"),
            "exness_key": magic_keys.get_key("exness_key"),
            "fbs_key": magic_keys.get_key("fbs_key")
        },
        "permissions": magic_keys.keys.get("permissions", {}),
        "expires_at": magic_keys.keys.get("expires_at"),
        "created_at": magic_keys.keys.get("created_at")
    }

def display_magic_keys():
    """Display magic key configuration for setup"""
    config = get_trading_config()
    
    print("\n" + "="*60)
    print("GENX MAGIC KEY CONFIGURATION")
    print("="*60)
    
    print("\nMAGIC NUMBERS:")
    for key, value in config["magic_numbers"].items():
        if isinstance(value, int):
            print(f"  {key}: {value}")
    
    print("\nAPI KEYS:")
    for key, value in config["keys"].items():
        if value:
            print(f"  {key}: {value[:16]}...{value[-8:]}")
    
    print("\nPERMISSIONS:")
    for key, value in config["permissions"].items():
        print(f"  {key}: {value}")
    
    print("\nEXPIRATION:")
    print(f"  Created: {config['created_at']}")
    print(f"  Expires: {config['expires_at']}")
    
    print("\n" + "="*60)
    print("Save these keys securely for trading platform setup!")
    print("="*60)

if __name__ == "__main__":
    # Display magic key configuration when run directly
    display_magic_keys()
    
    # Save configuration
    with open("genx_magic_config.json", "w") as f:
        json.dump(get_trading_config(), f, indent=2)
    
    print("\nConfiguration saved to: genx_magic_config.json")