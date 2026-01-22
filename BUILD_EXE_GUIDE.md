# 🚀 독립 실행 파일 (.exe) 생성 가이드

## 📋 개요

이 가이드는 **파이썬이 설치되지 않은 컴퓨터**에서도 실행할 수 있는 `.exe` 파일을 만드는 방법을 설명합니다.

## ⚡ 빠른 시작 (Windows)

### 방법 1: 배치 파일 사용 (가장 간단!)

```bash
# 프로젝트 폴더에서
build_exe.bat
```

더블클릭만 하면 자동으로:
1. PyInstaller 설치
2. 이전 빌드 정리
3. .exe 파일 생성

완료되면 `dist/네이버밴드자동포스팅.exe` 파일이 생성됩니다!

### 방법 2: Python 스크립트 사용

```bash
python build_exe.py
```

### 방법 3: 수동 명령어 사용

```bash
# PyInstaller 설치
pip install pyinstaller

# 실행 파일 생성
pyinstaller --name="네이버밴드자동포스팅" \
            --onefile \
            --windowed \
            --add-data="config;config" \
            --hidden-import=selenium \
            --hidden-import=webdriver_manager \
            --hidden-import=schedule \
            --hidden-import=pyperclip \
            --collect-all=selenium \
            --collect-all=webdriver_manager \
            --noconfirm \
            --clean \
            run.py
```

## 📁 생성 결과

빌드가 완료되면 다음 구조가 생성됩니다:

```
프로젝트/
├── dist/
│   └── 네이버밴드자동포스팅.exe  ← 이 파일을 배포!
├── build/                        (임시 파일, 삭제 가능)
├── 네이버밴드자동포스팅.spec     (빌드 설정, 삭제 가능)
└── ...
```

## 🎯 생성된 .exe 파일 사용 방법

### 1️⃣ 단일 파일 배포

`dist/네이버밴드자동포스팅.exe` 파일 하나만 있으면 됩니다!

**필요한 것:**
- ✅ `네이버밴드자동포스팅.exe` (단일 실행 파일)
- ❌ 파이썬 설치 **불필요**
- ❌ 의존성 패키지 설치 **불필요**

### 2️⃣ 권장 배포 구조

더 나은 사용성을 위해 다음과 같이 구성하세요:

```
네이버밴드자동포스팅/
├── 네이버밴드자동포스팅.exe    ← 실행 파일
├── config/
│   └── config.example.json     ← 설정 예시
└── README.txt                   ← 사용 설명
```

### 3️⃣ 실행 방법

1. **첫 실행:**
   - `네이버밴드자동포스팅.exe` 더블클릭
   - 프로그램이 실행되면 자동으로 `config/config.json` 생성

2. **설정:**
   - GUI에서 채팅방 URL 추가
   - 포스팅할 내용 추가
   - 스케줄 설정

3. **시작:**
   - [시작] 버튼 클릭
   - Chrome이 자동 실행되고 로그인 대기
   - 로그인 후 자동 포스팅 시작!

## ⚙️ PyInstaller 옵션 설명

| 옵션 | 설명 |
|------|------|
| `--name` | 생성될 .exe 파일 이름 |
| `--onefile` | 단일 .exe 파일로 패키징 |
| `--windowed` | 콘솔 창 숨김 (GUI만 표시) |
| `--add-data` | config 폴더 포함 |
| `--hidden-import` | 명시적으로 포함할 모듈 |
| `--collect-all` | 모듈의 모든 데이터 파일 포함 |
| `--noconfirm` | 확인 없이 덮어쓰기 |
| `--clean` | 빌드 전 임시 파일 정리 |

## 🔧 문제 해결

### 문제 1: "PyInstaller를 찾을 수 없습니다"

**해결:**
```bash
pip install pyinstaller
```

### 문제 2: 빌드는 성공했지만 실행 시 오류

**해결:**
1. `--hidden-import` 옵션에 누락된 모듈 추가
2. 로그 확인: 실행 파일과 같은 폴더에 로그 생성됨
3. 콘솔 모드로 빌드하여 오류 확인:
   ```bash
   pyinstaller --onefile run.py  # --windowed 제거
   ```

### 문제 3: .exe 파일 크기가 너무 큼

**원인:** 모든 의존성이 포함되어 있기 때문 (약 50-100MB)

**해결 (옵션):**
- UPX 압축 사용:
  ```bash
  pip install pyinstaller[encryption]
  pyinstaller --onefile --upx-dir=C:\upx run.py
  ```

### 문제 4: Chrome 드라이버 오류

**해결:**
- 첫 실행 시 인터넷 연결 필요 (ChromeDriver 자동 다운로드)
- `webdriver-manager`가 자동으로 처리

## 📦 배포 패키지 만들기

### 최종 사용자용 ZIP 패키지:

```bash
# Windows (PowerShell)
Compress-Archive -Path dist/네이버밴드자동포스팅.exe,config/,README.md -DestinationPath 네이버밴드자동포스팅_v1.0.zip
```

내용물:
```
네이버밴드자동포스팅_v1.0.zip
├── 네이버밴드자동포스팅.exe
├── config/
│   └── config.example.json
└── README.md
```

## 🎁 배포 체크리스트

최종 사용자에게 전달하기 전:

- [ ] .exe 파일이 정상 실행되는지 테스트
- [ ] config 폴더 포함
- [ ] README 또는 사용 설명서 포함
- [ ] 바이러스 검사 (일부 백신이 오탐지할 수 있음)
- [ ] Windows Defender 예외 등록 방법 안내

## 💡 사용 팁

### Tip 1: 실행 파일 이름 변경
```bash
# 빌드 시 원하는 이름 지정
pyinstaller --name="MyBandPoster" run.py
```

### Tip 2: 아이콘 추가
```bash
# .ico 파일 준비 후
pyinstaller --icon=icon.ico run.py
```

### Tip 3: 버전 정보 추가 (고급)
```python
# version_info.txt 생성 후
pyinstaller --version-file=version_info.txt run.py
```

## 📊 파일 크기 비교

| 방식 | 크기 | 장점 | 단점 |
|------|------|------|------|
| Python 소스 | ~10 KB | 작음 | 파이썬 필요 |
| .exe (onefile) | ~50 MB | 독립 실행 | 큼 |
| .exe (onedir) | ~80 MB | 빠른 시작 | 폴더 구조 |

## 🚀 고급: 자동 업데이트 구현

향후 버전에서 추가할 수 있는 기능:

1. **버전 확인:**
   ```python
   VERSION = "1.0.0"
   ```

2. **자동 업데이트 체크:**
   - GitHub Releases API 사용
   - 새 버전 알림

3. **원클릭 업데이트:**
   - 새 .exe 다운로드
   - 자동 교체 및 재시작

## 📞 문제 발생 시

1. **로그 확인:**
   - `logs/` 폴더의 로그 파일 확인
   - 콘솔 모드로 재빌드하여 오류 메시지 확인

2. **GitHub Issues:**
   - https://github.com/rpaakdi1-spec/naver-band-auto-poster/issues

3. **재빌드:**
   ```bash
   # 완전 클린 빌드
   build_exe.bat
   ```

## ✅ 최종 테스트

배포 전 체크:

```bash
# 1. 빌드
build_exe.bat

# 2. 테스트 폴더 생성
mkdir test_deploy
copy dist\네이버밴드자동포스팅.exe test_deploy\

# 3. 실행 테스트
cd test_deploy
네이버밴드자동포스팅.exe
```

## 🎉 완료!

이제 `dist/네이버밴드자동포스팅.exe` 파일을 **파이썬이 없는** 다른 컴퓨터에 복사하여 사용할 수 있습니다!

---

**프로젝트:** https://github.com/rpaakdi1-spec/naver-band-auto-poster  
**버전:** v4.1.0  
**빌드 도구:** PyInstaller
