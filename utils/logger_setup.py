#!/usr/bin/env python3
"""
Logger setup for GenX Trading Platform
"""

import logging
import sys
from pathlib import Path

def setup_logging(level='INFO'):
    """Setup logging configuration"""
    
    # Create logs directory
    logs_dir = Path('logs')
    logs_dir.mkdir(exist_ok=True)
    
    # Configure logging
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(logs_dir / 'genx_trading.log')
        ]
    )
    
    return logging.getLogger(__name__)