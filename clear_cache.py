#!/usr/bin/env python3
"""
WebDriver Manager 캐시 정리 스크립트

ChromeDriver 캐시 문제를 해결하기 위한 유틸리티
"""

import os
import shutil
import sys


def clear_webdriver_cache():
    """WebDriver Manager 캐시 삭제"""
    
    # 캐시 경로들
    cache_paths = [
        os.path.expanduser("~/.wdm"),  # Linux/Mac
        os.path.expanduser("~/AppData/Local/Temp/wdm"),  # Windows alternative
    ]
    
    # Windows 사용자별 경로
    if sys.platform == 'win32':
        username = os.environ.get('USERNAME', '')
        if username:
            cache_paths.append(f"C:\\Users\\{username}\\.wdm")
    
    deleted = False
    
    for cache_path in cache_paths:
        if os.path.exists(cache_path):
            try:
                print(f"캐시 삭제 중: {cache_path}")
                shutil.rmtree(cache_path)
                print(f"✓ 캐시 삭제 완료: {cache_path}")
                deleted = True
            except PermissionError:
                print(f"✗ 권한 오류: {cache_path}")
                print("  → 관리자 권한으로 다시 실행하세요.")
            except Exception as e:
                print(f"✗ 삭제 실패: {cache_path}")
                print(f"  → 오류: {str(e)}")
    
    if not deleted:
        print("\n캐시 폴더를 찾을 수 없습니다.")
        print("이미 정리되었거나 다른 경로에 있을 수 있습니다.")
    else:
        print("\n✓ 캐시 정리 완료!")
        print("프로그램을 다시 실행하면 ChromeDriver가 자동으로 다운로드됩니다.")


def show_cache_info():
    """캐시 정보 표시"""
    print("=" * 60)
    print("WebDriver Manager 캐시 정리 도구")
    print("=" * 60)
    print()
    print("이 도구는 ChromeDriver 캐시를 삭제합니다.")
    print()
    print("문제 상황:")
    print("  - [WinError 193] Win32 응용 프로그램 오류")
    print("  - ChromeDriver 실행 실패")
    print("  - THIRD_PARTY_NOTICES 오류")
    print()
    print("해결 방법:")
    print("  1. 이 스크립트 실행으로 캐시 삭제")
    print("  2. 프로그램 재실행으로 자동 재다운로드")
    print()
    print("-" * 60)
    print()


def main():
    """메인 함수"""
    show_cache_info()
    
    # 사용자 확인
    response = input("캐시를 삭제하시겠습니까? (y/n): ").strip().lower()
    
    if response in ['y', 'yes', '예', 'ㅇ']:
        print()
        clear_webdriver_cache()
    else:
        print("\n취소되었습니다.")
    
    print()
    input("엔터를 눌러 종료...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n중단되었습니다.")
    except Exception as e:
        print(f"\n오류 발생: {str(e)}")
        input("엔터를 눌러 종료...")
