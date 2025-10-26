#!/usr/bin/env python3
"""
Quick deployment test script
Tests the Docker build locally before deploying
"""
import subprocess
import sys
import os

def test_docker_build():
    """Test Docker build locally"""
    print("🔨 Testing Docker build locally...")
    
    try:
        # Build the Docker image
        result = subprocess.run([
            'docker', 'build', '-t', 'devops-backup-test', '.'
        ], check=True, capture_output=True, text=True)
        
        print("✅ Docker build successful!")
        
        # Test running the container
        print("🚀 Testing container startup...")
        container_result = subprocess.run([
            'docker', 'run', '--rm', '-d', '-p', '8080:8080', 
            '--name', 'devops-backup-test-container',
            'devops-backup-test'
        ], capture_output=True, text=True)
        
        if container_result.returncode == 0:
            container_id = container_result.stdout.strip()
            print(f"✅ Container started: {container_id}")
            
            # Wait a moment for startup
            import time
            time.sleep(5)
            
            # Test health check
            try:
                import requests
                response = requests.get('http://localhost:8080/health', timeout=10)
                if response.status_code == 200:
                    print("✅ Health check passed!")
                else:
                    print(f"❌ Health check failed: {response.status_code}")
            except Exception as e:
                print(f"❌ Health check error: {e}")
            
            # Stop the container
            subprocess.run(['docker', 'stop', container_id], capture_output=True)
            print("🛑 Test container stopped")
            
        else:
            print(f"❌ Container failed to start: {container_result.stderr}")
            return False
            
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Docker build failed: {e.stderr}")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def trigger_cloud_build():
    """Trigger a manual Cloud Build"""
    print("🚀 Triggering Cloud Build...")
    
    try:
        # Check if gcloud is available
        subprocess.run(['gcloud', 'version'], check=True, capture_output=True)
        
        # Trigger the build
        result = subprocess.run([
            'gcloud', 'builds', 'submit', 
            '--config=cloudbuild.yaml',
            '--project=gen-lang-client-0502058841'
        ], check=True)
        
        print("✅ Cloud Build triggered successfully!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Cloud Build failed: {e}")
        return False
    except FileNotFoundError:
        print("❌ gcloud CLI not found. Please install Google Cloud SDK.")
        return False

def main():
    """Main test function"""
    print("🤖 Alpaca Trading Bot - Deployment Test")
    print("=" * 50)
    
    # Test Docker build locally first
    if test_docker_build():
        print("\n" + "=" * 50)
        print("✅ Local tests passed!")
        
        # Ask if user wants to trigger Cloud Build
        response = input("\nTrigger Cloud Build deployment? (y/n): ").lower()
        if response == 'y':
            trigger_cloud_build()
        else:
            print("Manual deployment skipped.")
    else:
        print("❌ Local tests failed. Fix issues before deploying.")
        sys.exit(1)

if __name__ == "__main__":
    main()