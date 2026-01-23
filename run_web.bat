@echo off
chcp 65001 > nul
echo ========================================
echo 네이버밴드 자동 포스팅 웹 버전 실행
echo ========================================
echo.

echo [1/2] Streamlit 설치 확인 중...
pip show streamlit > nul 2>&1
if errorlevel 1 (
    echo Streamlit을 설치합니다...
    pip install streamlit==1.31.0
) else (
    echo ✓ Streamlit이 이미 설치되어 있습니다.
)
echo.

echo [2/2] 웹 서버 시작 중...
echo.
echo ========================================
echo ✓ 웹 브라우저가 자동으로 열립니다!
echo ========================================
echo.
echo 브라우저 주소: http://localhost:8501
echo.
echo 종료하려면 이 창에서 Ctrl+C를 누르세요.
echo.

streamlit run streamlit_app.py
