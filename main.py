# import requests
# import time
# import pandas as pd
# import threading
# from flask import Flask
# import logging

# # Set up logging to ensure all logs are shown
# logging.basicConfig(level=logging.DEBUG)

# app = Flask(__name__)

# # Moving Average Class
# class MovingAverage:
#     def __init__(self, index, close_ma, volume_ma):
#         self.index = index
#         self.close_ma = close_ma
#         self.volume_ma = volume_ma

# # Function to calculate Simple Moving Average (SMA)
# def calculate_ma(candles_ob, close_period, volume_period):
#     ma_list = []
#     for i in range(len(candles_ob)):
#         close_ma = sum(candle.close for candle in candles_ob[max(0, i - close_period + 1): i + 1]) / min(close_period, i + 1)
#         volume_ma = sum(candle.volume for candle in candles_ob[max(0, i - volume_period + 1): i + 1]) / min(volume_period, i + 1)
#         ma_list.append(MovingAverage(index=candles_ob[i].index, close_ma=close_ma, volume_ma=volume_ma))
#     return ma_list

# # Golden Area Classes
# class GoldAreaEndState:
#     END = "Ended"
#     NOT_END = "Not Ended"

# class GoldAreaType:
#     BULLISH = "bullish"
#     BEARISH = "bearish"

# class GoldArea:
#     def __init__(self, candle, area_type, end_state, end_candle=None):
#         self.type = area_type
#         self.candle = candle
#         self.end_state = end_state
#         self.end_candle = end_candle

# # Check if gold area has ended
# def check_gold_end_state(candle, candles_ob, area_type):
#     invalidation = candle.low if area_type == GoldAreaType.BULLISH else candle.high
#     for i in range(candle.index + 1, len(candles_ob)):
#         if (area_type == GoldAreaType.BULLISH and candles_ob[i].close < invalidation) or \
#            (area_type == GoldAreaType.BEARISH and candles_ob[i].close > invalidation):
#             return GoldAreaEndState.END, candles_ob[i]
#     return GoldAreaEndState.NOT_END, None

# # Identify golden areas
# def get_gold_area(candles_ob, ma_list):
#     gold_areas = []
#     for candle_index in range(50, len(candles_ob) - 1):
#         candle = candles_ob[candle_index]
#         if candle.volume > ma_list[candle_index].volume_ma and candles_ob[candle_index + 1].volume > ma_list[candle_index + 1].volume_ma:
#             if candle.low < candles_ob[candle_index - 1].low < candles_ob[candle_index - 2].low and candle.low < candles_ob[candle_index + 1].low:
#                 if candle.high < ma_list[candle_index].close_ma and candles_ob[candle_index + 1].close > ma_list[candle_index + 1].close_ma:
#                     area_type = GoldAreaType.BULLISH
#                     end_state, end_candle = check_gold_end_state(candle, candles_ob, area_type)
#                     gold_areas.append(GoldArea(candle, area_type, end_state, end_candle))
#     return gold_areas

# # Check if price is in a golden area
# def is_price_in_gold_area(candle, gold_areas):
#     for area in gold_areas:
#         if area.end_state == GoldAreaEndState.NOT_END and area.candle.low < candle.close < area.candle.high:
#             return True, area
#     return False, None

# # Candle Class
# class Candle:
#     def __init__(self, timestamp, open, high, low, close, volume, index):
#         self.timestamp = timestamp
#         self.open = float(open)
#         self.high = float(high)
#         self.low = float(low)
#         self.close = float(close)
#         self.volume = float(volume)
#         self.date = pd.to_datetime(timestamp, unit='ms')
#         self.index = index

# # Fetch Binance Data
# def fetch_binance_data(symbol, interval, limit=1000):
#     url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}"
#     response = requests.get(url)
#     if response.status_code == 200:
#         return [Candle(*entry[:6], index) for index, entry in enumerate(response.json())]
#     return []
# def fetch_binance_symbols():
#     url = "https://api.binance.com/api/v3/exchangeInfo"
    
#     # Retry 3 times in case of failure
#     for _ in range(3):
#         response = requests.get(url)
        
#         if response.status_code == 200:
#             return [s['symbol'] for s in response.json()['symbols'] if 'USDT' in s['symbol']]
        
#         # Log the error and retry
#         print(f"Failed to fetch Binance symbols: {response.status_code} - {response.text}")
#         time.sleep(5)  # Wait for 5 seconds before retrying

#     return []
# # ===> Telegram Bot Code  
# def telegram_bot_sendtext(bot_message):
#     bot_token = '7174908289:AAHdD6zn-t4IBDd6V1Vr6Zg0D71bWOVLbGI'
#     bot_chatID = '@SAMSRA_COMPANY'
#     # https://t.me/SAMSRA_COMPANY/
#     send_text = f'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={bot_chatID}&parse_mode=Markdown&text={bot_message}'

#     response = requests.get(send_text)
#     return response.json()

# # Main Trading Bot Logic
# def trading_bot():
#     HIGHER_TIMEFRAME = "4h"
#     LOWER_TIMEFRAME = "15m"
    
#     while True:
#         logging.info("Fetching Binance symbols...")
#         coin_list = fetch_binance_symbols()
#         for symbol in coin_list:
#             telegram_bot_sendtext(symbol)
#             logging.info(f"Processing {symbol} on {HIGHER_TIMEFRAME} timeframe...")
#             candles_high_tf = fetch_binance_data(symbol, HIGHER_TIMEFRAME)
#             if candles_high_tf:
#                 ma_list_high = calculate_ma(candles_high_tf, 14, 20)
#                 gold_areas_high = get_gold_area(candles_high_tf, ma_list_high)
#                 is_in_gold, gold_area_high = is_price_in_gold_area(candles_high_tf[-1], gold_areas_high)
#                 if is_in_gold and gold_area_high.type == GoldAreaType.BULLISH:
#                     message = f"{symbol} IN Buy ZONE on {HIGHER_TIMEFRAME}"
#                     print(message)
#                     logging.info(message)
#                     telegram_bot_sendtext(message)
#                     logging.info(f"Fetching {symbol} data for {LOWER_TIMEFRAME} timeframe...")
#                     candles_low_tf = fetch_binance_data(symbol, LOWER_TIMEFRAME)[:-1]
#                     if candles_low_tf:
#                         ma_list_low = calculate_ma(candles_low_tf, 14, 20)
#                         gold_areas_low = get_gold_area(candles_low_tf, ma_list_low)
#                         is_new_gold, new_gold_area_low = is_price_in_gold_area(candles_low_tf[-1], gold_areas_low)
#                         if is_new_gold and new_gold_area_low.type == GoldAreaType.BULLISH:
#                             message = f"{symbol} Alert: BUY SIGNAL\nBuy Market Now \nSL: Close under {new_gold_area_low.candle.low}"
#                             logging.info(message)
#                             telegram_bot_sendtext(message)
# # Run the bot in a separate thread
# threading.Thread(target=trading_bot, daemon=True).start()

# # Flask Web App
# @app.route('/')
# def home():
#     return "Trading bot is running!"

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=10000)

import requests

def fetch_coingecko_symbols():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        'vs_currency': 'usd',  # You can specify other currencies if needed
        'order': 'market_cap_desc',  # Sorting order by market cap
        'per_page': 100,  # Number of results to return
        'page': 1,  # Page number
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        return [coin['id'] for coin in response.json()]
    else:
        print(f"Error fetching data: {response.status_code}")
        return []

# Fetch the symbols from CoinGecko
symbols = fetch_coingecko_symbols()
print(symbols)


