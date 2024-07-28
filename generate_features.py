import pandas as pd
import pandas_ta as ta

def generate_features(df):
    df['rsi'] = ta.rsi(df['close'], length=14)
    df['sma'] = ta.sma(df['close'], length=50)
    df['ema'] = ta.ema(df['close'], length=50)
    df['macd'], df['macd_signal'], df['macd_hist'] = ta.macd(df['close'], fast=12, slow=26, signal=9)
    df['bb_upper'], df['bb_middle'], df['bb_lower'] = ta.bbands(df['close'], length=20, std=2)
    df['adx'] = ta.adx(df['high'], df['low'], df['close'], length=14)
    df['stoch_k'], df['stoch_d'] = ta.stoch(df['high'], df['low'], df['close'], length=14, signal=3)
    df['atr'] = ta.atr(df['high'], df['low'], df['close'], length=14)
    df['cci'] = ta.cci(df['high'], df['low'], df['close'], length=20)
    df.dropna(inplace=True)
    return df

if __name__ == "__main__":
    df = pd.read_csv('../data/ohlcv_data.csv', index_col='timestamp', parse_dates=True)
    df = generate_features(df)
    df.to_csv('../data/ohlcv_data_with_features.csv')
