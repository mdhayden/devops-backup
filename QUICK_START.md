# DevOps Quick Start Guide

## 🚀 Quick Demo (5 minutes)

### Option 1: PowerShell Script (Recommended for Windows)
```powershell
# Run complete demonstration
.\Demo-DevOps.ps1

# Run specific components
.\Demo-DevOps.ps1 -DemoType quality
.\Demo-DevOps.ps1 -DemoType docker -SkipDocker
.\Demo-DevOps.ps1 -DemoType summary
```

### Option 2: Python Script (Cross-platform)
```bash
# Full demonstration
python demo_devops.py

# Specific demonstrations
python demo_devops.py git
python demo_devops.py quality
python demo_devops.py docker
python demo_devops.py cicd
```

## 📋 Prerequisites Checklist

- [ ] **Git** - Version control (`git --version`)
- [ ] **Python 3.8+** - Runtime environment (`python --version`)
- [ ] **Docker** - Containerization (optional) (`docker --version`)
- [ ] **Azure CLI** - Azure operations (optional) (`az --version`)
- [ ] **kubectl** - Kubernetes (optional) (`kubectl version`)
- [ ] **Terraform** - Infrastructure as Code (optional) (`terraform --version`)

## ⚡ Instant Azure DevOps Setup

1. **Go to**: https://dev.azure.com
2. **Create Organization**: `your-name-devops`
3. **Create Project**: `Alpaca-Trading-Bot`
4. **Import Repository**: `https://github.com/MarioH88/devops.git`
5. **Create Pipeline**: Use existing `azure-pipelines.yml`
6. **Run Pipeline** 🚀

## 🔧 Core DevOps Components

### CI/CD Pipeline (`azure-pipelines.yml`)
- **Build**: Python dependency installation
- **Test**: Unit tests with pytest
- **Quality**: Code linting and security scanning
- **Security**: Bandit security analysis + dependency checks
- **Build**: Docker image creation
- **Deploy**: Azure Container Instances deployment

### Container Setup (`Dockerfile`)
- Multi-stage build for optimization
- Security hardening (non-root user)
- Minimal attack surface

### Kubernetes (`k8s/deployment.yaml`)
- Production-ready deployment
- Resource limits and requests
- Health checks and probes
- Security contexts

### Infrastructure (`terraform/main.tf`)
- Azure Container Registry
- Azure Container Instances
- Azure Key Vault for secrets
- Virtual Network configuration

### Monitoring (`monitoring/prometheus.yml`)
- Application metrics collection
- Performance monitoring
- Custom trading bot metrics

## 🎯 Demo Scenarios

### Scenario 1: Complete DevOps Workflow (15 minutes)
```powershell
# 1. Code quality check
.\Demo-DevOps.ps1 -DemoType quality

# 2. Container build
.\Demo-DevOps.ps1 -DemoType docker

# 3. CI/CD pipeline review
.\Demo-DevOps.ps1 -DemoType cicd

# 4. Summary report
.\Demo-DevOps.ps1 -DemoType summary
```

### Scenario 2: Security-Focused Demo (10 minutes)
```python
# Security scanning
python demo_devops.py quality

# Container security
python demo_devops.py docker

# Infrastructure security
python demo_devops.py terraform
```

### Scenario 3: Trading Bot Focus (5 minutes)
```powershell
# Bot configuration check
python check_config.py

# Safe testing mode
python test_bot.py

# Dashboard demo
python localhost_dashboard.py
```

## 📊 Key Metrics to Showcase

- **Build Time**: < 5 minutes from commit to deployment
- **Test Coverage**: Comprehensive unit testing
- **Security Scanning**: Zero high-severity vulnerabilities
- **Container Size**: Optimized multi-stage build
- **Deployment**: Automated with zero downtime
- **Monitoring**: Real-time application metrics

## 🔗 Quick Links

- **Repository**: https://github.com/MarioH88/devops.git
- **Azure DevOps Setup**: [AZURE_DEVOPS_SETUP.md](AZURE_DEVOPS_SETUP.md)
- **Trading Bot Guide**: [TESTING_GUIDE.md](TESTING_GUIDE.md)
- **Pipeline Config**: [azure-pipelines.yml](azure-pipelines.yml)
- **Docker Config**: [Dockerfile](Dockerfile)
- **K8s Config**: [k8s/deployment.yaml](k8s/deployment.yaml)

## 💡 Pro Tips

1. **Start Small**: Begin with `.\Demo-DevOps.ps1 -DemoType summary`
2. **Prerequisites**: Install Docker Desktop for full container demos
3. **Azure Account**: Free tier sufficient for demonstration
4. **Time Management**: Full demo takes ~20 minutes
5. **Backup Plan**: PowerShell script works even without Docker/K8s

## 🚨 Troubleshooting

### Common Issues:
- **PowerShell Execution Policy**: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`
- **Python Path Issues**: Use `python` or `py` depending on installation
- **Docker Not Running**: Start Docker Desktop before container demos
- **Git Authentication**: Use personal access tokens for GitHub

### Quick Fixes:
```powershell
# Fix PowerShell execution policy
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned

# Install missing Python packages
pip install -r requirements.txt

# Check Docker status
docker info

# Verify Git configuration
git config --list
```

This guide gets you from zero to full DevOps demonstration in under 30 minutes! 🎉