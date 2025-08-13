@echo off
REM Start the Device Agent for Snapdragon vs Intel Championship

echo.
echo ============================================================
echo   STARTING DEVICE AGENT
echo ============================================================
echo.
echo This agent will:
echo   - Auto-detect device type (Snapdragon/Intel)
echo   - Connect to server at 192.168.100.5:5001
echo   - Report real-time metrics
echo.

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Start the agent
echo Starting device agent...
python agent.py

pause
