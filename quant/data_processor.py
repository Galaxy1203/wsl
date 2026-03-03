"""
数据处理模块
负责生成和处理模拟的市场数据
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta

class DataGenerator:
    """模拟数据生成器"""
    
    def __init__(self):
        pass
    
    def generate_price_data(self, start_date, end_date, base_price=100, volatility=0.02):
        """
        生成模拟价格数据
        
        参数:
            start_date: 开始日期 (datetime)
            end_date: 结束日期 (datetime)
            base_price: 基准价格
            volatility: 波动率
            
        返回:
            DataFrame: 包含日期、开盘价、最高价、最低价、收盘价、成交量的数据
        """
        date_range = pd.date_range(start=start_date, end=end_date, freq='D')
        n_days = len(date_range)
        
        # 生成随机价格变化
        returns = np.random.normal(0, volatility, n_days)
        prices = base_price * np.cumprod(1 + returns)
        
        # 生成OHLC数据
        open_prices = prices * (1 + np.random.normal(0, 0.005, n_days))
        high_prices = np.maximum(prices, open_prices) * (1 + np.random.uniform(0, 0.01, n_days))
        low_prices = np.minimum(prices, open_prices) * (1 - np.random.uniform(0, 0.01, n_days))
        close_prices = prices
        volume = np.random.randint(100000, 1000000, n_days)
        
        df = pd.DataFrame({
            'date': date_range,
            'open': open_prices,
            'high': high_prices,
            'low': low_prices,
            'close': close_prices,
            'volume': volume
        })
        
        df.set_index('date', inplace=True)
        return df
    
    def generate_multiple_assets(self, start_date, end_date, n_assets=5):
        """
        生成多个资产的价格数据
        
        参数:
            start_date: 开始日期
            end_date: 结束日期
            n_assets: 资产数量
            
        返回:
            dict: 资产名称到价格数据的映射
        """
        assets = {}
        base_prices = np.random.uniform(50, 200, n_assets)
        volatilities = np.random.uniform(0.01, 0.03, n_assets)
        
        for i in range(n_assets):
            asset_name = f"STOCK_{i+1:02d}"
            assets[asset_name] = self.generate_price_data(
                start_date, end_date, 
                base_price=base_prices[i], 
                volatility=volatilities[i]
            )
        
        return assets


class TechnicalIndicators:
    """技术指标计算"""
    
    @staticmethod
    def sma(prices, window):
        """简单移动平均"""
        return prices.rolling(window=window).mean()
    
    @staticmethod
    def ema(prices, window):
        """指数移动平均"""
        return prices.ewm(span=window, adjust=False).mean()
    
    @staticmethod
    def rsi(prices, window=14):
        """相对强弱指标"""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))
    
    @staticmethod
    def bollinger_bands(prices, window=20, std_dev=2):
        """布林带"""
        sma = prices.rolling(window=window).mean()
        std = prices.rolling(window=window).std()
        upper_band = sma + (std * std_dev)
        lower_band = sma - (std * std_dev)
        return upper_band, sma, lower_band
    
    @staticmethod
    def macd(prices, fast=12, slow=26, signal=9):
        """MACD指标"""
        ema_fast = prices.ewm(span=fast, adjust=False).mean()
        ema_slow = prices.ewm(span=slow, adjust=False).mean()
        macd_line = ema_fast - ema_slow
        signal_line = macd_line.ewm(span=signal, adjust=False).mean()
        histogram = macd_line - signal_line
        return macd_line, signal_line, histogram