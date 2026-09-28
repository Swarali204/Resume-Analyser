@echo off
title AI Resume & Career Analyzer
echo ======================================================================
echo           🚀 Launching AI Resume & Career Analyzer Platform
echo ======================================================================
echo.

:: Detect virtual environment
if exist "%~dp0backend\.venv\Scripts\python.exe" (
    set "PYTHON_EXE=%~dp0backend\.venv\Scripts\python.exe"
) else if exist "%~dp0.venv\Scripts\python.exe" (
    set "PYTHON_EXE=%~dp0.venv\Scripts\python.exe"
) else (
    set "PYTHON_EXE=python"
)

echo [1/2] Launching browser at http://localhost:5000...
start http://localhost:5000

echo [2/2] Starting Flask server on http://localhost:5000...
"%PYTHON_EXE%" "%~dp0backend\app_mock.py"

pause
