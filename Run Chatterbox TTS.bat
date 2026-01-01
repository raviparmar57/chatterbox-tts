@echo off
echo Starting Chatterbox TTS Enhanced App...
echo.

set PYTHON_DIR=%~dp0python
set PYTHON_EXE=%PYTHON_DIR%\python.exe
set PROJECT_DIR=%~dp0

"%PYTHON_EXE%" "%PROJECT_DIR%app.py"
pause
