import pandas as pd

def get_ohlcv(exchange, symbol, timeframe):
    data = exchange.fetch_ohlcv(symbol, timeframe)
    df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)
    return df

def generate_features(df):
    df['rsi'] = ta.rsi(df['close'], length=14)
    df['sma'] = ta.sma(df['close'], length=50)
    df['ema'] = ta.ema(df['close'], length=50)
    
    # MACD
    df['macd'], df['macd_signal'], df['macd_hist'] = ta.macd(df['close'], fast=12, slow=26, signal=9)

    # Bollinger Bands
    df['bb_upper'], df['bb_middle'], df['bb_lower'] = ta.bbands(df['close'], length=20, std=2)

    # ADX
    df['adx'] = ta.adx(df['high'], df['low'], df['close'], length=14)

    # Stochastic Oscillator
    df['stoch_k'], df['stoch_d'] = ta.stoch(df['high'], df['low'], df['close'], length=14, signal=3)

    # Remove rows with NaN values
    df.dropna(inplace=True)

    return df
