@echo off
chcp 65001 > nul
echo ========================================
echo 네이버밴드 자동 포스팅 실행 파일 생성
echo ========================================
echo.

echo [1/3] PyInstaller 설치 확인 중...
pip show pyinstaller > nul 2>&1
if errorlevel 1 (
    echo PyInstaller를 설치합니다...
    pip install pyinstaller
) else (
    echo ✓ PyInstaller가 이미 설치되어 있습니다.
)
echo.

echo [2/3] 이전 빌드 파일 정리 중...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist *.spec del /q *.spec
echo ✓ 정리 완료
echo.

echo [3/3] 실행 파일 생성 중...
pyinstaller --name="네이버밴드자동포스팅" ^
            --onefile ^
            --windowed ^
            --add-data="config;config" ^
            --hidden-import=selenium ^
            --hidden-import=webdriver_manager ^
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
    echo ❌ 빌드 실패
    pause
    exit /b 1
)

echo.
echo ========================================
echo ✓ 빌드 완료!
echo ========================================
echo.
echo 생성된 파일: dist\네이버밴드자동포스팅.exe
echo.
echo dist 폴더에서 .exe 파일을 확인하세요.
echo 이 파일을 다른 컴퓨터에 복사하여 사용할 수 있습니다.
echo.
pause
