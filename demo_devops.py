#!/usr/bin/env python3
"""
DevOps Demonstration Script
This script demonstrates various DevOps tools and practices for the Alpaca Trading Bot
"""

import subprocess
import sys
import time
import os
from pathlib import Path


class DevOpsDemo:
    """Demonstrates DevOps tools and practices"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        
    def print_section(self, title):
        """Print a formatted section header"""
        print("\n" + "="*60)
        print(f"🚀 {title}")
        print("="*60)
        
    def run_command(self, command, description):
        """Run a command and display output"""
        print(f"\n📋 {description}")
        print(f"💻 Command: {command}")
        print("-" * 40)
        
        try:
            # Safer command execution with list instead of shell=True
            if isinstance(command, str):
                command_list = command.split()
            else:
                command_list = command
                
            result = subprocess.run(
                command_list,
                shell=False,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                print("✅ SUCCESS")
                if result.stdout:
                    print(result.stdout)
            else:
                print("❌ ERROR")
                if result.stderr:
                    print(result.stderr)
                    
        except subprocess.TimeoutExpired:
            print("⏰ TIMEOUT - Command took too long")
        except Exception as e:
            print(f"💥 EXCEPTION: {str(e)}")
            
    def demonstrate_git_operations(self):
        """Demonstrate Git version control"""
        self.print_section("Git Version Control")
        
        self.run_command("git --version", "Check Git version")
        self.run_command("git status", "Check repository status")
        self.run_command("git log --oneline -5", "Show recent commits")
        self.run_command("git branch -a", "Show all branches")
        
    def demonstrate_python_quality(self):
        """Demonstrate Python code quality tools"""
        self.print_section("Code Quality & Testing")
        
        # Check if we're in a virtual environment
        if sys.prefix == sys.base_prefix:
            print("⚠️  Not in virtual environment. Installing packages globally.")
        
        # Install required tools
        self.run_command(
            "pip install flake8 bandit safety pytest pytest-cov",
            "Install code quality tools"
        )
        
        # Code linting
        self.run_command("flake8 --max-line-length=88 *.py", "Run code linting")
        
        # Security scanning
        self.run_command("bandit -r *.py", "Run security analysis")
        
        # Dependency scanning
        self.run_command("safety check", "Check dependencies for vulnerabilities")
        
        # Run tests
        self.run_command("python -m pytest tests/ -v", "Run unit tests")
        
    def demonstrate_docker(self):
        """Demonstrate Docker containerization"""
        self.print_section("Docker Containerization")
        
        # Check Docker installation
        self.run_command("docker --version", "Check Docker version")
        
        # Build Docker image
        self.run_command(
            "docker build -t alpaca-trading-bot .",
            "Build Docker image"
        )
        
        # List Docker images
        self.run_command("docker images alpaca-trading-bot", "List built images")
        
        # Show Dockerfile
        print("\n📄 Dockerfile Contents:")
        print("-" * 40)
        try:
            with open(self.project_root / "Dockerfile", "r") as f:
                print(f.read())
        except FileNotFoundError:
            print("❌ Dockerfile not found")
            
    def demonstrate_kubernetes(self):
        """Demonstrate Kubernetes deployment"""
        self.print_section("Kubernetes Deployment")
        
        # Check kubectl
        self.run_command("kubectl version --client", "Check kubectl version")
        
        # Show Kubernetes manifest
        print("\n📄 Kubernetes Deployment:")
        print("-" * 40)
        try:
            with open(self.project_root / "k8s" / "deployment.yaml", "r") as f:
                print(f.read())
        except FileNotFoundError:
            print("❌ Kubernetes deployment file not found")
            
        # Validate Kubernetes YAML
        self.run_command(
            "kubectl apply --dry-run=client -f k8s/deployment.yaml",
            "Validate Kubernetes deployment (dry run)"
        )
        
    def demonstrate_terraform(self):
        """Demonstrate Infrastructure as Code"""
        self.print_section("Infrastructure as Code (Terraform)")
        
        # Check Terraform
        self.run_command("terraform --version", "Check Terraform version")
        
        # Show Terraform configuration
        print("\n📄 Terraform Configuration:")
        print("-" * 40)
        try:
            with open(self.project_root / "terraform" / "main.tf", "r") as f:
                print(f.read())
        except FileNotFoundError:
            print("❌ Terraform configuration not found")
            
        # Initialize and validate Terraform
        os.chdir(self.project_root / "terraform")
        self.run_command("terraform init", "Initialize Terraform")
        self.run_command("terraform validate", "Validate Terraform configuration")
        self.run_command("terraform plan", "Generate Terraform execution plan")
        os.chdir(self.project_root)
        
    def demonstrate_monitoring(self):
        """Demonstrate monitoring setup"""
        self.print_section("Monitoring & Observability")
        
        # Show Prometheus configuration
        print("\n📄 Prometheus Configuration:")
        print("-" * 40)
        try:
            with open(self.project_root / "monitoring" / "prometheus.yml", "r") as f:
                print(f.read())
        except FileNotFoundError:
            print("❌ Prometheus configuration not found")
            
        # Show Docker Compose for monitoring stack
        print("\n📄 Docker Compose (Monitoring Stack):")
        print("-" * 40)
        try:
            with open(self.project_root / "docker-compose.yml", "r") as f:
                print(f.read())
        except FileNotFoundError:
            print("❌ Docker Compose file not found")
            
    def demonstrate_cicd_pipeline(self):
        """Demonstrate CI/CD pipeline configuration"""
        self.print_section("CI/CD Pipeline Configuration")
        
        # Show Azure Pipelines YAML
        print("\n📄 Azure DevOps Pipeline:")
        print("-" * 40)
        try:
            with open(self.project_root / "azure-pipelines.yml", "r") as f:
                lines = f.readlines()
                for i, line in enumerate(lines[:50], 1):  # Show first 50 lines
                    print(f"{i:2d}: {line.rstrip()}")
                if len(lines) > 50:
                    print(f"... and {len(lines) - 50} more lines")
        except FileNotFoundError:
            print("❌ Azure Pipelines configuration not found")
            
        # Show GitHub Actions workflow
        print("\n📄 GitHub Actions Workflow:")
        print("-" * 40)
        try:
            with open(self.project_root / ".github" / "workflows" / "ci-cd.yml", "r") as f:
                lines = f.readlines()
                for i, line in enumerate(lines[:30], 1):  # Show first 30 lines
                    print(f"{i:2d}: {line.rstrip()}")
                if len(lines) > 30:
                    print(f"... and {len(lines) - 30} more lines")
        except FileNotFoundError:
            print("❌ GitHub Actions workflow not found")
            
    def demonstrate_trading_bot(self):
        """Demonstrate the trading bot functionality"""
        self.print_section("Trading Bot Demonstration")
        
        # Check configuration
        self.run_command("python check_config.py", "Validate bot configuration")
        
        # Run test bot
        print("\n📋 Running test bot (safe mode)")
        print("💻 Command: python test_bot.py")
        print("-" * 40)
        
        try:
            # Run for a short time to demonstrate
            process = subprocess.Popen(
                ["python", "test_bot.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Let it run for 10 seconds
            time.sleep(10)
            process.terminate()
            
            stdout, stderr = process.communicate(timeout=5)
            
            if stdout:
                print("📊 Output:")
                print(stdout[:1000])  # Show first 1000 characters
                
            if stderr:
                print("⚠️  Errors:")
                print(stderr[:500])  # Show first 500 characters
                
        except Exception as e:
            print(f"💥 Error running test bot: {str(e)}")
            
    def generate_summary_report(self):
        """Generate a summary report"""
        self.print_section("DevOps Demonstration Summary")
        
        print("""
🎯 DevOps Tools Demonstrated:
        
✅ Version Control (Git)
   - Repository management
   - Branching strategies
   - Commit history
   
✅ Code Quality & Security
   - Linting with flake8
   - Security scanning with bandit
   - Dependency vulnerability checks
   - Unit testing with pytest
   
✅ Containerization (Docker)
   - Multi-stage builds
   - Security best practices
   - Image optimization
   
✅ Container Orchestration (Kubernetes)
   - Deployment manifests
   - Resource management
   - Security policies
   
✅ Infrastructure as Code (Terraform)
   - Azure resource provisioning
   - Configuration management
   - State management
   
✅ Monitoring & Observability
   - Prometheus metrics collection
   - Grafana dashboards
   - Application monitoring
   
✅ CI/CD Pipelines
   - Azure DevOps pipelines
   - GitHub Actions workflows
   - Automated testing and deployment
   
✅ Trading Bot Application
   - Configuration validation
   - Safe testing mode
   - Real-time monitoring

🚀 Next Steps for Production:
1. Set up Azure DevOps organization
2. Import repository and configure pipelines
3. Deploy to Azure Container Instances
4. Set up monitoring dashboards
5. Configure alerts and notifications
6. Implement automated rollback strategies
        """)
        
    def run_full_demonstration(self):
        """Run the complete DevOps demonstration"""
        print("🎉 Welcome to the Alpaca Trading Bot DevOps Demonstration!")
        print("This script will showcase various DevOps tools and practices.")
        
        # Run all demonstrations
        self.demonstrate_git_operations()
        self.demonstrate_python_quality()
        self.demonstrate_docker()
        self.demonstrate_kubernetes()
        self.demonstrate_terraform()
        self.demonstrate_monitoring()
        self.demonstrate_cicd_pipeline()
        self.demonstrate_trading_bot()
        self.generate_summary_report()
        
        print("\n🎊 DevOps demonstration completed successfully!")
        print("📚 Check AZURE_DEVOPS_SETUP.md for detailed setup instructions.")


def main():
    """Main function"""
    demo = DevOpsDemo()
    
    if len(sys.argv) > 1:
        # Run specific demonstration
        demo_type = sys.argv[1].lower()
        
        demos = {
            'git': demo.demonstrate_git_operations,
            'quality': demo.demonstrate_python_quality,
            'docker': demo.demonstrate_docker,
            'kubernetes': demo.demonstrate_kubernetes,
            'terraform': demo.demonstrate_terraform,
            'monitoring': demo.demonstrate_monitoring,
            'cicd': demo.demonstrate_cicd_pipeline,
            'bot': demo.demonstrate_trading_bot,
            'summary': demo.generate_summary_report
        }
        
        if demo_type in demos:
            demos[demo_type]()
        else:
            print(f"❌ Unknown demo type: {demo_type}")
            print(f"Available demos: {', '.join(demos.keys())}")
    else:
        # Run full demonstration
        demo.run_full_demonstration()


if __name__ == "__main__":
    main()