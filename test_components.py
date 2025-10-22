#!/usr/bin/env python3
"""
Component testing script for the Alpaca ROC Trading Bot
This script tests individual functions without placing real trades
"""
import pandas as pd
import numpy as np
from datetime import datetime as dt, timedelta
from pytz import timezone
import json
import sys
import os

# Mock data for testing when market is closed or API issues
class MockAPI:
    def __init__(self):
        self.positions = []
        self.account_cash = 10000.0
        
    def get_latest_trade(self, symbol):
        class MockTrade:
            price = 150.0 + np.random.random() * 10  # Random price between 150-160
        return MockTrade()
    
    def get_account(self):
        class MockAccount:
            cash = 10000.0
            pattern_day_trader = False
        return MockAccount()
    
    def get_clock(self):
        class MockClock:
            is_open = True
        return MockClock()

def create_test_data():
    """Create sample CSV data for testing ROC calculations"""
    print("=== Creating Test Data ===")
    
    if not os.path.exists('tick_data'):
        os.makedirs('tick_data')
    
    tickers = ['AAPL', 'AMZN', 'TSLA', 'MA']
    
    for ticker in tickers:
        # Create sample price data with different ROC patterns
        timestamps = pd.date_range(
            start=dt.now() - timedelta(minutes=30), 
            end=dt.now(), 
            freq='1T'
        )
        
        # Generate different price patterns for testing
        if ticker == 'AAPL':
            # Upward trend (positive ROC)
            prices = np.linspace(150, 155, len(timestamps)) + np.random.normal(0, 0.5, len(timestamps))
            ask_prices = prices + np.random.uniform(0.01, 0.05, len(timestamps))
        elif ticker == 'TSLA':
            # High volatility (high ROC potential)
            prices = 200 + 10 * np.sin(np.linspace(0, 4*np.pi, len(timestamps))) + np.random.normal(0, 2, len(timestamps))
            ask_prices = prices + np.random.uniform(0.05, 0.15, len(timestamps))
        else:
            # More stable prices
            prices = 100 + np.random.normal(0, 1, len(timestamps))
            ask_prices = prices + np.random.uniform(0.01, 0.03, len(timestamps))
        
        df = pd.DataFrame({
            'timestamp': timestamps.strftime('%Y-%m-%d %H:%M'),
            'price': prices,
            'ask_price': ask_prices
        })
        
        df.to_csv(f'tick_data/{ticker}.csv', index=False)
        print(f"✓ Created test data for {ticker}")
    
    print(f"✓ Test data created for {len(tickers)} tickers\n")

def test_roc_calculation():
    """Test ROC calculation function"""
    print("=== Testing ROC Calculation ===")
    
    # Test with sample data
    ask_prices = pd.Series([100, 101, 102, 105, 103])
    
    def ROC(ask, timeframe):
        if timeframe == 30:
            rocs = (ask.iloc[-1] - ask.iloc[0]) / ask.iloc[0]
        else:
            rocs = (ask.iloc[-1] - ask.iloc[-2]) / ask.iloc[-2]
        return rocs * 1000
    
    roc_30 = ROC(ask_prices, 30)
    roc_1 = ROC(ask_prices, 1)
    
    print(f"✓ ROC (30-min): {roc_30:.2f}")
    print(f"✓ ROC (1-min): {roc_1:.2f}")
    print()

def test_stock_selection():
    """Test the stock selection algorithm"""
    print("=== Testing Stock Selection Algorithm ===")
    
    create_test_data()
    
    tickers = ['AAPL', 'AMZN', 'TSLA', 'MA']
    
    def ROC(ask, timeframe):
        if timeframe == 30:
            rocs = (ask.iloc[-1] - ask.iloc[0]) / ask.iloc[0]
        else:
            rocs = (ask.iloc[-1] - ask.iloc[-2]) / ask.iloc[-2]
        return rocs * 1000
    
    def return_ROC_list(tickers, timeframe):
        ROC_tickers = []
        for ticker in tickers:
            try:
                df = pd.read_csv(f'tick_data/{ticker}.csv')
                df.set_index('timestamp', inplace=True)
                roc = ROC(df['ask_price'], timeframe)
                ROC_tickers.append(roc)
                print(f"  {ticker}: ROC = {roc:.2f}")
            except Exception as e:
                print(f"  ✗ Error processing {ticker}: {e}")
                ROC_tickers.append(0)
        return ROC_tickers
    
    print("ROC calculations for all tickers:")
    rocs = return_ROC_list(tickers, 1)
    
    if rocs:
        max_roc = max(rocs)
        max_roc_ticker = tickers[rocs.index(max_roc)]
        print(f"\n✓ Highest ROC: {max_roc_ticker} with {max_roc:.2f}")
    else:
        print("✗ No valid ROC calculations")
    
    print()

def test_ask_vs_ltp():
    """Test ask vs last traded price comparison"""
    print("=== Testing Ask vs LTP Comparison ===")
    
    for ticker in ['AAPL', 'AMZN']:
        try:
            df = pd.read_csv(f'tick_data/{ticker}.csv')
            df.set_index('timestamp', inplace=True)
            
            latest_ask = df['ask_price'].iloc[-1]
            latest_price = df['price'].iloc[-1]
            
            condition = latest_ask > latest_price
            print(f"  {ticker}: Ask=${latest_ask:.2f}, Price=${latest_price:.2f}, Buy Condition: {condition}")
            
        except Exception as e:
            print(f"  ✗ Error processing {ticker}: {e}")
    
    print()

def dry_run_test():
    """Simulate a complete trading cycle without placing orders"""
    print("=== Dry Run Test (No Real Orders) ===")
    
    # Use mock API to simulate trading logic
    mock_api = MockAPI()
    
    tickers = ['AAPL', 'AMZN', 'TSLA', 'MA']
    
    print("1. Checking market status...")
    print(f"   Market is open: {mock_api.get_clock().is_open}")
    
    print("2. Checking account balance...")
    print(f"   Available cash: ${mock_api.get_account().cash}")
    
    print("3. Checking current positions...")
    print(f"   Current positions: {len(mock_api.positions)}")
    
    print("4. Simulating stock selection...")
    # This would normally call your algo() function
    selected_stock = "AAPL"  # Mock selection
    latest_price = mock_api.get_latest_trade(selected_stock).price
    
    print(f"   Selected stock: {selected_stock}")
    print(f"   Current price: ${latest_price:.2f}")
    
    print("5. Simulating order calculation...")
    position_size = mock_api.get_account().cash / latest_price
    total_cost = position_size * latest_price
    
    print(f"   Position size: {position_size:.2f} shares")
    print(f"   Total cost: ${total_cost:.2f}")
    
    print("✓ Dry run completed successfully - No orders placed")
    print()

def main():
    """Run all tests"""
    print("🤖 Alpaca ROC Trading Bot - Test Suite")
    print("=" * 50)
    
    try:
        test_roc_calculation()
        test_stock_selection()
        test_ask_vs_ltp()
        dry_run_test()
        
        print("🎉 All component tests completed!")
        print("\nNext steps:")
        print("1. Fix API credentials in AUTH/auth.txt")
        print("2. Verify paper trading account is active")
        print("3. Test during market hours for real data")
        print("4. Start with small amounts for live testing")
        
    except Exception as e:
        print(f"❌ Test suite failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()