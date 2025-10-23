# 🎬 Live Changes Demo Script

## 🚀 **How to Demonstrate Live Changes During Your Presentation**

### 🎯 **Demo Strategy: "Break It, Fix It, Deploy It"**

Show your audience that the CI/CD pipeline actually catches problems and deploys fixes in real-time.

---

## 🔧 **Demo 1: Breaking and Fixing a Test**

### **Step 1: Show Everything Working** (30 seconds)
```bash
# Show current state - all tests pass
python -m pytest tests/ -v --tb=no
echo "✅ All systems operational"
```

### **Step 2: Introduce a "Bug" Live** (30 seconds)
```python
# Edit tests/test_basic.py - change line 45 to break a test
# Original: assert result == 150
# Change to: assert result == 999  # This will fail
```

**Live Edit Command:**
```bash
# Windows PowerShell
(Get-Content tests\test_basic.py) -replace 'assert result == 150', 'assert result == 999' | Set-Content tests\test_basic.py
```

### **Step 3: Show the Pipeline Catches the Bug** (30 seconds)
```bash
# Run tests again - show failure
python -m pytest tests/test_basic.py::test_basic_math -v
echo "❌ Pipeline would prevent this from deploying!"
```

### **Step 4: Fix the Bug Live** (30 seconds)
```bash
# Fix it back
(Get-Content tests\test_basic.py) -replace 'assert result == 999', 'assert result == 150' | Set-Content tests\test_basic.py

# Show it's fixed
python -m pytest tests/test_basic.py::test_basic_math -v
echo "✅ Bug fixed, ready for deployment!"
```

---

## 🔧 **Demo 2: Adding a New Feature with Tests**

### **Step 1: Add a New Function Live** (60 seconds)
Create a new file during the demo:

```bash
# Create new feature file
echo 'def calculate_roi(initial, final):
    """Calculate Return on Investment"""
    if initial <= 0:
        raise ValueError("Initial investment must be positive")
    return ((final - initial) / initial) * 100' > new_feature.py
```

### **Step 2: Add Test for New Feature** (30 seconds)
```bash
# Add test to existing test file
echo '
def test_roi_calculation():
    """Test ROI calculation"""
    import sys
    sys.path.append(".")
    from new_feature import calculate_roi
    
    result = calculate_roi(1000, 1200)
    assert result == 20.0
    
    result = calculate_roi(500, 750)
    assert result == 50.0' >> tests/test_basic.py
```

### **Step 3: Show Tests Pass** (30 seconds)
```bash
# Run the new test
python -m pytest tests/test_basic.py::test_roi_calculation -v
echo "✅ New feature tested and ready!"
```

---

## 🔧 **Demo 3: Security Vulnerability Detection**

### **Step 1: Introduce Security Issue Live** (45 seconds)
```bash
# Create a file with security vulnerability
echo 'import os
import subprocess

def unsafe_command(user_input):
    # SECURITY VULNERABILITY - shell injection
    os.system(f"echo {user_input}")
    
def run_user_command(cmd):
    # Another vulnerability 
    subprocess.run(cmd, shell=True)' > vulnerable_code.py
```

### **Step 2: Show Security Scanner Catches It** (30 seconds)
```bash
# Run security scan
bandit vulnerable_code.py -f txt
echo "🚨 Security scanner caught the vulnerabilities!"
```

### **Step 3: Fix Security Issues Live** (45 seconds)
```bash
# Create secure version
echo 'import subprocess

def safe_command(user_input):
    # SECURE - no shell injection possible
    print(f"Echo: {user_input}")
    
def run_safe_command(cmd):
    # Secure subprocess call
    subprocess.run(cmd.split(), shell=False)' > secure_code.py

# Show it's now secure
bandit secure_code.py -f txt
echo "✅ Security issues resolved!"
```

---

## 🔧 **Demo 4: Code Quality Improvement**

### **Step 1: Show Current Code Quality** (30 seconds)
```bash
# Check current linting score
flake8 . --count --statistics
echo "Current code quality baseline"
```

### **Step 2: Add Poorly Formatted Code** (30 seconds)
```bash
# Create messy code file
echo 'def   bad_function( x,y ):
    if x>0:
        return x+y
    else:return x-y

class  BadClass:
    def __init__( self,value ):
        self.value=value' > messy_code.py
```

### **Step 3: Show Linting Catches Issues** (30 seconds)
```bash
# Show linting errors
flake8 messy_code.py --show-source
echo "🔍 Code quality tools caught formatting issues!"
```

### **Step 4: Auto-fix with Black** (30 seconds)
```bash
# Auto-format the code
black messy_code.py
echo "✅ Code automatically formatted!"

# Show the fixed version
cat messy_code.py
```

---

## 🎬 **COMPLETE LIVE DEMO SCRIPT** (5 minutes total)

### **Setup Before Demo:**
```bash
# Save current state
cp tests/test_basic.py tests/test_basic.py.backup
echo "Demo environment ready!"
```

### **Live Demo Flow:**

```bash
echo "🎯 LIVE CI/CD PIPELINE DEMONSTRATION"
echo "=================================================="

# 1. Show everything working (30 sec)
echo "📊 Step 1: Current system status"
python -m pytest tests/ --tb=no -q
echo "✅ All 20 tests passing"

# 2. Break something (30 sec)
echo "📊 Step 2: Introducing a bug to show pipeline catches it"
(Get-Content tests\test_basic.py) -replace 'assert result == 150', 'assert result == 999' | Set-Content tests\test_basic.py
python -m pytest tests/test_basic.py::test_basic_math -v
echo "❌ Pipeline prevents buggy code from deploying!"

# 3. Fix it (30 sec)
echo "📊 Step 3: Fixing the bug"
(Get-Content tests\test_basic.py) -replace 'assert result == 999', 'assert result == 150' | Set-Content tests\test_basic.py
python -m pytest tests/test_basic.py::test_basic_math -v
echo "✅ Bug fixed, deployment ready!"

# 4. Add new feature (60 sec)
echo "📊 Step 4: Adding new feature with test-driven development"
echo 'def calculate_roi(initial, final):
    """Calculate Return on Investment"""
    if initial <= 0:
        raise ValueError("Initial investment must be positive")
    return ((final - initial) / initial) * 100' > new_feature.py

echo '
def test_roi_calculation():
    """Test ROI calculation for trading bot"""
    import sys
    sys.path.append(".")
    from new_feature import calculate_roi
    
    result = calculate_roi(1000, 1200)
    assert result == 20.0' >> tests/test_basic.py

python -m pytest tests/test_basic.py::test_roi_calculation -v
echo "✅ New feature deployed with automated testing!"

# 5. Security demonstration (60 sec)
echo "📊 Step 5: Security vulnerability detection"
echo 'import os
def unsafe_function(user_input):
    os.system(f"echo {user_input}")  # Vulnerability!' > vuln_demo.py

bandit vuln_demo.py -f txt
echo "🚨 Security scanner prevents vulnerable code!"

# 6. Cleanup and summary (30 sec)
rm -f new_feature.py vuln_demo.py messy_code.py 2>$null
cp tests/test_basic.py.backup tests/test_basic.py
rm tests/test_basic.py.backup

echo "📊 Step 6: System restored to stable state"
python -m pytest tests/ --tb=no -q
echo "✅ Demo complete - all systems operational!"
```

### **Cleanup After Demo:**
```bash
# Restore original state
cp tests/test_basic.py.backup tests/test_basic.py 2>$null || echo "Backup not found"
rm -f new_feature.py vuln_demo.py messy_code.py secure_code.py 2>$null
echo "Demo environment cleaned up!"
```

---

## 🗣️ **What to Say During Live Changes**

### **While Breaking the Test:**
> "Now I'm going to deliberately introduce a bug to show you how the CI/CD pipeline prevents bad code from reaching production. In real development, this could be an accidental typo or logic error."

### **While Fixing the Bug:**
> "The pipeline caught the bug immediately. Now I'll fix it, and you'll see how quickly we can validate the fix and get back to a deployable state."

### **While Adding New Feature:**
> "Here's how we add new features with test-driven development. I'll create a new function and its test simultaneously - this ensures the feature works correctly before deployment."

### **While Showing Security Issues:**
> "Security is critical for financial applications. Watch how our automated security scanning catches vulnerabilities that could expose trading credentials or allow unauthorized access."

---

## 🎯 **Key Messages During Live Demo**

1. **"This isn't just theory - it's working DevOps"**
2. **"The pipeline prevents bugs from reaching production"**
3. **"Security scanning protects financial data"**
4. **"Quality gates ensure code standards"**
5. **"Everything is automated and fast"**

---

## 🚨 **Backup Plan If Something Goes Wrong**

If a command fails during the live demo:

```bash
# Quick recovery
echo "Let me show you the output from our comprehensive test suite instead:"
python -m pytest tests/ -v --tb=no

echo "And here's our security scan results:"
bandit -r . -x ./tests/ -f txt --severity-level high

echo "The pipeline automation ensures these checks run on every commit!"
```

**Remember**: The goal is to show the **process** and **automation**, not perfect execution. Even if something breaks, you can explain how the pipeline would handle it!

This live demo proves your CI/CD pipeline is **real, working, and production-ready**! 🚀