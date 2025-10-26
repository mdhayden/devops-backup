#!/usr/bin/env python3
"""
Web Server for Alpaca ROC Trading Bot Dashboard
Designed for Cloud Run deployment with authentication
"""
import json
import os
import time
from datetime import datetime
from pytz import timezone
import pandas as pd
import alpaca_trade_api as alpaca
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
import logging
from auth_system import auth_system

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
ORDERS_CSV_FILE = 'Orders.csv'
UNNAMED_COLUMN = 'Unnamed: 0'

class DashboardHandler(BaseHTTPRequestHandler):
    def get_session_id(self):
        """Extract session ID from cookies"""
        cookies = self.headers.get('Cookie', '')
        for cookie in cookies.split(';'):
            if 'session_id=' in cookie:
                return cookie.split('session_id=')[1].strip()
        return None
    
    def set_session_cookie(self, session_id):
        """Set session cookie"""
        self.send_header('Set-Cookie', f'session_id={session_id}; Path=/; HttpOnly; Max-Age=1800')
    
    def require_auth(self):
        """Check if user is authenticated"""
        session_id = self.get_session_id()
        username = auth_system.validate_session(session_id)
        return username is not None, username
    
    def send_login_page(self, error=False):
        """Send login form"""
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        with open('login_form.html', 'r', encoding='utf-8') as f:
            html = f.read()
        
        if error:
            html = html.replace('style="display: none"', 'style="display: block"', 1)
        
        self.wfile.write(html.encode('utf-8'))
    
    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        # Public endpoints (no auth required)
        if path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'OK')
            return
        
        elif path == '/login':
            self.send_login_page()
            return
        
        elif path == '/logout':
            session_id = self.get_session_id()
            if session_id:
                auth_system.logout(session_id)
            
            self.send_response(302)
            self.send_header('Location', '/login')
            self.send_header('Set-Cookie', 'session_id=; Path=/; HttpOnly; Max-Age=0')
            self.end_headers()
            return
        
        # Protected endpoints (auth required)
        is_authenticated, username = self.require_auth()
        if not is_authenticated:
            self.send_response(302)
            self.send_header('Location', '/login')
            self.end_headers()
            return
        
        if path == '/' or path == '/dashboard':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            html = self.generate_dashboard_html(username)
            self.wfile.write(html.encode('utf-8'))
        
        elif path == '/api/status':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            status_data = self.get_bot_status_json()
            self.wfile.write(status_data.encode('utf-8'))
        
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'404 Not Found')
    
    def do_POST(self):
        if self.path == '/login':
            # Parse form data
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            form_data = parse_qs(post_data)
            
            username = form_data.get('username', [''])[0]
            password = form_data.get('password', [''])[0]
            
            # Authenticate
            if auth_system.authenticate(username, password):
                # Create session
                session_id = auth_system.create_session(username)
                
                # Redirect to dashboard with session cookie
                self.send_response(302)
                self.send_header('Location', '/dashboard')
                self.set_session_cookie(session_id)
                self.end_headers()
                
                logger.info(f"User {username} logged in successfully")
            else:
                # Show login form with error
                self.send_login_page(error=True)
                logger.warning(f"Failed login attempt for username: {username}")
        else:
            self.send_response(404)
            self.end_headers()
    
    def get_bot_status_json(self):
        """Get bot status as JSON for API endpoint"""
        try:
            # Check if configuration files exist
            if not os.path.exists('AUTH/auth.txt') or not os.path.exists('TICKERS/my_tickers.txt'):
                return json.dumps({
                    'error': 'Configuration files not found',
                    'status': 'Configuration Error',
                    'message': 'AUTH/auth.txt or TICKERS/my_tickers.txt not found'
                })
            
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
            
            # Get ticker prices (limit to first 3 for performance)
            ticker_prices = {}
            for ticker in tickers[:3]:
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
            logger.error(f"Error getting bot status: {e}")
            return json.dumps({
                'error': str(e),
                'status': 'Error',
                'message': 'Unable to fetch bot status'
            })
    
    def load_dashboard_data(self):
        """Load all data needed for dashboard"""
        try:
            # Check if configuration files exist
            if not os.path.exists('AUTH/auth.txt') or not os.path.exists('TICKERS/my_tickers.txt'):
                return None
            
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
        except Exception as e:
            logger.error(f"Error loading dashboard data: {e}")
            return None

    def get_ticker_data(self, api, tickers):
        """Get ticker price data (limited for performance)"""
        ticker_data = []
        # Limit to first 4 tickers for Cloud Run performance
        for ticker in tickers[:4]:
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

    def generate_dashboard_html(self, username=None):
        """Generate the main dashboard HTML"""
        # Load all data
        data = self.load_dashboard_data()
        if not data:
            return self.generate_error_html("Configuration Error", 
                                           "Unable to load configuration. Please check AUTH/auth.txt and TICKERS/my_tickers.txt files.")
        
        try:
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
                bot_mode, first_trade_made, ticker_data, trading_history, username
            )
        except Exception as e:
            logger.error(f"Error generating dashboard: {e}")
            return self.generate_error_html("Dashboard Error", f"Error generating dashboard: {str(e)}")

    def generate_error_html(self, title, message):
        """Generate error page HTML"""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>{title} - Alpaca Trading Bot</title>
            <meta charset="UTF-8">
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    min-height: 100vh;
                    padding: 20px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                }}
                .error-container {{
                    background: rgba(255, 255, 255, 0.1);
                    backdrop-filter: blur(10px);
                    border-radius: 15px;
                    padding: 40px;
                    text-align: center;
                    max-width: 600px;
                }}
            </style>
        </head>
        <body>
            <div class="error-container">
                <h1>🤖 Alpaca ROC Trading Bot</h1>
                <h2>❌ {title}</h2>
                <p>{message}</p>
                <p><small>Check logs for more details</small></p>
                <button onclick="location.reload()" style="background: #667eea; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer;">
                    🔄 Retry
                </button>
            </div>
        </body>
        </html>
        """

    def generate_main_html_template(self, current_time, clock, account, positions, bot_mode, first_trade_made, ticker_data, trading_history, username=None):
        """Generate the main HTML template"""
        market_status_emoji = "🟢" if clock.is_open else "🔴"
        market_status_text = "OPEN" if clock.is_open else "CLOSED"
        market_status_class = "status-open" if clock.is_open else "status-closed"
        
        # User display
        user_display = f"👤 {username}" if username else "👤 User"
        
        return f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <title>🤖 Alpaca ROC Trading Bot - Live Dashboard</title>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <meta http-equiv="refresh" content="60">
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
                    max-width: 1200px;
                    margin: 0 auto;
                }}
                .header {{
                    text-align: center;
                    margin-bottom: 30px;
                    padding: 20px;
                    background: rgba(255, 255, 255, 0.1);
                    backdrop-filter: blur(10px);
                    border-radius: 15px;
                    position: relative;
                }}
                .logout-btn {{
                    position: absolute;
                    top: 20px;
                    right: 20px;
                    background: rgba(248, 113, 113, 0.8);
                    color: white;
                    border: none;
                    padding: 8px 16px;
                    border-radius: 8px;
                    cursor: pointer;
                    text-decoration: none;
                    font-size: 14px;
                    transition: all 0.3s ease;
                }}
                .logout-btn:hover {{
                    background: rgba(248, 113, 113, 1);
                    transform: translateY(-1px);
                }}
                .user-info {{
                    position: absolute;
                    top: 20px;
                    left: 20px;
                    color: #ffd700;
                    font-weight: bold;
                }}
                .status-banner {{
                    background: rgba(255, 255, 255, 0.15);
                    padding: 15px;
                    border-radius: 10px;
                    margin-bottom: 20px;
                    text-align: center;
                    font-size: 1.2em;
                    font-weight: bold;
                }}
                .status-bar {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                    gap: 15px;
                    margin-bottom: 20px;
                }}
                .status-item {{
                    background: rgba(255, 255, 255, 0.1);
                    padding: 15px;
                    border-radius: 10px;
                    text-align: center;
                }}
                .status-value {{
                    font-size: 1.5em;
                    font-weight: bold;
                    margin-bottom: 5px;
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
                }}
                .card h3 {{
                    margin-top: 0;
                    color: #ffd700;
                    border-bottom: 2px solid #ffd700;
                    padding-bottom: 10px;
                    margin-bottom: 15px;
                }}
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
                }}
                .refresh-info {{
                    text-align: center;
                    margin-top: 20px;
                    opacity: 0.7;
                }}
                .working-indicator {{
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
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <div class="user-info">{user_display}</div>
                    <a href="/logout" class="logout-btn">🚪 Logout</a>
                    <h1>🤖 Alpaca ROC Trading Bot Dashboard</h1>
                    <p><span class="working-indicator"></span>Last Updated: {current_time.strftime('%Y-%m-%d %H:%M:%S ET')}</p>
                    <p>🌐 Running on Cloud Run</p>
                </div>
                
                <div class="status-banner">
                    {market_status_emoji} Market is {market_status_text}
                    {' - Next open: ' + str(clock.next_open)[:16] if not clock.is_open else ''}
                </div>
                
                <div class="status-bar">
                    <div class="status-item">
                        <div class="status-value {market_status_class}">
                            {market_status_emoji} {market_status_text}
                        </div>
                        <div>Market Status</div>
                    </div>
                    <div class="status-item">
                        <div class="status-value">${float(account.cash):,.0f}</div>
                        <div>Available Cash</div>
                    </div>
                    <div class="status-item">
                        <div class="status-value">${float(account.portfolio_value):,.0f}</div>
                        <div>Portfolio Value</div>
                    </div>
                    <div class="status-item">
                        <div class="status-value">{len(positions)}</div>
                        <div>Open Positions</div>
                    </div>
                </div>
                
                <div class="dashboard-grid">
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
                            <span>PDT Status:</span>
                            <span class="{'negative' if account.pattern_day_trader else 'positive'}">
                                {'❌ Yes' if account.pattern_day_trader else '✅ No'}
                            </span>
                        </div>
                        <div class="metric">
                            <span>Connection:</span>
                            <span class="positive">✅ Connected</span>
                        </div>
                    </div>
                    
                    <!-- Account Details -->
                    <div class="card">
                        <h3>💰 Account Details</h3>
                        <div class="metric">
                            <span>Cash:</span>
                            <span>${float(account.cash):,.2f}</span>
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
                            <span>Account Type:</span>
                            <span>Paper Trading</span>
                        </div>
                    </div>
                </div>
                
                <!-- Ticker Prices -->
                <div class="card">
                    <h3>📈 Live Ticker Prices</h3>
                    <div class="ticker-grid">
                        {self.generate_tickers_html(ticker_data)}
                    </div>
                </div>
                
                <!-- Trading History -->
                {self.generate_history_html(trading_history)}
                
                <div class="refresh-info">
                    <p>🔄 Page auto-refreshes every 60 seconds</p>
                    <p>📊 <a href="/api/status" style="color: #ffd700;">View Raw JSON Data</a></p>
                    <p>🏥 <a href="/health" style="color: #ffd700;">Health Check</a></p>
                </div>
            </div>
        </body>
        </html>
        """

    def generate_tickers_html(self, ticker_data):
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

    def generate_history_html(self, trading_history):
        """Generate trading history HTML"""
        if not trading_history:
            return '<div class="card"><h3>📋 Trading History</h3><p>No trades yet - Ready for action!</p></div>'
        
        html = '<div class="card"><h3>📋 Recent Trading History</h3>'
        html += '<div style="overflow-x: auto;">'
        
        for trade in trading_history[-5:]:  # Last 5 trades
            trade_class = "positive" if trade['Type'] == 'sell' else "status-open"
            html += f'''
            <div class="metric">
                <span>{trade['Time']} - {trade['Type'].upper()} {trade['Ticker']}</span>
                <span class="{trade_class}">${trade['Total']:,.2f}</span>
            </div>
            '''
        
        html += '</div></div>'
        return html
    
    def log_message(self, format, *args):
        """Override to use proper logging"""
        logger.info("%s - - [%s] %s" % (self.address_string(), self.log_date_time_string(), format % args))

def start_dashboard_server(port=8080):
    """Start the dashboard web server for Cloud Run"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, DashboardHandler)
    
    logger.info(f"🚀 Alpaca Trading Bot Dashboard starting on port {port}")
    logger.info("✅ Ready to accept HTTP traffic")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        logger.info("🛑 Shutting down dashboard server...")
        httpd.shutdown()

if __name__ == "__main__":
    # Get port from environment variable (Cloud Run provides this)
    port = int(os.environ.get("PORT", 8080))
    logger.info(f"🌐 Starting server on 0.0.0.0:{port}")
    start_dashboard_server(port)