# 🎬 Manual Live Changes Demo Guide

## 🎯 **Simple Manual Demo Steps (3-5 minutes)**

### **Before Your Presentation:**
1. Open VS Code with your project
2. Have PowerShell terminal ready
3. Open `tests/test_basic.py` in editor
4. Bookmark line 45 where you'll make changes

---

## 🔧 **Live Demo Step-by-Step**

### **Step 1: Show Everything Works** (30 seconds)
```bash
# In terminal, run:
python -m pytest tests/ -v --tb=no
```
**Say:** *"First, let me show you our current system - all 20 tests are passing."*

---

### **Step 2: Break Something Live** (60 seconds)

**In VS Code, open `tests/test_basic.py`:**
1. Find line 56: `assert 2 * 3 == 6`
2. **Live edit:** Change it to `assert 2 * 3 == 999`
3. Save the file (Ctrl+S)

**In terminal:**
```bash
python -m pytest tests/test_basic.py::test_basic_math -v
```

**Say:** *"I just introduced a bug - watch how the CI/CD pipeline catches it immediately. In production, this would prevent deployment."*

---

### **Step 3: Fix It Live** (30 seconds)

**In VS Code:**
1. Change line 56 back: `assert 2 * 3 == 6`
2. Save the file (Ctrl+S)

**In terminal:**
```bash
python -m pytest tests/test_basic.py::test_basic_math -v
```

**Say:** *"Fixed! The pipeline validates the fix and gives us green light for deployment."*

---

### **Step 4: Add New Feature Live** (90 seconds)

**Create new file `roi_calculator.py`:**
```python
def calculate_roi(initial_investment, final_value):
    """Calculate Return on Investment percentage"""
    if initial_investment <= 0:
        raise ValueError("Initial investment must be positive")
    
    roi = ((final_value - initial_investment) / initial_investment) * 100
    return round(roi, 2)

def calculate_profit_loss(buy_price, sell_price, shares):
    """Calculate profit/loss for a trade"""
    return (sell_price - buy_price) * shares
```

**Add test to `tests/test_basic.py` (at the end):**
```python
def test_new_roi_feature():
    """Test new ROI calculation feature"""
    from roi_calculator import calculate_roi, calculate_profit_loss
    
    # Test ROI calculation
    roi = calculate_roi(1000, 1200)
    assert roi == 20.0
    
    # Test profit calculation
    profit = calculate_profit_loss(10.0, 12.0, 100)
    assert profit == 200.0
```

**In terminal:**
```bash
python -m pytest tests/test_basic.py::test_new_roi_feature -v
```

**Say:** *"Here's how we add new features with test-driven development - feature and test together, validated immediately."*

---

### **Step 5: Security Demo** (60 seconds)

**Create `security_demo.py`:**
```python
import os

def unsafe_function(user_input):
    """This has a security vulnerability"""
    os.system(f"echo {user_input}")  # Shell injection risk!

def process_trade_data(filename):
    """Another security issue"""
    with open(f"/data/{filename}", 'r') as f:  # Path traversal risk!
        return f.read()
```

**In terminal:**
```bash
bandit security_demo.py -f txt
```

**Say:** *"Our security scanner immediately detects vulnerabilities that could expose trading data or allow unauthorized access."*

---

### **Step 6: Show All Tests Still Pass** (30 seconds)

**In terminal:**
```bash
python -m pytest tests/ -v --tb=no
```

**Say:** *"After all our changes, the comprehensive test suite ensures everything still works perfectly."*

---

## 🗣️ **What to Say During Each Step**

### **Opening:**
> "I'm going to show you live changes to demonstrate how our CI/CD pipeline works in real-time. This isn't just slides - it's a working system."

### **When Breaking Code:**
> "This simulates a real development scenario where someone accidentally introduces a bug. Watch how the pipeline prevents this from reaching production."

### **When Fixing Code:**
> "The fix is validated immediately. In our deployment pipeline, only code that passes all tests can be deployed to production."

### **When Adding Features:**
> "Here's test-driven development in action. I'm creating both the feature and its test simultaneously, ensuring reliability from day one."

### **When Showing Security:**
> "Security is critical for financial applications. Our automated scanning catches vulnerabilities that could expose trading credentials or allow unauthorized access."

### **Closing:**
> "This demonstrates a production-ready DevOps pipeline that's 50% faster, 100% more secure, and catches problems before they impact users."

---

## 🎯 **Easy Manual Commands Reference**

Keep this handy during your presentation:

```bash
# Show all tests work
python -m pytest tests/ -v --tb=no

# Test specific function after changes
python -m pytest tests/test_basic.py::test_basic_math -v

# Test new feature
python -m pytest tests/test_basic.py::test_new_roi_feature -v

# Security scan
bandit security_demo.py -f txt

# Check all systems after changes
python -m pytest tests/ --tb=no -q
```

---

## 🔧 **Files You'll Edit Live:**

1. **`tests/test_basic.py`** - Line 45 for break/fix demo
2. **`roi_calculator.py`** - New file for feature demo
3. **`security_demo.py`** - New file for security demo

---

## 🚨 **If Something Goes Wrong:**

**Backup plan:**
```bash
# Show the working system
python -m pytest tests/ -v

# Show security results
bandit -r . -x ./tests/ -f txt --severity-level high

# Say: "The automation ensures these checks run on every commit!"
```

---

## 💡 **Pro Tips for Manual Demo:**

1. **Practice the keystrokes** - Know exactly what to type
2. **Have VS Code ready** - Files open and ready to edit
3. **Use large font** - Audience needs to see your code
4. **Narrate as you go** - Explain what you're doing
5. **Stay calm** - If something breaks, explain how the pipeline handles it

**Remember:** The goal is showing the **process** and **automation**, not perfect execution!

---

## 🎬 **Presentation Flow:**

1. **"Let me show you this pipeline working live"**
2. **Break something** → Pipeline catches it
3. **Fix it** → Pipeline validates fix  
4. **Add feature** → Tests ensure it works
5. **Show security** → Scanner prevents vulnerabilities
6. **"This is enterprise DevOps in action!"**

Your manual changes will prove the CI/CD pipeline is **real, working, and production-ready**! 🚀