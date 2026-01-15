@echo off
chcp 65001 > nul
echo ========================================
echo 네이버밴드 자동포스팅 - 긴급 수정
echo ========================================
echo.
echo ChromeDriver 캐시 문제를 해결합니다.
echo.
echo [1단계] 캐시 삭제 중...
echo.

set CACHE_DIR=%USERPROFILE%\.wdm

if exist "%CACHE_DIR%" (
    echo 발견: %CACHE_DIR%
    rd /s /q "%CACHE_DIR%"
    echo ✓ 캐시 삭제 완료!
) else (
    echo ! 캐시 폴더가 없습니다. (이미 정리됨)
)

echo.
echo [2단계] 프로그램 재시작...
echo.
echo 3초 후 프로그램이 자동으로 실행됩니다...
timeout /t 3 /nobreak > nul

echo.
echo ========================================
echo 프로그램 시작
echo ========================================
echo.

python run.py

if errorlevel 1 (
    echo.
    echo ========================================
    echo 오류가 발생했습니다!
    echo ========================================
    echo.
    echo 해결 방법:
    echo 1. Python이 설치되어 있는지 확인
    echo 2. 다음 명령어 실행: pip install -r requirements.txt
    echo 3. Chrome 브라우저가 설치되어 있는지 확인
    echo.
)

pause
