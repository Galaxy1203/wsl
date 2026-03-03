#!/usr/bin/env python3
"""
量化投资工具 - 主程序
一个模拟的量化投资回测工具
"""

import sys
import argparse
from datetime import datetime, timedelta
from data_processor import DataGenerator
from strategies import (
    SMACrossStrategy,
    RSIStrategy,
    BollingerBandsStrategy,
    MACDStrategy,
    MeanReversionStrategy,
    MomentumStrategy
)
from backtester import Backtester

class QuantTool:
    """量化投资工具主类"""
    
    def __init__(self):
        self.data_generator = DataGenerator()
        self.backtester = Backtester()
        self.strategies = {
            'sma_cross': SMACrossStrategy,
            'rsi': RSIStrategy,
            'bollinger': BollingerBandsStrategy,
            'macd': MACDStrategy,
            'mean_reversion': MeanReversionStrategy,
            'momentum': MomentumStrategy
        }
    
    def run_single_strategy(self, strategy_name, initial_capital=100000, **kwargs):
        """
        运行单个策略的回测
        
        参数:
            strategy_name: 策略名称
            initial_capital: 初始资金
            **kwargs: 策略参数
        """
        print(f"\n{'='*60}")
        print(f"策略: {strategy_name}")
        print(f"{'='*60}")
        
        # 生成模拟数据
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365)
        
        print(f"\n生成模拟数据 ({start_date.date()} 至 {end_date.date()})...")
        data = self.data_generator.generate_price_data(start_date, end_date)
        print(f"数据生成完成，共 {len(data)} 个交易日")
        
        # 创建策略实例
        strategy_class = self.strategies.get(strategy_name)
        if not strategy_class:
            print(f"错误: 未知的策略 '{strategy_name}'")
            return
        
        strategy = strategy_class(**kwargs)
        print(f"策略参数: {kwargs}")
        
        # 生成交易信号
        print("\n生成交易信号...")
        signals = strategy.generate_signals(data)
        n_signals = len(signals[signals != 0])
        print(f"共生成 {n_signals} 个交易信号")
        
        # 运行回测
        print("\n运行回测...")
        results = self.backtester.run_backtest(data, signals, initial_capital=initial_capital)
        
        # 打印结果
        self.backtester.print_performance_summary(results['performance'])
        
        # 打印交易记录
        if not results['trades'].empty:
            print("交易记录:")
            print(results['trades'].to_string(index=False))
            print()
        
        return results
    
    def run_all_strategies(self):
        """运行所有策略的回测并比较"""
        print(f"\n{'='*60}")
        print("所有策略对比")
        print(f"{'='*60}")
        
        # 生成模拟数据
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365)
        
        print(f"\n生成模拟数据 ({start_date.date()} 至 {end_date.date()})...")
        data = self.data_generator.generate_price_data(start_date, end_date)
        
        results_summary = []
        
        # 测试所有策略
        for strategy_name, strategy_class in self.strategies.items():
            print(f"\n测试策略: {strategy_name}...")
            
            strategy = strategy_class()
            signals = strategy.generate_signals(data)
            results = self.backtester.run_backtest(data, signals)
            
            perf = results['performance']
            results_summary.append({
                '策略': strategy_name,
                '总收益率': f"{perf['total_return']*100:+.2f}%",
                '年化收益率': f"{perf['annual_return']*100:+.2f}%",
                '夏普比率': f"{perf['sharpe_ratio']:.2f}",
                '最大回撤': f"{perf['max_drawdown']*100:.2f}%"
            })
        
        # 打印对比表格
        print(f"\n{'='*80}")
        print("策略对比结果")
        print(f"{'='*80}")
        try:
            from tabulate import tabulate
            print(tabulate(results_summary, headers='keys', tablefmt='grid'))
        except ImportError:
            # 如果没有tabulate，使用简单格式打印
            headers = list(results_summary[0].keys())
            print(" | ".join(headers))
            print("-" * 80)
            for result in results_summary:
                print(" | ".join(str(result[h]) for h in headers))
        print(f"{'='*80}\n")
        
        return results_summary
    
    def interactive_mode(self):
        """交互模式"""
        print("\n" + "="*60)
        print("量化投资工具 - 交互模式")
        print("="*60)
        
        while True:
            print("\n请选择操作:")
            print("1. 测试单个策略")
            print("2. 测试所有策略并对比")
            print("3. 查看策略列表")
            print("4. 退出")
            
            choice = input("\n请输入选项 (1-4): ").strip()
            
            if choice == '1':
                self.show_strategy_list()
                strategy_name = input("\n请输入策略名称: ").strip().lower()
                
                if strategy_name in self.strategies:
                    self.run_single_strategy(strategy_name)
                else:
                    print("无效的策略名称!")
            
            elif choice == '2':
                self.run_all_strategies()
            
            elif choice == '3':
                self.show_strategy_list()
            
            elif choice == '4':
                print("感谢使用量化投资工具，再见!")
                break
            
            else:
                print("无效的选项，请重新输入!")
    
    def show_strategy_list(self):
        """显示可用策略列表"""
        print("\n可用策略列表:")
        print("-" * 60)
        print("  sma_cross      - 双均线交叉策略")
        print("  rsi            - RSI策略")
        print("  bollinger      - 布林带策略")
        print("  macd           - MACD策略")
        print("  mean_reversion - 均值回归策略")
        print("  momentum       - 动量策略")
        print("-" * 60)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='量化投资工具 - 一个模拟的量化投资回测工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python quant_tool.py                          # 交互模式
  python quant_tool.py --strategy sma_cross    # 测试双均线策略
  python quant_tool.py --all                    # 测试所有策略
        """
    )
    
    parser.add_argument(
        '--strategy',
        type=str,
        help='要测试的策略名称'
    )
    
    parser.add_argument(
        '--all',
        action='store_true',
        help='测试所有策略并对比'
    )
    
    parser.add_argument(
        '--initial-capital',
        type=float,
        default=100000,
        help='初始资金 (默认: 100000)'
    )
    
    args = parser.parse_args()
    
    tool = QuantTool()
    
    if args.strategy:
        tool.run_single_strategy(args.strategy, initial_capital=args.initial_capital)
    elif args.all:
        tool.run_all_strategies()
    else:
        tool.interactive_mode()


if __name__ == '__main__':
    main()