"""
ChromeDriver 경로 테스트 스크립트
"""

import os
import glob
from webdriver_manager.chrome import ChromeDriverManager

print("ChromeDriver 다운로드 중...")
driver_path = ChromeDriverManager().install()

print(f"\n반환된 경로: {driver_path}")
print(f"파일 존재 여부: {os.path.exists(driver_path)}")
print(f"파일 이름: {os.path.basename(driver_path)}")

if not driver_path.endswith('.exe'):
    print("\n올바른 .exe 파일이 아닙니다. chromedriver.exe를 찾는 중...")
    
    # 같은 디렉토리에서 찾기
    driver_dir = os.path.dirname(driver_path)
    print(f"검색 디렉토리: {driver_dir}")
    
    exe_files = glob.glob(os.path.join(driver_dir, '**', 'chromedriver.exe'), recursive=True)
    
    if exe_files:
        print(f"\n찾은 chromedriver.exe 파일:")
        for exe in exe_files:
            print(f"  - {exe}")
        print(f"\n사용할 경로: {exe_files[0]}")
    else:
        # 상위 디렉토리에서 찾기
        parent_dir = os.path.dirname(driver_dir)
        print(f"\n상위 디렉토리 검색: {parent_dir}")
        
        exe_files = glob.glob(os.path.join(parent_dir, '**', 'chromedriver.exe'), recursive=True)
        
        if exe_files:
            print(f"\n찾은 chromedriver.exe 파일:")
            for exe in exe_files:
                print(f"  - {exe}")
            print(f"\n사용할 경로: {exe_files[0]}")
        else:
            print("\nchromedriver.exe를 찾을 수 없습니다!")
else:
    print("\n올바른 chromedriver.exe 경로입니다!")

print("\n완료!")
