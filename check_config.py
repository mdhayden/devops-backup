#!/usr/bin/env python3
"""
Configuration checker for Alpaca ROC Trading Bot
Run this before starting the main bot to verify everything is set up correctly
"""
import os
import json
import sys
from datetime import datetime

def check_files():
    """Check if all required files exist"""
    print("=== Checking Required Files ===")
    
    required_files = [
        'AUTH/auth.txt',
        'TICKERS/my_tickers.txt',
        'main.py',
        'requirements.txt'
    ]
    
    missing_files = []
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✓ {file_path}")
        else:
            print(f"✗ {file_path} - MISSING")
            missing_files.append(file_path)
    
    if not os.path.exists('tick_data'):
        print("✓ tick_data/ directory created")
        os.makedirs('tick_data', exist_ok=True)
    else:
        print("✓ tick_data/ directory exists")
    
    return len(missing_files) == 0

def check_credentials():
    """Check if credentials are properly formatted"""
    print("\n=== Checking Credentials ===")
    
    try:
        with open('AUTH/auth.txt', 'r') as f:
            creds = json.loads(f.read())
        
        required_keys = ['APCA-API-KEY-ID', 'APCA-API-SECRET-KEY']
        missing_keys = []
        
        for key in required_keys:
            if key in creds and creds[key]:
                print(f"✓ {key}: {creds[key][:8]}...")
            else:
                print(f"✗ {key}: MISSING")
                missing_keys.append(key)
        
        return len(missing_keys) == 0
        
    except FileNotFoundError:
        print("✗ AUTH/auth.txt not found")
        return False
    except json.JSONDecodeError:
        print("✗ AUTH/auth.txt is not valid JSON")
        return False

def check_tickers():
    """Check if tickers are properly configured"""
    print("\n=== Checking Tickers ===")
    
    try:
        with open('TICKERS/my_tickers.txt', 'r') as f:
            tickers = f.read().strip().upper().split()
        
        if len(tickers) > 0:
            print(f"✓ Found {len(tickers)} tickers: {', '.join(tickers)}")
            return True
        else:
            print("✗ No tickers found")
            return False
            
    except FileNotFoundError:
        print("✗ TICKERS/my_tickers.txt not found")
        return False

def check_dependencies():
    """Check if required packages are installed"""
    print("\n=== Checking Dependencies ===")
    
    required_packages = {
        'alpaca_trade_api': 'alpaca_trade_api',
        'pandas': 'pandas', 
        'numpy': 'numpy'
    }
    
    missing_packages = []
    for package_name, import_name in required_packages.items():
        try:
            __import__(import_name)
            print(f"✓ {package_name}")
        except ImportError:
            print(f"✗ {package_name} - MISSING")
            missing_packages.append(package_name)
    
    if missing_packages:
        print("\nTo install missing packages, run:")
        print(f"pip install {' '.join(missing_packages)}")
    
    return len(missing_packages) == 0

def check_market_hours():
    """Check if market is currently open"""
    print("\n=== Market Hours Info ===")
    
    from datetime import datetime
    import pytz
    
    et = pytz.timezone('America/New_York')
    now_et = datetime.now(et)
    
    print(f"Current ET time: {now_et.strftime('%Y-%m-%d %H:%M:%S %Z')}")
    
    # Simple market hours check (9:30 AM - 4:00 PM ET, Mon-Fri)
    weekday = now_et.weekday()
    hour = now_et.hour
    minute = now_et.minute
    
    is_weekend = weekday >= 5  # Saturday or Sunday
    market_open_time = (hour > 9) or (hour == 9 and minute >= 30)
    market_close_time = hour < 16
    
    if is_weekend:
        print("📅 Weekend - Market is CLOSED")
        print("   Next market open: Monday 9:30 AM ET")
    elif market_open_time and market_close_time:
        print("🟢 Market is likely OPEN")
        print("   (This is a simple check - verify with your broker)")
    else:
        print("🔴 Market is likely CLOSED")
        print("   Market hours: 9:30 AM - 4:00 PM ET, Monday-Friday")
    
    return not is_weekend and market_open_time and market_close_time

def main():
    """Run all configuration checks"""
    print("🤖 Alpaca ROC Trading Bot - Configuration Checker")
    print("=" * 60)
    
    checks = [
        ("Files", check_files),
        ("Credentials", check_credentials), 
        ("Tickers", check_tickers),
        ("Dependencies", check_dependencies),
        ("Market Hours", check_market_hours)
    ]
    
    all_passed = True
    
    for check_name, check_func in checks:
        try:
            passed = check_func()
            if not passed:
                all_passed = False
        except Exception as e:
            print(f"✗ Error in {check_name} check: {e}")
            all_passed = False
    
    print("\n" + "=" * 60)
    
    if all_passed:
        print("🎉 All checks passed! Your bot is ready to test.")
        print("\nNext steps:")
        print("1. Run: python test_connection.py")
        print("2. If connection test passes, run: python main.py")
    else:
        print("❌ Some checks failed. Please fix the issues above before testing.")
        print("\nCommon fixes:")
        print("1. Get valid Alpaca Paper Trading API credentials")
        print("2. Install missing packages: pip install -r requirements.txt")
        print("3. Check file paths and permissions")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)