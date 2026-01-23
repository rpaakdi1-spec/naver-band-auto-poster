@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion

echo ========================================
echo 네이버밴드 자동 포스팅 실행 파일 생성
echo ========================================
echo.

:: 관리자 권한 확인 (선택사항)
net session >nul 2>&1
if %errorLevel% == 0 (
    echo ✓ 관리자 권한으로 실행 중
) else (
    echo ℹ️  일반 권한으로 실행 중 (대부분의 경우 문제없음)
)
echo.

:: Python 버전 확인
echo [환경 체크]
echo ----------------------------------------
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python이 설치되어 있지 않습니다.
    echo.
    echo Python 3.8 이상을 설치하세요:
    echo https://www.python.org/downloads/
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo ✓ Python %PYTHON_VERSION% 감지됨
echo.

:: 필수 파일 확인
echo [필수 파일 체크]
echo ----------------------------------------
set "MISSING_FILES="

if not exist "run.py" (
    echo ❌ run.py 파일이 없습니다.
    set "MISSING_FILES=1"
) else (
    echo ✓ run.py 존재
)

if not exist "src\" (
    echo ❌ src 폴더가 없습니다.
    set "MISSING_FILES=1"
) else (
    echo ✓ src/ 폴더 존재
)

if not exist "config\" (
    echo ❌ config 폴더가 없습니다.
    set "MISSING_FILES=1"
) else (
    echo ✓ config/ 폴더 존재
)

if defined MISSING_FILES (
    echo.
    echo ❌ 필수 파일/폴더가 누락되었습니다.
    echo 프로젝트 루트 디렉토리에서 실행하세요.
    pause
    exit /b 1
)
echo.

:: PyInstaller 설치 확인
echo [PyInstaller 설치 확인]
echo ----------------------------------------
pip show pyinstaller > nul 2>&1
if errorlevel 1 (
    echo PyInstaller를 설치합니다...
    pip install pyinstaller
    if errorlevel 1 (
        echo.
        echo ❌ PyInstaller 설치 실패
        pause
        exit /b 1
    )
    echo ✓ PyInstaller 설치 완료
) else (
    echo ✓ PyInstaller가 이미 설치되어 있습니다.
)
echo.

:: 의존성 패키지 확인
echo [의존성 패키지 체크]
echo ----------------------------------------
set "MISSING_PACKAGES="

pip show selenium >nul 2>&1
if errorlevel 1 (
    echo ⚠️  selenium 미설치
    set "MISSING_PACKAGES=!MISSING_PACKAGES! selenium"
) else (
    echo ✓ selenium 설치됨
)

pip show webdriver-manager >nul 2>&1
if errorlevel 1 (
    echo ⚠️  webdriver-manager 미설치
    set "MISSING_PACKAGES=!MISSING_PACKAGES! webdriver-manager"
) else (
    echo ✓ webdriver-manager 설치됨
)

pip show schedule >nul 2>&1
if errorlevel 1 (
    echo ⚠️  schedule 미설치
    set "MISSING_PACKAGES=!MISSING_PACKAGES! schedule"
) else (
    echo ✓ schedule 설치됨
)

pip show pyperclip >nul 2>&1
if errorlevel 1 (
    echo ⚠️  pyperclip 미설치
    set "MISSING_PACKAGES=!MISSING_PACKAGES! pyperclip"
) else (
    echo ✓ pyperclip 설치됨
)

pip show pillow >nul 2>&1
if errorlevel 1 (
    echo ⚠️  pillow 미설치
    set "MISSING_PACKAGES=!MISSING_PACKAGES! pillow"
) else (
    echo ✓ pillow 설치됨
)

if defined MISSING_PACKAGES (
    echo.
    echo 누락된 패키지를 설치합니다...
    pip install%MISSING_PACKAGES%
    if errorlevel 1 (
        echo.
        echo ❌ 패키지 설치 실패
        pause
        exit /b 1
    )
    echo ✓ 누락된 패키지 설치 완료
)
echo.

:: 이전 빌드 정리
echo [이전 빌드 파일 정리]
echo ----------------------------------------
if exist build (
    rmdir /s /q build
    echo ✓ build/ 폴더 삭제
)
if exist dist (
    rmdir /s /q dist
    echo ✓ dist/ 폴더 삭제
)
if exist __pycache__ (
    rmdir /s /q __pycache__
    echo ✓ __pycache__/ 폴더 삭제
)
for %%f in (*.spec) do (
    del /q "%%f"
    echo ✓ %%f 삭제
)
echo ✓ 정리 완료
echo.

:: 실행 파일 생성
echo [실행 파일 생성 중...]
echo ----------------------------------------
echo 빌드 시작... (몇 분 소요될 수 있습니다)
echo.

pyinstaller --name="네이버밴드자동포스팅" ^
            --onefile ^
            --windowed ^
            --add-data="config;config" ^
            --add-data="src;src" ^
            --hidden-import=selenium ^
            --hidden-import=selenium.webdriver ^
            --hidden-import=selenium.webdriver.chrome ^
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
    echo ========================================
    echo ❌ 빌드 실패
    echo ========================================
    echo.
    echo 문제 해결:
    echo 1. EXE_BUILD_TROUBLESHOOTING.md 문서를 참고하세요
    echo 2. 오류 메시지를 GitHub Issues에 등록하세요
    echo    https://github.com/rpaakdi1-spec/naver-band-auto-poster/issues
    echo.
    pause
    exit /b 1
)

:: 빌드 검증
echo.
echo [빌드 결과 검증]
echo ----------------------------------------
if not exist "dist\" (
    echo ❌ dist 폴더가 생성되지 않았습니다.
    pause
    exit /b 1
)
echo ✓ dist 폴더 생성됨

if not exist "dist\네이버밴드자동포스팅.exe" (
    echo ❌ 실행 파일이 생성되지 않았습니다.
    echo.
    echo dist 폴더 내용:
    dir /b dist
    pause
    exit /b 1
)
echo ✓ 실행 파일 생성됨

:: 파일 크기 확인
for %%A in ("dist\네이버밴드자동포스팅.exe") do set FILE_SIZE=%%~zA
set /a FILE_SIZE_MB=FILE_SIZE/1024/1024
echo ✓ 파일 크기: %FILE_SIZE_MB% MB

if %FILE_SIZE_MB% LSS 10 (
    echo ⚠️  파일 크기가 너무 작습니다. 일부 의존성이 누락되었을 수 있습니다.
)
echo.

:: 완료 메시지
echo ========================================
echo ✅ 빌드 완료!
echo ========================================
echo.
echo 📁 생성된 파일 위치:
echo    dist\네이버밴드자동포스팅.exe
echo.
echo 📊 파일 정보:
echo    크기: %FILE_SIZE_MB% MB
echo    경로: %CD%\dist\네이버밴드자동포스팅.exe
echo.
echo 🚀 실행 방법:
echo    1. dist 폴더를 열고
echo    2. 네이버밴드자동포스팅.exe를 더블클릭
echo    3. GUI 창이 열리면 성공!
echo.
echo 📦 배포:
echo    - 실행 파일을 다른 컴퓨터에 복사하여 사용 가능
echo    - config 폴더는 자동으로 포함됨
echo    - 백신 오탐 시 ANTIVIRUS_FALSE_POSITIVE.md 참고
echo.
echo 💡 팁:
echo    - Windows Defender가 차단할 수 있습니다
echo    - 예외 항목에 추가하세요
echo    - 자세한 내용은 ANTIVIRUS_FALSE_POSITIVE.md 참고
echo.

:: 로그 생성
echo 빌드 로그 > build.log
echo ======================================== >> build.log
echo 날짜: %date% %time% >> build.log
echo Python 버전: %PYTHON_VERSION% >> build.log
echo 빌드 상태: 성공 >> build.log
echo 파일 크기: %FILE_SIZE_MB% MB >> build.log
echo ======================================== >> build.log
echo ✓ 빌드 로그 생성: build.log
echo.

:: dist 폴더 열기
echo dist 폴더를 여시겠습니까? (y/n)
set /p OPEN_FOLDER=
if /i "%OPEN_FOLDER%"=="y" (
    explorer dist
)

pause
