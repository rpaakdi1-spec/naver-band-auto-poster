# 빌드 가이드

## 🏗️ 빌드 결과

### ✅ Linux 실행 파일 (생성 완료)
- **파일 위치**: `dist/NaverBandAutoPoster`
- **파일 크기**: 79MB
- **플랫폼**: Linux x86_64
- **빌드 일시**: 2026-01-15
- **Python 버전**: 3.12.11

### 📋 빌드 명령어
```bash
# 의존성 설치
pip install -r requirements.txt
pip install pyinstaller

# 빌드 실행
pyinstaller --clean --noconfirm build_exe.spec
```

---

## 💻 Windows EXE 빌드 방법

### 방법 1: Windows에서 직접 빌드 (권장)

Windows 환경에서 빌드하면 `.exe` 파일이 생성됩니다:

```batch
# 1. Python 3.8+ 설치 확인
python --version

# 2. 의존성 설치
pip install -r requirements.txt
pip install pyinstaller

# 3. 빌드 실행
pyinstaller --clean --noconfirm build_exe.spec
```

또는 `build_exe.bat` 파일을 더블클릭하세요.

빌드 완료 후 `dist\NaverBandAutoPoster.exe` 생성됩니다.

### 방법 2: GitHub Actions를 통한 자동 빌드

`.github/workflows/build.yml` 파일을 생성하여 자동 빌드:

```yaml
name: Build EXE

on:
  push:
    tags:
      - 'v*'

jobs:
  build-windows:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pyinstaller
      - name: Build EXE
        run: pyinstaller --clean --noconfirm build_exe.spec
      - name: Upload artifact
        uses: actions/upload-artifact@v3
        with:
          name: NaverBandAutoPoster-Windows
          path: dist/NaverBandAutoPoster.exe
```

---

## 🔧 빌드 설정 (build_exe.spec)

현재 설정:
- **진입점**: `run.py`
- **모드**: GUI (console=False)
- **포함 파일**: 
  - `config/config.example.json`
  - `README.md`
- **Hidden imports**: selenium, webdriver-manager, schedule, tkinter
- **압축**: UPX enabled

---

## 📦 빌드된 파일 배포

### Linux 사용자용
```bash
# 실행 권한 부여
chmod +x dist/NaverBandAutoPoster

# 실행
./dist/NaverBandAutoPoster
```

### Windows 사용자용
1. `dist\NaverBandAutoPoster.exe` 파일을 원하는 위치에 복사
2. 더블클릭으로 실행
3. Windows Defender 경고 시: "추가 정보" > "실행"

---

## ⚠️ 주의사항

### Chrome 브라우저 필요
실행 파일은 독립 실행형이지만, Selenium 자동화를 위해 **Chrome 브라우저**가 시스템에 설치되어 있어야 합니다.

### 첫 실행 시
- Chrome WebDriver가 자동으로 다운로드됩니다 (인터넷 연결 필요)
- `config/config.json` 파일이 자동 생성됩니다
- `logs/` 폴더가 자동 생성됩니다

### 파일 크기
- Windows EXE: 약 80-100MB (예상)
- Linux 실행 파일: 79MB
- Python 인터프리터와 모든 의존성이 포함되어 있어 크기가 큽니다

---

## 🐛 문제 해결

### Q: "tkinter" 오류 발생
**A**: Python을 재설치하고 "tcl/tk and IDLE" 옵션을 선택하세요.

### Q: 빌드 시 "pillow" 오류
**A**: 이미 해결되었습니다. `requirements.txt`에서 pillow가 제거되었습니다.

### Q: Windows에서 "DLL load failed" 오류
**A**: Visual C++ Redistributable을 설치하세요:
- [Microsoft Visual C++ 재배포 패키지](https://aka.ms/vs/17/release/vc_redist.x64.exe)

### Q: 실행 파일이 너무 큼
**A**: 정상입니다. 단일 실행 파일에 Python과 모든 라이브러리가 포함되어 있습니다.

---

## 📊 빌드 로그

빌드 과정의 자세한 로그는 다음 파일에서 확인하세요:
- `build/build_exe/warn-build_exe.txt` - 경고 로그
- `build/build_exe/xref-build_exe.html` - 의존성 그래프
- `build_log.txt` - 전체 빌드 로그

---

## 🚀 자동 배포

GitHub Releases에 자동으로 업로드하려면:

1. GitHub에서 새 Release 생성
2. Tag 버전 입력 (예: `v1.0.0`)
3. 빌드된 파일 업로드:
   - Windows: `NaverBandAutoPoster.exe`
   - Linux: `NaverBandAutoPoster`
4. Release 설명 작성 및 게시

---

## 📞 지원

문제가 발생하면:
1. `build_log.txt` 확인
2. GitHub Issues에 문의: https://github.com/rpaakdi1-spec/naver-band-auto-poster/issues
