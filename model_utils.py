from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import GridSearchCV

def train_model(df):
    X = df[['rsi', 'sma', 'ema', 'macd', 'macd_signal', 'macd_hist', 'bb_upper', 'bb_middle', 'bb_lower', 'adx', 'stoch_k', 'stoch_d']]
    y = (df['close'].shift(-1) > df['close']).astype(int)  # إشارة الشراء إذا كان السعر يرتفع
    
    # إعداد معلمات البحث الشبكي
    param_grid = {
        'n_estimators': [100, 200, 300],
        'max_depth': [10, 20, 30],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 2, 4]
    }
    
    # تهيئة نموذج الغابة العشوائية
    rf = RandomForestClassifier()
    
    # البحث الشبكي
    grid_search = GridSearchCV(estimator=rf, param_grid=param_grid, cv=3, n_jobs=-1, verbose=2)
    grid_search.fit(X, y)
    
    # أفضل نموذج
    best_model = grid_search.best_estimator_
    
    return best_model, X, y

def generate_signals(model, df):
    X = df[['rsi', 'sma', 'ema', 'macd', 'macd_signal', 'macd_hist', 'bb_upper', 'bb_middle', 'bb_lower', 'adx', 'stoch_k', 'stoch_d']]
    df['signal'] = model.predict(X)
    return df['signal'].iloc[-1]

def evaluate_model(model, X, y):
    y_pred = model.predict(X)
    report = classification_report(y, y_pred)
    matrix = confusion_matrix(y, y_pred)
    return report, matrix

def backtest_strategy(model, df, initial_balance=10000, leverage=20, trade_amount_percentage=0.01):
    X = df[['rsi', 'sma', 'ema', 'macd', 'macd_signal', 'macd_hist', 'bb_upper', 'bb_middle', 'bb_lower', 'adx', 'stoch_k', 'stoch_d']]
    signals = model.predict(X)
    df['signal'] = signals
    df['returns'] = df['close'].pct_change()

    balance = initial_balance
    trade_amount = initial_balance * trade_amount_percentage
    positions = []
    for i in range(1, len(df)):
        if df['signal'].iloc[i-1] == 1:  # Buy signal
            position = trade_amount * leverage * (1 + df['returns'].iloc[i])
            balance += position - trade_amount
            positions.append(position)
        elif df['signal'].iloc[i-1] == 0:  # Sell signal
            position = trade_amount * leverage * (1 - df['returns'].iloc[i])
            balance += trade_amount - position
            positions.append(-position)
    
    total_profit = balance - initial_balance
    num_trades = len(positions)
    avg_profit_per_trade = total_profit / num_trades if num_trades > 0 else 0
    win_rate = sum(1 for pos in positions if pos > 0) / num_trades if num_trades > 0 else 0

    return {
        'total_profit': total_profit,
        'num_trades': num_trades,
        'avg_profit_per_trade': avg_profit_per_trade,
        'win_rate': win_rate,
        'final_balance': balance
    }
