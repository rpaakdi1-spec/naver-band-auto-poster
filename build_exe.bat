@echo off
chcp 65001 >nul
echo ================================================
echo 네이버밴드 자동 포스팅 프로그램 - EXE 빌드
echo ================================================
echo.
echo Python이 설치되어 있어야 합니다.
echo 빌드 후에는 EXE 파일만으로 실행 가능합니다.
echo.
pause

echo.
echo [1/3] 필요한 패키지 설치 중...
pip install -r requirements.txt
pip install pyinstaller

echo.
echo [2/3] EXE 파일 생성 중... (5-10분 소요)
pyinstaller --clean --noconfirm build_exe.spec

echo.
echo [3/3] 완료!
echo.
echo ================================================
echo 실행 파일 위치:
echo   dist\네이버밴드_자동포스팅.exe
echo ================================================
echo.
echo 이제 "dist" 폴더의 EXE 파일을 바탕화면으로
echo 복사해서 사용하세요!
echo.
pause
