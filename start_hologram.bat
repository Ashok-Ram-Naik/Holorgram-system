@echo off
echo Starting Hologram Interaction System...
echo The system is now served over a local web server to fix the microphone permission issue!
echo.
echo Please allow microphone access ONCE in the browser, and it will be remembered.
echo (Press Ctrl+C in this window to stop the server)
echo.

:: Open the browser to localhost
start http://localhost:8080/

:: Start the python http server in the frontend directory
cd frontend
python -m http.server 8080
