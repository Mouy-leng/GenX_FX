#!/usr/bin/env python3
"""
GenX Trading Platform Configuration
"""

import os
from pathlib import Path

class Config:
    def __init__(self):
        self.data = {
            'system': {
                'name': 'GenX Trading Platform',
                'version': '1.0.0'
            },
            'trading': {
                'symbols': ['EURUSD', 'GBPUSD', 'USDJPY'],
                'timeframes': ['H1', 'H4'],
                'primary_timeframe': 'H1',
                'signal_generation_interval': 300
            },
            'ai_models': {
                'ensemble_size': 5
            },
            'risk_management': {
                'max_risk_per_trade': 0.02
            },
            'spreadsheet': {
                'output_directory': 'signal_output'
            },
            'fxcm': {
                'use_mock': True
            }
        }
    
    def get(self, key, default=None):
        keys = key.split('.')
        value = self.data
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        return value

config = Config()