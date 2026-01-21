@echo off
chcp 65001 > nul
title 네이버밴드 안전 매크로 - Chrome 디버깅 모드 실행

echo ============================================================
echo 네이버밴드 안전 매크로
echo Chrome 디버깅 모드 실행 도구
echo ============================================================
echo.

REM Chrome 경로 찾기
set CHROME_PATH=
if exist "C:\Program Files\Google\Chrome\Application\chrome.exe" (
    set CHROME_PATH=C:\Program Files\Google\Chrome\Application\chrome.exe
) else if exist "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" (
    set CHROME_PATH=C:\Program Files (x86)\Google\Chrome\Application\chrome.exe
) else if exist "%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe" (
    set CHROME_PATH=%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe
)

if "%CHROME_PATH%"=="" (
    echo ❌ Chrome을 찾을 수 없습니다.
    echo Chrome을 설치하거나 경로를 수동으로 지정하세요.
    pause
    exit /b 1
)

echo ✅ Chrome 찾음: %CHROME_PATH%
echo.

REM 사용자 데이터 디렉토리
set USER_DATA_DIR=%USERPROFILE%\chrome_dev_session

REM 디버깅 포트
set DEBUG_PORT=9222

echo 📋 설정:
echo    - 디버깅 포트: %DEBUG_PORT%
echo    - 데이터 디렉토리: %USER_DATA_DIR%
echo.

REM 기존 Chrome 프로세스 확인
tasklist /FI "IMAGENAME eq chrome.exe" 2>NUL | find /I /N "chrome.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo ⚠️ Chrome이 이미 실행 중입니다.
    echo.
    echo Chrome을 완전히 종료하고 다시 시도하시겠습니까?
    echo 1. 예 - Chrome 종료 후 디버깅 모드로 실행
    echo 2. 아니오 - 현재 실행 중인 Chrome 사용 시도
    echo.
    choice /C 12 /N /M "선택하세요 (1 또는 2): "
    
    if errorlevel 2 goto SKIP_KILL
    if errorlevel 1 goto KILL_CHROME
    
    :KILL_CHROME
    echo.
    echo Chrome 종료 중...
    taskkill /F /IM chrome.exe >nul 2>&1
    timeout /t 2 /nobreak >nul
    echo ✅ Chrome 종료 완료
    echo.
    
    :SKIP_KILL
)

echo 🚀 Chrome을 디버깅 모드로 실행합니다...
echo.
echo ┌─────────────────────────────────────────────────────────┐
echo │ Chrome이 실행되면:                                       │
echo │ 1. 네이버에 로그인하세요                                │
echo │ 2. 네이버밴드 채팅방으로 이동하세요                     │
echo │ 3. 다른 명령 프롬프트에서 매크로를 실행하세요           │
echo │    python src/safe_band_macro.py --test                 │
echo └─────────────────────────────────────────────────────────┘
echo.

start "" "%CHROME_PATH%" --remote-debugging-port=%DEBUG_PORT% --user-data-dir="%USER_DATA_DIR%"

echo.
echo ✅ Chrome 디버깅 모드 실행 완료!
echo.
echo 💡 다음 단계:
echo    1. Chrome에서 네이버밴드 로그인 및 채팅방 열기
echo    2. 새 명령 프롬프트 열기
echo    3. 매크로 실행: python src/safe_band_macro.py --test
echo.
pause
