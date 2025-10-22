#!/usr/bin/env python3
"""
Dashboard Launcher - Easy access to all monitoring tools
"""
import subprocess
import sys
import os

def main():
    print("🤖 ALPACA ROC TRADING BOT - DASHBOARD LAUNCHER")
    print("=" * 55)
    print()
    print("Choose your monitoring option:")
    print()
    print("1. 📊 Terminal Dashboard (Interactive)")
    print("   - Real-time console dashboard")
    print("   - Options for single view or live monitoring")
    print()
    print("2. 🌐 Web Dashboard (Browser)")
    print("   - Beautiful HTML dashboard")
    print("   - Auto-refreshes every 30 seconds")
    print("   - Opens in your default browser")
    print()
    print("3. ⚡ Quick Status Check")
    print("   - Fast overview of key metrics")
    print("   - Perfect for quick checks")
    print()
    print("4. 🔧 Configuration Check")
    print("   - Verify bot setup and credentials")
    print("   - Check all required files")
    print()
    print("5. 🧪 Test Bot Connection")
    print("   - Test API connection and account access")
    print("   - Verify ticker data retrieval")
    print()
    
    while True:
        choice = input("Enter your choice (1-5, or 'q' to quit): ").strip().lower()
        
        if choice == 'q' or choice == 'quit':
            print("👋 Goodbye!")
            break
        elif choice == '1':
            print("\n🚀 Launching Terminal Dashboard...")
            try:
                subprocess.run([sys.executable, 'dashboard.py'], check=True)
            except subprocess.CalledProcessError:
                print("❌ Error launching terminal dashboard")
            except KeyboardInterrupt:
                print("\n👋 Dashboard closed")
        
        elif choice == '2':
            print("\n🚀 Launching Web Dashboard...")
            try:
                subprocess.run([sys.executable, 'web_dashboard.py'], check=True)
                print("✅ Web dashboard created! Check your browser.")
                input("Press Enter to continue...")
            except subprocess.CalledProcessError:
                print("❌ Error creating web dashboard")
        
        elif choice == '3':
            print("\n🚀 Running Quick Status Check...")
            try:
                result = subprocess.run([sys.executable, 'dashboard.py'], 
                                     input='3\n', text=True, 
                                     capture_output=True, timeout=30)
                print(result.stdout)
                if result.stderr:
                    print("Errors:", result.stderr)
            except subprocess.TimeoutExpired:
                print("❌ Status check timed out")
            except subprocess.CalledProcessError:
                print("❌ Error running status check")
        
        elif choice == '4':
            print("\n🚀 Running Configuration Check...")
            try:
                subprocess.run([sys.executable, 'check_config.py'], check=True)
            except subprocess.CalledProcessError:
                print("❌ Configuration issues found")
        
        elif choice == '5':
            print("\n🚀 Testing Bot Connection...")
            try:
                subprocess.run([sys.executable, 'test_connection.py'], check=True)
            except subprocess.CalledProcessError:
                print("❌ Connection test failed")
        
        else:
            print("❌ Invalid choice. Please enter 1-5 or 'q' to quit.")
        
        print("\n" + "-" * 55)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Launcher stopped")
    except Exception as e:
        print(f"❌ Launcher error: {e}")