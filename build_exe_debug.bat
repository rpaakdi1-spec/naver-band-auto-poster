@echo off
chcp 65001 > nul
echo ========================================
echo 네이버밴드 자동 포스팅 - 디버그 빌드
echo ========================================
echo.
echo 이 버전은 콘솔 창과 함께 실행되어
echo 오류 메시지를 확인할 수 있습니다.
echo.

echo [1/3] PyInstaller 설치 확인...
pip show pyinstaller > nul 2>&1
if errorlevel 1 (
    echo PyInstaller 설치 중...
    pip install pyinstaller==6.3.0
)
echo.

echo [2/3] 이전 빌드 정리...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist *.spec del /q *.spec
echo.

echo [3/3] 디버그 빌드 실행 중...
echo.
pyinstaller --name="BandAutoPoster" ^
            --onefile ^
            --add-data="config;config" ^
            --hidden-import=selenium ^
            --hidden-import=webdriver_manager ^
            --hidden-import=schedule ^
            --hidden-import=pyperclip ^
            --collect-all=selenium ^
            --collect-all=webdriver_manager ^
            --noconfirm ^
            --clean ^
            run.py

if errorlevel 1 (
    echo.
    echo ❌ 빌드 실패!
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo ✓ 디버그 빌드 완료!
echo ========================================
echo.
echo 생성된 파일: dist\BandAutoPoster.exe
echo.
echo 이 파일을 실행하면 콘솔 창이 함께 열립니다.
echo 오류가 발생하면 콘솔 창에서 메시지를 확인할 수 있습니다.
echo.
pause
