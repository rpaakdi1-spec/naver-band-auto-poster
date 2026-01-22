"""
네이버밴드 자동 포스팅 프로그램 실행
"""

import sys
from src.gui import main

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"오류 발생: {e}")
        sys.exit(1)
