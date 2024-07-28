import requests

def send_telegram_message(bot_token, chat_id, message):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'Markdown'
    }
    response = requests.post(url, json=payload)
    return response

def format_signal_message(symbol, direction, entry_price, targets, stop_loss, timeframe, achievement_time=None):
    message = f"*{symbol}*\n"
    message += f"*Direction:* {direction}\n"
    message += f"*Entry Price:* {entry_price}\n"
    message += "*Targets:*\n"
    for i, target in enumerate(targets, 1):
        message += f"  - Target {i}: {target}\n"
    message += f"*Stop Loss:* {stop_loss}\n"
    message += f"*Timeframe:* {timeframe}\n"
    if achievement_time:
        message += f"*Achievement Time:* {achievement_time}\n"
    return message

if __name__ == "__main__":
    bot_token = "YOUR_TELEGRAM_BOT_TOKEN"
    chat_id = "YOUR_TELEGRAM_CHAT_ID"
    symbol = "BTC/USDT"
    direction = "Buy"
    entry_price = 50000
    targets = [50500, 51000, 51500, 52000]
    stop_loss = 49500
    timeframe = "15m"
    achievement_time = "1h 30m"
    
    message = format_signal_message(symbol, direction, entry_price, targets, stop_loss, timeframe, achievement_time)
    response = send_telegram_message(bot_token, chat_id, message)
    print(response.json())
