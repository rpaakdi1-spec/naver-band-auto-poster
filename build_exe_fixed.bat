@echo off
chcp 65001 > nul
echo ========================================
echo 네이버밴드 자동 포스팅 실행 파일 생성
echo ========================================
echo.

echo [1/4] PyInstaller 설치 확인 중...
pip show pyinstaller > nul 2>&1
if errorlevel 1 (
    echo PyInstaller를 설치합니다...
    pip install pyinstaller==6.3.0
) else (
    echo ✓ PyInstaller가 이미 설치되어 있습니다.
)
echo.

echo [2/4] 이전 빌드 파일 정리 중...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist *.spec del /q *.spec
echo ✓ 정리 완료
echo.

echo [3/4] 실행 파일 생성 중 (영문 이름)...
echo 이 과정은 몇 분 정도 걸릴 수 있습니다...
echo.
pyinstaller --name="BandAutoPoster" ^
            --onefile ^
            --windowed ^
            --add-data="config;config" ^
            --hidden-import=selenium ^
            --hidden-import=selenium.webdriver ^
            --hidden-import=selenium.webdriver.chrome.service ^
            --hidden-import=selenium.webdriver.common.by ^
            --hidden-import=selenium.webdriver.common.keys ^
            --hidden-import=selenium.webdriver.support.ui ^
            --hidden-import=selenium.webdriver.support.expected_conditions ^
            --hidden-import=webdriver_manager ^
            --hidden-import=webdriver_manager.chrome ^
            --hidden-import=schedule ^
            --hidden-import=pyperclip ^
            --hidden-import=tkinter ^
            --collect-all=selenium ^
            --collect-all=webdriver_manager ^
            --noconfirm ^
            --clean ^
            run.py

if errorlevel 1 (
    echo.
    echo ========================================
    echo ❌ 빌드 실패
    echo ========================================
    echo.
    echo 오류가 발생했습니다. 위의 오류 메시지를 확인하세요.
    echo.
    echo 일반적인 해결 방법:
    echo 1. pip install --upgrade pyinstaller
    echo 2. pip install --upgrade -r requirements.txt
    echo 3. Python 버전 확인 (3.8 이상 권장)
    echo.
    pause
    exit /b 1
)

echo.
echo [4/4] 한글 이름으로 복사 중...
if exist "dist\BandAutoPoster.exe" (
    copy "dist\BandAutoPoster.exe" "dist\네이버밴드자동포스팅.exe" > nul
    echo ✓ 한글 이름으로 복사 완료
)

echo.
echo ========================================
echo ✓ 빌드 완료!
echo ========================================
echo.
echo 생성된 파일:
if exist "dist\BandAutoPoster.exe" (
    dir "dist\*.exe" | findstr ".exe"
)
echo.
echo dist 폴더에서 .exe 파일을 확인하세요.
echo 이 파일을 다른 컴퓨터에 복사하여 사용할 수 있습니다.
echo.
pause
