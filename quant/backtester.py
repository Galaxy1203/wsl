"""
回测引擎模块
用于评估量化策略的历史表现
"""

import numpy as np
import pandas as pd
from datetime import datetime

class Backtester:
    """回测引擎"""
    
    def __init__(self, initial_capital=100000, commission=0.001):
        """
        初始化回测引擎
        
        参数:
            initial_capital: 初始资金
            commission: 手续费率 (单边)
        """
        self.initial_capital = initial_capital
        self.commission = commission
    
    def run_backtest(self, data, signals, initial_capital=None):
        """
        运行回测
        
        参数:
            data: 价格数据 DataFrame
            signals: 交易信号 Series
            initial_capital: 初始资金 (可选，覆盖初始化时设置的值)
            
        返回:
            dict: 回测结果
        """
        prices = data['close']
        
        # 使用指定的初始资金，或者默认的
        if initial_capital is not None:
            self.initial_capital = initial_capital
        
        # 初始化回测变量
        position = 0  # 当前持仓：0 空仓，1 多头
        cash = self.initial_capital
        shares = 0
        portfolio_values = []
        trades = []
        
        for date, signal in signals.items():
            price = prices.loc[date]
            
            # 执行交易信号
            if signal == 1 and position == 0:
                # 买入
                max_shares = int(cash / (price * (1 + self.commission)))
                if max_shares > 0:
                    cost = max_shares * price * (1 + self.commission)
                    shares = max_shares
                    cash -= cost
                    position = 1
                    trades.append({
                        'date': date,
                        'type': 'buy',
                        'price': price,
                        'shares': shares,
                        'value': cost
                    })
            
            elif signal == -1 and position == 1:
                # 卖出
                proceeds = shares * price * (1 - self.commission)
                cash += proceeds
                trades.append({
                    'date': date,
                    'type': 'sell',
                    'price': price,
                    'shares': shares,
                    'value': proceeds
                })
                shares = 0
                position = 0
            
            # 计算当前组合价值
            portfolio_value = cash + shares * price
            portfolio_values.append({
                'date': date,
                'cash': cash,
                'shares': shares,
                'position_value': shares * price,
                'total_value': portfolio_value
            })
        
        # 如果最后还有持仓，强制平仓
        if position == 1:
            last_date = prices.index[-1]
            last_price = prices.iloc[-1]
            proceeds = shares * last_price * (1 - self.commission)
            cash += proceeds
            trades.append({
                'date': last_date,
                'type': 'sell',
                'price': last_price,
                'shares': shares,
                'value': proceeds
            })
            portfolio_values[-1]['total_value'] = cash
            portfolio_values[-1]['shares'] = 0
            portfolio_values[-1]['position_value'] = 0
        
        # 转换为DataFrame
        portfolio_df = pd.DataFrame(portfolio_values).set_index('date')
        trades_df = pd.DataFrame(trades) if trades else pd.DataFrame()
        
        # 计算性能指标
        performance = self.calculate_performance(portfolio_df, prices)
        
        return {
            'portfolio': portfolio_df,
            'trades': trades_df,
            'performance': performance
        }
    
    def calculate_performance(self, portfolio_df, prices):
        """
        计算性能指标
        
        参数:
            portfolio_df: 组合价值 DataFrame
            prices: 价格序列
            
        返回:
            dict: 性能指标
        """
        portfolio_values = portfolio_df['total_value']
        benchmark_returns = prices.pct_change().dropna()
        portfolio_returns = portfolio_values.pct_change().dropna()
        
        # 总收益率
        total_return = (portfolio_values.iloc[-1] - self.initial_capital) / self.initial_capital
        
        # 年化收益率
        n_days = len(portfolio_values)
        annual_return = (1 + total_return) ** (365 / n_days) - 1
        
        # 波动率
        volatility = portfolio_returns.std() * np.sqrt(252)
        
        # 夏普比率 (假设无风险利率为0)
        sharpe_ratio = (portfolio_returns.mean() / portfolio_returns.std()) * np.sqrt(252) if portfolio_returns.std() != 0 else 0
        
        # 最大回撤
        cumulative_returns = (1 + portfolio_returns).cumprod()
        running_max = cumulative_returns.cummax()
        drawdown = (cumulative_returns - running_max) / running_max
        max_drawdown = drawdown.min()
        
        # 基准收益
        benchmark_total_return = (prices.iloc[-1] - prices.iloc[0]) / prices.iloc[0]
        
        # 胜率
        trades_df = portfolio_df.copy()
        trades_df['position_change'] = trades_df['shares'].diff().fillna(0)
        
        performance = {
            'initial_capital': self.initial_capital,
            'final_value': portfolio_values.iloc[-1],
            'total_return': total_return,
            'annual_return': annual_return,
            'volatility': volatility,
            'sharpe_ratio': sharpe_ratio,
            'max_drawdown': max_drawdown,
            'benchmark_return': benchmark_total_return,
            'excess_return': total_return - benchmark_total_return,
            'n_days': n_days
        }
        
        return performance
    
    def print_performance_summary(self, performance):
        """打印性能摘要"""
        print("\n" + "="*60)
        print("回测性能摘要")
        print("="*60)
        print(f"初始资金: ¥{performance['initial_capital']:,.2f}")
        print(f"最终价值: ¥{performance['final_value']:,.2f}")
        print(f"总收益率: {performance['total_return']*100:+.2f}%")
        print(f"年化收益率: {performance['annual_return']*100:+.2f}%")
        print(f"波动率: {performance['volatility']*100:.2f}%")
        print(f"夏普比率: {performance['sharpe_ratio']:.2f}")
        print(f"最大回撤: {performance['max_drawdown']*100:.2f}%")
        print(f"基准收益: {performance['benchmark_return']*100:+.2f}%")
        print(f"超额收益: {performance['excess_return']*100:+.2f}%")
        print("="*60 + "\n")


class PortfolioOptimizer:
    """投资组合优化器"""
    
    def __init__(self):
        pass
    
    def calculate_equal_weight(self, n_assets):
        """等权重分配"""
        return np.ones(n_assets) / n_assets
    
    def calculate_risk_parity(self, returns):
        """风险平价 (简化版)"""
        volatilities = returns.std()
        weights = 1 / volatilities
        weights = weights / weights.sum()
        return weights