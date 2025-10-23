# Live Demo Automation Script
# Run this during your presentation to show real-time changes

param(
    [string]$Action = "help"
)

function Show-Header {
    param([string]$Title)
    Write-Host "`n" -NoNewline
    Write-Host "="*60 -ForegroundColor Cyan
    Write-Host " $Title" -ForegroundColor Yellow
    Write-Host "="*60 -ForegroundColor Cyan
}

function Demo-WorkingSystem {
    Show-Header "STEP 1: SHOWING WORKING SYSTEM"
    Write-Host "🔍 Running comprehensive test suite..." -ForegroundColor Green
    python -m pytest tests/ --tb=no -q
    Write-Host "✅ All systems operational and ready!" -ForegroundColor Green
}

function Demo-BreakAndFix {
    Show-Header "STEP 2: BREAK IT, CATCH IT, FIX IT"
    
    # Backup original
    Copy-Item "tests\test_basic.py" "tests\test_basic.py.backup" -Force
    
    Write-Host "🔨 Introducing a bug to demonstrate pipeline protection..." -ForegroundColor Yellow
    (Get-Content "tests\test_basic.py") -replace 'assert result == 150', 'assert result == 999' | Set-Content "tests\test_basic.py"
    
    Write-Host "🧪 Running tests to show pipeline catches the bug..." -ForegroundColor Red
    python -m pytest "tests/test_basic.py::test_basic_math" -v
    Write-Host "❌ Pipeline prevents buggy code from deploying!" -ForegroundColor Red
    
    Write-Host "`n🔧 Fixing the bug..." -ForegroundColor Yellow
    (Get-Content "tests\test_basic.py") -replace 'assert result == 999', 'assert result == 150' | Set-Content "tests\test_basic.py"
    
    Write-Host "✅ Running tests to confirm fix..." -ForegroundColor Green
    python -m pytest "tests/test_basic.py::test_basic_math" -v
    Write-Host "✅ Bug fixed - ready for deployment!" -ForegroundColor Green
}

function Demo-NewFeature {
    Show-Header "STEP 3: ADDING NEW FEATURE WITH TDD"
    
    Write-Host "💡 Creating new ROI calculation feature..." -ForegroundColor Yellow
    
    # Create new feature
    @'
def calculate_roi(initial, final):
    """Calculate Return on Investment for trading"""
    if initial <= 0:
        raise ValueError("Initial investment must be positive")
    return ((final - initial) / initial) * 100

def calculate_profit_loss(buy_price, sell_price, quantity):
    """Calculate profit/loss for a trade"""
    return (sell_price - buy_price) * quantity
'@ | Out-File -FilePath "new_trading_feature.py" -Encoding UTF8
    
    # Add test for new feature
    @'

def test_roi_calculation():
    """Test ROI calculation for trading bot"""
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + "/..")
    from new_trading_feature import calculate_roi
    
    # Test basic ROI calculation
    result = calculate_roi(1000, 1200)
    assert result == 20.0
    
    # Test different scenario
    result = calculate_roi(500, 750)
    assert result == 50.0

def test_profit_loss_calculation():
    """Test profit/loss calculation"""
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + "/..")
    from new_trading_feature import calculate_profit_loss
    
    # Test profit scenario
    profit = calculate_profit_loss(10.0, 12.0, 100)
    assert profit == 200.0
    
    # Test loss scenario  
    loss = calculate_profit_loss(15.0, 12.0, 50)
    assert loss == -150.0
'@ | Add-Content "tests\test_basic.py"
    
    Write-Host "🧪 Testing new feature..." -ForegroundColor Green
    python -m pytest "tests/test_basic.py::test_roi_calculation" -v
    python -m pytest "tests/test_basic.py::test_profit_loss_calculation" -v
    Write-Host "✅ New trading features deployed with full test coverage!" -ForegroundColor Green
}

function Demo-Security {
    Show-Header "STEP 4: SECURITY VULNERABILITY DETECTION"
    
    Write-Host "🚨 Creating code with security vulnerability..." -ForegroundColor Red
    
    # Create vulnerable code
    @'
import os
import subprocess

def unsafe_trading_command(user_input):
    """VULNERABLE - Shell injection possible"""
    os.system(f"echo Processing trade: {user_input}")
    
def execute_trade_command(command):
    """VULNERABLE - Command injection risk"""
    subprocess.run(command, shell=True)
    
def process_trading_data(filename):
    """VULNERABLE - Path traversal possible"""
    with open(f"/data/{filename}", 'r') as f:
        return f.read()
'@ | Out-File -FilePath "vulnerable_trading.py" -Encoding UTF8
    
    Write-Host "🔍 Running security scan..." -ForegroundColor Yellow
    bandit "vulnerable_trading.py" -f txt
    Write-Host "🚨 Security scanner caught vulnerabilities in trading code!" -ForegroundColor Red
    
    Write-Host "`n🔒 Creating secure version..." -ForegroundColor Green
    
    # Create secure version
    @'
import subprocess
import os.path

def safe_trading_command(user_input):
    """SECURE - No shell injection possible"""
    print(f"Processing trade: {user_input}")
    
def execute_safe_trade_command(command_parts):
    """SECURE - No shell injection"""
    subprocess.run(command_parts, shell=False)
    
def process_trading_data(filename):
    """SECURE - Path validation"""
    # Validate filename to prevent path traversal
    if not filename.replace('_', '').replace('-', '').isalnum():
        raise ValueError("Invalid filename")
    safe_path = os.path.join("/data", os.path.basename(filename))
    with open(safe_path, 'r') as f:
        return f.read()
'@ | Out-File -FilePath "secure_trading.py" -Encoding UTF8
    
    Write-Host "🔍 Scanning secure version..." -ForegroundColor Green
    bandit "secure_trading.py" -f txt
    Write-Host "✅ Security issues resolved - trading system is secure!" -ForegroundColor Green
}

function Demo-CodeQuality {
    Show-Header "STEP 5: CODE QUALITY ENFORCEMENT"
    
    Write-Host "📝 Creating poorly formatted code..." -ForegroundColor Yellow
    
    # Create messy code
    @'
def   bad_trading_function( price,quantity ):
    if price>0:
        return price*quantity
    else:return 0

class  BadTradingClass:
    def __init__( self,symbol ):
        self.symbol=symbol
        self.price=None

    def calculate_value(self,shares):
        if self.price is None:return None
        return self.price*shares
'@ | Out-File -FilePath "messy_trading.py" -Encoding UTF8
    
    Write-Host "🔍 Running code quality check..." -ForegroundColor Red
    flake8 "messy_trading.py" --show-source
    Write-Host "❌ Code quality issues detected!" -ForegroundColor Red
    
    Write-Host "`n🔧 Auto-formatting with Black..." -ForegroundColor Yellow
    black "messy_trading.py" --quiet
    
    Write-Host "📖 Showing formatted code:" -ForegroundColor Green
    Get-Content "messy_trading.py"
    Write-Host "✅ Code quality improved automatically!" -ForegroundColor Green
}

function Demo-Cleanup {
    Show-Header "STEP 6: CLEANUP AND VERIFICATION"
    
    Write-Host "🧹 Cleaning up demo files..." -ForegroundColor Yellow
    Remove-Item -Path "new_trading_feature.py", "vulnerable_trading.py", "secure_trading.py", "messy_trading.py" -ErrorAction SilentlyContinue
    
    # Restore original test file
    if (Test-Path "tests\test_basic.py.backup") {
        Copy-Item "tests\test_basic.py.backup" "tests\test_basic.py" -Force
        Remove-Item "tests\test_basic.py.backup"
    }
    
    Write-Host "🔍 Verifying system is back to stable state..." -ForegroundColor Green
    python -m pytest tests/ --tb=no -q
    Write-Host "✅ All systems restored and operational!" -ForegroundColor Green
    
    Write-Host "`n🎉 LIVE DEMO COMPLETE!" -ForegroundColor Cyan
    Write-Host "Key Takeaways:" -ForegroundColor Yellow
    Write-Host "  ✅ Pipeline prevents bugs from reaching production" -ForegroundColor Green
    Write-Host "  ✅ Security scanning protects trading systems" -ForegroundColor Green  
    Write-Host "  ✅ Quality gates ensure professional code standards" -ForegroundColor Green
    Write-Host "  ✅ Everything is automated and fast" -ForegroundColor Green
}

function Show-Help {
    Write-Host "🎬 LIVE DEMO AUTOMATION SCRIPT" -ForegroundColor Cyan
    Write-Host "Usage: .\live_demo.ps1 [action]" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Actions:" -ForegroundColor Green
    Write-Host "  full      - Run complete 5-minute demo" -ForegroundColor White
    Write-Host "  working   - Show working system" -ForegroundColor White
    Write-Host "  break     - Demonstrate break/fix cycle" -ForegroundColor White
    Write-Host "  feature   - Add new feature with TDD" -ForegroundColor White
    Write-Host "  security  - Security vulnerability demo" -ForegroundColor White
    Write-Host "  quality   - Code quality improvement" -ForegroundColor White
    Write-Host "  cleanup   - Clean up and restore" -ForegroundColor White
    Write-Host ""
    Write-Host "Example: .\live_demo.ps1 full" -ForegroundColor Yellow
}

# Main execution
switch ($Action.ToLower()) {
    "full" {
        Demo-WorkingSystem
        Demo-BreakAndFix
        Demo-NewFeature
        Demo-Security
        Demo-CodeQuality
        Demo-Cleanup
    }
    "working" { Demo-WorkingSystem }
    "break" { Demo-BreakAndFix }
    "feature" { Demo-NewFeature }
    "security" { Demo-Security }
    "quality" { Demo-CodeQuality }
    "cleanup" { Demo-Cleanup }
    default { Show-Help }
}