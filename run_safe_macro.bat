@echo off
chcp 65001 > nul
title 네이버밴드 안전 매크로 실행

echo ============================================================
echo 네이버밴드 안전 타이핑 매크로
echo ============================================================
echo.

REM Python 확인
python --version >nul 2>&1
if errorlevel 1 (
    echo [오류] Python이 설치되어 있지 않습니다.
    echo https://www.python.org/downloads/ 에서 다운로드하세요.
    pause
    exit /b 1
)

echo [확인] Python 설치 확인
python --version
echo.

REM 패키지 확인 및 설치
echo [확인] 필요한 패키지 확인 중...
pip show selenium >nul 2>&1
if errorlevel 1 (
    echo selenium 설치 중...
    pip install selenium webdriver-manager
)

pip show pyperclip >nul 2>&1
if errorlevel 1 (
    echo pyperclip 설치 중...
    pip install pyperclip
)

echo [완료] 패키지 확인 완료
echo.

REM Chrome 디버깅 모드 확인
echo [확인] Chrome 디버깅 모드 확인 중...
curl -s http://127.0.0.1:9222/json/version >nul 2>&1
if errorlevel 1 (
    echo.
    echo [경고] Chrome이 디버깅 모드로 실행되지 않았습니다!
    echo.
    echo 먼저 다음 명령으로 Chrome을 실행해야 합니다:
    echo.
    echo start_chrome_debug.bat
    echo.
    echo 또는 수동으로:
    echo chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chrome_dev_session"
    echo.
    pause
    exit /b 1
)

echo [확인] Chrome 디버깅 모드 실행 중
echo.

:MENU
echo ============================================================
echo 실행 모드 선택
echo ============================================================
echo.
echo 1. 테스트 모드 (1회만 실행, 수동 Enter)
echo 2. 연속 전송 모드 (자동 반복)
echo 3. 테스트 모드 (자동 전송 - 위험!)
echo 4. 종료
echo.
choice /C 1234 /N /M "선택하세요 (1-4): "

if errorlevel 4 goto END
if errorlevel 3 goto AUTO_TEST
if errorlevel 2 goto CONTINUOUS
if errorlevel 1 goto TEST

:TEST
echo.
echo [실행] 테스트 모드 실행 (수동 전송)
echo.
python src/safe_band_macro.py --test
goto MENU

:AUTO_TEST
echo.
echo [경고] 자동 전송 테스트 모드 (위험!)
echo.
set /P CONFIRM="정말 실행하시겠습니까? (y/N): "
if /I not "%CONFIRM%"=="y" goto MENU
echo.
python src/safe_band_macro.py --test --auto-send
goto MENU

:CONTINUOUS
echo.
echo [실행] 연속 전송 모드
echo.
set /P INTERVAL="전송 간격(분, 기본 5): "
if "%INTERVAL%"=="" set INTERVAL=5

set /P MAXSENDS="최대 전송 횟수(기본 20): "
if "%MAXSENDS%"=="" set MAXSENDS=20

set /P AUTOSEND="자동 전송? (y/N, 기본 N): "

echo.
echo [설정]
echo    - 간격: %INTERVAL%분
echo    - 최대: %MAXSENDS%회
echo    - 자동: %AUTOSEND%
echo.

if /I "%AUTOSEND%"=="y" (
    python src/safe_band_macro.py --interval %INTERVAL% --max-sends %MAXSENDS% --auto-send
) else (
    python src/safe_band_macro.py --interval %INTERVAL% --max-sends %MAXSENDS%
)
goto MENU

:END
echo.
echo 프로그램을 종료합니다.
echo.
pause
