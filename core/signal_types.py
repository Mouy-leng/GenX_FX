"""
Trading signal types and data structures
"""

from dataclasses import dataclass
from enum import Enum
from datetime import datetime
from typing import Optional

class SignalType(Enum):
    """Trading signal types"""
    BUY = "BUY"
    SELL = "SELL"
    HOLD = "HOLD"

@dataclass
class TradingSignal:
    """Trading signal data structure"""
    symbol: str
    signal_type: SignalType
    entry_price: float
    stop_loss: float
    take_profit: float
    confidence: float
    timestamp: datetime
    timeframe: str = "H1"
    risk_reward_ratio: float = 2.0
