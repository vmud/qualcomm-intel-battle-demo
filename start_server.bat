@echo off
REM Start the Demo Server for Snapdragon vs Intel Championship

echo.
echo ============================================================
echo   STARTING PERFORMANCE CHAMPIONSHIP SERVER
echo ============================================================
echo.
echo Server will run on: http://192.168.100.5:5001
echo Dashboard: http://192.168.100.5:5001/dashboard
echo.

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Start the server
echo Starting server...
python server.py

pause
