#!/usr/bin/env python3
"""
Test script for Qualcomm vs Intel Performance Championship Demo
Verifies all components are working correctly
"""

import sys
import json
import time
import requests
import subprocess
from pathlib import Path

# ANSI color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_header(text):
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text.center(60)}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}\n")

def print_status(test_name, passed):
    status = f"{Colors.OKGREEN}✓ PASSED{Colors.ENDC}" if passed else f"{Colors.FAIL}✗ FAILED{Colors.ENDC}"
    print(f"  {test_name}: {status}")

def check_file_exists(filepath, description):
    """Check if a required file exists"""
    path = Path(filepath)
    exists = path.exists()
    print_status(f"{description} ({filepath})", exists)
    return exists

def check_python_packages():
    """Check if required Python packages are installed"""
    print(f"{Colors.OKCYAN}Checking Python packages...{Colors.ENDC}")
    
    required_packages = [
        'flask',
        'flask-socketio',
        'flask-cors',
        'psutil',
        'numpy',
        'requests'
    ]
    
    all_installed = True
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print_status(f"  {package}", True)
        except ImportError:
            print_status(f"  {package}", False)
            all_installed = False
    
    return all_installed

def check_config_file():
    """Validate config.json structure"""
    print(f"{Colors.OKCYAN}Checking configuration...{Colors.ENDC}")
    
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
        
        # Check required sections
        required_sections = ['server', 'devices', 'simulation', 'ui']
        for section in required_sections:
            has_section = section in config
            print_status(f"  Config section '{section}'", has_section)
            if not has_section:
                return False
        
        return True
    except Exception as e:
        print_status(f"  Config file valid", False)
        print(f"    Error: {e}")
        return False

def test_server_startup():
    """Test if the server can start"""
    print(f"{Colors.OKCYAN}Testing server startup...{Colors.ENDC}")
    
    try:
        # Try to import server module
        import server
        print_status("  Server module imports", True)
        
        # Check if port is available
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('localhost', 5000))
        sock.close()
        
        if result == 0:
            print_status("  Port 5000 available", False)
            print(f"    {Colors.WARNING}Port 5000 is already in use{Colors.ENDC}")
            return False
        else:
            print_status("  Port 5000 available", True)
            return True
            
    except Exception as e:
        print_status("  Server module ready", False)
        print(f"    Error: {e}")
        return False

def test_agent_module():
    """Test if the agent module loads correctly"""
    print(f"{Colors.OKCYAN}Testing agent module...{Colors.ENDC}")
    
    try:
        import agent
        
        # Test device creation
        snapdragon = agent.DeviceAgent('snapdragon', {
            'model': 'Snapdragon X Elite',
            'base_cpu': 15,
            'base_temp': 35,
            'battery_drain_rate': 0.5,
            'ai_tops': 45
        })
        print_status("  Snapdragon agent creation", True)
        
        intel = agent.DeviceAgent('intel', {
            'model': 'Intel Core Ultra 7',
            'base_cpu': 25,
            'base_temp': 45,
            'battery_drain_rate': 2.0,
            'ai_tops': 11
        })
        print_status("  Intel agent creation", True)
        
        # Test metrics generation
        metrics = snapdragon.get_metrics()
        has_metrics = all(k in metrics for k in ['cpu', 'memory', 'temperature', 'battery'])
        print_status("  Metrics generation", has_metrics)
        
        return True
        
    except Exception as e:
        print_status("  Agent module ready", False)
        print(f"    Error: {e}")
        return False

def check_dashboard_files():
    """Check if all dashboard files exist"""
    print(f"{Colors.OKCYAN}Checking dashboard files...{Colors.ENDC}")
    
    dashboard_files = [
        ('dashboard/index.html', 'Main HTML'),
        ('dashboard/assets/css/main.css', 'Main CSS'),
        ('dashboard/assets/css/animations.css', 'Animations CSS'),
        ('dashboard/assets/js/app.js', 'Main JavaScript'),
        ('dashboard/assets/js/charts.js', 'Charts JavaScript')
    ]
    
    all_exist = True
    for filepath, description in dashboard_files:
        exists = check_file_exists(filepath, description)
        if not exists:
            all_exist = False
    
    return all_exist

def run_quick_simulation():
    """Run a quick simulation test"""
    print(f"{Colors.OKCYAN}Running quick simulation test...{Colors.ENDC}")
    
    try:
        import agent
        import numpy as np
        
        # Create test device
        device = agent.DeviceAgent('test', {
            'model': 'Test Device',
            'base_cpu': 20,
            'base_temp': 40,
            'battery_drain_rate': 1.0,
            'ai_tops': 30
        })
        
        # Simulate workload
        device.simulate_workload('high')
        metrics = device.get_metrics()
        
        # Check if values changed
        cpu_changed = metrics['cpu']['percent'] != 20
        temp_changed = metrics['temperature'] != 40
        
        print_status("  Workload simulation", cpu_changed and temp_changed)
        
        # Test AI performance
        ai_result = device.run_ai_inference()
        print_status("  AI inference test", 'inference_time' in ai_result)
        
        return True
        
    except Exception as e:
        print_status("  Simulation test", False)
        print(f"    Error: {e}")
        return False

def main():
    """Main test runner"""
    print_header("PERFORMANCE CHAMPIONSHIP DEMO TEST SUITE")
    
    print(f"{Colors.BOLD}Testing Qualcomm Snapdragon vs Intel Demo Setup{Colors.ENDC}")
    print(f"Time: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    all_tests_passed = True
    test_results = {}
    
    # Run tests
    tests = [
        ("Project Files", lambda: all([
            check_file_exists('server.py', 'Server script'),
            check_file_exists('agent.py', 'Agent module'),
            check_file_exists('config.json', 'Configuration'),
            check_file_exists('requirements.txt', 'Requirements'),
            check_file_exists('README.md', 'Documentation')
        ])),
        ("Python Packages", check_python_packages),
        ("Configuration", check_config_file),
        ("Dashboard Files", check_dashboard_files),
        ("Server Module", test_server_startup),
        ("Agent Module", test_agent_module),
        ("Simulation", run_quick_simulation)
    ]
    
    for test_name, test_func in tests:
        print(f"\n{Colors.BOLD}{test_name}:{Colors.ENDC}")
        try:
            result = test_func()
            test_results[test_name] = result
            if not result:
                all_tests_passed = False
        except Exception as e:
            print(f"  {Colors.FAIL}Error running test: {e}{Colors.ENDC}")
            test_results[test_name] = False
            all_tests_passed = False
    
    # Print summary
    print_header("TEST SUMMARY")
    
    passed_count = sum(1 for v in test_results.values() if v)
    total_count = len(test_results)
    
    print(f"Tests Passed: {Colors.OKGREEN}{passed_count}/{total_count}{Colors.ENDC}")
    
    if all_tests_passed:
        print(f"\n{Colors.OKGREEN}{Colors.BOLD}✓ ALL TESTS PASSED!{Colors.ENDC}")
        print(f"\n{Colors.OKCYAN}The demo is ready to run. Start with:{Colors.ENDC}")
        print(f"  python server.py")
        print(f"\nThen open: http://localhost:5000/dashboard")
        print(f"\n{Colors.WARNING}Note: Snapdragon will win every time (as it should! 😄){Colors.ENDC}")
    else:
        print(f"\n{Colors.FAIL}{Colors.BOLD}✗ SOME TESTS FAILED{Colors.ENDC}")
        print(f"\n{Colors.WARNING}Please fix the issues above before running the demo.{Colors.ENDC}")
        
        # Provide helpful hints
        if not test_results.get("Python Packages", True):
            print(f"\n{Colors.OKCYAN}To install missing packages:{Colors.ENDC}")
            print(f"  pip install -r requirements.txt")
        
        if not test_results.get("Dashboard Files", True):
            print(f"\n{Colors.OKCYAN}Dashboard files are missing. Check the dashboard/ directory.{Colors.ENDC}")
    
    return 0 if all_tests_passed else 1

if __name__ == "__main__":
    sys.exit(main())
