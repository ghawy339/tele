import pandas as pd
import ccxt

def get_ohlcv(exchange, symbol, timeframe, since):
    data = exchange.fetch_ohlcv(symbol, timeframe, since=since)
    df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)
    return df

if __name__ == "__main__":
    exchange = ccxt.binance()
    symbol = 'BTC/USDT'
    since = exchange.parse8601('2023-04-01T00:00:00Z')
    timeframe = '15m'
    df = get_ohlcv(exchange, symbol, timeframe, since)
    df.to_csv('../data/ohlcv_data.csv')
