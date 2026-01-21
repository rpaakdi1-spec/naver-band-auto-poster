@echo off
title Naver Band Safe Macro - Chrome Debug Mode

echo ============================================================
echo Naver Band Safe Typing Macro
echo Chrome Debug Mode Launcher
echo ============================================================
echo.

REM Find Chrome path
set CHROME_PATH=
if exist "C:\Program Files\Google\Chrome\Application\chrome.exe" (
    set CHROME_PATH="C:\Program Files\Google\Chrome\Application\chrome.exe"
) else if exist "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" (
    set CHROME_PATH="C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
) else if exist "%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe" (
    set CHROME_PATH="%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"
)

if "%CHROME_PATH%"=="" (
    echo [ERROR] Chrome not found.
    echo Please install Chrome or specify the path manually.
    pause
    exit /b 1
)

echo [OK] Chrome found: %CHROME_PATH%
echo.

REM User data directory
set USER_DATA_DIR=%USERPROFILE%\chrome_dev_session

REM Debug port
set DEBUG_PORT=9222

echo [Configuration]
echo    - Debug port: %DEBUG_PORT%
echo    - User data: %USER_DATA_DIR%
echo.

REM Check for existing Chrome processes
tasklist /FI "IMAGENAME eq chrome.exe" 2>NUL | find /I /N "chrome.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo [WARNING] Chrome is already running.
    echo.
    echo Do you want to close Chrome and restart in debug mode?
    echo 1. Yes - Close Chrome and launch in debug mode
    echo 2. No - Try to use current Chrome session
    echo.
    choice /C 12 /N /M "Choose (1 or 2): "
    
    if errorlevel 2 goto SKIP_KILL
    if errorlevel 1 goto KILL_CHROME
    
    :KILL_CHROME
    echo.
    echo Closing Chrome...
    taskkill /F /IM chrome.exe >nul 2>&1
    timeout /t 2 /nobreak >nul
    echo [OK] Chrome closed
    echo.
    
    :SKIP_KILL
)

echo [STARTING] Launching Chrome in debug mode...
echo.
echo +-----------------------------------------------------------+
echo ^| After Chrome starts:                                      ^|
echo ^| 1. Login to Naver                                         ^|
echo ^| 2. Go to Naver Band chatroom                              ^|
echo ^| 3. Run macro in another command prompt:                   ^|
echo ^|    python src/safe_band_macro.py --test                   ^|
echo +-----------------------------------------------------------+
echo.

start "" %CHROME_PATH% --remote-debugging-port=%DEBUG_PORT% --user-data-dir="%USER_DATA_DIR%"

echo.
echo [OK] Chrome launched in debug mode!
echo.
echo [Next Steps]
echo    1. Login to Naver Band and open chatroom
echo    2. Open new command prompt
echo    3. Run: python src/safe_band_macro.py --test
echo.
pause
