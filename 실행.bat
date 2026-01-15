@echo off
chcp 65001 >nul
title 네이버밴드 자동 포스팅 프로그램

echo ================================================
echo 네이버밴드 자동 포스팅 프로그램 v1.0
echo ================================================
echo.

REM Python 설치 확인
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python이 설치되어 있지 않습니다!
    echo.
    echo Python 다운로드: https://www.python.org/downloads/
    echo.
    echo ⚠️ 설치 시 "Add Python to PATH" 체크 필수!
    echo.
    pause
    exit /b 1
)

echo ✓ Python 설치 확인 완료
echo.

REM 첫 실행 시 패키지 설치
if not exist "venv" (
    echo [최초 실행] 필요한 패키지 설치 중...
    echo 이 작업은 처음 한 번만 수행됩니다. (1-2분 소요)
    echo.
    pip install -r requirements.txt
    if errorlevel 1 (
        echo.
        echo ❌ 패키지 설치 실패
        pause
        exit /b 1
    )
    echo.
    echo ✓ 패키지 설치 완료!
    echo.
)

echo 프로그램 시작 중...
echo.
python run.py

if errorlevel 1 (
    echo.
    echo ❌ 프로그램 실행 중 오류 발생
    pause
)
