@echo off
chcp 65001 > nul

echo ========================================
echo 네이버밴드 자동 포스팅 - 간단 빌드
echo ========================================
echo.

:: 필수 확인
if not exist "run.py" (
    echo ❌ run.py가 없습니다. 프로젝트 폴더에서 실행하세요.
    pause
    exit /b 1
)

:: 이전 빌드 정리
echo [1/3] 정리 중...
if exist build rmdir /s /q build 2>nul
if exist dist rmdir /s /q dist 2>nul
del *.spec 2>nul
echo ✅ 정리 완료
echo.

:: 빌드
echo [2/3] 빌드 중... (3~5분 소요)
echo.
pyinstaller --name="BandAutoPoster" --onefile --windowed --add-data="config;config" --add-data="src;src" --hidden-import=selenium --hidden-import=webdriver_manager --hidden-import=schedule --hidden-import=pyperclip --hidden-import=tkinter --collect-all=selenium --collect-all=webdriver_manager --noconfirm --clean run.py

if errorlevel 1 (
    echo.
    echo ❌ 빌드 실패!
    echo.
    echo 해결 방법:
    echo 1. pip install pyinstaller selenium webdriver-manager schedule pyperclip pillow
    echo 2. Python 3.8~3.11 사용 권장
    echo 3. EXE_BUILD_TROUBLESHOOTING.md 참고
    echo.
    pause
    exit /b 1
)
echo.

:: 검증
echo [3/3] 검증 중...
if not exist "dist\BandAutoPoster.exe" (
    echo ❌ .exe 파일이 생성되지 않았습니다.
    pause
    exit /b 1
)

:: 한글 이름 복사
copy "dist\BandAutoPoster.exe" "dist\네이버밴드자동포스팅.exe" >nul 2>&1

echo.
echo ========================================
echo ✅ 빌드 완료!
echo ========================================
echo.
echo 📁 dist\BandAutoPoster.exe
if exist "dist\네이버밴드자동포스팅.exe" (
    echo 📁 dist\네이버밴드자동포스팅.exe
)
echo.
echo 💡 실행: dist 폴더의 .exe 파일을 더블클릭
echo.
pause
