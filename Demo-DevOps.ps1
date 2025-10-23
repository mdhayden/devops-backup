# DevOps Demonstration PowerShell Script for Windows
# This script demonstrates the complete DevOps pipeline for the Alpaca Trading Bot

param(
    [string]$DemoType = "full",
    [switch]$SkipDocker = $false,
    [switch]$SkipKubernetes = $false
)

# Color functions for better output
function Write-Section {
    param([string]$Title)
    Write-Host "`n$('=' * 60)" -ForegroundColor Cyan
    Write-Host "🚀 $Title" -ForegroundColor Yellow
    Write-Host "$('=' * 60)" -ForegroundColor Cyan
}

function Write-Success {
    param([string]$Message)
    Write-Host "✅ $Message" -ForegroundColor Green
}

function Write-Error {
    param([string]$Message)
    Write-Host "❌ $Message" -ForegroundColor Red
}

function Write-Info {
    param([string]$Message)
    Write-Host "📋 $Message" -ForegroundColor Blue
}

function Write-Command {
    param([string]$Command)
    Write-Host "💻 Command: $Command" -ForegroundColor Gray
}

# Function to run commands with error handling
function Invoke-DemoCommand {
    param(
        [string]$Command,
        [string]$Description,
        [int]$TimeoutSeconds = 30,
        [switch]$IgnoreErrors = $false
    )
    
    Write-Info $Description
    Write-Command $Command
    Write-Host ("-" * 40)
    
    try {
        $job = Start-Job -ScriptBlock {
            param($cmd)
            Invoke-Expression $cmd
        } -ArgumentList $Command
        
        $result = Wait-Job $job -Timeout $TimeoutSeconds
        
        if ($result) {
            $output = Receive-Job $job
            Remove-Job $job
            
            if ($job.State -eq "Completed") {
                Write-Success "Command completed successfully"
                if ($output) {
                    Write-Host $output
                }
            } else {
                Write-Error "Command failed or timed out"
                if ($output) {
                    Write-Host $output
                }
            }
        } else {
            Stop-Job $job
            Remove-Job $job
            Write-Error "Command timed out after $TimeoutSeconds seconds"
        }
    }
    catch {
        Write-Error "Exception occurred: $($_.Exception.Message)"
        if (-not $IgnoreErrors) {
            throw
        }
    }
}

# Check prerequisites
function Test-Prerequisites {
    Write-Section "Prerequisites Check"
    
    $prerequisites = @{
        "Git" = "git --version"
        "Python" = "python --version"
        "Pip" = "pip --version"
        "Docker" = "docker --version"
        "Kubectl" = "kubectl version --client"
        "Terraform" = "terraform --version"
    }
    
    $missing = @()
    
    foreach ($tool in $prerequisites.Keys) {
        try {
            $output = Invoke-Expression $prerequisites[$tool] 2>$null
            if ($output) {
                Write-Success "$tool is installed: $($output.Split("`n")[0])"
            } else {
                $missing += $tool
            }
        }
        catch {
            $missing += $tool
        }
    }
    
    if ($missing.Count -gt 0) {
        Write-Error "Missing tools: $($missing -join ', ')"
        Write-Host "Please install missing tools before running the demo."
        return $false
    }
    
    return $true
}

# Git Operations Demo
function Demo-GitOperations {
    Write-Section "Git Version Control Operations"
    
    Invoke-DemoCommand "git --version" "Check Git version"
    Invoke-DemoCommand "git status" "Repository status"
    Invoke-DemoCommand "git log --oneline -10" "Recent commits"
    Invoke-DemoCommand "git branch -a" "All branches"
    Invoke-DemoCommand "git remote -v" "Remote repositories"
}

# Python Code Quality Demo
function Demo-PythonQuality {
    Write-Section "Python Code Quality & Security"
    
    # Install tools if needed
    Invoke-DemoCommand "pip install flake8 bandit safety pytest pytest-cov" "Install quality tools" -IgnoreErrors
    
    # Code quality checks
    Invoke-DemoCommand "flake8 --max-line-length=88 --count --statistics *.py" "Code linting with flake8" -IgnoreErrors
    Invoke-DemoCommand "bandit -r *.py -f json" "Security scanning with bandit" -IgnoreErrors
    Invoke-DemoCommand "safety check --json" "Dependency vulnerability check" -IgnoreErrors
    
    # Run tests if available
    if (Test-Path "tests") {
        Invoke-DemoCommand "python -m pytest tests/ -v --tb=short" "Run unit tests" -IgnoreErrors
    }
}

# Docker Demo
function Demo-Docker {
    Write-Section "Docker Containerization"
    
    if ($SkipDocker) {
        Write-Info "Skipping Docker demonstration (--SkipDocker specified)"
        return
    }
    
    Invoke-DemoCommand "docker --version" "Docker version"
    
    # Show Dockerfile content
    if (Test-Path "Dockerfile") {
        Write-Info "Dockerfile contents:"
        Write-Host ("-" * 40)
        Get-Content "Dockerfile" | Write-Host
    }
    
    # Build image (optional - can be slow)
    $build = Read-Host "Build Docker image? This may take several minutes (y/N)"
    if ($build -eq "y" -or $build -eq "Y") {
        Invoke-DemoCommand "docker build -t alpaca-trading-bot ." "Build Docker image" -TimeoutSeconds 300
        Invoke-DemoCommand "docker images alpaca-trading-bot" "List built images"
    }
}

# Kubernetes Demo
function Demo-Kubernetes {
    Write-Section "Kubernetes Deployment"
    
    if ($SkipKubernetes) {
        Write-Info "Skipping Kubernetes demonstration (--SkipKubernetes specified)"
        return
    }
    
    Invoke-DemoCommand "kubectl version --client" "Kubectl version" -IgnoreErrors
    
    # Show Kubernetes manifest
    if (Test-Path "k8s\deployment.yaml") {
        Write-Info "Kubernetes deployment manifest:"
        Write-Host ("-" * 40)
        Get-Content "k8s\deployment.yaml" | Write-Host
        
        # Validate manifest
        Invoke-DemoCommand "kubectl apply --dry-run=client -f k8s\deployment.yaml" "Validate Kubernetes manifest" -IgnoreErrors
    }
}

# Terraform Demo
function Demo-Terraform {
    Write-Section "Infrastructure as Code with Terraform"
    
    Invoke-DemoCommand "terraform --version" "Terraform version" -IgnoreErrors
    
    # Show Terraform configuration
    if (Test-Path "terraform\main.tf") {
        Write-Info "Terraform configuration:"
        Write-Host ("-" * 40)
        Get-Content "terraform\main.tf" | Select-Object -First 30 | Write-Host
        
        # Navigate to terraform directory and run commands
        Push-Location "terraform"
        try {
            Invoke-DemoCommand "terraform init" "Initialize Terraform" -IgnoreErrors
            Invoke-DemoCommand "terraform validate" "Validate configuration" -IgnoreErrors
            Invoke-DemoCommand "terraform plan" "Generate execution plan" -TimeoutSeconds 60 -IgnoreErrors
        }
        finally {
            Pop-Location
        }
    }
}

# Monitoring Demo
function Demo-Monitoring {
    Write-Section "Monitoring & Observability"
    
    # Show monitoring configurations
    if (Test-Path "monitoring\prometheus.yml") {
        Write-Info "Prometheus configuration:"
        Write-Host ("-" * 40)
        Get-Content "monitoring\prometheus.yml" | Write-Host
    }
    
    if (Test-Path "docker-compose.yml") {
        Write-Info "Docker Compose monitoring stack:"
        Write-Host ("-" * 40)
        Get-Content "docker-compose.yml" | Write-Host
    }
}

# CI/CD Pipeline Demo
function Demo-CICD {
    Write-Section "CI/CD Pipeline Configuration"
    
    # Azure Pipelines
    if (Test-Path "azure-pipelines.yml") {
        Write-Info "Azure DevOps Pipeline:"
        Write-Host ("-" * 40)
        Get-Content "azure-pipelines.yml" | Select-Object -First 50 | ForEach-Object { Write-Host "$($_.ReadCount): $_" }
        
        $totalLines = (Get-Content "azure-pipelines.yml").Count
        if ($totalLines -gt 50) {
            Write-Host "... and $($totalLines - 50) more lines"
        }
    }
    
    # GitHub Actions
    if (Test-Path ".github\workflows\ci-cd.yml") {
        Write-Info "GitHub Actions Workflow:"
        Write-Host ("-" * 40)
        Get-Content ".github\workflows\ci-cd.yml" | Select-Object -First 30 | ForEach-Object { Write-Host "$($_.ReadCount): $_" }
        
        $totalLines = (Get-Content ".github\workflows\ci-cd.yml").Count
        if ($totalLines -gt 30) {
            Write-Host "... and $($totalLines - 30) more lines"
        }
    }
}

# Trading Bot Demo
function Demo-TradingBot {
    Write-Section "Trading Bot Application"
    
    # Check configuration
    if (Test-Path "check_config.py") {
        Invoke-DemoCommand "python check_config.py" "Validate bot configuration" -IgnoreErrors
    }
    
    # Run test bot for a short demo
    if (Test-Path "test_bot.py") {
        Write-Info "Running test bot for 15 seconds (demonstration mode)"
        Write-Command "python test_bot.py"
        Write-Host ("-" * 40)
        
        try {
            $job = Start-Job -ScriptBlock {
                python test_bot.py
            }
            
            Start-Sleep -Seconds 15
            Stop-Job $job
            
            $output = Receive-Job $job
            Remove-Job $job
            
            if ($output) {
                Write-Success "Test bot executed successfully"
                $output | Select-Object -First 20 | Write-Host
            }
        }
        catch {
            Write-Error "Error running test bot: $($_.Exception.Message)"
        }
    }
}

# Generate summary report
function Show-Summary {
    Write-Section "DevOps Demonstration Summary"
    
    Write-Host @"
🎯 DevOps Tools Demonstrated:

✅ Version Control (Git)
   • Repository management and history
   • Branch and remote tracking
   • Commit workflow demonstration

✅ Code Quality & Security
   • Python linting with flake8
   • Security scanning with bandit  
   • Dependency vulnerability checks with safety
   • Unit testing framework with pytest

✅ Containerization (Docker)
   • Multi-stage Docker builds
   • Security best practices
   • Container image management

✅ Container Orchestration (Kubernetes)
   • Deployment manifests
   • Resource limits and security policies
   • Service configuration

✅ Infrastructure as Code (Terraform)
   • Azure resource provisioning
   • Configuration validation
   • Infrastructure planning

✅ Monitoring & Observability
   • Prometheus metrics collection
   • Docker Compose monitoring stack
   • Application performance monitoring

✅ CI/CD Pipelines
   • Azure DevOps multi-stage pipelines
   • GitHub Actions workflows
   • Automated testing and deployment

✅ Trading Bot Application
   • Configuration validation
   • Safe testing environment
   • Real-time operation demonstration

🚀 Next Steps for Azure DevOps:
1. Create Azure DevOps organization at https://dev.azure.com
2. Import repository: https://github.com/MarioH88/devops.git
3. Configure build and release pipelines
4. Set up Azure Container Registry
5. Deploy to Azure Container Instances
6. Configure monitoring and alerts

📚 Documentation:
• Check AZURE_DEVOPS_SETUP.md for detailed instructions
• Review azure-pipelines.yml for pipeline configuration
• Examine Dockerfile and k8s/ for deployment configs
"@ -ForegroundColor White
}

# Main execution logic
function Start-DevOpsDemo {
    Write-Host "🎉 Welcome to the Alpaca Trading Bot DevOps Demonstration!" -ForegroundColor Magenta
    Write-Host "This PowerShell script showcases DevOps tools and practices on Windows." -ForegroundColor White
    
    # Check prerequisites
    if (-not (Test-Prerequisites)) {
        Write-Error "Prerequisites check failed. Please install missing tools."
        exit 1
    }
    
    # Run demonstrations based on parameter
    switch ($DemoType.ToLower()) {
        "git" { Demo-GitOperations }
        "quality" { Demo-PythonQuality }
        "docker" { Demo-Docker }
        "kubernetes" { Demo-Kubernetes }
        "terraform" { Demo-Terraform }
        "monitoring" { Demo-Monitoring }
        "cicd" { Demo-CICD }
        "bot" { Demo-TradingBot }
        "summary" { Show-Summary }
        "full" {
            Demo-GitOperations
            Demo-PythonQuality
            Demo-Docker
            Demo-Kubernetes
            Demo-Terraform
            Demo-Monitoring
            Demo-CICD
            Demo-TradingBot
            Show-Summary
        }
        default {
            Write-Error "Unknown demo type: $DemoType"
            Write-Host "Available options: full, git, quality, docker, kubernetes, terraform, monitoring, cicd, bot, summary"
            exit 1
        }
    }
    
    Write-Host "`n🎊 DevOps demonstration completed successfully!" -ForegroundColor Green
    Write-Host "📚 Check AZURE_DEVOPS_SETUP.md for Azure DevOps configuration details." -ForegroundColor Cyan
}

# Run the demonstration
Start-DevOpsDemo