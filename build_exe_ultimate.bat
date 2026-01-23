@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion

:: ============================================
:: 네이버밴드 자동 포스팅 - 실행 파일 빌드
:: ============================================

echo.
echo ╔════════════════════════════════════════╗
echo ║  네이버밴드 자동 포스팅 빌드 시작     ║
echo ╚════════════════════════════════════════╝
echo.

:: ============================================
:: Step 1: 환경 체크
:: ============================================
echo [1/8] 환경 체크
echo ----------------------------------------

:: Python 설치 확인
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python이 설치되어 있지 않습니다.
    echo.
    echo 💡 해결 방법:
    echo    Python 3.8~3.11 다운로드:
    echo    https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

:: Python 버전 확인
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo ✅ Python %PYTHON_VERSION% 감지됨

:: 현재 디렉토리 표시
echo ✅ 현재 위치: %CD%
echo.

:: ============================================
:: Step 2: 필수 파일 체크
:: ============================================
echo [2/8] 필수 파일 체크
echo ----------------------------------------
set "MISSING_FILES=0"

if not exist "run.py" (
    echo ❌ run.py 파일이 없습니다.
    set "MISSING_FILES=1"
) else (
    echo ✅ run.py 존재
)

if not exist "src\" (
    echo ❌ src 폴더가 없습니다.
    set "MISSING_FILES=1"
) else (
    echo ✅ src/ 폴더 존재
)

if not exist "config\" (
    echo ❌ config 폴더가 없습니다.
    set "MISSING_FILES=1"
) else (
    echo ✅ config/ 폴더 존재
)

if "%MISSING_FILES%"=="1" (
    echo.
    echo ❌ 필수 파일/폴더가 누락되었습니다.
    echo.
    echo 💡 해결 방법:
    echo    프로젝트 루트 디렉토리에서 실행하세요.
    echo    예: cd C:\path\to\naver-band-auto-poster
    echo.
    pause
    exit /b 1
)
echo.

:: ============================================
:: Step 3: PyInstaller 설치 확인
:: ============================================
echo [3/8] PyInstaller 설치 확인
echo ----------------------------------------
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo ⚠️  PyInstaller가 설치되어 있지 않습니다.
    echo 📦 PyInstaller를 설치합니다...
    pip install pyinstaller
    if errorlevel 1 (
        echo.
        echo ❌ PyInstaller 설치 실패
        echo.
        echo 💡 해결 방법:
        echo    pip install --upgrade pip
        echo    pip install pyinstaller
        echo.
        pause
        exit /b 1
    )
    echo ✅ PyInstaller 설치 완료
) else (
    for /f "tokens=2" %%v in ('pip show pyinstaller ^| findstr "Version:"') do set PYINSTALLER_VERSION=%%v
    echo ✅ PyInstaller !PYINSTALLER_VERSION! 이미 설치됨
)
echo.

:: ============================================
:: Step 4: 의존성 패키지 체크
:: ============================================
echo [4/8] 의존성 패키지 체크
echo ----------------------------------------
set "MISSING_PACKAGES="

pip show selenium >nul 2>&1
if errorlevel 1 (
    echo ⚠️  selenium 미설치
    set "MISSING_PACKAGES=!MISSING_PACKAGES! selenium"
) else (
    echo ✅ selenium 설치됨
)

pip show webdriver-manager >nul 2>&1
if errorlevel 1 (
    echo ⚠️  webdriver-manager 미설치
    set "MISSING_PACKAGES=!MISSING_PACKAGES! webdriver-manager"
) else (
    echo ✅ webdriver-manager 설치됨
)

pip show schedule >nul 2>&1
if errorlevel 1 (
    echo ⚠️  schedule 미설치
    set "MISSING_PACKAGES=!MISSING_PACKAGES! schedule"
) else (
    echo ✅ schedule 설치됨
)

pip show pyperclip >nul 2>&1
if errorlevel 1 (
    echo ⚠️  pyperclip 미설치
    set "MISSING_PACKAGES=!MISSING_PACKAGES! pyperclip"
) else (
    echo ✅ pyperclip 설치됨
)

pip show pillow >nul 2>&1
if errorlevel 1 (
    echo ⚠️  pillow 미설치
    set "MISSING_PACKAGES=!MISSING_PACKAGES! pillow"
) else (
    echo ✅ pillow 설치됨
)

if defined MISSING_PACKAGES (
    echo.
    echo 📦 누락된 패키지를 설치합니다...
    pip install%MISSING_PACKAGES%
    if errorlevel 1 (
        echo.
        echo ❌ 패키지 설치 실패
        echo.
        echo 💡 해결 방법:
        echo    pip install --upgrade pip
        echo    pip install selenium webdriver-manager schedule pyperclip pillow
        echo.
        pause
        exit /b 1
    )
    echo ✅ 누락된 패키지 설치 완료
)
echo.

:: ============================================
:: Step 5: 이전 빌드 정리
:: ============================================
echo [5/8] 이전 빌드 파일 정리
echo ----------------------------------------
set "CLEANED=0"

if exist build (
    rmdir /s /q build 2>nul
    echo ✅ build/ 폴더 삭제
    set "CLEANED=1"
)

if exist dist (
    rmdir /s /q dist 2>nul
    echo ✅ dist/ 폴더 삭제
    set "CLEANED=1"
)

if exist __pycache__ (
    rmdir /s /q __pycache__ 2>nul
    echo ✅ __pycache__/ 폴더 삭제
    set "CLEANED=1"
)

for %%f in (*.spec) do (
    del /q "%%f" 2>nul
    echo ✅ %%f 삭제
    set "CLEANED=1"
)

if "%CLEANED%"=="0" (
    echo ✅ 정리할 파일 없음 (깨끗한 상태)
)
echo.

:: ============================================
:: Step 6: PyInstaller 빌드 실행
:: ============================================
echo [6/8] 실행 파일 생성 중
echo ----------------------------------------
echo ⏳ 빌드 시작... (3~5분 소요될 수 있습니다)
echo    잠시만 기다려주세요...
echo.

:: 영문 이름으로 먼저 빌드 (한글 이름 문제 회피)
pyinstaller --name="BandAutoPoster" ^
            --onefile ^
            --windowed ^
            --add-data="config;config" ^
            --add-data="src;src" ^
            --hidden-import=selenium ^
            --hidden-import=selenium.webdriver ^
            --hidden-import=selenium.webdriver.chrome ^
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
            --hidden-import=tkinter.ttk ^
            --hidden-import=PIL ^
            --hidden-import=PIL.Image ^
            --hidden-import=PIL.ImageTk ^
            --collect-all=selenium ^
            --collect-all=webdriver_manager ^
            --noconfirm ^
            --clean ^
            run.py

if errorlevel 1 (
    echo.
    echo ════════════════════════════════════════
    echo ❌ 빌드 실패!
    echo ════════════════════════════════════════
    echo.
    echo 💡 문제 해결:
    echo.
    echo 1. Python 버전 확인:
    echo    python --version
    echo    ^(Python 3.8~3.11 권장^)
    echo.
    echo 2. 패키지 재설치:
    echo    pip install --upgrade pyinstaller
    echo    pip install --upgrade selenium webdriver-manager schedule pyperclip pillow
    echo.
    echo 3. 상세 가이드:
    echo    EXE_BUILD_TROUBLESHOOTING.md 파일 참고
    echo.
    echo 4. GitHub Issues:
    echo    https://github.com/rpaakdi1-spec/naver-band-auto-poster/issues
    echo.
    pause
    exit /b 1
)

echo ✅ PyInstaller 빌드 완료
echo.

:: ============================================
:: Step 7: 빌드 결과 검증
:: ============================================
echo [7/8] 빌드 결과 검증
echo ----------------------------------------

:: dist 폴더 확인
if not exist "dist\" (
    echo ❌ dist 폴더가 생성되지 않았습니다.
    echo.
    echo 💡 문제 해결:
    echo    위의 오류 메시지를 확인하고
    echo    EXE_BUILD_TROUBLESHOOTING.md 파일을 참고하세요.
    echo.
    pause
    exit /b 1
)
echo ✅ dist/ 폴더 생성됨

:: .exe 파일 확인
if not exist "dist\BandAutoPoster.exe" (
    echo ❌ 실행 파일이 생성되지 않았습니다.
    echo.
    echo 📁 dist 폴더 내용:
    dir /b dist
    echo.
    echo 💡 문제 해결:
    echo    EXE_BUILD_TROUBLESHOOTING.md 파일을 참고하세요.
    echo.
    pause
    exit /b 1
)
echo ✅ BandAutoPoster.exe 생성됨

:: 파일 크기 확인
for %%A in ("dist\BandAutoPoster.exe") do set FILE_SIZE=%%~zA
set /a FILE_SIZE_MB=FILE_SIZE/1024/1024
echo ✅ 파일 크기: %FILE_SIZE_MB% MB

if %FILE_SIZE_MB% LSS 10 (
    echo ⚠️  파일 크기가 작습니다 (의존성 누락 가능성)
) else if %FILE_SIZE_MB% LSS 50 (
    echo ✅ 파일 크기 정상 범위
) else if %FILE_SIZE_MB% LSS 150 (
    echo ✅ 파일 크기 정상 범위
) else (
    echo ⚠️  파일 크기가 큽니다 (정상 작동하지만 최적화 가능)
)

:: 한글 이름으로 복사
echo.
echo 📝 한글 이름으로 복사 중...
copy "dist\BandAutoPoster.exe" "dist\네이버밴드자동포스팅.exe" >nul 2>&1
if errorlevel 1 (
    echo ⚠️  한글 이름 복사 실패 (BandAutoPoster.exe를 사용하세요)
) else (
    echo ✅ 네이버밴드자동포스팅.exe 생성됨
)
echo.

:: ============================================
:: Step 8: 빌드 완료 및 정보 표시
:: ============================================
echo [8/8] 빌드 완료!
echo ----------------------------------------
echo.
echo ╔════════════════════════════════════════╗
echo ║         ✅ 빌드 성공!                  ║
echo ╚════════════════════════════════════════╝
echo.
echo 📁 생성된 파일:
echo    dist\BandAutoPoster.exe
if exist "dist\네이버밴드자동포스팅.exe" (
    echo    dist\네이버밴드자동포스팅.exe
)
echo.
echo 📊 파일 정보:
echo    크기: %FILE_SIZE_MB% MB
echo    위치: %CD%\dist\
echo.
echo 🚀 실행 방법:
echo    1. dist 폴더 열기
echo    2. BandAutoPoster.exe 더블클릭
echo    3. GUI 창이 열리면 성공!
echo.
echo 📦 배포:
echo    ✅ 다른 컴퓨터에 복사하여 사용 가능
echo    ✅ Python 설치 불필요
echo    ✅ config 폴더 자동 포함
echo.
echo 💡 주의사항:
echo    ⚠️  Windows Defender가 차단할 수 있습니다
echo    ⚠️  백신 프로그램에서 오탐 가능
echo.
echo    해결 방법:
echo    1. Windows 보안 → 바이러스 및 위협 방지
echo    2. 제외 항목 추가 → 파일 추가
echo    3. BandAutoPoster.exe 선택
echo.
echo    자세한 내용: ANTIVIRUS_FALSE_POSITIVE.md
echo.

:: 로그 생성
echo ════════ 빌드 로그 ════════ > build.log
echo 날짜: %date% %time% >> build.log
echo Python 버전: %PYTHON_VERSION% >> build.log
if defined PYINSTALLER_VERSION (
    echo PyInstaller 버전: !PYINSTALLER_VERSION! >> build.log
)
echo 빌드 상태: 성공 >> build.log
echo 파일 크기: %FILE_SIZE_MB% MB >> build.log
echo 파일 위치: %CD%\dist\BandAutoPoster.exe >> build.log
echo ═══════════════════════════ >> build.log
echo ✅ 빌드 로그 저장: build.log
echo.

:: dist 폴더 열기 제안
set /p OPEN_FOLDER="📂 dist 폴더를 여시겠습니까? (y/n): "
if /i "%OPEN_FOLDER%"=="y" (
    explorer dist
    echo ✅ dist 폴더를 열었습니다.
) else if /i "%OPEN_FOLDER%"=="yes" (
    explorer dist
    echo ✅ dist 폴더를 열었습니다.
) else (
    echo 💡 수동으로 dist 폴더를 열어서 .exe 파일을 확인하세요.
)

echo.
echo ════════════════════════════════════════
echo 빌드가 완료되었습니다!
echo 문제가 있으면 build.log를 확인하세요.
echo ════════════════════════════════════════
echo.
pause
