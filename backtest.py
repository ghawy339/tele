import pandas as pd
from data_utils import get_ohlcv, generate_features
from model_utils import train_model, generate_signals
from config import EXCHANGE_NAME, SYMBOL, TIMEFRAME
import ccxt

exchange = getattr(ccxt, EXCHANGE_NAME)()

def backtest(model, data):
    balance = 10000  # رصيد ابتدائي بالدولار
    position = None
    entry_price = 0
    balance_history = []

    for i in range(len(data) - 1):
        signal = generate_signals(model, data.iloc[:i+1])
        current_price = data['close'].iloc[i]
        
        if signal == 1 and position != 'long':
            position = 'long'
            entry_price = current_price
        elif signal == 0 and position != 'short':
            position = 'short'
            entry_price = current_price

        if position == 'long':
            profit_loss = (current_price - entry_price) / entry_price * 100
        elif position == 'short':
            profit_loss = (entry_price - current_price) / entry_price * 100

        balance_history.append(balance + (balance * profit_loss / 100))

    return balance_history

# الحصول على البيانات التاريخية
historical_data = get_ohlcv(exchange, SYMBOL, '1h')

# تدريب النموذج
model = train_model(historical_data)

# تطبيق الباك تيست
balance_history = backtest(model, historical_data)

# عرض النتائج
import matplotlib.pyplot as plt

plt.plot(balance_history)
plt.title('Backtest Balance Over Time')
plt.xlabel('Time')
plt.ylabel('Balance')
plt.show()
