@echo off
title Naver Band Auto Poster

echo ================================================
echo Naver Band Auto Poster v1.0
echo ================================================
echo.

REM Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed!
    echo.
    echo Please download Python from: https://www.python.org/downloads/
    echo.
    echo IMPORTANT: Check "Add Python to PATH" during installation!
    echo.
    pause
    exit /b 1
)

echo [OK] Python installed
echo.

REM Install packages on first run
if not exist ".installed" (
    echo [FIRST RUN] Installing required packages...
    echo This will take 1-2 minutes.
    echo.
    pip install -r requirements.txt
    if errorlevel 1 (
        echo.
        echo [ERROR] Package installation failed
        pause
        exit /b 1
    )
    echo. > .installed
    echo.
    echo [OK] Packages installed!
    echo.
)

echo Starting program...
echo.
python run.py

if errorlevel 1 (
    echo.
    echo [ERROR] Program execution failed
    pause
)
