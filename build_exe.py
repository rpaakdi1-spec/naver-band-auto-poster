"""
네이버밴드 자동 포스팅 실행 파일 빌드 스크립트
PyInstaller를 사용하여 .exe 파일을 생성합니다.
"""

import os
import sys
import shutil
import subprocess

def main():
    print("=" * 60)
    print("네이버밴드 자동 포스팅 실행 파일 빌드 시작")
    print("=" * 60)
    
    # PyInstaller 설치 확인
    try:
        import PyInstaller
        print("✅ PyInstaller가 이미 설치되어 있습니다.")
    except ImportError:
        print("📦 PyInstaller를 설치합니다...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✅ PyInstaller 설치 완료")
    
    # 이전 빌드 정리
    print("\n🧹 이전 빌드 파일 정리 중...")
    for folder in ['build', 'dist', '__pycache__']:
        if os.path.exists(folder):
            shutil.rmtree(folder)
            print(f"   삭제: {folder}/")
    
    spec_files = [f for f in os.listdir('.') if f.endswith('.spec')]
    for spec_file in spec_files:
        os.remove(spec_file)
        print(f"   삭제: {spec_file}")
    
    print("✅ 정리 완료\n")
    
    # PyInstaller 명령 실행
    print("🔨 실행 파일 생성 중...\n")
    
    pyinstaller_args = [
        'run.py',
        '--name=네이버밴드자동포스팅',
        '--onefile',
        '--windowed',
        '--icon=NONE',
        '--add-data=config:config',
        '--hidden-import=selenium',
        '--hidden-import=webdriver_manager',
        '--hidden-import=schedule',
        '--hidden-import=pyperclip',
        '--hidden-import=tkinter',
        '--hidden-import=PIL',
        '--collect-all=selenium',
        '--collect-all=webdriver_manager',
        '--noconfirm',
        '--clean',
    ]
    
    try:
        subprocess.check_call(['pyinstaller'] + pyinstaller_args)
        print("\n✅ 실행 파일 생성 완료!")
        print("\n📁 생성된 파일 위치:")
        print(f"   dist/네이버밴드자동포스팅.exe")
        print("\n" + "=" * 60)
        print("빌드 완료! dist/ 폴더에서 .exe 파일을 확인하세요.")
        print("=" * 60)
        return 0
    except subprocess.CalledProcessError as e:
        print(f"\n❌ 오류 발생: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
