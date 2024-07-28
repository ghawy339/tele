import pandas as pd
import joblib

def backtest_strategy(model, df, initial_balance=10, leverage=25, trade_amount_percentage=0.02):
    X = df[['rsi', 'sma', 'ema', 'macd', 'macd_signal', 'macd_hist', 'bb_upper', 'bb_middle', 'bb_lower', 'adx', 'stoch_k', 'stoch_d', 'atr', 'cci']]
    signals = model.predict(X)
    df['signal'] = signals
    df['returns'] = df['close'].pct_change()

    balance = initial_balance
    trade_amount = initial_balance * trade_amount_percentage
    positions = []
    num_trades = 0
    profitable_trades = 0
    for i in range(1, len(df)):
        if df['signal'].iloc[i-1] == 1:  # Buy signal
            num_trades += 1
            position = trade_amount * leverage * (1 + df['returns'].iloc[i])
            balance += position - trade_amount
            positions.append(position)
            if position > trade_amount:
                profitable_trades += 1
        elif df['signal'].iloc[i-1] == 0:  # Sell signal
            num_trades += 1
            position = trade_amount * leverage * (1 - df['returns'].iloc[i])
            balance += trade_amount - position
            positions.append(-position)
            if -position > trade_amount:
                profitable_trades += 1
    
    total_profit = balance - initial_balance
    avg_profit_per_trade = total_profit / num_trades if num_trades > 0 else 0
    win_rate = profitable_trades / num_trades if num_trades > 0 else 0

    return {
        'total_profit': total_profit,
        'num_trades': num_trades,
        'avg_profit_per_trade': avg_profit_per_trade,
        'win_rate': win_rate,
        'final_balance': balance,
        'false_signals': df['signal'].iloc[:-1][(df['signal'].shift(-1) != df['signal'])].count(),
        'true_signals': df['signal'].iloc[:-1][(df['signal'].shift(-1) == df['signal'])].count()
    }

if __name__ == "__main__":
    df = pd.read_csv('../data/ohlcv_data_with_features.csv', index_col='timestamp', parse_dates=True)
    best_model = joblib.load('../models/best_model.pkl')
    backtest_results = backtest_strategy(best_model, df, leverage=25, trade_amount_percentage=0.02)
    print("Backtest Results:\n", backtest_results)
