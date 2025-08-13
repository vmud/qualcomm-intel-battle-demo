#!/usr/bin/env python3
"""
Device Agent for Snapdragon vs Intel Performance Championship
Runs on each laptop to monitor and report metrics
"""

import json
import time
import threading
import platform
import socket
import psutil
import socketio
import logging
import sys
import random
from datetime import datetime
import subprocess

# Windows-specific imports (conditional)
try:
    import wmi
    import pythoncom
    WINDOWS_WMI_AVAILABLE = True
except ImportError:
    WINDOWS_WMI_AVAILABLE = False
    if platform.system() == 'Windows':
        logging.warning("WMI not available. Install with: pip install wmi pywin32")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load configuration
with open('config.json', 'r') as f:
    config = json.load(f)

class DeviceAgent:
    def __init__(self, device_type=None, device_config=None):
        """Initialize the device agent
        
        Args:
            device_type: Optional device type ('snapdragon' or 'intel') for testing
            device_config: Optional device configuration dict for testing
        """
        self.device_type = device_type if device_type else self.detect_device_type()
        self.device_config = device_config if device_config else config['devices'].get(self.device_type, {})
        self.sio = socketio.Client()
        self.running = True
        self.current_test = None
        self.workload = 'idle'
        self.server_url = f"http://{config['network']['server_ip']}:{config['network']['server_port']}"
        
        # Store device metrics
        self.base_cpu = self.device_config.get('base_cpu', 20)
        self.base_temp = self.device_config.get('base_temp', 40)
        self.battery_drain_rate = self.device_config.get('battery_drain_rate', 1.0)
        self.ai_tops = self.device_config.get('ai_tops', 20)
        
        # Setup Socket.IO event handlers
        self.setup_handlers()
        
        logger.info(f"Device Agent initialized as: {self.device_type}")
        
    def detect_device_type(self):
        """Detect if this is Snapdragon or Intel device"""
        processor = platform.processor().lower()
        machine = platform.machine().lower()
        
        # Check for ARM/Snapdragon
        if 'arm' in machine or 'aarch64' in machine:
            return 'snapdragon'
        
        # Check hostname as fallback
        hostname = socket.gethostname().lower()
        if 'snapdragon' in hostname or 'samsung' in hostname or 'galaxy' in hostname:
            return 'snapdragon'
        elif 'intel' in hostname or 'lenovo' in hostname or 'yoga' in hostname:
            return 'intel'
        
        # Default based on processor
        if 'intel' in processor:
            return 'intel'
        
        # Manual selection if unable to detect
        print("\n=== Device Type Selection ===")
        print("Unable to auto-detect device type.")
        print("1. Snapdragon X Elite (Samsung Galaxy Book4 Edge)")
        print("2. Intel Core Ultra 7 (Lenovo Yoga 7i)")
        choice = input("Select device type (1 or 2): ")
        return 'snapdragon' if choice == '1' else 'intel'
    
    def setup_handlers(self):
        """Setup Socket.IO event handlers"""
        
        @self.sio.event
        def connect():
            logger.info(f"Connected to server at {self.server_url}")
            # Register device
            self.sio.emit('device_register', {
                'device_type': self.device_type,
                'hostname': socket.gethostname(),
                'platform': platform.platform()
            })
        
        @self.sio.event
        def disconnect():
            logger.info("Disconnected from server")
        
        @self.sio.event
        def device_welcome(data):
            logger.info(f"Server welcome: {data['message']}")
        
        @self.sio.event
        def execute_test(data):
            """Execute a test scenario"""
            scenario = data['scenario']
            test_config = data['config']
            logger.info(f"Starting test: {scenario}")
            
            self.current_test = scenario
            
            # Start test in separate thread
            test_thread = threading.Thread(
                target=self.run_test,
                args=(scenario, test_config),
                daemon=True
            )
            test_thread.start()
        
        @self.sio.event
        def demo_stopped(data):
            """Handle demo stop"""
            logger.info("Demo stopped by server")
            self.current_test = None
    
    def get_system_metrics(self):
        """Get current system metrics"""
        metrics = {}
        
        try:
            # CPU metrics
            metrics['cpu'] = {
                'percent': psutil.cpu_percent(interval=0.1),
                'freq': psutil.cpu_freq().current if psutil.cpu_freq() else 0,
                'cores': psutil.cpu_count()
            }
            
            # Memory metrics
            mem = psutil.virtual_memory()
            metrics['memory'] = {
                'percent': mem.percent,
                'used': mem.used / (1024**3),  # GB
                'total': mem.total / (1024**3)  # GB
            }
            
            # Battery metrics
            battery = psutil.sensors_battery()
            if battery:
                metrics['battery'] = {
                    'percent': battery.percent,
                    'charging': battery.power_plugged,
                    'time_left': battery.secsleft if battery.secsleft != -1 else None
                }
            
            # Temperature - use real data on Windows if available
            if platform.system() == 'Windows':
                metrics['temperature'] = self.get_temperature_windows()
                metrics['fan_rpm'] = self.get_fan_speed_windows()
            else:
                # Simulation for non-Windows development
                metrics['temperature'] = self.get_temperature_simulation()
                metrics['fan_rpm'] = self.get_fan_speed_simulation()
            
        except Exception as e:
            logger.error(f"Error getting metrics: {e}")
        
        return metrics
    
    def get_temperature_windows(self):
        """Get real temperature on Windows using WMI"""
        if not WINDOWS_WMI_AVAILABLE:
            return self.get_temperature_simulation()
        
        try:
            pythoncom.CoInitialize()
            c = wmi.WMI(namespace="root\\wmi")
            
            # Try to get CPU temperature from WMI
            temperature_info = c.MSAcpi_ThermalZoneTemperature()
            if temperature_info:
                # Convert from tenths of Kelvin to Celsius
                temp_kelvin = temperature_info[0].CurrentTemperature / 10.0
                temp_celsius = temp_kelvin - 273.15
                return round(temp_celsius, 1)
        except Exception as e:
            logger.debug(f"Could not get real temperature via WMI: {e}")
        finally:
            pythoncom.CoUninitialize()
        
        # Fallback to simulation
        return self.get_temperature_simulation()
    
    def get_temperature_simulation(self):
        """Simulate temperature based on device type and load"""
        cpu_percent = psutil.cpu_percent()
        
        if self.device_type == 'snapdragon':
            # Snapdragon runs cooler
            base_temp = 35
            load_factor = 0.15
            noise = random.uniform(-2, 2)
        else:
            # Intel runs hotter
            base_temp = 45
            load_factor = 0.4
            noise = random.uniform(-3, 5)
        
        temp = base_temp + (cpu_percent * load_factor) + noise
        
        # Add extra heat during tests
        if self.current_test:
            temp += 10 if self.device_type == 'snapdragon' else 25
        
        return round(min(max(temp, 30), 100), 1)
    
    def get_fan_speed_windows(self):
        """Get real fan speed on Windows using WMI"""
        if not WINDOWS_WMI_AVAILABLE:
            return self.get_fan_speed_simulation()
        
        try:
            pythoncom.CoInitialize()
            c = wmi.WMI(namespace="root\\OpenHardwareMonitor")
            
            # Try to get fan speed from OpenHardwareMonitor
            for sensor in c.Sensor():
                if sensor.SensorType == 'Fan':
                    return int(sensor.Value)
        except Exception as e:
            logger.debug(f"Could not get real fan speed via WMI: {e}")
        finally:
            pythoncom.CoUninitialize()
        
        # Fallback to simulation
        return self.get_fan_speed_simulation()
    
    def get_fan_speed_simulation(self):
        """Simulate fan speed based on temperature"""
        # Use Windows method if available, otherwise simulate
        if platform.system() == 'Windows':
            temp = self.get_temperature_windows()
        else:
            temp = self.get_temperature_simulation()
        
        if self.device_type == 'snapdragon':
            # Snapdragon rarely needs fan
            if temp < 60:
                return 0
            else:
                return int((temp - 60) * 50)
        else:
            # Intel fan kicks in early and often
            if temp < 40:
                return 0
            elif temp < 50:
                return 1500
            elif temp < 60:
                return 2500
            elif temp < 70:
                return 3500
            else:
                return min(4500, int(1000 + (temp - 40) * 100))
    
    def simulate_workload(self, workload_type):
        """Simulate a workload type for testing
        
        Args:
            workload_type: Type of workload ('idle', 'normal', 'high', 'stress')
        """
        self.workload = workload_type
        logger.info(f"Simulating {workload_type} workload on {self.device_type}")
        
        # Update CPU and temperature based on workload
        if workload_type in config.get('simulation', {}).get('workload_profiles', {}):
            profile = config['simulation']['workload_profiles'][workload_type]
            self.base_cpu = self.device_config.get('base_cpu', 20) * profile.get('cpu_multiplier', 1.0)
            self.base_temp = self.device_config.get('base_temp', 40) + profile.get('temp_increase', 0)
    
    def get_metrics(self):
        """Get current device metrics for testing"""
        return self.get_system_metrics()
    
    def run_ai_inference(self):
        """Simulate AI inference for testing
        
        Returns:
            dict: AI inference results
        """
        # Simulate AI performance based on device TOPS
        if self.device_type == 'snapdragon':
            inference_time = random.uniform(0.8, 1.2)  # Fast inference
            accuracy = random.uniform(0.95, 0.99)
        else:
            inference_time = random.uniform(2.5, 3.5)  # Slower inference
            accuracy = random.uniform(0.92, 0.96)
        
        return {
            'inference_time': round(inference_time, 3),
            'accuracy': round(accuracy, 3),
            'tops_utilized': self.ai_tops,
            'model': 'Stable Diffusion XL'
        }
    
    def run_test(self, scenario, test_config):
        """Run a specific test scenario"""
        start_time = time.time()
        
        if scenario == 'ai_showdown':
            # Simulate AI image generation
            logger.info("Starting AI image generation simulation...")
            
            # Simulate different completion times
            if self.device_type == 'snapdragon':
                duration = random.uniform(8, 12)
            else:
                duration = random.uniform(25, 35)
            
            # Show progress updates
            steps = test_config.get('steps', 20)
            for step in range(steps):
                if not self.current_test:
                    break
                    
                progress = (step + 1) / steps * 100
                self.sio.emit('test_progress', {
                    'device_type': self.device_type,
                    'scenario': scenario,
                    'progress': progress,
                    'step': step + 1,
                    'total_steps': steps
                })
                
                time.sleep(duration / steps)
            
            # Report completion
            completion_time = time.time() - start_time
            self.sio.emit('test_complete', {
                'device_type': self.device_type,
                'scenario': scenario,
                'result': {
                    'time': round(completion_time, 1),
                    'success': True
                }
            })
            
        elif scenario == 'battery_race':
            # Simulate battery drain test
            logger.info("Starting battery efficiency test...")
            duration = test_config.get('duration', 180)
            
            # Simulate CPU/GPU stress
            start_battery = psutil.sensors_battery().percent if psutil.sensors_battery() else 100
            
            for i in range(duration):
                if not self.current_test:
                    break
                    
                # Simulate workload
                _ = sum(j*j for j in range(10000))
                time.sleep(1)
            
            # Report battery drain
            end_battery = psutil.sensors_battery().percent if psutil.sensors_battery() else 95
            drain = start_battery - end_battery
            
            # Simulate different drain rates
            if self.device_type == 'snapdragon':
                drain = random.uniform(2, 3)
            else:
                drain = random.uniform(5, 7)
            
            self.sio.emit('test_complete', {
                'device_type': self.device_type,
                'scenario': scenario,
                'result': {
                    'battery_drain': round(drain, 1),
                    'duration': duration,
                    'success': True
                }
            })
            
        elif scenario == 'thermal_test':
            # Simulate thermal stress test
            logger.info("Starting thermal stress test...")
            duration = test_config.get('duration', 180)
            
            max_temp = 0
            for i in range(duration):
                if not self.current_test:
                    break
                    
                # Simulate workload
                _ = sum(j*j for j in range(50000))
                
                # Track max temperature
                current_temp = self.get_temperature_simulation()
                max_temp = max(max_temp, current_temp)
                
                time.sleep(1)
            
            self.sio.emit('test_complete', {
                'device_type': self.device_type,
                'scenario': scenario,
                'result': {
                    'max_temperature': round(max_temp, 1),
                    'duration': duration,
                    'success': True
                }
            })
        
        self.current_test = None
    
    def metrics_reporter(self):
        """Continuously report metrics to server"""
        while self.running:
            try:
                if self.sio.connected:
                    metrics = self.get_system_metrics()
                    self.sio.emit('metrics_update', {
                        'device_type': self.device_type,
                        'metrics': metrics,
                        'timestamp': datetime.now().isoformat()
                    })
                
                time.sleep(config['monitoring']['update_interval'])
                
            except Exception as e:
                logger.error(f"Error reporting metrics: {e}")
                time.sleep(5)
    
    def connect_to_server(self):
        """Connect to the championship server"""
        max_retries = 5
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                logger.info(f"Attempting to connect to {self.server_url}...")
                self.sio.connect(self.server_url)
                logger.info("Successfully connected to server!")
                return True
                
            except Exception as e:
                retry_count += 1
                logger.error(f"Connection attempt {retry_count} failed: {e}")
                
                if retry_count < max_retries:
                    wait_time = retry_count * 2
                    logger.info(f"Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                else:
                    logger.error("Max retries reached. Unable to connect to server.")
                    return False
        
        return False
    
    def run(self):
        """Main agent loop"""
        # Connect to server
        if not self.connect_to_server():
            logger.error("Failed to connect to server. Exiting.")
            return
        
        # Start metrics reporter thread
        reporter_thread = threading.Thread(target=self.metrics_reporter, daemon=True)
        reporter_thread.start()
        
        # Keep running
        try:
            logger.info(f"Agent running as {self.device_type}. Press Ctrl+C to stop.")
            while self.running:
                time.sleep(1)
                
        except KeyboardInterrupt:
            logger.info("Shutting down agent...")
            self.running = False
            self.sio.disconnect()

def main():
    """Main entry point"""
    print("\n" + "="*60)
    print("  SNAPDRAGON vs INTEL PERFORMANCE CHAMPIONSHIP")
    print("  Device Agent v1.0")
    print("="*60 + "\n")
    
    agent = DeviceAgent()
    agent.run()

if __name__ == '__main__':
    main()
