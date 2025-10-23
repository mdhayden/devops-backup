@echo off
cls
echo.
echo 🎉 AZURE DEVOPS LIVE DEMO LAUNCHER
echo ==========================================
echo.
echo Choose your demo type:
echo.
echo 1. Quick Overview (2 minutes)
echo 2. Full Azure DevOps Demo (15 minutes)  
echo 3. Trading Bot Dashboard Only
echo 4. Show All DevOps Files
echo 5. Exit
echo.
set /p choice=Enter your choice (1-5): 

if "%choice%"=="1" goto quick
if "%choice%"=="2" goto full
if "%choice%"=="3" goto dashboard
if "%choice%"=="4" goto files
if "%choice%"=="5" goto exit
goto menu

:quick
cls
echo 🚀 QUICK DEVOPS OVERVIEW
echo ========================
echo.
echo Repository: https://github.com/MarioH88/devops.git
git status
echo.
echo 📋 DevOps Components:
if exist "azure-pipelines.yml" echo ✅ Azure DevOps Pipeline
if exist "Dockerfile" echo ✅ Docker Containerization  
if exist "k8s\deployment.yaml" echo ✅ Kubernetes Deployment
if exist "terraform\main.tf" echo ✅ Infrastructure as Code
if exist ".github\workflows\ci-cd.yml" echo ✅ GitHub Actions
if exist "monitoring\prometheus.yml" echo ✅ Monitoring Stack
echo.
echo 🎯 Next: Go to https://dev.azure.com
echo 1. Create organization: "your-name-devops"
echo 2. Import: https://github.com/MarioH88/devops.git
echo 3. Run the CI/CD pipeline!
pause
goto menu

:full
cls
echo 🎯 FULL AZURE DEVOPS DEMO GUIDE
echo ================================
echo.
echo STEP 1: Show Repository Structure
dir /w
echo.
echo STEP 2: Azure DevOps Pipeline Configuration
type azure-pipelines.yml | findstr /n "stage\|displayName" | findstr /r "^[1-9]:"
echo.
echo STEP 3: Show Docker Configuration
echo --- Dockerfile Preview ---
type Dockerfile | findstr /n "FROM\|RUN\|COPY\|CMD" | findstr /r "^[1-9]:"
echo.
echo STEP 4: Infrastructure as Code
echo --- Terraform Configuration ---
type terraform\main.tf | findstr /n "resource\|provider" | findstr /r "^[1-5]:"
echo.
echo 🔗 LIVE DEMO STEPS:
echo 1. Go to https://dev.azure.com
echo 2. Create project and import repository
echo 3. Configure pipeline with azure-pipelines.yml
echo 4. Run pipeline and show results
echo 5. Demonstrate trading bot dashboard
echo.
pause
goto menu

:dashboard
cls
echo 📊 TRADING BOT DASHBOARD DEMO
echo =============================
echo.
echo Starting trading bot dashboard...
python web_dashboard.py
echo.
echo ✅ Dashboard created: dashboard.html
echo 🌐 Opening in browser...
start dashboard.html
echo.
echo 🎯 Demo Points:
echo - Real-time market data
echo - Account status monitoring  
echo - Trading history tracking
echo - Auto-refreshing interface
echo.
pause
goto menu

:files
cls
echo 📁 DEVOPS FILES OVERVIEW
echo =========================
echo.
echo 🔧 CI/CD Pipeline:
if exist "azure-pipelines.yml" echo   ✅ azure-pipelines.yml - Azure DevOps pipeline
if exist ".github\workflows\ci-cd.yml" echo   ✅ .github/workflows/ci-cd.yml - GitHub Actions

echo.
echo 🐳 Containerization:
if exist "Dockerfile" echo   ✅ Dockerfile - Multi-stage container build
if exist "docker-compose.yml" echo   ✅ docker-compose.yml - Monitoring stack

echo.
echo ☸️  Kubernetes:
if exist "k8s\deployment.yaml" echo   ✅ k8s/deployment.yaml - K8s deployment manifest

echo.
echo 🏗️  Infrastructure:
if exist "terraform\main.tf" echo   ✅ terraform/main.tf - Azure infrastructure code

echo.
echo 📊 Monitoring:
if exist "monitoring\prometheus.yml" echo   ✅ monitoring/prometheus.yml - Metrics collection

echo.
echo 🧪 Testing:
if exist "tests\test_trading_bot.py" echo   ✅ tests/test_trading_bot.py - Unit tests

echo.
echo 📚 Documentation:
if exist "AZURE_DEVOPS_SETUP.md" echo   ✅ AZURE_DEVOPS_SETUP.md - Setup guide
if exist "QUICK_START.md" echo   ✅ QUICK_START.md - Quick start guide
if exist "LIVE_DEMO_GUIDE.md" echo   ✅ LIVE_DEMO_GUIDE.md - Demo instructions

echo.
pause
goto menu

:exit
echo.
echo 👋 Thanks for using the DevOps Demo Launcher!
echo 🚀 Repository: https://github.com/MarioH88/devops.git
echo 📚 Full setup guide: AZURE_DEVOPS_SETUP.md
echo.
exit /b 0

:menu
goto start

:start
cls
echo.
echo 🎉 AZURE DEVOPS LIVE DEMO LAUNCHER
echo ==========================================
echo.
echo Choose your demo type:
echo.
echo 1. Quick Overview (2 minutes)
echo 2. Full Azure DevOps Demo (15 minutes)  
echo 3. Trading Bot Dashboard Only
echo 4. Show All DevOps Files
echo 5. Exit
echo.
set /p choice=Enter your choice (1-5): 

if "%choice%"=="1" goto quick
if "%choice%"=="2" goto full
if "%choice%"=="3" goto dashboard
if "%choice%"=="4" goto files
if "%choice%"=="5" goto exit
echo Invalid choice. Please enter 1-5.
pause
goto menu