# 🔧 PyInstaller 빌드 문제 해결 가이드

## 🚨 증상: .exe 파일이 생성되지 않고 .spec 파일만 생성됨

이 문제는 PyInstaller 빌드 과정에서 오류가 발생했을 때 나타납니다.

---

## 🔍 1단계: 오류 확인

### 방법 1: 디버그 빌드 실행

```bash
build_exe_debug.bat
```

이 버전은 콘솔 창을 표시하여 오류 메시지를 볼 수 있습니다.

### 방법 2: 직접 실행

```bash
python build_exe.py
```

또는

```powershell
pyinstaller --name="BandAutoPoster" --onefile --windowed run.py
```

---

## 🛠️ 2단계: 일반적인 문제와 해결 방법

### 문제 1: PyInstaller 버전 문제

**증상:**
```
ModuleNotFoundError: No module named 'PyInstaller'
```

**해결:**
```bash
pip uninstall pyinstaller -y
pip install pyinstaller==6.3.0
```

---

### 문제 2: 의존성 패키지 누락

**증상:**
```
ModuleNotFoundError: No module named 'selenium'
```

**해결:**
```bash
pip install -r requirements.txt --upgrade
```

---

### 문제 3: Python 버전 문제

**증상:**
```
Python version not supported
```

**해결:**
- Python 3.8 이상 사용 확인
```bash
python --version
```

Python 3.8 미만이면 업그레이드:
- https://www.python.org/downloads/

---

### 문제 4: 한글 경로 또는 파일명 문제

**증상:**
```
UnicodeDecodeError
FileNotFoundError
```

**해결:**
새로운 빌드 스크립트 사용:
```bash
build_exe_fixed.bat
```

이 버전은 영문 이름(`BandAutoPoster.exe`)으로 먼저 빌드한 후 한글 이름으로 복사합니다.

---

### 문제 5: tkinter 모듈 누락

**증상:**
```
No module named '_tkinter'
```

**해결 (Windows):**

**방법 A: Python 재설치**
1. Python 설치 프로그램 실행
2. "Modify" 선택
3. "tcl/tk and IDLE" 체크
4. 설치 완료

**방법 B: 다른 Python 배포판 사용**
```bash
# Anaconda 사용 시
conda install tk

# 또는 시스템 Python 사용
```

---

### 문제 6: 메모리 부족

**증상:**
```
MemoryError
killed
```

**해결:**
- 다른 프로그램 종료
- 가상 메모리 증가
- RAM 업그레이드 고려

---

### 문제 7: Windows Defender 또는 백신 프로그램

**증상:**
- 빌드 중 갑자기 중단
- 파일이 삭제됨

**해결:**
1. Windows Defender 실시간 보호 일시 비활성화
2. 프로젝트 폴더를 예외 목록에 추가

**예외 추가 방법:**
```
Windows 보안 → 바이러스 및 위협 방지 → 설정 관리 → 
제외 항목 추가 → 폴더 → 프로젝트 폴더 선택
```

---

### 문제 8: config 폴더 경로 문제

**증상:**
```
Unable to find "config" when adding binary and data files.
```

**해결:**

**방법 A: config 폴더 확인**
```bash
# 프로젝트 루트에 config 폴더가 있는지 확인
dir config
```

없으면 생성:
```bash
mkdir config
copy config\config.example.json config\
```

**방법 B: --add-data 옵션 제거**

임시로 config 없이 빌드:
```bash
pyinstaller --name="BandAutoPoster" --onefile --windowed run.py
```

---

## 🎯 3단계: 단계별 해결 프로세스

### Step 1: 환경 확인

```bash
# Python 버전 확인 (3.8 이상)
python --version

# pip 업그레이드
python -m pip install --upgrade pip

# 필수 패키지 확인
pip list | findstr "pyinstaller selenium webdriver"
```

### Step 2: 깨끗한 재설치

```bash
# 가상환경 사용 권장
python -m venv venv
venv\Scripts\activate

# 패키지 재설치
pip install -r requirements.txt
```

### Step 3: 최소 빌드 테스트

```bash
# 가장 간단한 빌드
pyinstaller --onefile run.py
```

성공하면:
```bash
# 옵션 추가해가며 빌드
pyinstaller --onefile --windowed run.py
```

### Step 4: 최종 빌드

```bash
build_exe_fixed.bat
```

---

## 📋 빌드 체크리스트

빌드 전 확인:

- [ ] Python 3.8 이상 설치됨
- [ ] pip 최신 버전
- [ ] requirements.txt 모든 패키지 설치됨
- [ ] PyInstaller 6.3.0 설치됨
- [ ] config 폴더 존재
- [ ] 백신 프로그램 예외 설정
- [ ] 충분한 디스크 공간 (최소 500MB)
- [ ] 충분한 메모리 (최소 4GB)

---

## 🚀 권장 빌드 순서

### 1. 디버그 빌드 (오류 확인)

```bash
build_exe_debug.bat
```

콘솔 창에서 오류 메시지 확인

### 2. 수정 빌드 (한글 문제 해결)

```bash
build_exe_fixed.bat
```

영문 이름으로 먼저 빌드 후 한글 복사

### 3. 기본 빌드 (모두 정상인 경우)

```bash
build_exe.bat
```

---

## 💡 대안: 수동 빌드

자동 스크립트가 작동하지 않으면 수동으로:

```bash
# 1. 정리
rmdir /s /q build
rmdir /s /q dist
del /q *.spec

# 2. 빌드 (한 줄씩 실행)
pyinstaller ^
  --name=BandAutoPoster ^
  --onefile ^
  --windowed ^
  --hidden-import=selenium ^
  --hidden-import=webdriver_manager ^
  --hidden-import=schedule ^
  --hidden-import=pyperclip ^
  --collect-all=selenium ^
  --collect-all=webdriver_manager ^
  run.py

# 3. 결과 확인
dir dist\*.exe
```

---

## 🔍 로그 파일 확인

빌드 실패 시 다음 위치에서 로그 확인:

```
build/BandAutoPoster/warn-BandAutoPoster.txt
build/BandAutoPoster/xref-BandAutoPoster.html
```

---

## 📞 추가 도움이 필요한 경우

### GitHub Issues
https://github.com/rpaakdi1-spec/naver-band-auto-poster/issues

오류 메시지 전체를 복사하여 이슈로 등록하세요.

### 포함할 정보:
1. Python 버전 (`python --version`)
2. PyInstaller 버전 (`pip show pyinstaller`)
3. OS 버전 (Windows 10/11)
4. 오류 메시지 전체
5. 빌드 명령어

---

## ✅ 성공 확인

빌드가 성공하면:

```
dist/
├── BandAutoPoster.exe           (영문)
└── 네이버밴드자동포스팅.exe     (한글)
```

테스트:
```bash
dist\BandAutoPoster.exe
```

프로그램이 실행되면 성공! 🎉

---

## 🎯 빠른 해결 방법 요약

```bash
# 1단계: 환경 재설정
python -m pip install --upgrade pip
pip install -r requirements.txt --upgrade
pip install pyinstaller==6.3.0 --force-reinstall

# 2단계: 디버그 빌드
build_exe_debug.bat

# 3단계: 오류 확인 후 수정

# 4단계: 정식 빌드
build_exe_fixed.bat
```

---

## 📊 문제별 발생 빈도

| 문제 | 빈도 | 해결 난이도 |
|------|------|------------|
| 의존성 누락 | ⭐⭐⭐⭐⭐ | 쉬움 |
| 한글 경로 | ⭐⭐⭐⭐ | 쉬움 |
| tkinter 누락 | ⭐⭐⭐ | 보통 |
| 백신 차단 | ⭐⭐⭐ | 쉬움 |
| 메모리 부족 | ⭐⭐ | 보통 |
| Python 버전 | ⭐ | 쉬움 |

---

**대부분의 문제는 의존성 재설치로 해결됩니다!**

```bash
pip install -r requirements.txt --upgrade
build_exe_fixed.bat
```
