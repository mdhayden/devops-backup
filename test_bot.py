#!/usr/bin/env python3
"""
Test version of the main bot with enhanced logging and disabled email
This version shows what the bot is doing and skips email alerts for testing
"""
import pandas as pd
import datetime
from datetime import datetime as dt
from pytz import timezone
import time

import alpaca_trade_api as alpaca
import json

from datetime import timedelta
import os.path

# Load configuration
print("🤖 Starting Alpaca ROC Trading Bot (Test Mode)")
print("=" * 50)

try:
    key = json.loads(open('AUTH/auth.txt', 'r').read())
    api = alpaca.REST(key['APCA-API-KEY-ID'], key['APCA-API-SECRET-KEY'], base_url='https://paper-api.alpaca.markets', api_version = 'v2')
    tickers = open('TICKERS/my_tickers.txt', 'r').read()
    tickers = tickers.upper().split()
    global TICKERS 
    TICKERS = tickers
    print(f"✓ Loaded {len(tickers)} tickers: {tickers}")
except Exception as e:
    print(f"❌ Configuration error: {e}")
    exit(1)

def get_minute_data(tickers):
    print(f"📊 Fetching 1-minute data for {len(tickers)} tickers...")
    
    def save_min_data(ticker):
        try:
            prices = api.get_trades(str(ticker), start = ((dt.now().astimezone(timezone('America/New_York'))) - timedelta(minutes=2)).isoformat(),
                                            end = dt.now().astimezone(timezone('America/New_York')).isoformat(), 
                                            limit = 10000).df[['price']]
            prices.index = pd.to_datetime(prices.index, format = '%Y-%m-%d').strftime('%Y-%m-%d %H:%M')
            prices = prices[~prices.index.duplicated(keep='first')]

            quotes = api.get_quotes(str(ticker), start = ((dt.now().astimezone(timezone('America/New_York'))) - timedelta(minutes=2)).isoformat(),
                                            end = dt.now().astimezone(timezone('America/New_York')).isoformat(), 
                                            limit = 10000).df[['ask_price']]
            quotes.index = pd.to_datetime(quotes.index, format = '%Y-%m-%d').strftime('%Y-%m-%d %H:%M')
            quotes = quotes[~quotes.index.duplicated(keep='first')]

            df = pd.merge(prices, quotes, how='inner', left_index=True, right_index=True, on=None, validate='one_to_one')
            df.to_csv('tick_data/{}.csv'.format(ticker))
            print(f"  ✓ {ticker}: {len(df)} data points")
        except Exception as e:
            print(f"  ✗ {ticker}: Error - {e}")
        
    for ticker in tickers:
        save_min_data(ticker)

def get_past30_data(tickers):
    print(f"📊 Fetching 30-minute data for {len(tickers)} tickers...")
    
    def save_30_data(ticker):
        try:
            prices_1 = api.get_trades(str(ticker), start = ((dt.now().astimezone(timezone('America/New_York'))) - timedelta(minutes=30)).isoformat(),
                                            end = ((dt.now().astimezone(timezone('America/New_York'))) - timedelta(minutes=28, seconds = 30)).isoformat(), 
                                            limit = 10000).df[['price']]
            prices_2 = api.get_trades(str(ticker), start = ((dt.now().astimezone(timezone('America/New_York'))) - timedelta(minutes=1, seconds = 30)).isoformat(),
                                            end = dt.now().astimezone(timezone('America/New_York')).isoformat(), 
                                            limit = 10000).df[['price']]
            
            prices_1.index = pd.to_datetime(prices_1.index, format = '%Y-%m-%d').strftime('%Y-%m-%d %H:%M')
            prices_2.index = pd.to_datetime(prices_2.index, format = '%Y-%m-%d').strftime('%Y-%m-%d %H:%M')
            
            prices = pd.concat([prices_1, prices_2])
            prices = prices[~prices.index.duplicated(keep='first')]

            quotes_1 = api.get_quotes(str(ticker), start = ((dt.now().astimezone(timezone('America/New_York'))) - timedelta(minutes=30)).isoformat(),
                                            end = ((dt.now().astimezone(timezone('America/New_York'))) - timedelta(minutes=28, seconds = 30)).isoformat(), 
                                            limit = 10000).df[['ask_price']]
            quotes_2 = api.get_quotes(str(ticker), start = ((dt.now().astimezone(timezone('America/New_York'))) - timedelta(minutes=1, seconds = 30)).isoformat(),
                                            end = dt.now().astimezone(timezone('America/New_York')).isoformat(), 
                                            limit = 10000).df[['ask_price']]
            
            quotes_1.index = pd.to_datetime(quotes_1.index, format = '%Y-%m-%d').strftime('%Y-%m-%d %H:%M')
            quotes_2.index = pd.to_datetime(quotes_2.index, format = '%Y-%m-%d').strftime('%Y-%m-%d %H:%M')
            
            quotes = pd.concat([quotes_1, quotes_2])
            quotes = quotes[~quotes.index.duplicated(keep='first')]
            
            df = pd.merge(prices, quotes, how='inner', left_index=True, right_index=True, on=None, validate='one_to_one')
            df.to_csv('tick_data/{}.csv'.format(ticker))
            print(f"  ✓ {ticker}: {len(df)} data points")
        except Exception as e:
            print(f"  ✗ {ticker}: Error - {e}")
    
    for ticker in tickers:
        save_30_data(ticker)

def calculate_roc(ask, timeframe):
        if timeframe == 30:
            rocs = (ask[ask.shape[0] - 1] - ask[0])/(ask[0])
        else:
            rocs = (ask[ask.shape[0] - 1] - ask[ask.shape[0] -2])/(ask[ask.shape[0] - 2])
        return rocs*1000

def get_roc_list(tickers, timeframe):
    roc_tickers = []
    print(f"🧮 Calculating ROC for {timeframe}-min timeframe:")
    for i in range(len(tickers)):
        try:
            df = pd.read_csv('tick_data/{}.csv'.format(tickers[i]))
            df.set_index('timestamp', inplace= True)
            df.index = pd.to_datetime(df.index, format ='%Y-%m-%d').strftime('%Y-%m-%d %H:%M')
            roc = calculate_roc(df['ask_price'], timeframe)
            roc_tickers.append(roc)
            print(f"  {tickers[i]}: {roc:.2f}")
        except Exception as e:
            print(f"  ✗ {tickers[i]}: Error - {e}")
            roc_tickers.append(0)
    return roc_tickers

def check_buy_condition(ticker):
    """Check if ticker meets buy condition (ask > price)"""
    try:
        df = pd.read_csv('tick_data/{}.csv'.format(ticker))
        df.set_index('timestamp', inplace=True)
        df.index = pd.to_datetime(df.index, format='%Y-%m-%d').strftime('%Y-%m-%d %H:%M')

        buy_condition = []
        ask_col = df.columns.get_loc('ask_price')
        price_col = df.columns.get_loc('price')
        for i in range(df.shape[0] - 2, df.shape[0]):
            buy_condition.append(df.iloc[i, ask_col] > df.iloc[i, price_col])

        latest_ask = df.iloc[-1, ask_col]
        latest_price = df.iloc[-1, price_col]
        
        print(f"  {ticker}: Ask=${latest_ask:.2f}, Price=${latest_price:.2f}, Condition: {buy_condition[-1]}")
        
        return buy_condition[-1], latest_ask, latest_price
    except Exception as e:
        print(f"  ✗ {ticker}: Error - {e}")
        return False, 0, 0

def find_best_stock(tickers, rocs):
    """Find the best stock that meets buy conditions"""
    max_roc = max(rocs)
    if max_roc <= 0:
        print("❌ All ROCs are <= 0")
        return None
    
    while len(tickers) > 0:
        max_roc_index = rocs.index(max_roc)
        buy_stock_candidate = tickers[max_roc_index]
        
        buy_condition, _, _ = check_buy_condition(buy_stock_candidate)
        
        if buy_condition:
            print(f"✅ Selected: {buy_stock_candidate}")
            return buy_stock_candidate
        else:
            tickers.pop(max_roc_index)
            rocs.pop(max_roc_index)
            if len(tickers) == 0:
                print("❌ No stocks meet Ask > LTP criteria")
                return None
            max_roc = max(rocs)
    
    return None

def compare_ask_ltp(tickers, timeframe):
    if len(tickers) == 0:
        return TICKERS
        
    rocs = get_roc_list(tickers, timeframe)
    
    print("🎯 Checking stocks in ROC order...")
    
    result = find_best_stock(tickers.copy(), rocs.copy())
    return result if result is not None else -1

def stock_to_buy(tickers, timeframe):
        entry_buy = compare_ask_ltp(tickers, timeframe)
        return entry_buy

def algo(tickers):
    if os.path.isfile('FirstTrade.csv'):
        timeframe = 1
        print("📈 Using 1-minute timeframe (subsequent trades)")
    else:
        timeframe = 30
        print("📈 Using 30-minute timeframe (first trade)")
    
    stock = stock_to_buy(tickers, timeframe)
    return stock

def test_main():
    print(f"🕐 Current ET time: {dt.now(timezone('America/New_York')).strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Check account
    account = api.get_account()
    print(f"💰 Account balance: ${account.cash}")
    print(f"📊 Portfolio value: ${account.portfolio_value}")
    
    # Check market status
    market_open = api.get_clock().is_open
    print(f"🏛️ Market open: {market_open}")
    
    if not market_open:
        print("⏳ Market is closed. Bot would normally wait for market to open.")
        print("   For testing, let's simulate what happens when market opens...")
        
        # Simulate first trade logic
        if not os.path.isfile('FirstTrade.csv'):
            print("\n🎯 Simulating FIRST TRADE logic:")
            print("   - Would wait until 10:00 AM ET")
            print("   - Would fetch 30-minute historical data")
            print("   - Would calculate ROC and select stock")
            
            # Try to get some data for demonstration
            try:
                print("\n📊 Testing data retrieval...")
                latest_aapl = api.get_latest_trade('AAPL')
                print(f"   AAPL latest price: ${latest_aapl.price}")
                
                latest_amzn = api.get_latest_trade('AMZN') 
                print(f"   AMZN latest price: ${latest_amzn.price}")
                
                print("✅ Data retrieval working!")
                
            except Exception as e:
                print(f"❌ Data retrieval error: {e}")
        else:
            print("\n🔄 Simulating SUBSEQUENT TRADE logic:")
            print("   - Would fetch 1-minute data every few seconds")
            print("   - Would calculate ROC and look for trades")
    
    else:
        print("🟢 Market is open! Running actual trading logic...")
        # Run the actual algorithm when market is open
        stock = algo(TICKERS)
        print(f"🎯 Algorithm result: {stock}")
    
    print("\n✅ Test completed successfully!")
    print("💡 To run the full bot during market hours, use: python main.py")

if __name__ == '__main__':
    try:
        test_main()
    except KeyboardInterrupt:
        print("\n👋 Bot stopped by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()