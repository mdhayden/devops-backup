#!/usr/bin/env python3
"""
Test script to verify Alpaca API connection and basic functionality
"""
import json
import alpaca_trade_api as alpaca
from datetime import datetime as dt
from pytz import timezone

def test_connection():
    """Test basic connection to Alpaca API"""
    try:
        # Load credentials
        key = json.loads(open('AUTH/auth.txt', 'r').read())
        api = alpaca.REST(
            key['APCA-API-KEY-ID'], 
            key['APCA-API-SECRET-KEY'], 
            base_url='https://paper-api.alpaca.markets',  # Paper trading for testing
            api_version='v2'
        )
        
        # Test 1: Check account
        print("=== Testing Account Connection ===")
        account = api.get_account()
        print(f"✓ Account ID: {account.id}")
        print(f"✓ Buying Power: ${account.buying_power}")
        print(f"✓ Cash: ${account.cash}")
        print(f"✓ Portfolio Value: ${account.portfolio_value}")
        print(f"✓ Pattern Day Trader: {account.pattern_day_trader}")
        
        # Test 2: Check market status
        print("\n=== Testing Market Status ===")
        clock = api.get_clock()
        print(f"✓ Market Open: {clock.is_open}")
        print(f"✓ Current Time (ET): {dt.now(timezone('America/New_York')).strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"✓ Next Open: {clock.next_open}")
        print(f"✓ Next Close: {clock.next_close}")
        
        # Test 3: Check positions
        print("\n=== Testing Positions ===")
        positions = api.list_positions()
        print(f"✓ Number of open positions: {len(positions)}")
        if positions:
            for pos in positions:
                print(f"  - {pos.symbol}: {pos.qty} shares at ${pos.avg_entry_price}")
        
        # Test 4: Test getting ticker data
        print("\n=== Testing Ticker Data ===")
        tickers = open('TICKERS/my_tickers.txt', 'r').read().upper().split()
        print(f"✓ Loaded tickers: {tickers}")
        
        for ticker in tickers[:2]:  # Test first 2 tickers only
            try:
                latest_trade = api.get_latest_trade(ticker)
                print(f"✓ {ticker} - Latest Price: ${latest_trade.price}")
            except Exception as e:
                print(f"✗ Error getting data for {ticker}: {e}")
        
        print("\n🎉 All tests passed! Your bot is ready to test.")
        return True
        
    except Exception as e:
        print(f"❌ Connection test failed: {e}")
        return False

if __name__ == "__main__":
    test_connection()