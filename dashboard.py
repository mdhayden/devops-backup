#!/usr/bin/env python3
"""
Alpaca ROC Trading Bot Dashboard
Real-time monitoring and performance analytics
"""
import pandas as pd
import json
import os
import time
from datetime import datetime, timedelta
from pytz import timezone
import alpaca_trade_api as alpaca

class TradingBotDashboard:
    def __init__(self):
        self.load_config()
        self.et_tz = timezone('America/New_York')
    
    def load_config(self):
        """Load bot configuration"""
        try:
            key = json.loads(open('AUTH/auth.txt', 'r').read())
            self.api = alpaca.REST(
                key['APCA-API-KEY-ID'], 
                key['APCA-API-SECRET-KEY'], 
                base_url='https://paper-api.alpaca.markets', 
                api_version='v2'
            )
            
            with open('TICKERS/my_tickers.txt', 'r') as f:
                self.tickers = f.read().upper().split()
                
        except Exception as e:
            print(f"❌ Configuration error: {e}")
            self.api = None
            self.tickers = []
    
    def get_account_status(self):
        """Get current account information"""
        if not self.api:
            return None
            
        try:
            account = self.api.get_account()
            positions = self.api.list_positions()
            
            return {
                'cash': float(account.cash),
                'portfolio_value': float(account.portfolio_value),
                'buying_power': float(account.buying_power),
                'day_trade_count': account.daytrade_count,
                'pattern_day_trader': account.pattern_day_trader,
                'positions': len(positions),
                'current_positions': [
                    {
                        'symbol': pos.symbol,
                        'qty': float(pos.qty),
                        'market_value': float(pos.market_value),
                        'unrealized_pl': float(pos.unrealized_pl),
                        'unrealized_plpc': float(pos.unrealized_plpc) * 100
                    } for pos in positions
                ]
            }
        except Exception as e:
            print(f"❌ Account error: {e}")
            return None
    
    def get_trading_history(self):
        """Load and analyze trading history"""
        if not os.path.exists('Orders.csv'):
            return None
            
        try:
            df = pd.read_csv('Orders.csv')
            if 'Unnamed: 0' in df.columns:
                df = df.drop(columns=['Unnamed: 0'])
            
            if len(df) == 0:
                return None
                
            # Calculate metrics
            buys = df[df['Type'] == 'buy']
            sells = df[df['Type'] == 'sell']
            
            total_trades = len(df)
            total_buy_value = buys['Total'].sum() if len(buys) > 0 else 0
            total_sell_value = sells['Total'].sum() if len(sells) > 0 else 0
            
            # Calculate P&L if we have matched buy/sell pairs
            realized_pnl = total_sell_value - total_buy_value
            
            return {
                'total_trades': total_trades,
                'buy_orders': len(buys),
                'sell_orders': len(sells),
                'total_buy_value': total_buy_value,
                'total_sell_value': total_sell_value,
                'realized_pnl': realized_pnl,
                'recent_trades': df.tail(10).to_dict('records')
            }
            
        except Exception as e:
            print(f"❌ Trading history error: {e}")
            return None
    
    def get_market_status(self):
        """Get current market status"""
        if not self.api:
            return None
            
        try:
            clock = self.api.get_clock()
            current_time = datetime.now(self.et_tz)
            
            return {
                'is_open': clock.is_open,
                'current_time': current_time.strftime('%Y-%m-%d %H:%M:%S %Z'),
                'next_open': str(clock.next_open),
                'next_close': str(clock.next_close)
            }
        except Exception as e:
            print(f"❌ Market status error: {e}")
            return None
    
    def get_ticker_prices(self):
        """Get current prices for monitored tickers"""
        if not self.api or not self.tickers:
            return None
            
        prices = {}
        for ticker in self.tickers:
            try:
                trade = self.api.get_latest_trade(ticker)
                prices[ticker] = {
                    'price': float(trade.price),
                    'timestamp': str(trade.timestamp)
                }
            except Exception as e:
                prices[ticker] = {'error': str(e)}
        
        return prices
    
    def get_bot_status(self):
        """Check if bot has made first trade and current mode"""
        first_trade_exists = os.path.exists('FirstTrade.csv')
        
        status = {
            'first_trade_made': first_trade_exists,
            'mode': '1-minute analysis' if first_trade_exists else '30-minute analysis (first trade)',
            'data_files': []
        }
        
        # Check for recent data files
        if os.path.exists('tick_data'):
            for ticker in self.tickers:
                file_path = f'tick_data/{ticker}.csv'
                if os.path.exists(file_path):
                    mod_time = os.path.getmtime(file_path)
                    mod_datetime = datetime.fromtimestamp(mod_time)
                    status['data_files'].append({
                        'ticker': ticker,
                        'last_updated': mod_datetime.strftime('%Y-%m-%d %H:%M:%S')
                    })
        
        return status
    
    def print_market_status_section(self):
        """Print market status section"""
        print("🏛️  MARKET STATUS")
        print("-" * 20)
        market = self.get_market_status()
        if market:
            status_emoji = "🟢" if market['is_open'] else "🔴"
            print(f"{status_emoji} Market: {'OPEN' if market['is_open'] else 'CLOSED'}")
            if not market['is_open']:
                print(f"   Next Open: {market['next_open']}")
        else:
            print("❌ Unable to fetch market status")
        print()

    def print_account_status_section(self):
        """Print account status section"""
        print("💰 ACCOUNT STATUS")
        print("-" * 20)
        account = self.get_account_status()
        if account:
            print(f"💵 Cash: ${account['cash']:,.2f}")
            print(f"📊 Portfolio Value: ${account['portfolio_value']:,.2f}")
            print(f"⚡ Buying Power: ${account['buying_power']:,.2f}")
            print(f"📈 Day Trades: {account['day_trade_count']}/3")
            print(f"🚨 PDT Status: {'Yes' if account['pattern_day_trader'] else 'No'}")
            
            self.print_current_positions(account['current_positions'])
        else:
            print("❌ Unable to fetch account data")
        print()

    def print_current_positions(self, positions):
        """Print current positions subsection"""
        if positions:
            print(f"\n📍 Current Positions ({len(positions)}):")
            for pos in positions:
                pnl_emoji = "📈" if pos['unrealized_pl'] >= 0 else "📉"
                print(f"   {pnl_emoji} {pos['symbol']}: {pos['qty']:.2f} shares")
                print(f"      Value: ${pos['market_value']:,.2f}")
                print(f"      P&L: ${pos['unrealized_pl']:,.2f} ({pos['unrealized_plpc']:+.2f}%)")
        else:
            print("\n📍 No current positions")

    def print_bot_status_section(self):
        """Print bot status section"""
        print("🤖 BOT STATUS")
        print("-" * 20)
        bot_status = self.get_bot_status()
        print(f"🎯 Mode: {bot_status['mode']}")
        print(f"🏁 First Trade: {'Yes' if bot_status['first_trade_made'] else 'Pending'}")
        
        if bot_status['data_files']:
            print("\n📊 Recent Data Updates:")
            for file_info in bot_status['data_files']:
                print(f"   {file_info['ticker']}: {file_info['last_updated']}")
        print()

    def print_ticker_prices_section(self):
        """Print ticker prices section"""
        print("📈 TICKER PRICES")
        print("-" * 20)
        prices = self.get_ticker_prices()
        if prices:
            for ticker, data in prices.items():
                if 'error' not in data:
                    print(f"💹 {ticker}: ${data['price']:.2f}")
                else:
                    print(f"❌ {ticker}: {data['error']}")
        else:
            print("❌ Unable to fetch prices")
        print()

    def print_trading_history_section(self):
        """Print trading history section"""
        print("📋 TRADING HISTORY")
        print("-" * 20)
        history = self.get_trading_history()
        if history:
            print(f"📊 Total Trades: {history['total_trades']}")
            print(f"🛒 Buy Orders: {history['buy_orders']}")
            print(f"💰 Sell Orders: {history['sell_orders']}")
            print(f"💵 Total Bought: ${history['total_buy_value']:,.2f}")
            print(f"💰 Total Sold: ${history['total_sell_value']:,.2f}")
            
            pnl_emoji = "📈" if history['realized_pnl'] >= 0 else "📉"
            print(f"{pnl_emoji} Realized P&L: ${history['realized_pnl']:,.2f}")
            
            self.print_recent_trades(history['recent_trades'])
        else:
            print("📝 No trading history yet")

    def print_recent_trades(self, recent_trades):
        """Print recent trades subsection"""
        if recent_trades:
            print(f"\n🕐 Recent Trades ({min(5, len(recent_trades))}):")
            for trade in recent_trades[-5:]:
                trade_emoji = "🛒" if trade['Type'] == 'buy' else "💰"
                print(f"   {trade_emoji} {trade['Time']} - {trade['Type'].upper()} {trade['Ticker']}")
                print(f"      {trade['Quantity']:.2f} @ ${trade['Price']:.2f} = ${trade['Total']:,.2f}")

    def print_dashboard(self):
        """Display the complete dashboard with reduced complexity"""
        print("🤖 ALPACA ROC TRADING BOT DASHBOARD")
        print("=" * 60)
        
        # Current time
        current_time = datetime.now(self.et_tz)
        print(f"� Current Time (ET): {current_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # Print all sections
        self.print_market_status_section()
        self.print_account_status_section()
        self.print_bot_status_section()
        self.print_ticker_prices_section()
        self.print_trading_history_section()
        
        print("\n" + "=" * 60)
    
    def live_monitor(self, refresh_seconds=30):
        """Continuously update dashboard"""
        print("🔄 Starting live monitoring... (Press Ctrl+C to stop)")
        try:
            while True:
                os.system('cls' if os.name == 'nt' else 'clear')  # Clear screen
                self.print_dashboard()
                print(f"🔄 Refreshing in {refresh_seconds} seconds...")
                time.sleep(refresh_seconds)
        except KeyboardInterrupt:
            print("\n👋 Dashboard stopped")

def main():
    """Main dashboard function"""
    dashboard = TradingBotDashboard()
    
    print("Choose an option:")
    print("1. View dashboard once")
    print("2. Live monitoring (refreshes every 30 seconds)")
    print("3. Quick status check")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    if choice == "1":
        dashboard.print_dashboard()
    elif choice == "2":
        dashboard.live_monitor()
    elif choice == "3":
        # Quick status
        account = dashboard.get_account_status()
        market = dashboard.get_market_status()
        if account and market:
            status = "🟢 OPEN" if market['is_open'] else "🔴 CLOSED"
            print("\n📊 Quick Status:")
            print(f"   Market: {status}")
            print(f"   Cash: ${account['cash']:,.2f}")
            print(f"   Portfolio: ${account['portfolio_value']:,.2f}")
            print(f"   Positions: {account['positions']}")
        else:
            print("❌ Unable to fetch status")
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()