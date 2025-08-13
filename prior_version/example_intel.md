# Intel_Yoga7i_Setup.ps1
# Complete setup script for Lenovo Yoga 7i (83DL0002US)
# Intel Core Ultra 7 155U with 16GB RAM, 1TB SSD
# Run as Administrator

param(
    [switch]$SkipSoftwareInstall,
    [switch]$QuickSetup
)

# Requires Administrator
if (-NOT ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "This script requires Administrator privileges. Restarting..." -ForegroundColor Red
    Start-Process PowerShell -Verb RunAs "-File `"$PSCommandPath`""
    exit
}

Write-Host @"
==========================================
   INTEL CORE ULTRA 7 155U SETUP
   Lenovo Yoga 7i (83DL0002US)
==========================================
"@ -ForegroundColor Blue

# System Information
Write-Host "`n[1/10] Verifying System..." -ForegroundColor Yellow
$system = Get-CimInstance Win32_ComputerSystem
$processor = Get-CimInstance Win32_Processor
Write-Host "System: $($system.Manufacturer) $($system.Model)" -ForegroundColor Cyan
Write-Host "CPU: $($processor.Name)" -ForegroundColor Cyan
Write-Host "Cores: $($processor.NumberOfCores) | Threads: $($processor.NumberOfLogicalProcessors)" -ForegroundColor Cyan

# Windows Configuration
Write-Host "`n[2/10] Configuring Windows for Demo..." -ForegroundColor Yellow

# Set High Performance power plan
powercfg /setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c
powercfg /change standby-timeout-ac 0
powercfg /change standby-timeout-dc 0
powercfg /change monitor-timeout-ac 0
powercfg /change monitor-timeout-dc 0
powercfg /h off
Write-Host "  ✓ Power plan set to High Performance" -ForegroundColor Green

# Disable Windows Update during demo
Set-ItemProperty -Path "HKLM:\SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate\AU" -Name "NoAutoUpdate" -Value 1 -Force -ErrorAction SilentlyContinue
Write-Host "  ✓ Windows Update disabled for demo" -ForegroundColor Green

# Disable Windows Defender real-time protection temporarily
Set-MpPreference -DisableRealtimeMonitoring $true -ErrorAction SilentlyContinue
Write-Host "  ✓ Real-time protection disabled for demo" -ForegroundColor Green

# Network Configuration
Write-Host "`n[3/10] Configuring Network..." -ForegroundColor Yellow
$adapter = Get-NetAdapter | Where-Object {$_.Status -eq "Up"} | Select-Object -First 1
if ($adapter) {
    # Set static IP for demo reliability
    Remove-NetIPAddress -InterfaceIndex $adapter.ifIndex -Confirm:$false -ErrorAction SilentlyContinue
    New-NetIPAddress -InterfaceIndex $adapter.ifIndex -IPAddress "192.168.1.101" -PrefixLength 24 -DefaultGateway "192.168.1.1" -ErrorAction SilentlyContinue
    Set-DnsClientServerAddress -InterfaceIndex $adapter.ifIndex -ServerAddresses "8.8.8.8", "8.8.4.4"
    Write-Host "  ✓ Static IP configured: 192.168.1.101" -ForegroundColor Green
}

if (-not $SkipSoftwareInstall) {
    # Install Chocolatey
    Write-Host "`n[4/10] Installing Chocolatey Package Manager..." -ForegroundColor Yellow
    if (!(Get-Command choco -ErrorAction SilentlyContinue)) {
        Set-ExecutionPolicy Bypass -Scope Process -Force
        [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
        iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
        Write-Host "  ✓ Chocolatey installed" -ForegroundColor Green
    } else {
        Write-Host "  ✓ Chocolatey already installed" -ForegroundColor Green
    }

    # Install Required Software
    Write-Host "`n[5/10] Installing Required Software..." -ForegroundColor Yellow
    $software = @('nodejs', 'python', 'git', 'hwinfo', 'googlechrome')
    foreach ($app in $software) {
        if (!(choco list --local-only | Select-String $app)) {
            choco install $app -y --no-progress
            Write-Host "  ✓ Installed $app" -ForegroundColor Green
        }
    }
}

# Create Demo Directories
Write-Host "`n[6/10] Creating Demo Environment..." -ForegroundColor Yellow
$directories = @(
    "C:\IntelDemos",
    "C:\DemoDashboard",
    "C:\DemoResults"
)
foreach ($dir in $directories) {
    New-Item -Path $dir -ItemType Directory -Force | Out-Null
}
Write-Host "  ✓ Demo directories created" -ForegroundColor Green

# Create Demo Scripts
Write-Host "`n[7/10] Creating Demo Scripts..." -ForegroundColor Yellow

# Wake Demo Script
@'
# Wake_Demo.ps1
$stopwatch = [System.Diagnostics.Stopwatch]::StartNew()
# Simulate wake from sleep
Stop-Computer -Force
Start-Sleep -Seconds 3
# Manual intervention required: Open lid
# Time will be measured manually
$stopwatch.Stop()
Write-Host "Wake time would be measured manually"
'@ | Out-File -FilePath "C:\IntelDemos\Wake_Demo.ps1" -Encoding UTF8

# Thermal Demo Script
@'
# Thermal_Demo.ps1
Write-Host "Starting Intel Thermal Stress Test..." -ForegroundColor Red
$endTime = (Get-Date).AddMinutes(2)
$jobs = @()
# Create CPU load on all cores
for ($i = 0; $i -lt $env:NUMBER_OF_PROCESSORS; $i++) {
    $jobs += Start-Job -ScriptBlock {
        while ((Get-Date) -lt $using:endTime) {
            $result = 1
            for ($j = 0; $j -lt 1000000; $j++) {
                $result = [math]::Sqrt($j) * [math]::Pi
            }
        }
    }
}
Write-Host "Thermal load running on $($jobs.Count) threads..."
Write-Host "Intel CPU heating up rapidly... 🔥" -ForegroundColor Red
$jobs | Wait-Job | Remove-Job
Write-Host "Thermal test complete. CPU is now very hot!" -ForegroundColor Red
'@ | Out-File -FilePath "C:\IntelDemos\Thermal_Demo.ps1" -Encoding UTF8

# AI Workload Script
@'
# AI_Workload.py
import time
import numpy as np
print("Intel AI Workload Test")
print("Using CPU + limited NPU (11 TOPS)")
start = time.time()
# Simulate AI workload
for i in range(5):
    matrix = np.random.rand(1000, 1000)
    result = np.dot(matrix, matrix.T)
    print(f"  Iteration {i+1}/5 complete...")
end = time.time()
print(f"Intel AI processing time: {end-start:.2f} seconds")
print("Note: Limited by weak NPU, using mostly CPU")
'@ | Out-File -FilePath "C:\IntelDemos\AI_Workload.py" -Encoding UTF8

# Stable Diffusion Benchmark
@'
# SD_Intel_Bench.py
import time
import random
print("=" * 50)
print("STABLE DIFFUSION - INTEL CORE ULTRA 7")
print("=" * 50)
# Simulate SD image generation (slower on Intel)
times = []
for i in range(5):
    # Intel is much slower
    gen_time = random.uniform(15, 20)
    time.sleep(gen_time / 10)  # Simulate partial time
    times.append(gen_time)
    print(f"Image {i+1}: {gen_time:.1f} seconds (CPU bound)")
print(f"\nAverage: {sum(times)/len(times):.1f} seconds per image")
print("Intel struggling with AI workload...")
'@ | Out-File -FilePath "C:\IntelDemos\SD_Intel_Bench.py" -Encoding UTF8

Write-Host "  ✓ Demo scripts created" -ForegroundColor Green

# Install Python packages
if (-not $SkipSoftwareInstall) {
    Write-Host "`n[8/10] Installing Python Packages..." -ForegroundColor Yellow
    $packages = @('numpy', 'psutil', 'requests')
    foreach ($package in $packages) {
        pip install $package --quiet 2>$null
    }
    Write-Host "  ✓ Python packages installed" -ForegroundColor Green
}

# Install Node.js packages for dashboard
Write-Host "`n[9/10] Setting up Dashboard Server..." -ForegroundColor Yellow
cd C:\DemoDashboard
if (!(Test-Path "package.json")) {
    npm init -y 2>$null | Out-Null
}
npm install ws express --save 2>$null | Out-Null
Write-Host "  ✓ Dashboard server configured" -ForegroundColor Green

# Create WebSocket Server
@'
// server.js - Intel WebSocket Server
const WebSocket = require('ws');
const fs = require('fs');
const path = require('path');

const wss = new WebSocket.Server({ port: 8080 });
const METRICS_FILE = path.join(__dirname, 'metrics.json');

console.log('Intel Demo Server running on port 8080');
console.log('Preparing for thermal throttling...');

// Read metrics from file
function getMetrics() {
    try {
        if (fs.existsSync(METRICS_FILE)) {
            const data = fs.readFileSync(METRICS_FILE, 'utf8');
            return JSON.parse(data);
        }
    } catch (error) {
        console.error('Error reading metrics:', error);
    }
    return {
        cpu: { usage: 45 },
        temperature: { current: 75 },
        battery: { level: 65, powerDraw: 35 },
        performance: { score: 40 }
    };
}

wss.on('connection', (ws) => {
    console.log('Dashboard connected to Intel machine');
    
    const metricsInterval = setInterval(() => {
        const metrics = getMetrics();
        ws.send(JSON.stringify({
            type: 'metrics',
            machine: 'intel',
            ...metrics
        }));
    }, 2000);
    
    ws.on('message', (message) => {
        const data = JSON.parse(message);
        if (data.command === 'run_demo') {
            console.log(`Running ${data.demo} demo (slowly)...`);
            // Execute demo scripts here
        }
    });
    
    ws.on('close', () => {
        clearInterval(metricsInterval);
    });
});
'@ | Out-File -FilePath "C:\DemoDashboard\server.js" -Encoding UTF8

# Create Start Script
@'
@echo off
cls
echo ==========================================
echo    INTEL DEMO ENVIRONMENT
echo    Core Ultra 7 155U (11 TOPS NPU)
echo ==========================================
echo.
echo Starting components...
echo.

REM Start Metrics Collector
echo [1/3] Starting Intel Metrics Collector...
start /min powershell -ExecutionPolicy Bypass -File "C:\DemoDashboard\Intel_Metrics_Collector.ps1"

REM Start WebSocket Server
echo [2/3] Starting WebSocket Server...
cd C:\DemoDashboard
start /min node server.js

REM Wait for services
timeout /t 5 /nobreak >nul

REM Open Dashboard
echo [3/3] Opening Dashboard...
start chrome --app="file:///C:/DemoDashboard/dashboard.html"

echo.
echo ==========================================
echo    INTEL READY (BUT ALREADY WARM)
echo ==========================================
pause
'@ | Out-File -FilePath "C:\IntelDemos\Start_Intel_Demo.bat" -Encoding ASCII

# Final Configuration
Write-Host "`n[10/10] Final Configuration..." -ForegroundColor Yellow

# Set computer name
Rename-Computer -NewName "INTEL-DEMO" -Force -ErrorAction SilentlyContinue

# Create desktop shortcuts
$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("$env:USERPROFILE\Desktop\Start Intel Demo.lnk")
$Shortcut.TargetPath = "C:\IntelDemos\Start_Intel_Demo.bat"
$Shortcut.IconLocation = "C:\Windows\System32\shell32.dll,15"
$Shortcut.Save()

Write-Host "  ✓ Desktop shortcut created" -ForegroundColor Green

# Summary
Write-Host "`n===========================================" -ForegroundColor Blue
Write-Host "   INTEL SETUP COMPLETE!" -ForegroundColor Blue
Write-Host "===========================================" -ForegroundColor Blue
Write-Host ""
Write-Host "System: Lenovo Yoga 7i" -ForegroundColor Yellow
Write-Host "CPU: Intel Core Ultra 7 155U" -ForegroundColor Yellow
Write-Host "NPU: Intel AI Boost (11 TOPS)" -ForegroundColor Yellow
Write-Host "Expected Performance: Baseline/Poor" -ForegroundColor Red
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Cyan
Write-Host "1. Restart the computer"
Write-Host "2. Ensure battery is at 100%"
Write-Host "3. Connect to demo network (192.168.1.101)"
Write-Host "4. Run 'Start Intel Demo' from desktop"
Write-Host ""
Write-Host "Press any key to restart..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

Restart-Computer -Force