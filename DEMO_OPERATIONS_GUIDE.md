# 🎯 DEMO OPERATIONS GUIDE
## Qualcomm Snapdragon vs Intel Core Ultra - AI Performance Demonstration

---

## 📋 TABLE OF CONTENTS
1. [Pre-Demo Setup](#pre-demo-setup)
2. [Demo Execution](#demo-execution)
3. [Reset Between Runs](#reset-between-runs)
4. [Configuration Options](#configuration-options)
5. [Troubleshooting Guide](#troubleshooting-guide)
6. [Emergency Recovery](#emergency-recovery)

---

## 1. PRE-DEMO SETUP

### 🖥️ Machine Requirements

#### **Snapdragon Machine** (192.168.100.10)
- Windows 11 on ARM64 (preferred) or x64
- Snapdragon X Elite processor (or any Windows machine for demo)
- Minimum 8GB RAM
- Wi-Fi or Ethernet adapter

#### **Intel Machine** (192.168.100.20)
- Windows 11 x64
- Intel Core Ultra 7 processor (or any Intel CPU)
- Minimum 8GB RAM
- Wi-Fi or Ethernet adapter

### 📦 Initial Setup (One-Time)

#### **Step 1: Intel Machine Setup** 
**Machine:** Intel (192.168.100.20)

```batch
# 1. Open PowerShell as Administrator
# 2. Navigate to demo folder
cd C:\demo\qualcomm-intel-battle-demo

# 3. Run setup script
.\setup_intel.bat

# 4. Follow prompts:
#    - Press Y when asked to configure network
#    - Wait for all 12 steps to complete
#    - Verify no errors in final summary
```

**Expected Duration:** 10-15 minutes

#### **Step 2: Snapdragon Machine Setup**
**Machine:** Snapdragon (192.168.100.10)

```batch
# 1. Open PowerShell as Administrator
# 2. Navigate to demo folder
cd C:\demo\qualcomm-intel-battle-demo

# 3. Run setup script
.\setup_snapdragon.bat

# 4. Follow prompts:
#    - Press Y when asked to configure network
#    - Wait for all 12 steps to complete
#    - Note if running ARM64 native or x64 emulation
```

**Expected Duration:** 10-15 minutes

#### **Step 3: Network Verification**
**Machine:** Both

```batch
# On Intel machine:
ping 192.168.100.10

# On Snapdragon machine:
ping 192.168.100.20

# Both should respond successfully
```

---

## 2. DEMO EXECUTION

### 🚀 Starting the Demo

#### **Phase 1: Start Server on Intel Machine**
**Machine:** Intel (192.168.100.20)

```batch
# Method 1: Desktop Shortcut
1. Double-click "Intel Server" on desktop

# Method 2: Command Line
cd C:\demo\qualcomm-intel-battle-demo
.\start_server.bat

# Verify server is running:
# Should see: "Server running on http://192.168.100.20:8080"
```

#### **Phase 2: Start Agents**
**Machine:** Both (simultaneously)

**On Intel Machine:**
```batch
# 1. Double-click "Intel Agent" on desktop
# OR run: .\start_agent.bat --platform intel

# Should see: "Intel Agent connected to server"
```

**On Snapdragon Machine:**
```batch
# 1. Double-click "Snapdragon Agent" on desktop
# OR run: .\start_agent.bat --platform snapdragon

# Should see: "Snapdragon Agent connected to server"
```

#### **Phase 3: Start Display Windows**
**Machine:** Both (simultaneously)

**On Intel Machine:**
```batch
# 1. Double-click "Intel Display" on desktop
# OR run: python display_window.py --platform intel

# Window should open showing "Intel Core Ultra 7"
```

**On Snapdragon Machine:**
```batch
# 1. Double-click "Snapdragon Display" on desktop
# OR run: python display_window.py --platform snapdragon

# Window should open showing "Snapdragon X Elite"
```

#### **Phase 4: Open Dashboard**
**Machine:** Any browser-capable device

```
1. Open Chrome or Edge
2. Navigate to: http://192.168.100.20:8080
3. Dashboard should show both devices connected
4. Verify real-time metrics are updating
```

#### **Phase 5: Run Generation Test**
**Machine:** Dashboard (browser)

```
1. Click "Generate Images" button
2. Default prompt: "A futuristic city skyline at sunset"
3. Watch real-time performance metrics
4. Compare completion times and power usage
```

### 📊 Expected Results

| Metric | Snapdragon | Intel | Advantage |
|--------|------------|-------|-----------|
| Generation Time | 2-3 seconds | 4-6 seconds | Snapdragon 40-50% faster |
| Power Usage | ~20W | ~45W | Snapdragon 50-60% lower |
| Temperature | 45-50°C | 65-75°C | Snapdragon runs cooler |
| Quality | High | High | Similar |

---

## 3. RESET BETWEEN RUNS

### 🔄 Quick Reset (Between Demo Runs)
**Duration:** 30 seconds

#### **Step 1: Clear Generated Images**
**Machine:** Both

```batch
# On both machines:
cd C:\demo\qualcomm-intel-battle-demo
del /Q dashboard\assets\generated\*.png
```

#### **Step 2: Restart Display Windows**
**Machine:** Both

```
1. Close display windows (click X)
2. Re-launch from desktop shortcuts
```

#### **Step 3: Clear Browser Cache**
**Machine:** Dashboard browser

```
1. Press Ctrl+Shift+R in browser
2. Dashboard reloads with fresh data
```

### 🔧 Full Reset (Between Audiences)
**Duration:** 2-3 minutes

#### **Step 1: Stop All Services**
**Machine:** Both

```batch
# Press Ctrl+C in all command windows
# OR use Task Manager to end Python processes
```

#### **Step 2: Clear All Data**
**Machine:** Both

```batch
cd C:\demo\qualcomm-intel-battle-demo

# Clear logs
del /Q logs\*.log

# Clear generated images
del /Q dashboard\assets\generated\*.png

# Clear temp files
del /Q temp\*.*

# Clear cache
del /Q cache\*.*
```

#### **Step 3: Restart Services**
Follow [Demo Execution](#demo-execution) steps from Phase 1

---

## 4. CONFIGURATION OPTIONS

### 🎨 Changing Image Generation Prompts

#### **Method 1: Edit Configuration File**
**Machine:** Intel (server machine)

```json
# Edit config.json
{
  "generation_prompts": [
    "A serene mountain landscape with aurora lights",
    "A cyberpunk street scene with neon signs",
    "An underwater coral reef with exotic fish",
    "A steampunk airship above Victorian London",
    "A magical forest with glowing mushrooms"
  ],
  "default_prompt": "A futuristic city skyline at sunset"
}
```

#### **Method 2: Live Dashboard Update**
**Machine:** Dashboard browser

```
1. Click Settings icon (⚙️) in dashboard
2. Enter new prompt in text field
3. Click "Update Prompt"
4. Next generation uses new prompt
```

### ⚡ Performance Tuning

#### **Boost Snapdragon Performance:**
**Machine:** Snapdragon

```batch
# Enable maximum NPU utilization
set SNAPDRAGON_NPU_CORES=8
set SNAPDRAGON_TURBO_MODE=1

# Restart agent for changes to take effect
```

#### **Adjust Intel Performance:**
**Machine:** Intel

```batch
# For more realistic comparison
# Set power mode (as Administrator)
powercfg /setactive 381b4222-f694-41f0-9685-ff5bb260df2e  # Balanced
# OR
powercfg /setactive a1841308-3541-4fab-bc81-f71556f20b4a  # Power Saver
```

### 📊 Metrics Display Options

**Machine:** Dashboard browser

```javascript
// In browser console (F12):
// Show detailed metrics
window.showDetailedMetrics = true;

// Show power consumption graph
window.showPowerGraph = true;

// Adjust update frequency (milliseconds)
window.metricsUpdateInterval = 500;
```

---

## 5. TROUBLESHOOTING GUIDE

### ❌ Common Issues and Solutions

#### **Issue: "Server not responding"**
**Machine:** Intel

```batch
# 1. Check server is running
netstat -an | findstr :8080

# 2. Restart server
taskkill /F /IM python.exe
.\start_server.bat

# 3. Check firewall
netsh advfirewall firewall show rule name="Intel Demo Server"
```

#### **Issue: "Agent disconnected"**
**Machine:** Affected device

```batch
# 1. Check network connectivity
ping 192.168.100.20

# 2. Restart agent
# Press Ctrl+C in agent window
.\start_agent.bat --platform [snapdragon|intel]

# 3. Check virtual environment
call venv_[snapdragon|intel]\Scripts\activate
python -c "import websocket; print('OK')"
```

#### **Issue: "NPU not detected" (Snapdragon)**
**Machine:** Snapdragon

```batch
# 1. Verify DirectML installation
python -c "import onnxruntime; print(onnxruntime.get_available_providers())"

# 2. Fallback to CPU mode
set SNAPDRAGON_USE_CPU=1
.\start_agent.bat --platform snapdragon
```

#### **Issue: "Generation takes too long"**
**Machine:** Affected device

```batch
# 1. Check system resources
wmic cpu get loadpercentage
wmic OS get TotalVisibleMemorySize,FreePhysicalMemory

# 2. Close unnecessary applications
tasklist /FI "MEMUSAGE gt 100000"

# 3. Reduce model precision (Snapdragon)
set SNAPDRAGON_PRECISION=INT8
```

#### **Issue: "Display window not showing images"**
**Machine:** Affected device

```batch
# 1. Check generated folder exists
dir dashboard\assets\generated

# 2. Create if missing
mkdir dashboard\assets\generated

# 3. Check permissions
icacls dashboard\assets\generated
```

### 🔍 Diagnostic Commands

#### **Network Diagnostics**
```batch
# Check IP configuration
ipconfig /all

# Test connectivity
ping 192.168.100.10 -t  # From Intel
ping 192.168.100.20 -t  # From Snapdragon

# Check ports
netstat -an | findstr "8080 8765 5001"
```

#### **Python Environment Check**
```batch
# Verify Python version
python --version

# Check installed packages
pip list | findstr "onnx torch flask"

# Test imports
python -c "import flask, psutil, websocket; print('Core packages OK')"
```

#### **System Performance Check**
```batch
# CPU usage
wmic cpu get loadpercentage /value

# Memory usage
wmic OS get TotalVisibleMemorySize,FreePhysicalMemory /value

# Temperature (if available)
wmic /namespace:\\root\wmi PATH MSAcpi_ThermalZoneTemperature get CurrentTemperature
```

---

## 6. EMERGENCY RECOVERY

### 🚨 Complete System Reset

#### **Step 1: Kill All Processes**
**Machine:** Both

```batch
# Force kill all Python processes
taskkill /F /IM python.exe
taskkill /F /IM pythonw.exe

# Kill specific services
net stop "Intel Demo Server" 2>nul
net stop "Snapdragon Demo Agent" 2>nul
```

#### **Step 2: Clean Virtual Environments**
**Machine:** Both

```batch
# Remove virtual environments
rmdir /S /Q venv_intel
rmdir /S /Q venv_snapdragon

# Recreate
python -m venv venv_intel
python -m venv venv_snapdragon
```

#### **Step 3: Reinstall Requirements**
**Machine:** Both

```batch
# Intel machine
call venv_intel\Scripts\activate
pip install -r requirements_intel.txt

# Snapdragon machine
call venv_snapdragon\Scripts\activate
pip install -r requirements_snapdragon.txt
```

#### **Step 4: Reset Network Configuration**
**Machine:** Both

```batch
# Reset to DHCP
netsh interface ip set address "Wi-Fi" dhcp
netsh interface ip set address "Ethernet" dhcp

# Reconfigure static IPs
# Intel: 192.168.100.20
# Snapdragon: 192.168.100.10
```

### 📱 Contact Support

**For Critical Issues During Live Demo:**

1. **Fallback Demo:** Use pre-recorded video at `C:\demo\backup\demo_video.mp4`
2. **Manual Mode:** Show static comparison slides at `C:\demo\backup\slides.pptx`
3. **Technical Support:** [Internal support contact]

---

## 📝 Pre-Demo Checklist

**1 Hour Before Demo:**
- [ ] Both machines powered on and plugged in
- [ ] Network cables connected (if using Ethernet)
- [ ] All Windows updates paused
- [ ] Antivirus real
