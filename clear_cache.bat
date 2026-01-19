@echo off
chcp 65001 > nul
echo ========================================
echo WebDriver 캐시 정리 도구
echo ========================================
echo.
echo ChromeDriver 캐시를 삭제합니다.
echo.
pause
echo.

set CACHE_DIR=%USERPROFILE%\.wdm

if exist "%CACHE_DIR%" (
    echo 캐시 폴더 발견: %CACHE_DIR%
    echo 삭제 중...
    rd /s /q "%CACHE_DIR%"
    echo.
    echo ✓ 캐시 삭제 완료!
    echo.
    echo 프로그램을 다시 실행하면 ChromeDriver가
    echo 자동으로 다운로드됩니다.
) else (
    echo 캐시 폴더를 찾을 수 없습니다.
    echo 이미 정리되었거나 다른 경로에 있을 수 있습니다.
)

echo.
echo ========================================
pause
