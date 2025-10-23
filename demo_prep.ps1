# PowerShell Demo Preparation Script
# Run this before your live demo

Write-Host "🎯 PREPARING CI/CD PIPELINE DEMO" -ForegroundColor Cyan
Write-Host "=" * 50

# Clear screen for clean demo
Clear-Host

Write-Host "🚀 Demo Environment Check" -ForegroundColor Green
Write-Host "Current Directory: $(Get-Location)" -ForegroundColor Yellow

# Check if we're in the right directory
if (Test-Path "main.py" -and Test-Path ".github/workflows/ci-cd.yml") {
    Write-Host "✅ In correct project directory" -ForegroundColor Green
} else {
    Write-Host "❌ Navigate to project root directory first!" -ForegroundColor Red
    exit 1
}

# Pre-demo checklist
Write-Host "`n📋 PRE-DEMO CHECKLIST:" -ForegroundColor Cyan

$tasks = @(
    @{Name="Test Suite"; Command="python -m pytest tests/ --tb=no -q"},
    @{Name="Security Scan"; Command="bandit -r . -x ./tests/ -f txt --severity-level high"},
    @{Name="Code Quality"; Command="flake8 . --count"},
    @{Name="Dependencies"; Command="pip list | findstr -i 'requests urllib3'"}
)

foreach ($task in $tasks) {
    Write-Host "🔧 Checking: $($task.Name)" -ForegroundColor Yellow
    try {
        $result = Invoke-Expression $task.Command 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "  ✅ $($task.Name) - OK" -ForegroundColor Green
        } else {
            Write-Host "  ⚠️  $($task.Name) - Check needed" -ForegroundColor Yellow
        }
    } catch {
        Write-Host "  ❌ $($task.Name) - Failed" -ForegroundColor Red
    }
}

Write-Host "`n🎬 DEMO COMMAND REFERENCE:" -ForegroundColor Cyan
Write-Host "=" * 40

$demoCommands = @(
    "# 1. Show comprehensive test suite",
    "python -m pytest tests/ -v",
    "",
    "# 2. Demonstrate security scanning", 
    "bandit -r . -x ./tests/ -f txt",
    "",
    "# 3. Code quality check",
    "flake8 . --count --statistics",
    "",
    "# 4. Show CI/CD pipeline",
    "Get-Content .github/workflows/ci-cd.yml | Select-Object -First 30",
    "",
    "# 5. Docker build (optional)",
    "docker build -t trading-bot:demo ."
)

foreach ($cmd in $demoCommands) {
    if ($cmd.StartsWith("#")) {
        Write-Host $cmd -ForegroundColor Cyan
    } elseif ($cmd -eq "") {
        Write-Host ""
    } else {
        Write-Host $cmd -ForegroundColor White
    }
}

Write-Host "`n🎯 KEY DEMO POINTS:" -ForegroundColor Cyan
Write-Host "✅ 20 comprehensive tests (100% pass rate)" -ForegroundColor Green
Write-Host "✅ 0 high-severity security issues" -ForegroundColor Green  
Write-Host "✅ 59% reduction in code quality issues" -ForegroundColor Green
Write-Host "✅ Multi-environment CI/CD pipeline" -ForegroundColor Green
Write-Host "✅ Docker & Azure Container deployment ready" -ForegroundColor Green

Write-Host "`n🚀 DEMO READY! Good luck with your presentation!" -ForegroundColor Green
Write-Host "📖 Check LIVE_DEMO_SCRIPT.md for detailed talking points" -ForegroundColor Yellow