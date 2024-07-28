import collect_data
import generate_features
import train_model
import evaluate_model
import backtest_strategy
import send_signal
import joblib
import pandas as pd

def main():
    # جمع البيانات
    collect_data.main()
    
    # توليد الميزات
    generate_features.main()
    
    # تدريب النموذج
    train_model.main()
    
    # تقييم النموذج
    evaluate_model.main()
    
    # Backtest الاستراتيجية
    backtest_strategy.main()

    # إرسال الإشارة إلى Telegram
    bot_token = "YOUR_TELEGRAM_BOT_TOKEN"
    chat_id = "YOUR_TELEGRAM_CHAT_ID"
    
    df = pd.read_csv('../data/ohlcv_data_with_features.csv', index_col='timestamp', parse_dates=True)
    best_model = joblib.load('../models/best_model.pkl')
    X = df[['rsi', 'sma', 'ema', 'macd', 'macd_signal', 'macd_hist', 'bb_upper', 'bb_middle', 'bb_lower', 'adx', 'stoch_k', 'stoch_d', 'atr', 'cci']]
    signals = best_model.predict(X)
    
    for i in range(1, len(df)):
        if signals[i-1] != signals[i]:
            symbol = "BTC/USDT"
            direction = "Buy" if signals[i] == 1 else "Sell"
            entry_price = df['close'].iloc[i]
            targets = [entry_price * 1.01, entry_price * 1.02, entry_price * 1.03, entry_price * 1.04]
            stop_loss = entry_price * 0.99
            timeframe = "15m"
            achievement_time = None # يمكنك حسابها بناءً على البيانات التاريخية
            
            message = send_signal.format_signal_message(symbol, direction, entry_price, targets, stop_loss, timeframe, achievement_time)
            response = send_signal.send_telegram_message(bot_token, chat_id, message)
            print(response.json())

if __name__ == "__main__":
    main()
