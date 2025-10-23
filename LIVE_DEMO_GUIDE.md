# Azure DevOps Live Demo Script
# Perfect for demonstrating CI/CD, DevOps practices, and cloud deployment

## 🎯 LIVE DEMO FLOW (15 minutes)

### PART 1: Repository & Setup (3 minutes)
1. **Show GitHub Repository**: https://github.com/MarioH88/devops.git
   - "Here's our complete trading bot with DevOps infrastructure"
   - Show key files: azure-pipelines.yml, Dockerfile, k8s/, terraform/

2. **Azure DevOps Setup**:
   - Go to https://dev.azure.com
   - Create organization: "tradingbot-demo"
   - Create project: "Alpaca-Trading-Bot"
   - Import repository from GitHub

### PART 2: CI/CD Pipeline (8 minutes)
3. **Pipeline Configuration**:
   - Show azure-pipelines.yml
   - Explain stages: Build → Test → Security → Deploy
   - Highlight DevOps best practices

4. **Run Live Pipeline**:
   - Trigger pipeline execution
   - Show real-time build logs
   - Demonstrate automated testing
   - Security scanning results
   - Container building

5. **Infrastructure as Code**:
   - Show terraform/main.tf
   - Explain Azure resource provisioning
   - Kubernetes deployment manifests

### PART 3: Monitoring & Results (4 minutes)
6. **Show Pipeline Results**:
   - Test results and coverage
   - Security scan reports
   - Deployment status

7. **DevOps Benefits**:
   - Automated quality gates
   - Security-first approach
   - Infrastructure automation
   - Monitoring & observability

## 🛠️ DEMO COMMANDS TO RUN

```bash
# Show project structure
dir

# Show CI/CD configuration
type azure-pipelines.yml

# Show Docker configuration  
type Dockerfile

# Show Kubernetes deployment
type k8s\deployment.yaml

# Show infrastructure code
type terraform\main.tf

# Show monitoring setup
type monitoring\prometheus.yml

# Demonstrate trading bot
python check_config.py
python web_dashboard.py
```

## 🎯 KEY TALKING POINTS

### DevOps Practices Demonstrated:
- ✅ **Version Control**: Git with branching strategy
- ✅ **CI/CD**: Automated build, test, deploy
- ✅ **Code Quality**: Linting, testing, coverage
- ✅ **Security**: Automated security scanning
- ✅ **Containerization**: Docker with best practices
- ✅ **Orchestration**: Kubernetes deployment
- ✅ **Infrastructure as Code**: Terraform
- ✅ **Monitoring**: Prometheus & Grafana setup

### Business Value:
- 🚀 **Faster Deployment**: Minutes instead of hours
- 🔒 **Enhanced Security**: Automated vulnerability scanning
- 📊 **Quality Assurance**: Automated testing & gates
- 📈 **Scalability**: Container orchestration
- 🔧 **Reliability**: Infrastructure as code
- 📊 **Observability**: Real-time monitoring

## 🎪 ALTERNATIVE: Quick Local Demo (5 minutes)

If Azure setup takes too long, run local demonstration:

```bash
# Show all DevOps components
python demo_devops.py summary

# Show trading bot functionality
python web_dashboard.py
# Opens browser with real-time dashboard

# Show configuration validation
python check_config.py

# Show pipeline configuration
type azure-pipelines.yml | findstr /n "stage\|job\|task"
```

## 📋 DEMO CHECKLIST

Pre-demo:
- [ ] Azure DevOps account ready
- [ ] GitHub repository accessible
- [ ] Python environment working
- [ ] Trading bot dashboard functional

During demo:
- [ ] Show repository structure
- [ ] Import to Azure DevOps  
- [ ] Configure pipeline
- [ ] Run pipeline
- [ ] Show results & monitoring
- [ ] Demonstrate trading bot

Post-demo talking points:
- [ ] Enterprise scalability
- [ ] Security compliance
- [ ] Cost optimization
- [ ] Team collaboration benefits