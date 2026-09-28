# AI Resume & Career Analyzer Launcher (PowerShell)
$Host.UI.RawUI.WindowTitle = "AI Resume & Career Analyzer"
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "          🚀 Launching AI Resume & Career Analyzer Platform" -ForegroundColor Green
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

$pythonExe = "python"
if (Test-Path "$scriptDir\backend\.venv\Scripts\python.exe") {
    $pythonExe = "$scriptDir\backend\.venv\Scripts\python.exe"
} elseif (Test-Path "$scriptDir\.venv\Scripts\python.exe") {
    $pythonExe = "$scriptDir\.venv\Scripts\python.exe"
}

Write-Host "[1/2] Opening browser at http://localhost:5000..." -ForegroundColor Yellow
Start-Process "http://localhost:5000"

Write-Host "[2/2] Starting server with $pythonExe..." -ForegroundColor Green
& $pythonExe "$scriptDir\backend\app_mock.py"
