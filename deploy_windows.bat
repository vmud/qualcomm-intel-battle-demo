@echo off
REM ============================================================
REM   SNAPDRAGON vs INTEL CHAMPIONSHIP - Windows Deployment
REM ============================================================

echo.
echo ============================================================
echo   PERFORMANCE CHAMPIONSHIP DEPLOYMENT SCRIPT
echo   Target: Windows ARM64 (Snapdragon) / x86 (Intel)
echo ============================================================
echo.

REM Check Python installation
echo Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org
    pause
    exit /b 1
)

REM Create virtual environment
echo.
echo Creating Python virtual environment...
if not exist "venv" (
    python -m venv venv
    echo Virtual environment created.
) else (
    echo Virtual environment already exists.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo.
echo Installing Python dependencies...
pip install --upgrade pip
pip install -r requirements.txt

REM Install Windows-specific packages
echo.
echo Installing Windows monitoring packages...
pip install pywin32 wmi

REM Create shortcuts
echo.
echo Creating desktop shortcuts...

REM Create server shortcut
echo Set oWS = WScript.CreateObject("WScript.Shell") > CreateShortcut.vbs
echo sLinkFile = "%USERPROFILE%\Desktop\Demo Server.lnk" >> CreateShortcut.vbs
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> CreateShortcut.vbs
echo oLink.TargetPath = "%CD%\start_server.bat" >> CreateShortcut.vbs
echo oLink.WorkingDirectory = "%CD%" >> CreateShortcut.vbs
echo oLink.IconLocation = "%SystemRoot%\System32\SHELL32.dll, 13" >> CreateShortcut.vbs
echo oLink.Description = "Start Demo Server" >> CreateShortcut.vbs
echo oLink.Save >> CreateShortcut.vbs
cscript CreateShortcut.vbs
del CreateShortcut.vbs

REM Create agent shortcut
echo Set oWS = WScript.CreateObject("WScript.Shell") > CreateShortcut.vbs
echo sLinkFile = "%USERPROFILE%\Desktop\Device Agent.lnk" >> CreateShortcut.vbs
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> CreateShortcut.vbs
echo oLink.TargetPath = "%CD%\start_agent.bat" >> CreateShortcut.vbs
echo oLink.WorkingDirectory = "%CD%" >> CreateShortcut.vbs
echo oLink.IconLocation = "%SystemRoot%\System32\SHELL32.dll, 144" >> CreateShortcut.vbs
echo oLink.Description = "Start Device Agent" >> CreateShortcut.vbs
echo oLink.Save >> CreateShortcut.vbs
cscript CreateShortcut.vbs
del CreateShortcut.vbs

echo.
echo ============================================================
echo   DEPLOYMENT COMPLETE!
echo ============================================================
echo.
echo Desktop shortcuts created:
echo   - Demo Server.lnk (Run on presenter device)
echo   - Device Agent.lnk (Run on each laptop)
echo.
echo Next steps:
echo   1. Configure network (all devices on 192.168.100.x)
echo   2. Run "Demo Server" on presenter device
echo   3. Run "Device Agent" on each laptop
echo   4. Open browser to http://192.168.100.5:5001
echo.
echo ============================================================
pause
