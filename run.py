#!/usr/bin/env python3
"""
네이버밴드 자동 포스팅 프로그램 실행 스크립트
"""

import sys
import os

# 현재 디렉토리를 Python 경로에 추가
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.gui import main

if __name__ == "__main__":
    main()
