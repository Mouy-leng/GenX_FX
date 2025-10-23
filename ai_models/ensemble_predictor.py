"""
Ensemble Predictor - AI model for trading predictions
"""

import asyncio
import logging
import numpy as np
import pandas as pd
from typing import List, Dict, Any, Optional
from datetime import datetime
import joblib
from pathlib import Path

logger = logging.getLogger(__name__)

class EnsemblePredictor:
    """Ensemble AI predictor for trading signals"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.models = {}
        self.feature_engineer = None
        self.is_initialized = False
        
        logger.info("Ensemble Predictor initialized")
    
    async def initialize(self):
        """Initialize the ensemble predictor"""
        try:
            # Initialize feature engineer
            self.feature_engineer = FeatureEngineer()
            
            # Load or create models
            await self._load_models()
            
            self.is_initialized = True
            logger.info("✅ Ensemble Predictor initialized")
            
        except Exception as e:
            logger.error(f"Failed to initialize ensemble predictor: {e}")
            raise
    
    async def _load_models(self):
        """Load or create ensemble models"""
        models_dir = Path("models")
        models_dir.mkdir(exist_ok=True)
        
        # For now, create simple mock models
        # In a real implementation, these would be trained ML models
        self.models = {
            'trend_model': MockModel('trend'),
            'momentum_model': MockModel('momentum'),
            'volatility_model': MockModel('volatility'),
            'sentiment_model': MockModel('sentiment'),
            'volume_model': MockModel('volume')
        }
        
        logger.info(f"Loaded {len(self.models)} ensemble models")
    
    async def predict(self, symbol: str, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate prediction for symbol using historical data"""
        if not self.is_initialized:
            await self.initialize()
        
        try:
            # Convert data to DataFrame
            df = pd.DataFrame(data)
            
            # Engineer features
            features = self.feature_engineer.create_features(df)
            
            # Get predictions from all models
            predictions = {}
            confidences = []
            
            for model_name, model in self.models.items():
                pred = model.predict(features)
                predictions[model_name] = pred
                confidences.append(pred['confidence'])
            
            # Ensemble prediction
            ensemble_confidence = np.mean(confidences)
            ensemble_direction = 1 if ensemble_confidence > 0.5 else -1
            
            # Add some randomness for realistic behavior
            noise = np.random.normal(0, 0.1)
            ensemble_confidence = max(0.1, min(0.95, ensemble_confidence + noise))
            
            return {
                'direction': ensemble_direction,
                'confidence': ensemble_confidence,
                'predictions': predictions,
                'timestamp': datetime.now()
            }
            
        except Exception as e:
            logger.error(f"Error generating prediction for {symbol}: {e}")
            return {
                'direction': 0,
                'confidence': 0.0,
                'predictions': {},
                'timestamp': datetime.now()
            }

class FeatureEngineer:
    """Feature engineering for trading data"""
    
    def create_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create technical features from OHLC data"""
        try:
            features_df = df.copy()
            
            # Price-based features
            features_df['price_change'] = features_df['close'].pct_change()
            features_df['high_low_ratio'] = features_df['high'] / features_df['low']
            features_df['close_open_ratio'] = features_df['close'] / features_df['open']
            
            # Moving averages
            features_df['sma_5'] = features_df['close'].rolling(5).mean()
            features_df['sma_10'] = features_df['close'].rolling(10).mean()
            features_df['sma_20'] = features_df['close'].rolling(20).mean()
            
            # Price relative to moving averages
            features_df['price_sma5_ratio'] = features_df['close'] / features_df['sma_5']
            features_df['price_sma10_ratio'] = features_df['close'] / features_df['sma_10']
            features_df['price_sma20_ratio'] = features_df['close'] / features_df['sma_20']
            
            # Volatility features
            features_df['volatility'] = features_df['price_change'].rolling(10).std()
            features_df['atr'] = self._calculate_atr(features_df)
            
            # Momentum features
            features_df['rsi'] = self._calculate_rsi(features_df['close'])
            features_df['macd'] = self._calculate_macd(features_df['close'])
            
            # Volume features (if available)
            if 'volume' in features_df.columns:
                features_df['volume_sma'] = features_df['volume'].rolling(10).mean()
                features_df['volume_ratio'] = features_df['volume'] / features_df['volume_sma']
            else:
                features_df['volume_ratio'] = 1.0
            
            # Fill NaN values
            features_df = features_df.fillna(method='bfill').fillna(0)
            
            return features_df
            
        except Exception as e:
            logger.error(f"Error creating features: {e}")
            return df
    
    def _calculate_atr(self, df: pd.DataFrame, period: int = 14) -> pd.Series:
        """Calculate Average True Range"""
        high = df['high']
        low = df['low']
        close = df['close']
        
        tr1 = high - low
        tr2 = abs(high - close.shift(1))
        tr3 = abs(low - close.shift(1))
        
        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        return tr.rolling(period).mean()
    
    def _calculate_rsi(self, prices: pd.Series, period: int = 14) -> pd.Series:
        """Calculate Relative Strength Index"""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def _calculate_macd(self, prices: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9) -> pd.Series:
        """Calculate MACD"""
        ema_fast = prices.ewm(span=fast).mean()
        ema_slow = prices.ewm(span=slow).mean()
        macd = ema_fast - ema_slow
        return macd

class MockModel:
    """Mock AI model for testing"""
    
    def __init__(self, model_type: str):
        self.model_type = model_type
    
    def predict(self, features: pd.DataFrame) -> Dict[str, Any]:
        """Generate mock prediction"""
        # Simple mock prediction based on recent price action
        if len(features) < 2:
            return {'direction': 0, 'confidence': 0.0}
        
        recent_data = features.tail(5)
        
        # Calculate simple trend
        price_change = recent_data['close'].iloc[-1] - recent_data['close'].iloc[0]
        price_change_pct = price_change / recent_data['close'].iloc[0]
        
        # Generate confidence based on trend strength
        confidence = min(0.9, max(0.1, abs(price_change_pct) * 10))
        
        # Generate direction
        direction = 1 if price_change > 0 else -1
        
        # Add some randomness
        noise = np.random.normal(0, 0.1)
        confidence = max(0.1, min(0.95, confidence + noise))
        
        return {
            'direction': direction,
            'confidence': confidence,
            'model_type': self.model_type
        }
