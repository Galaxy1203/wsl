"""
策略模块
包含多种量化投资策略
"""

import numpy as np
import pandas as pd
from data_processor import TechnicalIndicators

class Strategy:
    """策略基类"""
    
    def __init__(self, name):
        self.name = name
    
    def generate_signals(self, data):
        """
        生成交易信号
        
        参数:
            data: 价格数据 DataFrame
            
        返回:
            Series: 信号序列 (1: 买入, -1: 卖出, 0: 持有)
        """
        raise NotImplementedError("子类必须实现此方法")


class SMACrossStrategy(Strategy):
    """双均线交叉策略"""
    
    def __init__(self, short_window=5, long_window=20):
        super().__init__(f"SMA_Cross_{short_window}_{long_window}")
        self.short_window = short_window
        self.long_window = long_window
    
    def generate_signals(self, data):
        prices = data['close']
        short_sma = TechnicalIndicators.sma(prices, self.short_window)
        long_sma = TechnicalIndicators.sma(prices, self.long_window)
        
        signals = pd.Series(0, index=prices.index)
        
        # 短期均线上穿长期均线：买入
        signals[(short_sma > long_sma) & (short_sma.shift(1) <= long_sma.shift(1))] = 1
        
        # 短期均线下穿长期均线：卖出
        signals[(short_sma < long_sma) & (short_sma.shift(1) >= long_sma.shift(1))] = -1
        
        return signals


class RSIStrategy(Strategy):
    """RSI策略"""
    
    def __init__(self, window=14, oversold=30, overbought=70):
        super().__init__(f"RSI_{window}_{oversold}_{overbought}")
        self.window = window
        self.oversold = oversold
        self.overbought = overbought
    
    def generate_signals(self, data):
        prices = data['close']
        rsi = TechnicalIndicators.rsi(prices, self.window)
        
        signals = pd.Series(0, index=prices.index)
        
        # RSI低于超卖线：买入
        signals[(rsi < self.oversold) & (rsi.shift(1) >= self.oversold)] = 1
        
        # RSI高于超买线：卖出
        signals[(rsi > self.overbought) & (rsi.shift(1) <= self.overbought)] = -1
        
        return signals


class BollingerBandsStrategy(Strategy):
    """布林带策略"""
    
    def __init__(self, window=20, std_dev=2):
        super().__init__(f"Bollinger_{window}_{std_dev}")
        self.window = window
        self.std_dev = std_dev
    
    def generate_signals(self, data):
        prices = data['close']
        upper_band, _, lower_band = TechnicalIndicators.bollinger_bands(
            prices, self.window, self.std_dev
        )
        
        signals = pd.Series(0, index=prices.index)
        
        # 价格跌破下轨：买入
        signals[(prices < lower_band) & (prices.shift(1) >= lower_band.shift(1))] = 1
        
        # 价格突破上轨：卖出
        signals[(prices > upper_band) & (prices.shift(1) <= upper_band.shift(1))] = -1
        
        return signals


class MACDStrategy(Strategy):
    """MACD策略"""
    
    def __init__(self, fast=12, slow=26, signal=9):
        super().__init__(f"MACD_{fast}_{slow}_{signal}")
        self.fast = fast
        self.slow = slow
        self.signal = signal
    
    def generate_signals(self, data):
        prices = data['close']
        macd_line, signal_line, _ = TechnicalIndicators.macd(
            prices, self.fast, self.slow, self.signal
        )
        
        signals = pd.Series(0, index=prices.index)
        
        # MACD线上穿信号线：买入
        signals[(macd_line > signal_line) & (macd_line.shift(1) <= signal_line.shift(1))] = 1
        
        # MACD线下穿信号线：卖出
        signals[(macd_line < signal_line) & (macd_line.shift(1) >= signal_line.shift(1))] = -1
        
        return signals


class MeanReversionStrategy(Strategy):
    """均值回归策略"""
    
    def __init__(self, window=20, entry_threshold=1.0, exit_threshold=0.0):
        super().__init__(f"MeanReversion_{window}")
        self.window = window
        self.entry_threshold = entry_threshold
        self.exit_threshold = exit_threshold
    
    def generate_signals(self, data):
        prices = data['close']
        sma = TechnicalIndicators.sma(prices, self.window)
        std = prices.rolling(window=self.window).std()
        
        z_score = (prices - sma) / std
        
        signals = pd.Series(0, index=prices.index)
        
        # 价格低于均值一定标准差：买入
        signals[(z_score < -self.entry_threshold) & (z_score.shift(1) >= -self.entry_threshold)] = 1
        
        # 价格回归到均值附近：卖出
        signals[(z_score > -self.exit_threshold) & (z_score.shift(1) <= -self.exit_threshold)] = -1
        
        return signals


class MomentumStrategy(Strategy):
    """动量策略"""
    
    def __init__(self, lookback=20, hold_period=10):
        super().__init__(f"Momentum_{lookback}_{hold_period}")
        self.lookback = lookback
        self.hold_period = hold_period
    
    def generate_signals(self, data):
        prices = data['close']
        returns = prices.pct_change(self.lookback)
        
        signals = pd.Series(0, index=prices.index)
        
        # 过去N天涨幅为正：买入
        signals[(returns > 0) & (returns.shift(1) <= 0)] = 1
        
        # 持有M天后卖出
        for i in range(len(signals)):
            if signals.iloc[i] == 1:
                sell_idx = i + self.hold_period
                if sell_idx < len(signals):
                    signals.iloc[sell_idx] = -1
        
        return signals