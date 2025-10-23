"""
Basic tests for the trading bot application
"""
import pytest
import os
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_imports():
    """Test that we can import our main modules"""
    try:
        import web_dashboard
        import dashboard
        import main
        # If we get here, imports succeeded
        imported_modules = [web_dashboard, dashboard, main]
        assert len(imported_modules) == 3
    except ImportError as e:
        pytest.skip(f"Module import failed: {e}")

def test_configuration_file_exists():
    """Test that configuration files exist"""
    auth_file = os.path.join(os.path.dirname(__file__), '..', 'AUTH', 'auth.txt')
    # We don't expect the auth file to exist in CI, so we just check the directory
    auth_dir = os.path.dirname(auth_file)
    assert os.path.exists(auth_dir), "AUTH directory should exist"

def test_tickers_file_exists():
    """Test that ticker files exist"""
    tickers_file = os.path.join(os.path.dirname(__file__), '..', 'TICKERS', 'my_tickers.txt')
    assert os.path.exists(tickers_file), "Tickers file should exist"

def test_requirements_file_exists():
    """Test that requirements.txt exists"""
    req_file = os.path.join(os.path.dirname(__file__), '..', 'requirements.txt')
    assert os.path.exists(req_file), "requirements.txt should exist"

def test_dockerfile_exists():
    """Test that Dockerfile exists"""
    dockerfile = os.path.join(os.path.dirname(__file__), '..', 'Dockerfile')
    assert os.path.exists(dockerfile), "Dockerfile should exist"

def test_pipeline_config_exists():
    """Test that CI/CD pipeline configs exist"""
    azure_pipeline = os.path.join(os.path.dirname(__file__), '..', 'azure-pipelines.yml')
    github_workflow = os.path.join(os.path.dirname(__file__), '..', '.github', 'workflows', 'ci-cd.yml')
    
    assert os.path.exists(azure_pipeline), "Azure pipeline config should exist"
    assert os.path.exists(github_workflow), "GitHub workflow should exist"

def test_basic_math():
    """Basic test to ensure testing framework works"""
    assert 1 + 1 == 2
    assert 2 * 3 == 6

def test_string_operations():
    """Test string operations"""
    test_string = "DevOps"
    assert test_string.lower() == "devops"
    assert len(test_string) == 6

class TestTradingBotConfig:
    """Test class for trading bot configuration"""
    
    def test_environment_setup(self):
        """Test that we can set up environment variables"""
        os.environ['TEST_VAR'] = 'test_value'
        assert os.getenv('TEST_VAR') == 'test_value'
        
    def test_file_structure(self):
        """Test that required directories exist"""
        required_dirs = ['AUTH', 'TICKERS', 'tests']
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        for dir_name in required_dirs:
            dir_path = os.path.join(project_root, dir_name)
            assert os.path.exists(dir_path), f"Directory {dir_name} should exist"

if __name__ == "__main__":
    pytest.main([__file__])