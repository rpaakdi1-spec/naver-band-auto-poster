"""
네이버밴드 자동 포스팅 웹 버전 실행
"""

import sys
import subprocess

def main():
    print("=" * 60)
    print("네이버밴드 자동 포스팅 웹 버전 실행")
    print("=" * 60)
    print()
    
    # Streamlit 설치 확인
    try:
        import streamlit
        print("✅ Streamlit이 이미 설치되어 있습니다.")
    except ImportError:
        print("📦 Streamlit을 설치합니다...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "streamlit==1.31.0"])
        print("✅ Streamlit 설치 완료")
    
    print()
    print("=" * 60)
    print("✓ 웹 서버 시작 중...")
    print("=" * 60)
    print()
    print("브라우저 주소: http://localhost:8501")
    print()
    print("종료하려면 Ctrl+C를 누르세요.")
    print()
    
    # Streamlit 실행
    subprocess.call([sys.executable, "-m", "streamlit", "run", "streamlit_app.py"])

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n프로그램을 종료합니다.")
        sys.exit(0)
    except Exception as e:
        print(f"\n오류 발생: {e}")
        sys.exit(1)
