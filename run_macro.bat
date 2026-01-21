@echo off
title Safe Macro Runner

echo Starting PowerShell script...
echo.

powershell -ExecutionPolicy Bypass -File "%~dp0Start-SafeMacro.ps1"

if errorlevel 1 (
    echo.
    echo Failed to run PowerShell script.
    echo Please run manually: powershell -File Start-SafeMacro.ps1
    pause
)
