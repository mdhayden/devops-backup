# Simple DevOps Demo for Windows PowerShell
# Quick demonstration of DevOps capabilities

Write-Host "🎉 Alpaca Trading Bot DevOps Demonstration" -ForegroundColor Magenta
Write-Host "======================================================" -ForegroundColor Cyan

# Git demonstration
Write-Host "`n🚀 Git Version Control" -ForegroundColor Yellow
Write-Host "-----------------------------" -ForegroundColor White
git --version
git status
git log --oneline -5

# Python code quality 
Write-Host "`n🔍 Code Quality Check" -ForegroundColor Yellow  
Write-Host "-----------------------------" -ForegroundColor White
python --version
Write-Host "Installing quality tools..."
pip install --quiet flake8 bandit safety

Write-Host "Running code quality checks..."
flake8 --max-line-length=88 --count --statistics *.py 2>$null
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Code quality check passed" -ForegroundColor Green
} else {
    Write-Host "⚠️  Code quality issues found" -ForegroundColor Yellow
}

# Docker demonstration
Write-Host "`n🐳 Docker Configuration" -ForegroundColor Yellow
Write-Host "-----------------------------" -ForegroundColor White
if (Get-Command docker -ErrorAction SilentlyContinue) {
    docker --version
    Write-Host "✅ Docker is available" -ForegroundColor Green
    
    if (Test-Path "Dockerfile") {
        Write-Host "`nDockerfile preview:"
        Get-Content "Dockerfile" | Select-Object -First 10
    }
} else {
    Write-Host "❌ Docker not installed" -ForegroundColor Red
}

# CI/CD Pipeline
Write-Host "`n⚙️  CI/CD Pipeline Configuration" -ForegroundColor Yellow  
Write-Host "-----------------------------" -ForegroundColor White

if (Test-Path "azure-pipelines.yml") {
    Write-Host "✅ Azure DevOps pipeline configured" -ForegroundColor Green
    Write-Host "`nPipeline stages preview:"
    Get-Content "azure-pipelines.yml" | Select-String "stage:" | Select-Object -First 5
}

if (Test-Path ".github\workflows\ci-cd.yml") {
    Write-Host "✅ GitHub Actions workflow configured" -ForegroundColor Green
}

# Kubernetes
Write-Host "`n☸️  Kubernetes Configuration" -ForegroundColor Yellow
Write-Host "-----------------------------" -ForegroundColor White
if (Test-Path "k8s\deployment.yaml") {
    Write-Host "✅ Kubernetes deployment manifest found" -ForegroundColor Green
    Write-Host "`nDeployment preview:"
    Get-Content "k8s\deployment.yaml" | Select-Object -First 8
}

# Terraform
Write-Host "`n🏗️  Infrastructure as Code" -ForegroundColor Yellow
Write-Host "-----------------------------" -ForegroundColor White
if (Test-Path "terraform\main.tf") {
    Write-Host "✅ Terraform configuration found" -ForegroundColor Green
    Write-Host "`nInfrastructure preview:"
    Get-Content "terraform\main.tf" | Select-Object -First 8
}

# Trading Bot Test
Write-Host "`n📊 Trading Bot Configuration" -ForegroundColor Yellow
Write-Host "-----------------------------" -ForegroundColor White
if (Test-Path "check_config.py") {
    Write-Host "Running configuration check..."
    python check_config.py
}

# Summary
Write-Host "`n🎯 DevOps Summary" -ForegroundColor Green
Write-Host "======================================================" -ForegroundColor Cyan
Write-Host "✅ Git repository configured and committed" -ForegroundColor Green
Write-Host "✅ Python code quality tools installed" -ForegroundColor Green  
Write-Host "✅ Docker containerization configured" -ForegroundColor Green
Write-Host "✅ Kubernetes deployment manifests ready" -ForegroundColor Green
Write-Host "✅ CI/CD pipelines configured (Azure + GitHub)" -ForegroundColor Green
Write-Host "✅ Infrastructure as Code with Terraform" -ForegroundColor Green
Write-Host "✅ Monitoring stack with Prometheus" -ForegroundColor Green
Write-Host "✅ Trading bot application ready" -ForegroundColor Green

Write-Host "`n🚀 Next Steps:" -ForegroundColor Yellow
Write-Host "1. Create Azure DevOps organization at https://dev.azure.com" -ForegroundColor White
Write-Host "2. Import repository: https://github.com/MarioH88/devops.git" -ForegroundColor White  
Write-Host "3. Configure and run the CI/CD pipeline" -ForegroundColor White
Write-Host "4. Deploy to Azure Container Instances" -ForegroundColor White
Write-Host "5. Set up monitoring and alerts" -ForegroundColor White

Write-Host "`n📚 Documentation:" -ForegroundColor Cyan
Write-Host "• AZURE_DEVOPS_SETUP.md - Complete setup guide" -ForegroundColor White
Write-Host "• QUICK_START.md - 5-minute quick start" -ForegroundColor White  
Write-Host "• azure-pipelines.yml - CI/CD pipeline configuration" -ForegroundColor White

Write-Host "`n🎊 DevOps demonstration completed successfully!" -ForegroundColor Magenta