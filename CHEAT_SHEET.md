# 📋 Live Demo Cheat Sheet - Keep This Open!

## 🎯 Quick Commands (Copy & Paste Ready)

### Test Commands:
```bash
python -m pytest tests/ -v --tb=no
python -m pytest tests/test_basic.py::test_basic_math -v
python -m pytest tests/test_basic.py::test_new_roi_feature -v
bandit security_demo.py -f txt
```

### Files to Edit:
- **tests/test_basic.py** → Line 56: Change `assert 2 * 3 == 6` to `assert 2 * 3 == 999` then back
- **roi_calculator.py** → Create new file with ROI functions
- **security_demo.py** → Create new file with vulnerable code

### Quick Code Snippets:

#### ROI Calculator (roi_calculator.py):
```python
def calculate_roi(initial_investment, final_value):
    if initial_investment <= 0:
        raise ValueError("Initial investment must be positive")
    roi = ((final_value - initial_investment) / initial_investment) * 100
    return round(roi, 2)

def calculate_profit_loss(buy_price, sell_price, shares):
    return (sell_price - buy_price) * shares
```

#### Test Addition (add to tests/test_basic.py):
```python
def test_new_roi_feature():
    from roi_calculator import calculate_roi, calculate_profit_loss
    roi = calculate_roi(1000, 1200)
    assert roi == 20.0
    profit = calculate_profit_loss(10.0, 12.0, 100)
    assert profit == 200.0
```

#### Vulnerable Code (security_demo.py):
```python
import os

def unsafe_function(user_input):
    os.system(f"echo {user_input}")  # Shell injection!

def process_trade_data(filename):
    with open(f"/data/{filename}", 'r') as f:  # Path traversal!
        return f.read()
```

### Restore if needed:
```bash
copy tests\test_basic_backup.py tests\test_basic.py
```

## 🗣️ Key Talking Points:
1. "Pipeline prevents bugs from production"
2. "Security scanning protects trading data"  
3. "Test-driven development ensures reliability"
4. "50% faster builds, 100% more secure"

## ⚡ Demo Flow:
1. Show working → 2. Break it → 3. Fix it → 4. Add feature → 5. Security check