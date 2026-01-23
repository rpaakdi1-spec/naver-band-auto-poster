"""
네이버밴드 자동 포스팅 실행 파일 빌드 스크립트 (개선 버전)
PyInstaller를 사용하여 .exe 파일을 생성합니다.

특징:
- 자동 의존성 체크
- 상세한 오류 메시지
- 빌드 전/후 검증
- 로그 파일 생성
"""

import os
import sys
import shutil
import subprocess
import platform
from datetime import datetime

# 색상 출력 (Windows에서도 작동)
try:
    from colorama import init, Fore, Style
    init()
    GREEN = Fore.GREEN
    RED = Fore.RED
    YELLOW = Fore.YELLOW
    BLUE = Fore.BLUE
    RESET = Style.RESET_ALL
except ImportError:
    GREEN = RED = YELLOW = BLUE = RESET = ""

def print_header(text):
    """헤더 출력"""
    print("\n" + "=" * 70)
    print(f"{BLUE}{text}{RESET}")
    print("=" * 70)

def print_success(text):
    """성공 메시지"""
    print(f"{GREEN}✅ {text}{RESET}")

def print_error(text):
    """오류 메시지"""
    print(f"{RED}❌ {text}{RESET}")

def print_warning(text):
    """경고 메시지"""
    print(f"{YELLOW}⚠️  {text}{RESET}")

def print_info(text):
    """정보 메시지"""
    print(f"ℹ️  {text}")

def check_environment():
    """환경 체크"""
    print_header("환경 체크")
    
    # OS 확인
    os_name = platform.system()
    print_info(f"운영체제: {os_name}")
    
    if os_name != "Windows":
        print_warning(f"현재 OS는 {os_name}입니다.")
        print_warning("Windows용 .exe 파일은 Windows에서만 빌드할 수 있습니다.")
        print_info("계속 진행하면 현재 OS용 실행 파일이 생성됩니다.")
        response = input("\n계속하시겠습니까? (y/n): ")
        if response.lower() != 'y':
            print_error("빌드 취소됨")
            return False
    
    # Python 버전 확인
    python_version = sys.version_info
    print_info(f"Python 버전: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
        print_error("Python 3.8 이상이 필요합니다.")
        return False
    
    if python_version.major == 3 and python_version.minor >= 12:
        print_warning("Python 3.12+는 일부 패키지와 호환성 문제가 있을 수 있습니다.")
    
    print_success("환경 체크 완료")
    return True

def check_required_files():
    """필수 파일 체크"""
    print_header("필수 파일 체크")
    
    required_files = ['run.py']
    required_dirs = ['src', 'config']
    
    all_exists = True
    
    # 파일 체크
    for file in required_files:
        if os.path.exists(file):
            print_success(f"파일 존재: {file}")
        else:
            print_error(f"파일 없음: {file}")
            all_exists = False
    
    # 디렉토리 체크
    for directory in required_dirs:
        if os.path.isdir(directory):
            print_success(f"디렉토리 존재: {directory}/")
        else:
            print_error(f"디렉토리 없음: {directory}/")
            all_exists = False
    
    if not all_exists:
        print_error("필수 파일/디렉토리가 누락되었습니다.")
        return False
    
    print_success("필수 파일 체크 완료")
    return True

def install_pyinstaller():
    """PyInstaller 설치"""
    print_header("PyInstaller 설치 확인")
    
    try:
        import PyInstaller
        version = PyInstaller.__version__
        print_success(f"PyInstaller {version} 이미 설치됨")
        return True
    except ImportError:
        print_info("PyInstaller를 설치합니다...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
            print_success("PyInstaller 설치 완료")
            return True
        except subprocess.CalledProcessError as e:
            print_error(f"PyInstaller 설치 실패: {e}")
            return False

def check_dependencies():
    """의존성 패키지 체크"""
    print_header("의존성 패키지 체크")
    
    required_packages = [
        'selenium',
        'webdriver_manager',
        'schedule',
        'pyperclip',
        'pillow',  # PIL
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print_success(f"{package} 설치됨")
        except ImportError:
            print_warning(f"{package} 미설치")
            missing_packages.append(package)
    
    if missing_packages:
        print_warning(f"누락된 패키지: {', '.join(missing_packages)}")
        print_info("누락된 패키지를 설치합니다...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install"] + missing_packages)
            print_success("누락된 패키지 설치 완료")
        except subprocess.CalledProcessError as e:
            print_error(f"패키지 설치 실패: {e}")
            return False
    
    print_success("의존성 체크 완료")
    return True

def clean_build():
    """이전 빌드 정리"""
    print_header("이전 빌드 정리")
    
    dirs_to_clean = ['build', 'dist', '__pycache__']
    files_to_clean = []
    
    # .spec 파일 찾기
    for file in os.listdir('.'):
        if file.endswith('.spec'):
            files_to_clean.append(file)
    
    # 디렉토리 삭제
    for directory in dirs_to_clean:
        if os.path.exists(directory):
            try:
                shutil.rmtree(directory)
                print_success(f"삭제: {directory}/")
            except Exception as e:
                print_warning(f"{directory}/ 삭제 실패: {e}")
    
    # 파일 삭제
    for file in files_to_clean:
        try:
            os.remove(file)
            print_success(f"삭제: {file}")
        except Exception as e:
            print_warning(f"{file} 삭제 실패: {e}")
    
    print_success("정리 완료")

def build_exe():
    """실행 파일 빌드"""
    print_header("실행 파일 빌드 시작")
    
    # PyInstaller 명령 구성
    pyinstaller_args = [
        'pyinstaller',
        'run.py',
        '--name=네이버밴드자동포스팅',
        '--onefile',
        '--windowed',
        '--add-data=config:config' if platform.system() != 'Windows' else '--add-data=config;config',
        '--add-data=src:src' if platform.system() != 'Windows' else '--add-data=src;src',
        '--hidden-import=selenium',
        '--hidden-import=selenium.webdriver',
        '--hidden-import=selenium.webdriver.chrome',
        '--hidden-import=webdriver_manager',
        '--hidden-import=webdriver_manager.chrome',
        '--hidden-import=schedule',
        '--hidden-import=pyperclip',
        '--hidden-import=tkinter',
        '--hidden-import=tkinter.ttk',
        '--hidden-import=PIL',
        '--hidden-import=PIL.Image',
        '--hidden-import=PIL.ImageTk',
        '--collect-all=selenium',
        '--collect-all=webdriver_manager',
        '--noconfirm',
        '--clean',
    ]
    
    print_info("PyInstaller 명령:")
    print(" ".join(pyinstaller_args))
    print()
    
    # 빌드 실행
    try:
        result = subprocess.run(
            pyinstaller_args,
            capture_output=False,
            text=True,
            check=True
        )
        print_success("빌드 완료!")
        return True
    except subprocess.CalledProcessError as e:
        print_error(f"빌드 실패: {e}")
        print_error("위의 오류 메시지를 확인하세요.")
        return False
    except FileNotFoundError:
        print_error("pyinstaller를 찾을 수 없습니다.")
        print_info("다음 명령으로 직접 설치해보세요:")
        print_info("  pip install pyinstaller")
        return False

def verify_build():
    """빌드 결과 검증"""
    print_header("빌드 결과 검증")
    
    # dist 폴더 확인
    if not os.path.exists('dist'):
        print_error("dist 폴더가 생성되지 않았습니다.")
        return False
    
    print_success("dist 폴더 생성됨")
    
    # .exe 파일 확인
    exe_name = '네이버밴드자동포스팅.exe' if platform.system() == 'Windows' else '네이버밴드자동포스팅'
    exe_path = os.path.join('dist', exe_name)
    
    if not os.path.exists(exe_path):
        print_error(f"실행 파일이 생성되지 않았습니다: {exe_path}")
        # dist 폴더 내용 출력
        print_info("dist 폴더 내용:")
        try:
            for item in os.listdir('dist'):
                print(f"  - {item}")
        except:
            pass
        return False
    
    # 파일 크기 확인
    file_size = os.path.getsize(exe_path)
    file_size_mb = file_size / (1024 * 1024)
    
    print_success(f"실행 파일 생성됨: {exe_path}")
    print_info(f"파일 크기: {file_size_mb:.2f} MB")
    
    if file_size_mb < 10:
        print_warning("파일 크기가 너무 작습니다. 일부 의존성이 누락되었을 수 있습니다.")
    
    print_success("빌드 검증 완료")
    return True

def create_log():
    """빌드 로그 생성"""
    log_content = f"""
빌드 로그
========================================
날짜: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
OS: {platform.system()} {platform.release()}
Python: {sys.version}
빌드 상태: 성공
========================================

실행 파일 위치:
  dist/네이버밴드자동포스팅{'exe' if platform.system() == 'Windows' else ''}

사용 방법:
1. dist 폴더로 이동
2. 실행 파일을 더블클릭하여 실행
3. 다른 컴퓨터에 복사하여 사용 가능

주의사항:
- 백신 프로그램이 차단할 수 있습니다
  (ANTIVIRUS_FALSE_POSITIVE.md 참고)
- config 폴더가 자동으로 포함되어 있습니다
- 처음 실행 시 설정을 진행하세요
"""
    
    try:
        with open('build.log', 'w', encoding='utf-8') as f:
            f.write(log_content)
        print_success("빌드 로그 생성: build.log")
    except Exception as e:
        print_warning(f"로그 파일 생성 실패: {e}")

def main():
    """메인 함수"""
    print_header("네이버밴드 자동 포스팅 실행 파일 빌드")
    
    # 환경 체크
    if not check_environment():
        return 1
    
    # 필수 파일 체크
    if not check_required_files():
        return 1
    
    # PyInstaller 설치
    if not install_pyinstaller():
        return 1
    
    # 의존성 체크
    if not check_dependencies():
        return 1
    
    # 이전 빌드 정리
    clean_build()
    
    # 빌드 실행
    if not build_exe():
        print_error("\n빌드 실패!")
        print_info("\n문제 해결:")
        print_info("1. EXE_BUILD_TROUBLESHOOTING.md 문서 참고")
        print_info("2. 오류 메시지를 복사하여 GitHub Issues에 등록")
        print_info("3. https://github.com/rpaakdi1-spec/naver-band-auto-poster/issues")
        return 1
    
    # 빌드 검증
    if not verify_build():
        print_error("\n빌드 검증 실패!")
        return 1
    
    # 로그 생성
    create_log()
    
    # 완료 메시지
    print_header("빌드 완료!")
    print()
    print_success("실행 파일이 성공적으로 생성되었습니다!")
    print()
    print_info("📁 생성된 파일 위치:")
    exe_name = '네이버밴드자동포스팅.exe' if platform.system() == 'Windows' else '네이버밴드자동포스팅'
    print(f"   dist/{exe_name}")
    print()
    print_info("🚀 실행 방법:")
    print("   1. dist 폴더로 이동")
    print("   2. 실행 파일을 더블클릭")
    print("   3. GUI 창이 열리면 성공!")
    print()
    print_info("📦 배포:")
    print("   - 실행 파일을 다른 컴퓨터에 복사하여 사용 가능")
    print("   - config 폴더는 자동으로 포함됨")
    print("   - 백신 오탐 시 ANTIVIRUS_FALSE_POSITIVE.md 참고")
    print()
    
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print_error("\n\n빌드 취소됨 (Ctrl+C)")
        sys.exit(1)
    except Exception as e:
        print_error(f"\n\n예상치 못한 오류 발생: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
