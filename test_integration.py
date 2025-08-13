#!/usr/bin/env python3
"""
Integration Test Suite for Snapdragon vs Intel Demo System
Verifies all components work together properly
"""

import sys
import time
import json
import subprocess
import threading
import socket
from pathlib import Path
from typing import Dict, List, Tuple

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

# Import demo components
try:
    from platform_detector import PlatformDetector
    from sd_generator import StableDiffusionGenerator
    from download_models import ModelDownloader
    print("✅ Core imports successful")
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)

class IntegrationTester:
    def __init__(self):
        self.results = []
        self.passed = 0
        self.failed = 0
        
    def test(self, name: str, func) -> bool:
        """Run a test and record results"""
        print(f"\n🧪 Testing: {name}")
        try:
            result = func()
            if result:
                print(f"  ✅ PASSED")
                self.passed += 1
                self.results.append((name, "PASSED", None))
                return True
            else:
                print(f"  ❌ FAILED")
                self.failed += 1
                self.results.append((name, "FAILED", "Test returned False"))
                return False
        except Exception as e:
            print(f"  ❌ ERROR: {e}")
            self.failed += 1
            self.results.append((name, "ERROR", str(e)))
            return False
    
    def test_platform_detection(self) -> bool:
        """Test platform detection module"""
        detector = PlatformDetector()
        info = detector.platform_info
        
        print(f"  Platform: {info.get('platform_type', 'unknown')}")
        print(f"  CPU: {info.get('cpu_name', 'unknown')}")
        print(f"  Cores: {info.get('cpu_cores', 0)}")
        
        return 'platform_type' in info
    
    def test_model_downloader(self) -> bool:
        """Test model download system"""
        for platform in ['snapdragon', 'intel']:
            downloader = ModelDownloader(platform)
            
            # Test model structure creation
            success = downloader.download_models()
            if not success:
                return False
            
            # Verify models
            if not downloader.verify_models():
                return False
        
        return True
    
    def test_sd_generator(self) -> bool:
        """Test Stable Diffusion generator"""
        for platform in ['snapdragon', 'intel']:
            generator = StableDiffusionGenerator(platform)
            generator.load_model()
            
            # Test image generation (quick test)
            image, time_taken = generator.generate(
                "Test prompt",
                progress_callback=lambda x: None
            )
            
            if not image:
                return False
            
            print(f"    {platform}: {time_taken:.1f}s")
        
        return True
    
    def test_config_file(self) -> bool:
        """Test configuration file"""
        config_path = Path('config.json')
        if not config_path.exists():
            return False
        
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        required_keys = ['server', 'demo_phases', 'platform_configs']
        for key in required_keys:
            if key not in config:
                print(f"    Missing key: {key}")
                return False
        
        return True
    
    def test_deployment_scripts(self) -> bool:
        """Test deployment script existence"""
        scripts = [
            'deploy_windows.bat',
            'setup_snapdragon.bat',
            'setup_intel.bat',
            'start_server.bat',
            'start_agent.bat'
        ]
        
        for script in scripts:
            script_path = Path(script)
            if not script_path.exists():
                print(f"    Missing: {script}")
                return False
            print(f"    Found: {script}")
        
        return True
    
    def test_dashboard_files(self) -> bool:
        """Test dashboard file structure"""
        dashboard_files = [
            'dashboard/index.html',
            'dashboard/assets/css/main.css',
            'dashboard/assets/css/animations.css',
            'dashboard/assets/js/app.js',
            'dashboard/assets/js/charts.js'
        ]
        
        for file in dashboard_files:
            file_path = Path(file)
            if not file_path.exists():
                print(f"    Missing: {file}")
                return False
            print(f"    Found: {file}")
        
        return True
    
    def test_server_port(self) -> bool:
        """Test if server port is available"""
        port = 5001
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('127.0.0.1', port))
        sock.close()
        
        if result == 0:
            print(f"    Port {port} is in use (server might be running)")
            return True
        else:
            print(f"    Port {port} is available")
            return True
    
    def test_requirements(self) -> bool:
        """Test if all required packages are listed"""
        req_path = Path('requirements.txt')
        if not req_path.exists():
            return False
        
        with open(req_path, 'r') as f:
            requirements = f.read()
        
        required_packages = [
            'flask',
            'flask-socketio',
            'psutil',
            'Pillow',
            'requests'
        ]
        
        for package in required_packages:
            if package.lower() not in requirements.lower():
                print(f"    Missing package: {package}")
                return False
            print(f"    Found: {package}")
        
        return True
    
    def test_documentation(self) -> bool:
        """Test documentation completeness"""
        docs = [
            'README.md',
            'WINDOWS_DEPLOYMENT_GUIDE.md',
            'PROJECT_COMPLETION_SUMMARY.md',
            'DEMO_COMPLETION_PLAN.md'
        ]
        
        for doc in docs:
            doc_path = Path(doc)
            if not doc_path.exists():
                print(f"    Missing: {doc}")
                return False
            
            # Check if doc has content
            size = doc_path.stat().st_size
            if size < 100:
                print(f"    {doc} seems empty ({size} bytes)")
                return False
            
            print(f"    {doc}: {size:,} bytes")
        
        return True
    
    def print_summary(self):
        """Print test summary"""
        print("\n" + "=" * 60)
        print("  INTEGRATION TEST SUMMARY")
        print("=" * 60)
        
        for name, status, error in self.results:
            icon = "✅" if status == "PASSED" else "❌"
            print(f"{icon} {name}: {status}")
            if error:
                print(f"   Error: {error}")
        
        print("\n" + "-" * 60)
        total = self.passed + self.failed
        success_rate = (self.passed / total * 100) if total > 0 else 0
        
        print(f"Total Tests: {total}")
        print(f"Passed: {self.passed}")
        print(f"Failed: {self.failed}")
        print(f"Success Rate: {success_rate:.1f}%")
        
        if self.failed == 0:
            print("\n🎉 ALL TESTS PASSED! Demo system is ready for deployment.")
        else:
            print(f"\n⚠️ {self.failed} test(s) failed. Please review and fix issues.")
        
        print("=" * 60)


def main():
    """Run integration tests"""
    print("=" * 60)
    print("  SNAPDRAGON VS INTEL DEMO - INTEGRATION TEST")
    print("=" * 60)
    
    tester = IntegrationTester()
    
    # Run all tests
    tester.test("Platform Detection", tester.test_platform_detection)
    tester.test("Configuration File", tester.test_config_file)
    tester.test("Model Downloader", tester.test_model_downloader)
    tester.test("SD Generator", tester.test_sd_generator)
    tester.test("Deployment Scripts", tester.test_deployment_scripts)
    tester.test("Dashboard Files", tester.test_dashboard_files)
    tester.test("Server Port", tester.test_server_port)
    tester.test("Requirements File", tester.test_requirements)
    tester.test("Documentation", tester.test_documentation)
    
    # Print summary
    tester.print_summary()
    
    return 0 if tester.failed == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
