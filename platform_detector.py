#!/usr/bin/env python3
"""
Platform Detection System
Automatically identifies hardware platform and capabilities
"""

import platform
import subprocess
import json
import psutil
import sys
import os
from typing import Dict, Optional

class PlatformDetector:
    def __init__(self):
        self.platform_info = {}
        self.detect_all()
    
    def detect_all(self) -> Dict:
        """Comprehensive platform detection"""
        self.platform_info = {
            'os': platform.system(),
            'os_version': platform.version(),
            'machine': platform.machine(),
            'processor': platform.processor(),
            'cpu_count': psutil.cpu_count(),
            'memory_gb': round(psutil.virtual_memory().total / (1024**3), 2),
            'python_version': sys.version,
            'architecture': platform.architecture()[0]
        }
        
        # Detect specific platform
        self.platform_info['platform_type'] = self._detect_platform_type()
        self.platform_info['has_npu'] = self._detect_npu()
        self.platform_info['gpu_info'] = self._detect_gpu()
        
        return self.platform_info
    
    def _detect_platform_type(self) -> str:
        """Detect if running on Snapdragon or Intel"""
        machine = platform.machine().lower()
        processor = platform.processor().lower()
        
        # Check for ARM64/Snapdragon
        if 'arm' in machine or 'aarch64' in machine:
            return 'snapdragon'
        
        # Check processor info for Qualcomm
        try:
            if os.name == 'nt':  # Windows
                result = subprocess.run(['wmic', 'cpu', 'get', 'name'], 
                                      capture_output=True, text=True)
                cpu_name = result.stdout.lower()
                
                if 'snapdragon' in cpu_name or 'qualcomm' in cpu_name:
                    return 'snapdragon'
                elif 'intel' in cpu_name:
                    return 'intel'
                elif 'amd' in cpu_name:
                    return 'amd'
        except:
            pass
        
        # Default to x86 platforms
        if 'x86' in machine or 'amd64' in machine:
            return 'intel'
        
        return 'unknown'
    
    def _detect_npu(self) -> bool:
        """Detect if NPU is available"""
        platform_type = self.platform_info.get('platform_type', 'unknown')
        
        if platform_type == 'snapdragon':
            # Snapdragon X Elite has 45 TOPS NPU
            return True
        
        # Check for Intel NPU (Core Ultra has NPU)
        if platform_type == 'intel':
            try:
                # Try to detect Intel NPU
                result = subprocess.run(['wmic', 'path', 'Win32_PnPEntity', 
                                       'where', "name like '%NPU%' or name like '%Neural%'"],
                                      capture_output=True, text=True)
                if 'NPU' in result.stdout or 'Neural' in result.stdout:
                    return True
            except:
                pass
        
        return False
    
    def _detect_gpu(self) -> Optional[str]:
        """Detect GPU information"""
        try:
            if os.name == 'nt':
                result = subprocess.run(['wmic', 'path', 'win32_VideoController', 
                                       'get', 'name'], 
                                      capture_output=True, text=True)
                lines = result.stdout.strip().split('\n')
                if len(lines) > 1:
                    return lines[1].strip()
        except:
            pass
        return None
    
    def get_optimal_config(self) -> Dict:
        """Return optimal configuration for detected platform"""
        platform_type = self.platform_info.get('platform_type', 'unknown')
        
        configs = {
            'snapdragon': {
                'use_onnx': True,
                'use_directml': True,
                'model_format': 'onnx',
                'optimization_level': 'O3',
                'precision': 'fp16',
                'batch_size': 1,
                'num_inference_steps': 20,
                'device_ip': '192.168.100.10'
            },
            'intel': {
                'use_onnx': False,
                'use_directml': False,
                'model_format': 'pytorch',
                'optimization_level': 'O1',
                'precision': 'fp32',
                'batch_size': 1,
                'num_inference_steps': 30,
                'device_ip': '192.168.100.20'
            },
            'unknown': {
                'use_onnx': False,
                'use_directml': False,
                'model_format': 'pytorch',
                'optimization_level': 'O0',
                'precision': 'fp32',
                'batch_size': 1,
                'num_inference_steps': 30,
                'device_ip': '192.168.100.30'
            }
        }
        
        return configs.get(platform_type, configs['unknown'])
    
    def save_config(self, filepath: str = 'platform_config.json'):
        """Save platform configuration to file"""
        config = {
            'platform_info': self.platform_info,
            'optimal_config': self.get_optimal_config()
        }
        
        with open(filepath, 'w') as f:
            json.dump(config, f, indent=2)
        
        return config
    
    def is_snapdragon(self) -> bool:
        """Check if running on Snapdragon"""
        return self.platform_info.get('platform_type') == 'snapdragon'
    
    def is_intel(self) -> bool:
        """Check if running on Intel"""
        return self.platform_info.get('platform_type') == 'intel'


def main():
    """Main function for standalone execution"""
    print("=" * 60)
    print("  PLATFORM DETECTION SYSTEM")
    print("=" * 60)
    
    detector = PlatformDetector()
    
    print(f"\n🔍 Detected Platform: {detector.platform_info.get('platform_type', 'unknown').upper()}")
    print(f"📊 System Information:")
    print(f"  • OS: {detector.platform_info.get('os')} {detector.platform_info.get('os_version')[:20]}...")
    print(f"  • Architecture: {detector.platform_info.get('architecture')}")
    print(f"  • CPU: {detector.platform_info.get('processor')[:50]}...")
    print(f"  • Cores: {detector.platform_info.get('cpu_count')}")
    print(f"  • Memory: {detector.platform_info.get('memory_gb')} GB")
    print(f"  • NPU Available: {'✅' if detector.platform_info.get('has_npu') else '❌'}")
    
    if detector.platform_info.get('gpu_info'):
        print(f"  • GPU: {detector.platform_info.get('gpu_info')}")
    
    # Save configuration
    config = detector.save_config()
    optimal = config['optimal_config']
    
    print(f"\n⚙️ Optimal Configuration:")
    print(f"  • Model Format: {optimal['model_format']}")
    print(f"  • Precision: {optimal['precision']}")
    print(f"  • Use ONNX: {'✅' if optimal['use_onnx'] else '❌'}")
    print(f"  • Use DirectML: {'✅' if optimal['use_directml'] else '❌'}")
    print(f"  • Device IP: {optimal['device_ip']}")
    
    print("\n✅ Configuration saved to platform_config.json")
    
    # Write platform type to file for batch scripts
    with open('platform.txt', 'w') as f:
        f.write(detector.platform_info.get('platform_type', 'unknown'))
    
    return detector.platform_info.get('platform_type', 'unknown')


if __name__ == '__main__':
    platform_type = main()
    sys.exit(0 if platform_type != 'unknown' else 1)
