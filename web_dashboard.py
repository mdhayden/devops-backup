#!/usr/bin/env python3
"""
Web-based Dashboard for Alpaca ROC Trading Bot
Simple HTML dashboard that auto-refreshes
"""
import json
import os
import time
from datetime import datetime
from pytz import timezone
import pandas as pd
import alpaca_trade_api as alpaca
import webbrowser
from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading

def load_configuration():
    """Load API configuration and tickers"""
    try:
        key = json.loads(open('AUTH/auth.txt', 'r').read())
        api = alpaca.REST(
            key['APCA-API-KEY-ID'], 
            key['APCA-API-SECRET-KEY'], 
            base_url='https://paper-api.alpaca.markets', 
            api_version='v2'
        )
        
        with open('TICKERS/my_tickers.txt', 'r') as f:
            tickers = f.read().upper().split()
        
        return api, tickers
    except Exception:
        return None, None

def get_ticker_prices(api, tickers):
    """Get current prices for all tickers"""
    ticker_data = []
    for ticker in tickers:
        try:
            trade = api.get_latest_trade(ticker)
            ticker_data.append({
                'symbol': ticker,
                'price': float(trade.price),
                'timestamp': str(trade.timestamp)
            })
        except Exception:
            ticker_data.append({
                'symbol': ticker,
                'price': 'Error',
                'timestamp': 'N/A'
            })
    return ticker_data

def get_trading_history():
    """Get trading history from Orders.csv"""
    trading_history = []
    if os.path.exists('Orders.csv'):
        try:
            df = pd.read_csv('Orders.csv')
            if 'Unnamed: 0' in df.columns:
                df = df.drop(columns=['Unnamed: 0'])
            trading_history = df.tail(10).to_dict('records')
        except Exception:
            pass
    return trading_history

def get_bot_status():
    """Get current bot status"""
    first_trade_made = os.path.exists('FirstTrade.csv')
    bot_mode = '1-minute analysis' if first_trade_made else '30-minute analysis (first trade)'
    return first_trade_made, bot_mode

def generate_main_dashboard_html(current_time, clock, account, positions, bot_mode, first_trade_made, ticker_data, trading_history):
    """Generate the main dashboard HTML structure"""
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Alpaca ROC Trading Bot Dashboard</title>
        <meta charset="UTF-8">
        <meta http-equiv="refresh" content="30">
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 0;
                padding: 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                min-height: 100vh;
            }}
            .container {{
                max-width: 1200px;
                margin: 0 auto;
            }}
            .header {{
                text-align: center;
                margin-bottom: 30px;
            }}
            .dashboard-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 20px;
                margin-bottom: 30px;
            }}
            .card {{
                background: rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(10px);
                border-radius: 15px;
                padding: 20px;
                border: 1px solid rgba(255, 255, 255, 0.2);
            }}
            .card h3 {{
                margin-top: 0;
                color: #ffd700;
                border-bottom: 2px solid #ffd700;
                padding-bottom: 10px;
            }}
            .status-open {{ color: #4ade80; }}
            .status-closed {{ color: #f87171; }}
            .positive {{ color: #4ade80; }}
            .negative {{ color: #f87171; }}
            .metric {{
                display: flex;
                justify-content: space-between;
                margin: 10px 0;
                padding: 8px 0;
                border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            }}
            .metric:last-child {{
                border-bottom: none;
            }}
            .ticker-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
                gap: 10px;
            }}
            .ticker-card {{
                background: rgba(255, 255, 255, 0.05);
                padding: 10px;
                border-radius: 8px;
                text-align: center;
            }}
            .refresh-info {{
                text-align: center;
                margin-top: 20px;
                opacity: 0.7;
                font-size: 0.9em;
            }}
            .trade-table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 10px;
            }}
            .trade-table th, .trade-table td {{
                padding: 8px;
                text-align: left;
                border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            }}
            .trade-table th {{
                background: rgba(255, 255, 255, 0.1);
            }}
            .buy {{ color: #4ade80; }}
            .sell {{ color: #f87171; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🤖 Alpaca ROC Trading Bot Dashboard</h1>
                <p>Last Updated: {current_time.strftime('%Y-%m-%d %H:%M:%S ET')}</p>
            </div>
            
            <div class="dashboard-grid">
                <!-- Market Status -->
                <div class="card">
                    <h3>🏛️ Market Status</h3>
                    <div class="metric">
                        <span>Status:</span>
                        <span class="{'status-open' if clock.is_open else 'status-closed'}">
                            {'🟢 OPEN' if clock.is_open else '🔴 CLOSED'}
                        </span>
                    </div>
                    <div class="metric">
                        <span>Next Open:</span>
                        <span>{clock.next_open}</span>
                    </div>
                </div>
                
                <!-- Account Status -->
                <div class="card">
                    <h3>💰 Account Status</h3>
                    <div class="metric">
                        <span>Cash:</span>
                        <span>${float(account.cash):,.2f}</span>
                    </div>
                    <div class="metric">
                        <span>Portfolio Value:</span>
                        <span>${float(account.portfolio_value):,.2f}</span>
                    </div>
                    <div class="metric">
                        <span>Buying Power:</span>
                        <span>${float(account.buying_power):,.2f}</span>
                    </div>
                    <div class="metric">
                        <span>Day Trades:</span>
                        <span>{account.daytrade_count}/3</span>
                    </div>
                    <div class="metric">
                        <span>Positions:</span>
                        <span>{len(positions)}</span>
                    </div>
                </div>
                
                <!-- Bot Status -->
                <div class="card">
                    <h3>🤖 Bot Status</h3>
                    <div class="metric">
                        <span>Mode:</span>
                        <span>{bot_mode}</span>
                    </div>
                    <div class="metric">
                        <span>First Trade:</span>
                        <span>{'✅ Yes' if first_trade_made else '⏳ Pending'}</span>
                    </div>
                    <div class="metric">
                        <span>Pattern Day Trader:</span>
                        <span class="{'negative' if account.pattern_day_trader else 'positive'}">
                            {'❌ Yes' if account.pattern_day_trader else '✅ No'}
                        </span>
                    </div>
                </div>
            </div>
            
            <!-- Current Positions -->
            {generate_positions_html(positions)}
            
            <!-- Ticker Prices -->
            <div class="card">
                <h3>📈 Ticker Prices</h3>
                <div class="ticker-grid">
                    {generate_tickers_html(ticker_data)}
                </div>
            </div>
            
            <!-- Trading History -->
            {generate_history_html(trading_history)}
            
            <div class="refresh-info">
                🔄 Dashboard auto-refreshes every 30 seconds<br>
                🤖 Bot data updates when market is open
            </div>
        </div>
    </body>
    </html>
    """

def generate_dashboard_html():
    """Generate HTML dashboard with reduced complexity"""
    # Load configuration
    api, tickers = load_configuration()
    if api is None:
        return "<h1>Configuration Error</h1>"
    
    # Get data
    try:
        account = api.get_account()
        clock = api.get_clock()
        positions = api.list_positions()
        et_tz = timezone('America/New_York')
        current_time = datetime.now(et_tz)
        
        ticker_data = get_ticker_prices(api, tickers)
        trading_history = get_trading_history()
        first_trade_made, bot_mode = get_bot_status()
        
        return generate_main_dashboard_html(
            current_time, clock, account, positions, 
            bot_mode, first_trade_made, ticker_data, trading_history
        )
        
    except Exception as e:
        return f"<h1>API Error: {e}</h1>"

def generate_positions_html(positions):
    """Generate positions section"""
    if not positions:
        return ""
    
    html = '<div class="card"><h3>📍 Current Positions</h3>'
    for pos in positions:
        pnl_class = "positive" if float(pos.unrealized_pl) >= 0 else "negative"
        pnl_emoji = "📈" if float(pos.unrealized_pl) >= 0 else "📉"
        html += f'''
        <div class="metric">
            <span>{pnl_emoji} {pos.symbol} ({pos.qty} shares)</span>
            <span class="{pnl_class}">${float(pos.unrealized_pl):,.2f} ({float(pos.unrealized_plpc)*100:+.2f}%)</span>
        </div>
        '''
    html += '</div>'
    return html

def generate_tickers_html(ticker_data):
    """Generate ticker prices HTML"""
    html = ""
    for ticker in ticker_data:
        if ticker['price'] != 'Error':
            html += f'''
            <div class="ticker-card">
                <div style="font-weight: bold;">{ticker['symbol']}</div>
                <div style="font-size: 1.2em; color: #ffd700;">${ticker['price']:.2f}</div>
            </div>
            '''
        else:
            html += f'''
            <div class="ticker-card">
                <div style="font-weight: bold;">{ticker['symbol']}</div>
                <div style="color: #f87171;">Error</div>
            </div>
            '''
    return html

def generate_history_html(trading_history):
    """Generate trading history HTML"""
    if not trading_history:
        return '<div class="card"><h3>📋 Trading History</h3><p>No trades yet</p></div>'
    
    html = '<div class="card"><h3>📋 Recent Trading History</h3>'
    html += '''
    <table class="trade-table">
        <tr>
            <th>Time</th>
            <th>Type</th>
            <th>Ticker</th>
            <th>Quantity</th>
            <th>Price</th>
            <th>Total</th>
        </tr>
    '''
    
    for trade in trading_history[-10:]:  # Last 10 trades
        trade_class = "buy" if trade['Type'] == 'buy' else "sell"
        html += f'''
        <tr>
            <td>{trade['Time']}</td>
            <td class="{trade_class}">{trade['Type'].upper()}</td>
            <td>{trade['Ticker']}</td>
            <td>{trade['Quantity']:.2f}</td>
            <td>${trade['Price']:.2f}</td>
            <td>${trade['Total']:,.2f}</td>
        </tr>
        '''
    
    html += '</table></div>'
    return html

def create_web_dashboard():
    """Create and serve web dashboard"""
    print("🌐 Creating web dashboard...")
    
    # Generate HTML
    html_content = generate_dashboard_html()
    
    # Save to file
    with open('dashboard.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("✅ Dashboard created: dashboard.html")
    print("🌐 Opening in browser...")
    
    # Open in browser
    webbrowser.open('dashboard.html')
    
    return html_content

if __name__ == "__main__":
    create_web_dashboard()