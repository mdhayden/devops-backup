import pandas as pd
import datetime
from datetime import datetime as dt
from pytz import timezone
import time

import alpaca_trade_api as alpaca
import json

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from datetime import timedelta
import os.path

# Constants
TIMEZONE_NY = 'America/New_York'
TICK_DATA_CSV_PATH = 'tick_data/{}.csv'
ORDERS_CSV_FILE = 'Orders.csv'
FIRST_TRADE_CSV_FILE = 'FirstTrade.csv'
UNNAMED_COLUMN = 'Unnamed: 0'

# Load configuration
key = json.loads(open('AUTH/auth.txt', 'r').read())
api = alpaca.REST(key['APCA-API-KEY-ID'], key['APCA-API-SECRET-KEY'], base_url='https://paper-api.alpaca.markets', api_version = 'v2')
tickers = open('TICKERS/my_tickers.txt', 'r').read()
tickers = tickers.upper().split()
global TICKERS 
TICKERS = tickers

def get_minute_data(tickers):
    
    def save_min_data(ticker):
        ny_tz = timezone(TIMEZONE_NY)
        current_time = dt.now().astimezone(ny_tz)
        
        prices = api.get_trades(str(ticker), start = (current_time - timedelta(minutes=2)).isoformat(),
                                        end = current_time.isoformat(), 
                                        limit = 10000).df[['price']]
        prices.index = pd.to_datetime(prices.index, format = '%Y-%m-%d').strftime('%Y-%m-%d %H:%M')
        prices = prices[~prices.index.duplicated(keep='first')]

        quotes = api.get_quotes(str(ticker), start = (current_time - timedelta(minutes=2)).isoformat(),
                                        end = current_time.isoformat(), 
                                        limit = 10000).df[['ask_price']]
        quotes.index = pd.to_datetime(quotes.index, format = '%Y-%m-%d').strftime('%Y-%m-%d %H:%M')
        quotes = quotes[~quotes.index.duplicated(keep='first')]

        df = prices.join(quotes, how='inner')
        df.to_csv(TICK_DATA_CSV_PATH.format(ticker))
        
    for ticker in tickers:
        save_min_data(ticker)

def get_past30_data(tickers):
    
    def save_30_data(ticker):
        ny_tz = timezone(TIMEZONE_NY)
        current_time = dt.now().astimezone(ny_tz)
        
        prices_1 = api.get_trades(str(ticker), start = (current_time - timedelta(minutes=30)).isoformat(),
                                        end = (current_time - timedelta(minutes=28, seconds = 30)).isoformat(), 
                                        limit = 10000).df[['price']]
        prices_2 = api.get_trades(str(ticker), start = (current_time - timedelta(minutes=1, seconds = 30)).isoformat(),
                                        end = current_time.isoformat(), 
                                        limit = 10000).df[['price']]
        
        prices_1.index = pd.to_datetime(prices_1.index, format = '%Y-%m-%d').strftime('%Y-%m-%d %H:%M')
        prices_2.index = pd.to_datetime(prices_2.index, format = '%Y-%m-%d').strftime('%Y-%m-%d %H:%M')
        
        prices = pd.concat([prices_1, prices_2])
        prices = prices[~prices.index.duplicated(keep='first')]

        quotes_1 = api.get_quotes(str(ticker), start = (current_time - timedelta(minutes=30)).isoformat(),
                                        end = (current_time - timedelta(minutes=28, seconds = 30)).isoformat(), 
                                        limit = 10000).df[['ask_price']]
        quotes_2 = api.get_quotes(str(ticker), start = (current_time - timedelta(minutes=1, seconds = 30)).isoformat(),
                                        end = current_time.isoformat(), 
                                        limit = 10000).df[['ask_price']]
        
        quotes_1.index = pd.to_datetime(quotes_1.index, format = '%Y-%m-%d').strftime('%Y-%m-%d %H:%M')
        quotes_2.index = pd.to_datetime(quotes_2.index, format = '%Y-%m-%d %H:%M')
        
        quotes = pd.concat([quotes_1, quotes_2])
        quotes = quotes[~quotes.index.duplicated(keep='first')]
        
        df = prices.join(quotes, how='inner')
        df.to_csv(TICK_DATA_CSV_PATH.format(ticker))
    
    for ticker in tickers:
        save_30_data(ticker)

def calculate_rate_of_change(ask, timeframe):
    """Calculate Rate of Change (ROC) for given timeframe"""
    if timeframe == 30:
        rocs = (ask[ask.shape[0] - 1] - ask[0])/(ask[0])
    else:
        rocs = (ask[ask.shape[0] - 1] - ask[ask.shape[0] -2])/(ask[ask.shape[0] - 2])
    return rocs*1000

# Returns a list of most recent ROCs for all tickers
def get_roc_list(tickers, timeframe):
    """Get list of ROC values for all tickers"""
    roc_tickers = []
    for i in range(len(tickers)):
        df = pd.read_csv(TICK_DATA_CSV_PATH.format(tickers[i]))
        df = df.set_index('timestamp')  # Remove inplace=True
        df.index = pd.to_datetime(df.index, format ='%Y-%m-%d').strftime('%Y-%m-%d %H:%M')
        roc_tickers.append(calculate_rate_of_change(df['ask_price'], timeframe)) # [-1] forlast value (latest)
    return roc_tickers

def check_buy_condition(ticker):
    """Check if ask price > last traded price for a ticker"""
    df = pd.read_csv(TICK_DATA_CSV_PATH.format(ticker))
    df = df.set_index('timestamp')  # Remove inplace=True
    df.index = pd.to_datetime(df.index, format ='%Y-%m-%d').strftime('%Y-%m-%d %H:%M')

    # Check if ask_price > price for recent data points
    ask_col = df.columns.get_loc('ask_price')
    price_col = df.columns.get_loc('price')
    
    buy_conditions = []
    for i in range(max(0, df.shape[0] - 2), df.shape[0]):
        buy_conditions.append(df.iloc[i, ask_col] > df.iloc[i, price_col])
    
    return buy_conditions[-1] if buy_conditions else False

# compared ASK vs LTP
def compare_ask_ltp(tickers, timeframe):
    """Compare ask price vs last traded price for ticker selection"""
    if len(tickers) == 0:
        return None
        
    rocs = get_roc_list(tickers, timeframe)
    max_roc = max(rocs)

    if max_roc <= 0:
        return 0
        
    max_roc_index = rocs.index(max_roc)

    while tickers:
        buy_stock_candidate = tickers[max_roc_index]
        
        if check_buy_condition(buy_stock_candidate):
            return buy_stock_candidate
        else:
            tickers.pop(max_roc_index)
            rocs.pop(max_roc_index)
            
            if not tickers:
                return -1
                
            max_roc = max(rocs)
            max_roc_index = rocs.index(max_roc)
    
    return None# returns which stock to buy
def stock_to_buy(tickers, timeframe):
        entry_buy = compare_ask_ltp(tickers, timeframe)
        return entry_buy

def algo(tickers):
    """Main algorithm to determine which stock to buy"""
    if os.path.isfile(FIRST_TRADE_CSV_FILE):
        timeframe = 1
    else:
        timeframe = 30
    stock = stock_to_buy(tickers, timeframe)
    return stock


def buy(stock_to_buy: str):
    """Execute buy order for selected stock"""
    cash_balance = api.get_account().cash
    price_stock = api.get_latest_trade(str(stock_to_buy)).price
    target_position_size = float(cash_balance) / price_stock  # Calculates required position size
    api.submit_order(str(stock_to_buy), target_position_size, "buy", "market", "day") # Market order to open position    
    
    mail_content = '''ALERT
    
    BUY Order Placed for {}: {} Shares at ${}'''.format(stock_to_buy, target_position_size, price_stock)
    
    if os.path.isfile(ORDERS_CSV_FILE):
        df = pd.read_csv(ORDERS_CSV_FILE)
        df = df.drop(columns=UNNAMED_COLUMN)  # Remove inplace=True
        df.loc[len(df.index)] = [((dt.now()).astimezone(timezone(TIMEZONE_NY))).strftime("%Y-%m-%d %H:%M:%S"), stock_to_buy, 'buy',
                                 price_stock, target_position_size, target_position_size*price_stock, api.get_account().cash] 
    else:    
        df = pd.DataFrame()
        df[['Time', 'Ticker', 'Type', 'Price', 'Quantity', 'Total', 'Acc Balance']] = ''
        df.loc[len(df.index)] = [((dt.now()).astimezone(timezone(TIMEZONE_NY))).strftime("%Y-%m-%d %H:%M:%S"), stock_to_buy, 'buy',
                                 price_stock, target_position_size, target_position_size*price_stock, api.get_account().cash] 
    df.to_csv(ORDERS_CSV_FILE)
    return mail_content

def sell(current_stock):
    """Execute sell order for current stock"""
    # sells current_stock
    quantity = float(api.get_position(str(current_stock)).qty)    
    sell_price = api.get_latest_trade(str(current_stock)).price
    api.cancel_all_orders() # cancels all pending (to be filled) orders 
    api.close_position(str(current_stock)) # sells current stock
    
    mail_content = '''ALERT

    SELL Order Placed for {}: {} Shares at ${}'''.format(current_stock, quantity, sell_price)
    
    df = pd.read_csv(ORDERS_CSV_FILE)
    df = df.drop(columns=UNNAMED_COLUMN)  # Remove inplace=True
    df.loc[len(df.index)] = [((dt.now()).astimezone(timezone(TIMEZONE_NY))).strftime("%Y-%m-%d %H:%M:%S"), current_stock, 'sell', sell_price, quantity, quantity*sell_price, api.get_account().cash] 
    
    df.to_csv(ORDERS_CSV_FILE)
    return mail_content

def check_rets(current_stock):
    # checks returns for stock in portfolio (api.get_positions()[0].symbol)
    returns = float(api.get_position(str(current_stock)).unrealized_plpc)*100
    if (returns >= 2):
        mail_content = sell(current_stock)
    else: 
        mail_content = 0              
    return mail_content

def mail_alert(mail_content, sleep_time):
    # The mail addresses and password
    sender_address = 'sender_address'
    sender_pass = 'sender_password'
    receiver_address = 'receiver_address'

    # Setup MIME
    message = MIMEMultipart()
    message['From'] = 'Trading Bot'
    message['To'] = receiver_address
    message['Subject'] = 'HFT Second-Bot'
    
    # The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'plain'))

    # Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587)  # use gmail with port
    session.starttls()  # enable security

    # login with mail_id and password
    session.login(sender_address, sender_pass)
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    time.sleep(sleep_time)

def wait_for_market_open():
    """Wait for market to open at 10:00 AM ET for first trade"""
    ny_tz = timezone(TIMEZONE_NY)
    current_time = dt.now().astimezone(ny_tz)
    
    if current_time.strftime('%H:%M:%S') < '10:00:00':
        time_to_10_str = str(dt.strptime('10:00:00', '%H:%M:%S') - dt.strptime(current_time.strftime('%H:%M:%S'), '%H:%M:%S'))
        time_parts = time_to_10_str.split(':')
        time_to_10 = int(time_parts[1]) * 60 + int(time_parts[2])
        time.sleep(max(0, time_to_10 - 20))

def handle_first_trade(tickers):
    """Handle the first trade logic (30-minute analysis)"""
    wait_for_market_open()
    get_past30_data(tickers)
    stock_to_buy = algo(tickers)

    if stock_to_buy == 0:
        print('All ROCs are <= 0')
        return False
    elif stock_to_buy == -1:
        print('All Ask < LTP')
        return False
    
    mail_content = buy(stock_to_buy)
    mail_alert(mail_content, 5)
    
    # Mark first trade as completed
    df = pd.DataFrame()
    df['First Stock'] = [stock_to_buy]
    df.to_csv(FIRST_TRADE_CSV_FILE)
    return True

def handle_subsequent_trades(tickers):
    """Handle subsequent trades (1-minute analysis)"""
    if float(api.get_account().cash) <= 10:
        return handle_position_management()
    
    get_minute_data(tickers)
    stock_to_buy = algo(tickers)

    if stock_to_buy == 0:
        print('All ROCs are <= 0')
        time.sleep(2)
        return True
    elif stock_to_buy == -1:
        print('All Ask < LTP')
        time.sleep(2)
        return True
    
    if not should_buy_stock(stock_to_buy):
        return True
    
    try:
        if api.get_activities() and api.get_activities()[0].order_status == 'partially_filled':
            api.cancel_all_orders()
    except Exception:
        pass
    
    mail_content = buy(stock_to_buy)
    mail_alert(mail_content, 5)
    return True

def should_buy_stock(stock_to_buy):
    """Check if we should buy the selected stock"""
    positions = api.list_positions()
    
    if len(positions) > 0:
        current_symbols = [pos.symbol for pos in positions]
        
        if stock_to_buy in current_symbols:
            latest_price = api.get_latest_trade(stock_to_buy).price
            avg_entry_price = float(api.get_position(stock_to_buy).avg_entry_price)
            
            if latest_price > avg_entry_price:
                print('LTP for {} > Average Entry Price'.format(stock_to_buy))
                time.sleep(2)
                return False
    
    return True

def handle_position_management():
    """Handle position management when cash is low"""
    positions = api.list_positions()
    mail_content_list = []
    
    for position in positions:
        mail_content = check_rets(position.symbol)
        mail_content_list.append(mail_content)
    
    if any(mail_content_list):
        for mail in mail_content_list:
            if mail != 0:
                mail_alert(mail, 0)
    else:
        time.sleep(3)
    
    return True

def trading_loop():
    """Main trading loop"""
    tickers = TICKERS
    
    try:
        if not api.get_clock().is_open:
            return False
            
        if os.path.isfile(FIRST_TRADE_CSV_FILE):
            return handle_subsequent_trades(tickers)
        else:
            return handle_first_trade(tickers)
            
    except Exception as e:
        print(f"Trading error: {e}")
        return True

def main():
    """Main function with simplified logic"""
    # Send startup notification if market is open
    if api.get_clock().is_open:
        mail_content = 'The bot started running on {} at {} UTC'.format(
            dt.now().strftime('%Y-%m-%d'), 
            dt.now().strftime('%H:%M:%S')
        )
        mail_alert(mail_content, 0)

    while True:
        # Check for pattern day trader restriction
        if api.get_account().pattern_day_trader:
            mail_alert('Pattern day trading notification, bot is stopping now', 0)
            break

        if api.get_clock().is_open:
            if not trading_loop():
                break
        else:
            # Market is closed
            time.sleep(300)
            if api.get_clock().is_open:
                continue
            else:
                mail_content = 'The market is closed now'
                mail_alert(mail_content, 0)
                break

    # Send shutdown notification
    if not api.get_clock().is_open:
        mail_content = 'The bot stopped running on {} at {} UTC'.format(
            dt.now().strftime('%Y-%m-%d'), 
            dt.now().strftime('%H:%M:%S')
        )
        mail_alert(mail_content, 0)

if __name__ == '__main__':
    main()
