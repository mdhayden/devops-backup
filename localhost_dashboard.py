#!/usr/bin/env python3
"""
Local Web Server Dashboard for Alpaca ROC Trading Bot
Runs on http://localhost:8080 with real-time updates
"""
import json
import os
import time
import threading
from datetime import datetime
from pytz import timezone
import pandas as pd
import alpaca_trade_api as alpaca
from http.server import HTTPServer, BaseHTTPRequestHandler
import webbrowser
import urllib.parse

# Constants
ORDERS_CSV_FILE = 'Orders.csv'
UNNAMED_COLUMN = 'Unnamed: 0'

class DashboardHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '/dashboard':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            html = self.generate_dashboard_html()
            self.wfile.write(html.encode('utf-8'))
        
        elif self.path == '/api/status':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            status_data = self.get_bot_status_json()
            self.wfile.write(status_data.encode('utf-8'))
        
        elif self.path == '/refresh':
            # Force refresh endpoint
            self.send_response(302)
            self.send_header('Location', '/')
            self.end_headers()
        
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'404 Not Found')
    
    def get_bot_status_json(self):
        """Get bot status as JSON for API endpoint"""
        try:
            # Load configuration
            key = json.loads(open('AUTH/auth.txt', 'r').read())
            api = alpaca.REST(
                key['APCA-API-KEY-ID'], 
                key['APCA-API-SECRET-KEY'], 
                base_url='https://paper-api.alpaca.markets', 
                api_version='v2'
            )
            
            # Get current data
            account = api.get_account()
            clock = api.get_clock()
            positions = api.list_positions()
            
            with open('TICKERS/my_tickers.txt', 'r') as f:
                tickers = f.read().upper().split()
            
            # Get ticker prices
            ticker_prices = {}
            for ticker in tickers:
                try:
                    trade = api.get_latest_trade(ticker)
                    ticker_prices[ticker] = float(trade.price)
                except Exception:
                    ticker_prices[ticker] = 0
            
            # Get trading history
            trades_count = 0
            recent_trades = []
            if os.path.exists(ORDERS_CSV_FILE):
                try:
                    df = pd.read_csv(ORDERS_CSV_FILE)
                    if UNNAMED_COLUMN in df.columns:
                        df = df.drop(columns=[UNNAMED_COLUMN])
                    trades_count = len(df)
                    recent_trades = df.tail(5).to_dict('records')
                except Exception:
                    pass
            
            # Bot status
            first_trade_made = os.path.exists('FirstTrade.csv')
            
            status = {
                'timestamp': datetime.now().isoformat(),
                'market_open': clock.is_open,
                'next_open': str(clock.next_open),
                'account': {
                    'cash': float(account.cash),
                    'portfolio_value': float(account.portfolio_value),
                    'buying_power': float(account.buying_power),
                    'positions_count': len(positions)
                },
                'bot': {
                    'first_trade_made': first_trade_made,
                    'mode': '1-minute analysis' if first_trade_made else '30-minute analysis'
                },
                'tickers': ticker_prices,
                'trading': {
                    'total_trades': trades_count,
                    'recent_trades': recent_trades
                }
            }
            
            return json.dumps(status, indent=2)
            
        except Exception as e:
            return json.dumps({'error': str(e)})
    
    def load_dashboard_data(self):
        """Load all data needed for dashboard"""
        try:
            # Load configuration
            key = json.loads(open('AUTH/auth.txt', 'r').read())
            api = alpaca.REST(
                key['APCA-API-KEY-ID'], 
                key['APCA-API-SECRET-KEY'], 
                base_url='https://paper-api.alpaca.markets', 
                api_version='v2'
            )
            
            # Get current data
            account = api.get_account()
            clock = api.get_clock()
            positions = api.list_positions()
            et_tz = timezone('America/New_York')
            current_time = datetime.now(et_tz)
            
            with open('TICKERS/my_tickers.txt', 'r') as f:
                tickers = f.read().upper().split()
            
            return {
                'api': api,
                'account': account,
                'clock': clock,
                'positions': positions,
                'current_time': current_time,
                'tickers': tickers
            }
        except Exception:
            return None

    def get_ticker_data(self, api, tickers):
        """Get ticker price data"""
        ticker_data = []
        for ticker in tickers:
            try:
                trade = api.get_latest_trade(ticker)
                ticker_data.append({
                    'symbol': ticker,
                    'price': float(trade.price)
                })
            except Exception:
                ticker_data.append({
                    'symbol': ticker,
                    'price': 'Error'
                })
        return ticker_data

    def get_dashboard_trading_history(self):
        """Get trading history for dashboard"""
        trading_history = []
        if os.path.exists(ORDERS_CSV_FILE):
            try:
                df = pd.read_csv(ORDERS_CSV_FILE)
                if UNNAMED_COLUMN in df.columns:
                    df = df.drop(columns=[UNNAMED_COLUMN])
                trading_history = df.tail(10).to_dict('records')
            except Exception:
                pass
        return trading_history

    def generate_dashboard_html(self):
        """Generate the main dashboard HTML with reduced complexity"""
        # Load all data
        data = self.load_dashboard_data()
        if not data:
            return "<h1>Error: Unable to load configuration</h1>"
        
        # Extract data
        account = data['account']
        clock = data['clock']
        positions = data['positions']
        current_time = data['current_time']
        tickers = data['tickers']
        
        # Get additional data
        ticker_data = self.get_ticker_data(data['api'], tickers)
        trading_history = self.get_dashboard_trading_history()
        
        # Bot status
        first_trade_made = os.path.exists('FirstTrade.csv')
        bot_mode = '1-minute analysis' if first_trade_made else '30-minute analysis (first trade)'
        
        return self.generate_main_html_template(
            current_time, clock, account, positions, 
            bot_mode, first_trade_made, ticker_data, trading_history
        )

    def generate_main_html_template(self, current_time, clock, account, positions, bot_mode, first_trade_made, ticker_data, trading_history):
        """Generate the main HTML template"""
        # Generate HTML with live updates
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>🤖 Alpaca ROC Trading Bot - Live Dashboard</title>
            <meta charset="UTF-8">
            <style>
                * {{
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }}
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    min-height: 100vh;
                    padding: 20px;
                }}
                .container {{
                    max-width: 1400px;
                    margin: 0 auto;
                }}
                .header {{
                    text-align: center;
                    margin-bottom: 30px;
                    padding: 20px;
                    background: rgba(255, 255, 255, 0.1);
                    backdrop-filter: blur(10px);
                    border-radius: 15px;
                    border: 1px solid rgba(255, 255, 255, 0.2);
                }}
                .status-bar {{
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    margin-bottom: 20px;
                    padding: 15px 20px;
                    background: rgba(255, 255, 255, 0.1);
                    backdrop-filter: blur(10px);
                    border-radius: 10px;
                    border: 1px solid rgba(255, 255, 255, 0.2);
                }}
                .status-item {{
                    text-align: center;
                }}
                .status-value {{
                    font-size: 1.5em;
                    font-weight: bold;
                    margin-bottom: 5px;
                }}
                .status-label {{
                    font-size: 0.9em;
                    opacity: 0.8;
                }}
                .dashboard-grid {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
                    gap: 20px;
                    margin-bottom: 30px;
                }}
                .card {{
                    background: rgba(255, 255, 255, 0.1);
                    backdrop-filter: blur(10px);
                    border-radius: 15px;
                    padding: 25px;
                    border: 1px solid rgba(255, 255, 255, 0.2);
                    transition: transform 0.3s ease;
                }}
                .card:hover {{
                    transform: translateY(-5px);
                }}
                .card h3 {{
                    margin-top: 0;
                    color: #ffd700;
                    border-bottom: 2px solid #ffd700;
                    padding-bottom: 15px;
                    margin-bottom: 20px;
                    font-size: 1.3em;
                }}
                .metric {{
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    margin: 15px 0;
                    padding: 12px 0;
                    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
                }}
                .metric:last-child {{
                    border-bottom: none;
                }}
                .metric-label {{
                    font-weight: 500;
                }}
                .metric-value {{
                    font-weight: bold;
                    font-size: 1.1em;
                }}
                .status-open {{ color: #4ade80; }}
                .status-closed {{ color: #f87171; }}
                .positive {{ color: #4ade80; }}
                .negative {{ color: #f87171; }}
                .ticker-grid {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
                    gap: 15px;
                }}
                .ticker-card {{
                    background: rgba(255, 255, 255, 0.05);
                    padding: 15px;
                    border-radius: 10px;
                    text-align: center;
                    transition: all 0.3s ease;
                }}
                .ticker-card:hover {{
                    background: rgba(255, 255, 255, 0.1);
                    transform: scale(1.05);
                }}
                .ticker-symbol {{
                    font-weight: bold;
                    font-size: 1.1em;
                    margin-bottom: 8px;
                }}
                .ticker-price {{
                    font-size: 1.3em;
                    color: #ffd700;
                    font-weight: bold;
                }}
                .live-indicator {{
                    display: inline-block;
                    width: 12px;
                    height: 12px;
                    background: #4ade80;
                    border-radius: 50%;
                    animation: pulse 2s infinite;
                    margin-right: 8px;
                }}
                @keyframes pulse {{
                    0% {{ opacity: 1; transform: scale(1); }}
                    50% {{ opacity: 0.7; transform: scale(1.1); }}
                    100% {{ opacity: 1; transform: scale(1); }}
                }}
                .trade-table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin-top: 15px;
                }}
                .trade-table th, .trade-table td {{
                    padding: 12px 8px;
                    text-align: left;
                    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
                }}
                .trade-table th {{
                    background: rgba(255, 255, 255, 0.1);
                    font-weight: bold;
                }}
                .buy {{ color: #4ade80; }}
                .sell {{ color: #f87171; }}
                .refresh-controls {{
                    text-align: center;
                    margin-top: 30px;
                    padding: 20px;
                    background: rgba(255, 255, 255, 0.1);
                    backdrop-filter: blur(10px);
                    border-radius: 15px;
                    border: 1px solid rgba(255, 255, 255, 0.2);
                }}
                .btn {{
                    background: linear-gradient(45deg, #667eea, #764ba2);
                    color: white;
                    border: none;
                    padding: 12px 24px;
                    margin: 0 10px;
                    border-radius: 25px;
                    cursor: pointer;
                    font-weight: bold;
                    transition: all 0.3s ease;
                }}
                .btn:hover {{
                    transform: translateY(-2px);
                    box-shadow: 0 5px 15px rgba(0,0,0,0.3);
                }}
                .auto-refresh {{
                    color: #4ade80;
                    font-weight: bold;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🤖 Alpaca ROC Trading Bot</h1>
                    <h2><span class="live-indicator"></span>Live Dashboard</h2>
                    <p>Last Updated: <span id="lastUpdate">{current_time.strftime('%Y-%m-%d %H:%M:%S ET')}</span></p>
                </div>
                
                <div class="status-bar">
                    <div class="status-item">
                        <div class="status-value {'status-open' if clock.is_open else 'status-closed'}">
                            {'🟢 OPEN' if clock.is_open else '🔴 CLOSED'}
                        </div>
                        <div class="status-label">Market Status</div>
                    </div>
                    <div class="status-item">
                        <div class="status-value">${float(account.cash):,.0f}</div>
                        <div class="status-label">Available Cash</div>
                    </div>
                    <div class="status-item">
                        <div class="status-value">${float(account.portfolio_value):,.0f}</div>
                        <div class="status-label">Portfolio Value</div>
                    </div>
                    <div class="status-item">
                        <div class="status-value">{len(positions)}</div>
                        <div class="status-label">Open Positions</div>
                    </div>
                    <div class="status-item">
                        <div class="status-value">{'✅' if first_trade_made else '⏳'}</div>
                        <div class="status-label">First Trade</div>
                    </div>
                </div>
                
                <div class="dashboard-grid">
                    <!-- Bot Status -->
                    <div class="card">
                        <h3>🤖 Bot Status</h3>
                        <div class="metric">
                            <span class="metric-label">Current Mode:</span>
                            <span class="metric-value">{bot_mode}</span>
                        </div>
                        <div class="metric">
                            <span class="metric-label">First Trade:</span>
                            <span class="metric-value">{'✅ Completed' if first_trade_made else '⏳ Pending'}</span>
                        </div>
                        <div class="metric">
                            <span class="metric-label">Next Trade Time:</span>
                            <span class="metric-value">{'1-3 minutes' if first_trade_made else '10:00 AM ET'}</span>
                        </div>
                        <div class="metric">
                            <span class="metric-label">Strategy:</span>
                            <span class="metric-value">ROC Momentum</span>
                        </div>
                    </div>
                    
                    <!-- Account Details -->
                    <div class="card">
                        <h3>💰 Account Details</h3>
                        <div class="metric">
                            <span class="metric-label">Cash Balance:</span>
                            <span class="metric-value">${float(account.cash):,.2f}</span>
                        </div>
                        <div class="metric">
                            <span class="metric-label">Buying Power:</span>
                            <span class="metric-value">${float(account.buying_power):,.2f}</span>
                        </div>
                        <div class="metric">
                            <span class="metric-label">Day Trades:</span>
                            <span class="metric-value">{account.daytrade_count}/3</span>
                        </div>
                        <div class="metric">
                            <span class="metric-label">PDT Status:</span>
                            <span class="metric-value {'negative' if account.pattern_day_trader else 'positive'}">
                                {'❌ Active' if account.pattern_day_trader else '✅ Clear'}
                            </span>
                        </div>
                    </div>
                    
                    <!-- Market Information -->
                    <div class="card">
                        <h3>🏛️ Market Information</h3>
                        <div class="metric">
                            <span class="metric-label">Status:</span>
                            <span class="metric-value {'status-open' if clock.is_open else 'status-closed'}">
                                {'🟢 Open' if clock.is_open else '🔴 Closed'}
                            </span>
                        </div>
                        <div class="metric">
                            <span class="metric-label">Next Open:</span>
                            <span class="metric-value">{str(clock.next_open)[:16]}</span>
                        </div>
                        <div class="metric">
                            <span class="metric-label">Current Time (ET):</span>
                            <span class="metric-value">{current_time.strftime('%H:%M:%S')}</span>
                        </div>
                    </div>
                </div>
                
                <!-- Current Positions -->
                {self.generate_positions_section(positions)}
                
                <!-- Ticker Prices -->
                <div class="card">
                    <h3>📈 Live Ticker Prices</h3>
                    <div class="ticker-grid">
                        {self.generate_tickers_section(ticker_data)}
                    </div>
                </div>
                
                <!-- Trading History -->
                {self.generate_trading_history_section(trading_history)}
                
                <div class="refresh-controls">
                    <p class="auto-refresh">🔄 Auto-refreshing every 15 seconds</p>
                    <button class="btn" onclick="location.reload()">🔄 Manual Refresh</button>
                    <button class="btn" onclick="window.open('/api/status', '_blank')">📊 Raw Data</button>
                </div>
            </div>
            
            <script>
                // Auto-refresh every 15 seconds
                setTimeout(function() {{
                    location.reload();
                }}, 15000);
                
                // Update timestamp
                document.getElementById('lastUpdate').textContent = new Date().toLocaleString();
            </script>
        </body>
        </html>
        """
        
        return html
    
    def generate_positions_section(self, positions):
        """Generate current positions HTML"""
        if not positions:
            return ""
        
        html = '<div class="card"><h3>📍 Current Positions</h3>'
        for pos in positions:
            pnl_class = "positive" if float(pos.unrealized_pl) >= 0 else "negative"
            pnl_emoji = "📈" if float(pos.unrealized_pl) >= 0 else "📉"
            html += f'''
            <div class="metric">
                <span class="metric-label">{pnl_emoji} {pos.symbol} ({pos.qty} shares)</span>
                <span class="metric-value {pnl_class}">
                    ${float(pos.unrealized_pl):,.2f} ({float(pos.unrealized_plpc)*100:+.2f}%)
                </span>
            </div>
            '''
        html += '</div>'
        return html
    
    def generate_tickers_section(self, ticker_data):
        """Generate ticker prices HTML"""
        html = ""
        for ticker in ticker_data:
            if ticker['price'] != 'Error':
                html += f'''
                <div class="ticker-card">
                    <div class="ticker-symbol">{ticker['symbol']}</div>
                    <div class="ticker-price">${ticker['price']:.2f}</div>
                </div>
                '''
            else:
                html += f'''
                <div class="ticker-card">
                    <div class="ticker-symbol">{ticker['symbol']}</div>
                    <div style="color: #f87171;">Error</div>
                </div>
                '''
        return html
    
    def generate_trading_history_section(self, trading_history):
        """Generate trading history HTML"""
        if not trading_history:
            return '<div class="card"><h3>📋 Trading History</h3><p>No trades yet - Ready for first trade!</p></div>'
        
        html = '<div class="card"><h3>📋 Recent Trading History</h3>'
        html += '''
        <table class="trade-table">
            <tr>
                <th>Time</th>
                <th>Type</th>
                <th>Ticker</th>
                <th>Qty</th>
                <th>Price</th>
                <th>Total</th>
            </tr>
        '''
        
        for trade in trading_history[-5:]:  # Last 5 trades
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
    
    def log_message(self, format, *args):
        """Suppress default logging"""
        pass

def start_dashboard_server(port=8080):
    """Start the dashboard web server"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, DashboardHandler)
    
    print("🌐 Starting Alpaca Trading Bot Dashboard Server...")
    print(f"📍 Server running at: http://localhost:{port}")
    print("🚀 Opening dashboard in browser...")
    print("🔄 Dashboard auto-refreshes every 15 seconds")
    print("⚠️  Press Ctrl+C to stop the server")
    print("-" * 50)
    
    # Open browser
    webbrowser.open(f'http://localhost:{port}')
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 Dashboard server stopped")
        httpd.shutdown()

if __name__ == "__main__":
    from http.server import HTTPServer
    import os
    PORT = int(os.environ.get("PORT", 8080))
    server_address = ("", PORT)
    httpd = HTTPServer(server_address, DashboardHandler)
    print(f"🚀 Dashboard server running on port {PORT}")
    httpd.serve_forever()

