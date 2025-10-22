# Alpaca ROC Trading Bot - Testing Guide

## 🚀 How to Test Your Trading Bot

### 1. **Pre-Testing Setup**

#### A. **Fix Authentication Issues**
Your current API credentials may be invalid or for live trading. You need:

1. **Get Paper Trading Credentials:**
   - Go to [Alpaca Markets](https://alpaca.markets/)
   - Sign up for a paper trading account
   - Get your Paper Trading API keys
   - Update `AUTH/auth.txt` with valid credentials

2. **Verify API Endpoint:**
   The bot is configured for paper trading: `https://paper-api.alpaca.markets`

#### B. **Install Dependencies**
```bash
pip install alpaca_trade_api==2.0.0 pandas==1.4.1 numpy==1.22.3
```

### 2. **Testing Stages**

#### **Stage 1: Component Testing (✅ COMPLETED)**
- ✅ ROC calculations work correctly
- ✅ Stock selection algorithm functions
- ✅ Ask vs LTP comparison works
- ✅ Order simulation successful

#### **Stage 2: API Connection Testing**
```bash
python test_connection.py
```
This will verify:
- Account connection
- Market status
- Position checking
- Data retrieval

#### **Stage 3: Dry Run Testing**
```bash
python test_components.py
```
This tests all functions with mock data without placing real orders.

#### **Stage 4: Live Paper Trading**
Once API credentials are fixed, run:
```bash
python main.py
```

### 3. **Testing Checklist**

#### **Before First Run:**
- [ ] Valid Alpaca Paper Trading API credentials
- [ ] All dependencies installed
- [ ] Market is open (9:30 AM - 4:00 PM ET, Monday-Friday)
- [ ] `tick_data/` directory exists
- [ ] Email credentials configured (optional)

#### **Safety Checks:**
- [ ] Using paper trading endpoint (not live)
- [ ] Small test amounts only
- [ ] Pattern Day Trader flag monitoring
- [ ] Stop-loss mechanisms in place

### 4. **Common Issues & Solutions**

#### **API Authentication Errors:**
```
❌ Connection test failed: unauthorized.
```
**Solution:** Get new Paper Trading API credentials from Alpaca

#### **Market Closed Errors:**
```
❌ Market is closed
```
**Solution:** Test during market hours (9:30 AM - 4:00 PM ET)

#### **No Tickers File:**
```
❌ FileNotFoundError: [Errno 2] No such file or directory: 'AUTH/Tickers.txt'
```
**Solution:** Fixed - now uses `TICKERS/my_tickers.txt`

#### **Missing tick_data Directory:**
```
❌ FileNotFoundError: [Errno 2] No such file or directory: 'tick_data/AAPL.csv'
```
**Solution:** Directory created automatically

### 5. **Testing Scenarios**

#### **Scenario A: Normal Market Conditions**
- Bot should fetch data every minute
- Calculate ROC for all tickers
- Select highest ROC stock with Ask > LTP
- Place buy orders with full capital

#### **Scenario B: No Good Stocks (All ROC ≤ 0)**
- Bot should print "All ROCs are <= 0"
- No orders placed
- Continue monitoring

#### **Scenario C: No Ask > LTP Conditions**
- Bot should print "All Ask < LTP"
- No orders placed
- Continue monitoring

#### **Scenario D: Profit Target Hit (≥2% gain)**
- Bot should sell current position
- Buy new highest ROC stock
- Send email alerts

### 6. **Monitoring & Logs**

The bot creates these files:
- `FirstTrade.csv` - Tracks if bot has made its first trade
- `Orders.csv` - Log of all buy/sell orders
- `tick_data/*.csv` - Market data for each ticker

### 7. **Email Alerts Setup (Optional)**

To enable email notifications, update the `mail_alert()` function:
```python
sender_address = 'your_email@gmail.com'
sender_pass = 'your_app_password'  # Gmail App Password
receiver_address = 'your_email@gmail.com'
```

### 8. **Risk Management**

#### **Built-in Safety Features:**
- 2% profit target (automatic selling)
- Pattern Day Trader detection
- Paper trading environment
- Full capital allocation per trade

#### **Additional Recommendations:**
- Start with small amounts
- Monitor during first few hours
- Set up proper stop-losses
- Test extensively in paper trading first

### 9. **Performance Testing**

#### **Metrics to Monitor:**
- Number of trades per day
- Win/loss ratio
- Average holding time
- Maximum drawdown
- ROC prediction accuracy

#### **Optimization Areas:**
- ROC timeframe (currently 1-min vs 30-min)
- Profit target (currently 2%)
- Stock selection criteria
- Position sizing strategy

### 10. **Next Steps**

1. **Fix API Credentials** - Get valid Alpaca Paper Trading keys
2. **Run Connection Test** - Verify API access
3. **Monitor During Market Hours** - Test real-time functionality
4. **Analyze Performance** - Review Orders.csv for results
5. **Optimize Parameters** - Adjust ROC thresholds, profit targets
6. **Scale Up Gradually** - Increase capital after successful testing

### 🎯 Quick Start Commands

```bash
# 1. Test components (works offline)
python test_components.py

# 2. Test API connection (requires valid credentials)
python test_connection.py

# 3. Run the actual bot (paper trading)
python main.py
```

### ⚠️ Important Notes

- **Never run with live credentials until thoroughly tested**
- **Monitor the bot closely during first runs**
- **Paper trading only until you're confident**
- **Markets are closed weekends and holidays**
- **Bot uses aggressive 100% capital allocation strategy**