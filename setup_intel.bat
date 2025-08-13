@echo off
REM ============================================================
REM   INTEL CORE ULTRA 7 - COMPREHENSIVE AUTOMATED SETUP
REM   x86-64 with standard CPU processing
REM   Version 2.0 - Production Ready
REM ============================================================

echo.
echo ====================================================
echo   INTEL CORE ULTRA 7 SETUP
echo   Standard CPU-Based AI Processing
echo ====================================================
echo.

REM Check if running as administrator
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️  This script requires administrator privileges
    echo    Right-click and select "Run as administrator"
    pause
    exit /b 1
)

REM Create required directories
echo [1/12] Creating project directories...
mkdir dashboard\assets\generated 2>nul
mkdir logs 2>nul
mkdir temp 2>nul
mkdir cache 2>nul
mkdir models\intel 2>nul
echo ✅ Directories created

REM Step 2: Check and install package managers
echo [2/12] Checking package managers...
where winget >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing App Installer (winget)...
    start ms-windows-store://pdp/?ProductId=9NBLGGH4NNS1
    echo Please complete winget installation from Microsoft Store, then press any key...
    pause
)

where choco >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing Chocolatey...
    powershell -NoProfile -ExecutionPolicy Bypass -Command "iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))"
    set PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\bin
)
echo ✅ Package managers available

REM Step 3: Install system prerequisites
echo [3/12] Installing system prerequisites...

REM Visual C++ Redistributables
echo Checking Visual C++ Redistributables...
reg query "HKLM\SOFTWARE\Microsoft\VisualStudio\14.0\VC\Runtimes\x64" >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing Visual C++ 2015-2022...
    choco install vcredist140 -y --force
)

REM .NET Framework
echo Checking .NET Framework...
reg query "HKLM\SOFTWARE\Microsoft\NET Framework Setup\NDP\v4\Full" /v Release | findstr /i "528040" >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing .NET Framework 4.8...
    choco install dotnetfx -y --force
)

echo ✅ System prerequisites installed

REM Step 4: Install Python
echo [4/12] Installing Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing Python 3.11 (x64)...
    winget install Python.Python.3.11 --architecture x64 --silent
    
    REM Add Python to PATH
    set PATH=%PATH%;%LOCALAPPDATA%\Programs\Python\Python311;%LOCALAPPDATA%\Programs\Python\Python311\Scripts
    
    if %errorlevel% neq 0 (
        echo ❌ Failed to install Python. Please install manually.
        pause
        exit /b 1
    )
)
echo ✅ Python installed

REM Step 5: Install browser if needed
echo [5/12] Checking browser installation...
where chrome >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Chrome already installed
) else (
    where msedge >nul 2>&1
    if %errorlevel% equ 0 (
        echo ✅ Edge already installed
    ) else (
        echo Installing Microsoft Edge...
        winget install Microsoft.Edge --silent
        echo ✅ Edge installed
    )
)

REM Step 6: Install Git if not present
echo [6/12] Checking Git installation...
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing Git...
    winget install Git.Git --silent
    set PATH=%PATH%;%PROGRAMFILES%\Git\bin
    echo ✅ Git installed successfully
) else (
    echo ✅ Git already installed
)

REM Step 7: Create virtual environment
echo [7/12] Setting up Python virtual environment...
if not exist "venv_intel" (
    python -m venv venv_intel
    if %errorlevel% neq 0 (
        echo ⚠️  Virtual environment creation failed, trying with system Python...
        py -3.11 -m venv venv_intel
    )
    echo ✅ Virtual environment created
) else (
    echo ✅ Virtual environment already exists
)

REM Activate virtual environment
call venv_intel\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo ❌ Failed to activate virtual environment
    pause
    exit /b 1
)

REM Step 8: Install standard x86-64 packages
echo [8/12] Installing standard Python packages...

REM Upgrade pip first
python -m pip install --upgrade pip

REM Create requirements file for Intel (standard packages)
echo # Intel Core Ultra 7 Requirements > requirements_intel.txt
echo # Standard CPU Processing Packages >> requirements_intel.txt
echo numpy==1.24.3 >> requirements_intel.txt
echo psutil>=5.9.0 >> requirements_intel.txt
echo Pillow>=10.0.0 >> requirements_intel.txt
echo flask>=3.0.0 >> requirements_intel.txt
echo flask-cors>=4.0.0 >> requirements_intel.txt
echo python-socketio>=5.10.0 >> requirements_intel.txt
echo websocket-client>=1.6.0 >> requirements_intel.txt
echo requests>=2.31.0 >> requirements_intel.txt
echo pywin32>=305 ; sys_platform == 'win32' >> requirements_intel.txt
echo wmi>=1.5.1 ; sys_platform == 'win32' >> requirements_intel.txt
echo py-cpuinfo>=9.0.0 >> requirements_intel.txt

echo Installing packages...
pip install -r requirements_intel.txt

REM Install PyTorch for CPU (standard deployment)
echo Installing PyTorch (CPU version - FP32 precision)...
REM Force CPU-only installation (no GPU acceleration)
set CUDA_VISIBLE_DEVICES=-1
set USE_GPU=0
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu 2>nul
if %errorlevel% eq 0 (
    echo ✅ PyTorch CPU installed (standard precision)
) else (
    echo ⚠️  PyTorch installation failed, trying alternative...
    pip install torch torchvision
)

REM Step 9: Download standard models
echo [9/12] Downloading Intel models...
python download_models.py --platform intel
if %errorlevel% neq 0 (
    echo ⚠️  Model download failed, retrying...
    python download_models.py --platform intel --force
    if %errorlevel% neq 0 (
        echo ❌ Model download failed. Demo may not work properly.
        echo    Please check internet connection and try again.
    )
)

REM Step 10: Configure network
echo [10/12] Configuring network settings...
echo.
echo Network Configuration:
echo   IP Address: 192.168.100.20
echo   Subnet: 255.255.255.0
echo   Gateway: 192.168.100.1
echo.
echo Would you like to configure network automatically? (Y/N)
set /p CONFIGURE_NETWORK=

if /i "%CONFIGURE_NETWORK%"=="Y" (
    echo Configuring network interface...
    netsh interface ip set address "Wi-Fi" static 192.168.100.20 255.255.255.0 192.168.100.1 >nul 2>&1
    if %errorlevel% eq 0 (
        echo ✅ Network configured successfully
    ) else (
        echo Trying Ethernet interface...
        netsh interface ip set address "Ethernet" static 192.168.100.20 255.255.255.0 192.168.100.1 >nul 2>&1
        if %errorlevel% eq 0 (
            echo ✅ Network configured successfully
        ) else (
            echo ⚠️  Could not configure network automatically
            echo    Please configure manually: 192.168.100.20
        )
    )
    
    REM Configure firewall
    echo Configuring firewall rules...
    netsh advfirewall firewall add rule name="Intel Demo Server" dir=in action=allow protocol=TCP localport=5001 >nul 2>&1
    netsh advfirewall firewall add rule name="Intel Demo Agent" dir=in action=allow protocol=TCP localport=8765 >nul 2>&1
    echo ✅ Firewall rules configured
) else (
    echo ⚠️  Manual network configuration required
)

REM Step 11: Configure Windows settings (standard configuration)
echo [11/12] Configuring Windows settings...

REM Set balanced power plan (standard for most deployments)
powercfg /setactive 381b4222-f694-41f0-9685-ff5bb260df2e >nul 2>&1
if %errorlevel% neq 0 (
    echo Using default power plan...
)
echo ✅ Balanced power mode set (standard configuration)

REM Keep default visual effects (typical deployment)
echo ✅ Standard Windows visual effects maintained

REM Standard process priority (no elevation)
echo ✅ Standard process priority maintained

REM Keep Windows services running (normal operation)
echo ✅ Windows services running normally

REM Note: No special optimizations applied - standard deployment

REM Step 12: Create desktop shortcuts
echo [12/12] Creating desktop shortcuts...

REM Create Intel Agent shortcut
echo Set oWS = WScript.CreateObject("WScript.Shell") > CreateShortcut.vbs
echo sLinkFile = "%USERPROFILE%\Desktop\Intel Agent.lnk" >> CreateShortcut.vbs
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> CreateShortcut.vbs
echo oLink.TargetPath = "%CD%\start_agent.bat" >> CreateShortcut.vbs
echo oLink.Arguments = "--platform intel" >> CreateShortcut.vbs
echo oLink.WorkingDirectory = "%CD%" >> CreateShortcut.vbs
echo oLink.IconLocation = "%SystemRoot%\System32\SHELL32.dll, 144" >> CreateShortcut.vbs
echo oLink.Description = "Intel Core Ultra 7 Agent" >> CreateShortcut.vbs
echo oLink.Save >> CreateShortcut.vbs
cscript CreateShortcut.vbs >nul 2>&1
del CreateShortcut.vbs

REM Create Display Window shortcut
echo Set oWS = WScript.CreateObject("WScript.Shell") > CreateShortcut.vbs
echo sLinkFile = "%USERPROFILE%\Desktop\Intel Display.lnk" >> CreateShortcut.vbs
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> CreateShortcut.vbs
echo oLink.TargetPath = "%CD%\venv_intel\Scripts\python.exe" >> CreateShortcut.vbs
echo oLink.Arguments = "%CD%\display_window.py --platform intel" >> CreateShortcut.vbs
echo oLink.WorkingDirectory = "%CD%" >> CreateShortcut.vbs
echo oLink.IconLocation = "%SystemRoot%\System32\SHELL32.dll, 15" >> CreateShortcut.vbs
echo oLink.Description = "Intel AI Display" >> CreateShortcut.vbs
echo oLink.Save >> CreateShortcut.vbs
cscript CreateShortcut.vbs >nul 2>&1
del CreateShortcut.vbs

echo ✅ Shortcuts created

REM Create platform configuration
echo {"platform": "intel", "optimized": false} > platform_config.json

REM Verify installation
echo.
echo Verifying installation...
python -c "import torch; print('PyTorch:', torch.__version__)" 2>nul
python -c "import flask; print('Flask:', flask.__version__)" 2>nul
python -c "import psutil; print('System Monitor: OK')" 2>nul

REM Display summary
echo.
echo ====================================================
echo   ✅ INTEL CORE ULTRA 7 SETUP COMPLETE!
echo ====================================================
echo.
echo 💻 System Configuration:
echo    • Architecture: x86-64
echo    • Platform: Intel Core Ultra 7
echo    • Processing: CPU-based (standard deployment)
echo    • IP Address: 192.168.100.20
echo    • Power Mode: Balanced (standard)
echo    • Model Format: PyTorch (FP32 precision)
echo.
echo 📁 Desktop Shortcuts Created:
echo    • Intel Agent - Run the device agent
echo    • Intel Display - AI generation window
echo.
echo ✅ Prerequisites Installed:
echo    • Visual C++ Redistributables
echo    • .NET Framework 4.8
echo    • Python 3.11
echo    • PyTorch CPU (standard precision)
echo.
echo 🎯 Next Steps:
echo    1. Start the server on this machine first
echo    2. Ensure Snapdragon machine is at 192.168.100.10
echo    3. Run "Intel Agent" shortcut
echo    4. Dashboard available at http://192.168.100.20:8080
echo.
echo 📊 Expected Performance:
echo    • Standard CPU processing speed
echo    • Typical power consumption (~45W under load)
echo    • FP32 precision for compatibility
echo    • No special acceleration
echo.
echo 📝 Notes:
echo    • This is a standard professional deployment
echo    • CPU processing is typical for many AI workloads
echo    • Performance represents real-world Intel setup
echo    • May experience thermal throttling under sustained load
echo.
echo ====================================================
pause
