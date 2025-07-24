"""
Technical Indicators Utility
Comprehensive technical analysis indicators for forex trading
"""

import pandas as pd
import numpy as np
import logging
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

class TechnicalIndicators:
    """
    Comprehensive technical indicators calculator
    Optimized for forex trading signal generation
    """
    
    def __init__(self):
        self.indicators = {}
        logger.debug("Technical Indicators utility initialized")
    
    def add_all_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add all technical indicators to the dataframe"""
        try:
            # Make a copy to avoid modifying original data
            data = df.copy()
            
            # Price-based indicators
            data = self.add_moving_averages(data)
            data = self.add_momentum_indicators(data)
            data = self.add_volatility_indicators(data)
            data = self.add_volume_indicators(data)
            data = self.add_trend_indicators(data)
            data = self.add_support_resistance(data)
            
            logger.debug(f"Added {len(data.columns) - len(df.columns)} technical indicators")
            return data
            
        except Exception as e:
            logger.error(f"Error adding technical indicators: {e}")
            return df
    
    def add_moving_averages(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add moving average indicators"""
        try:
            periods = [5, 10, 20, 50, 100, 200]
            
            for period in periods:
                if len(df) >= period:
                    # Simple Moving Average
                    df[f'sma_{period}'] = df['close'].rolling(window=period).mean()
                    
                    # Exponential Moving Average
                    df[f'ema_{period}'] = df['close'].ewm(span=period).mean()
                    
                    # Weighted Moving Average
                    weights = np.arange(1, period + 1)
                    df[f'wma_{period}'] = df['close'].rolling(window=period).apply(
                        lambda x: np.dot(x, weights) / weights.sum(), raw=True
                    )
            
            # Moving Average Convergence Divergence (MACD)
            if len(df) >= 26:
                ema12 = df['close'].ewm(span=12).mean()
                ema26 = df['close'].ewm(span=26).mean()
                df['macd'] = ema12 - ema26
                df['macd_signal'] = df['macd'].ewm(span=9).mean()
                df['macd_histogram'] = df['macd'] - df['macd_signal']
            
            return df
            
        except Exception as e:
            logger.error(f"Error adding moving averages: {e}")
            return df
    
    def add_momentum_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add momentum-based indicators"""
        try:
            # Relative Strength Index (RSI)
            if len(df) >= 14:
                delta = df['close'].diff()
                gain = delta.where(delta > 0, 0)
                loss = -delta.where(delta < 0, 0)
                
                avg_gain = gain.rolling(window=14).mean()
                avg_loss = loss.rolling(window=14).mean()
                
                rs = avg_gain / avg_loss
                df['rsi'] = 100 - (100 / (1 + rs))
            
            # Stochastic Oscillator
            if len(df) >= 14:
                low_min = df['low'].rolling(window=14).min()
                high_max = df['high'].rolling(window=14).max()
                
                df['stoch_k'] = 100 * (df['close'] - low_min) / (high_max - low_min)
                df['stoch_d'] = df['stoch_k'].rolling(window=3).mean()
            
            # Williams %R
            if len(df) >= 14:
                high_max = df['high'].rolling(window=14).max()
                low_min = df['low'].rolling(window=14).min()
                df['williams_r'] = -100 * (high_max - df['close']) / (high_max - low_min)
            
            # Rate of Change (ROC)
            periods = [5, 10, 20]
            for period in periods:
                if len(df) >= period:
                    df[f'roc_{period}'] = df['close'].pct_change(periods=period) * 100
            
            # Commodity Channel Index (CCI)
            if len(df) >= 20:
                typical_price = (df['high'] + df['low'] + df['close']) / 3
                sma_tp = typical_price.rolling(window=20).mean()
                mean_dev = typical_price.rolling(window=20).apply(
                    lambda x: np.mean(np.abs(x - x.mean())), raw=True
                )
                df['cci'] = (typical_price - sma_tp) / (0.015 * mean_dev)
            
            return df
            
        except Exception as e:
            logger.error(f"Error adding momentum indicators: {e}")
            return df
    
    def add_volatility_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add volatility-based indicators"""
        try:
            # Average True Range (ATR)
            if len(df) >= 14:
                high_low = df['high'] - df['low']
                high_close = np.abs(df['high'] - df['close'].shift())
                low_close = np.abs(df['low'] - df['close'].shift())
                
                true_range = np.maximum(high_low, np.maximum(high_close, low_close))
                df['atr'] = true_range.rolling(window=14).mean()
            
            # Bollinger Bands
            if len(df) >= 20:
                sma_20 = df['close'].rolling(window=20).mean()
                std_20 = df['close'].rolling(window=20).std()
                
                df['bb_upper'] = sma_20 + (2 * std_20)
                df['bb_lower'] = sma_20 - (2 * std_20)
                df['bb_middle'] = sma_20
                df['bb_width'] = df['bb_upper'] - df['bb_lower']
                df['bb_position'] = (df['close'] - df['bb_lower']) / df['bb_width']
            
            # Volatility indicators
            periods = [10, 20, 50]
            for period in periods:
                if len(df) >= period:
                    df[f'volatility_{period}'] = df['close'].rolling(window=period).std()
                    df[f'volatility_ratio_{period}'] = df[f'volatility_{period}'] / df['close']
            
            # Donchian Channels
            if len(df) >= 20:
                df['donchian_upper'] = df['high'].rolling(window=20).max()
                df['donchian_lower'] = df['low'].rolling(window=20).min()
                df['donchian_middle'] = (df['donchian_upper'] + df['donchian_lower']) / 2
                df['donchian_position'] = (df['close'] - df['donchian_lower']) / (df['donchian_upper'] - df['donchian_lower'])
            
            return df
            
        except Exception as e:
            logger.error(f"Error adding volatility indicators: {e}")
            return df
    
    def add_volume_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add volume-based indicators"""
        try:
            if 'volume' not in df.columns or df['volume'].sum() == 0:
                # Create synthetic volume for forex data
                df['volume'] = (df['high'] - df['low']) * 1000000
            
            # Volume Moving Averages
            periods = [10, 20, 50]
            for period in periods:
                if len(df) >= period:
                    df[f'volume_sma_{period}'] = df['volume'].rolling(window=period).mean()
                    df[f'volume_ratio_{period}'] = df['volume'] / df[f'volume_sma_{period}']
            
            # On-Balance Volume (OBV)
            if len(df) >= 2:
                price_change = df['close'].diff()
                volume_direction = np.where(price_change > 0, df['volume'], 
                                          np.where(price_change < 0, -df['volume'], 0))
                df['obv'] = volume_direction.cumsum()
            
            # Volume Price Trend (VPT)
            if len(df) >= 2:
                price_change_pct = df['close'].pct_change()
                df['vpt'] = (price_change_pct * df['volume']).cumsum()
            
            # Accumulation/Distribution Line
            if len(df) >= 1:
                money_flow_multiplier = ((df['close'] - df['low']) - (df['high'] - df['close'])) / (df['high'] - df['low'])
                money_flow_volume = money_flow_multiplier * df['volume']
                df['ad_line'] = money_flow_volume.cumsum()
            
            return df
            
        except Exception as e:
            logger.error(f"Error adding volume indicators: {e}")
            return df
    
    def add_trend_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add trend-based indicators"""
        try:
            # Parabolic SAR
            if len(df) >= 5:
                df['sar'] = self._calculate_parabolic_sar(df)
            
            # Average Directional Index (ADX)
            if len(df) >= 14:
                df = self._calculate_adx(df)
            
            # Aroon Indicator
            if len(df) >= 25:
                period = 25
                aroon_up = 100 * (period - df['high'].rolling(window=period).apply(np.argmax)) / period
                aroon_down = 100 * (period - df['low'].rolling(window=period).apply(np.argmin)) / period
                
                df['aroon_up'] = aroon_up
                df['aroon_down'] = aroon_down
                df['aroon_oscillator'] = aroon_up - aroon_down
            
            # Trend strength
            periods = [10, 20, 50]
            for period in periods:
                if len(df) >= period:
                    # Linear regression slope
                    df[f'trend_strength_{period}'] = df['close'].rolling(window=period).apply(
                        lambda x: np.polyfit(range(len(x)), x, 1)[0], raw=True
                    )
            
            return df
            
        except Exception as e:
            logger.error(f"Error adding trend indicators: {e}")
            return df
    
    def add_support_resistance(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add support and resistance levels"""
        try:
            # Pivot Points
            if len(df) >= 1:
                df['pivot'] = (df['high'] + df['low'] + df['close']) / 3
                df['r1'] = 2 * df['pivot'] - df['low']
                df['s1'] = 2 * df['pivot'] - df['high']
                df['r2'] = df['pivot'] + (df['high'] - df['low'])
                df['s2'] = df['pivot'] - (df['high'] - df['low'])
            
            # Price position relative to recent highs/lows
            periods = [20, 50]
            for period in periods:
                if len(df) >= period:
                    high_max = df['high'].rolling(window=period).max()
                    low_min = df['low'].rolling(window=period).min()
                    
                    df[f'price_position_{period}'] = (df['close'] - low_min) / (high_max - low_min)
                    df[f'resistance_distance_{period}'] = (high_max - df['close']) / df['close']
                    df[f'support_distance_{period}'] = (df['close'] - low_min) / df['close']
            
            return df
            
        except Exception as e:
            logger.error(f"Error adding support/resistance indicators: {e}")
            return df
    
    def _calculate_parabolic_sar(self, df: pd.DataFrame, af_start: float = 0.02, af_increment: float = 0.02, af_max: float = 0.2) -> pd.Series:
        """Calculate Parabolic SAR"""
        try:
            high = df['high'].values
            low = df['low'].values
            close = df['close'].values
            
            length = len(df)
            sar = np.zeros(length)
            trend = np.zeros(length)
            af = np.zeros(length)
            ep = np.zeros(length)
            
            # Initialize
            sar[0] = low[0]
            trend[0] = 1  # 1 for up, -1 for down
            af[0] = af_start
            ep[0] = high[0]
            
            for i in range(1, length):
                if trend[i-1] == 1:  # Uptrend
                    sar[i] = sar[i-1] + af[i-1] * (ep[i-1] - sar[i-1])
                    
                    if low[i] <= sar[i]:
                        trend[i] = -1
                        sar[i] = ep[i-1]
                        af[i] = af_start
                        ep[i] = low[i]
                    else:
                        trend[i] = 1
                        if high[i] > ep[i-1]:
                            ep[i] = high[i]
                            af[i] = min(af[i-1] + af_increment, af_max)
                        else:
                            ep[i] = ep[i-1]
                            af[i] = af[i-1]
                else:  # Downtrend
                    sar[i] = sar[i-1] + af[i-1] * (ep[i-1] - sar[i-1])
                    
                    if high[i] >= sar[i]:
                        trend[i] = 1
                        sar[i] = ep[i-1]
                        af[i] = af_start
                        ep[i] = high[i]
                    else:
                        trend[i] = -1
                        if low[i] < ep[i-1]:
                            ep[i] = low[i]
                            af[i] = min(af[i-1] + af_increment, af_max)
                        else:
                            ep[i] = ep[i-1]
                            af[i] = af[i-1]
            
            return pd.Series(sar, index=df.index)
            
        except Exception as e:
            logger.error(f"Error calculating Parabolic SAR: {e}")
            return pd.Series(np.nan, index=df.index)
    
    def _calculate_adx(self, df: pd.DataFrame, period: int = 14) -> pd.DataFrame:
        """Calculate Average Directional Index (ADX)"""
        try:
            high = df['high']
            low = df['low']
            close = df['close']
            
            # Calculate True Range
            tr1 = high - low
            tr2 = abs(high - close.shift())
            tr3 = abs(low - close.shift())
            tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
            
            # Calculate Directional Movement
            dm_plus = high - high.shift()
            dm_minus = low.shift() - low
            
            dm_plus[dm_plus < 0] = 0
            dm_minus[dm_minus < 0] = 0
            dm_plus[(dm_plus - dm_minus) < 0] = 0
            dm_minus[(dm_minus - dm_plus) < 0] = 0
            
            # Calculate smoothed averages
            atr = tr.rolling(window=period).mean()
            di_plus = 100 * (dm_plus.rolling(window=period).mean() / atr)
            di_minus = 100 * (dm_minus.rolling(window=period).mean() / atr)
            
            # Calculate ADX
            dx = 100 * abs(di_plus - di_minus) / (di_plus + di_minus)
            adx = dx.rolling(window=period).mean()
            
            df['di_plus'] = di_plus
            df['di_minus'] = di_minus
            df['adx'] = adx
            
            return df
            
        except Exception as e:
            logger.error(f"Error calculating ADX: {e}")
            return df
    
    def get_indicator_summary(self, df: pd.DataFrame) -> Dict:
        """Get summary of current indicator values"""
        try:
            if len(df) == 0:
                return {}
            
            latest = df.iloc[-1]
            summary = {}
            
            # Trend indicators
            if 'sma_20' in df.columns and 'sma_50' in df.columns:
                summary['trend'] = 'UPTREND' if latest['sma_20'] > latest['sma_50'] else 'DOWNTREND'
            
            # Momentum
            if 'rsi' in df.columns:
                rsi = latest['rsi']
                if rsi > 70:
                    summary['momentum'] = 'OVERBOUGHT'
                elif rsi < 30:
                    summary['momentum'] = 'OVERSOLD'
                else:
                    summary['momentum'] = 'NEUTRAL'
            
            # Volatility
            if 'atr' in df.columns:
                current_atr = latest['atr']
                avg_atr = df['atr'].tail(20).mean()
                summary['volatility'] = 'HIGH' if current_atr > avg_atr * 1.5 else 'NORMAL'
            
            # Bollinger Bands position
            if 'bb_position' in df.columns:
                bb_pos = latest['bb_position']
                if bb_pos > 0.8:
                    summary['bb_position'] = 'UPPER'
                elif bb_pos < 0.2:
                    summary['bb_position'] = 'LOWER'
                else:
                    summary['bb_position'] = 'MIDDLE'
            
            return summary
            
        except Exception as e:
            logger.error(f"Error getting indicator summary: {e}")
            return {}