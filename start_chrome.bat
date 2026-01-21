@echo off
title Chrome Debug Mode Launcher

echo Starting PowerShell script...
echo.

powershell -ExecutionPolicy Bypass -File "%~dp0Start-ChromeDebug.ps1"

if errorlevel 1 (
    echo.
    echo Failed to run PowerShell script.
    echo Please run manually: powershell -File Start-ChromeDebug.ps1
    pause
)
