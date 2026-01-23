# GitHub Release 생성 가이드 📦

## 목표
Windows에서 .exe 파일을 빌드하고 GitHub Release를 생성하여 다른 사용자가 다운로드할 수 있도록 합니다.

---

## 📋 준비사항

### 필요한 것
- ✅ Windows 10/11 PC
- ✅ Python 3.8 이상 설치
- ✅ Git 설치
- ✅ GitHub 계정 (저장소 쓰기 권한)

---

## 🚀 단계별 가이드

### 1단계: 저장소 최신화

```bash
# 저장소로 이동
cd naver-band-auto-poster

# 최신 코드 받기
git pull origin main
```

### 2단계: .exe 파일 빌드

#### 방법 A: 자동 빌드 (추천)

**Windows 탐색기에서:**
1. `build_exe_fixed.bat` 파일 찾기
2. 더블클릭
3. 빌드 완료 대기 (약 2-5분)

**명령 프롬프트에서:**
```bash
build_exe_fixed.bat
```

#### 방법 B: 수동 빌드

```bash
# 1. 의존성 업그레이드
pip install --upgrade pip
pip install -r requirements.txt --upgrade

# 2. PyInstaller 최신 버전 설치
pip install pyinstaller --upgrade

# 3. 빌드 실행
pyinstaller --name=BandAutoPoster --onefile --windowed --hidden-import=selenium --hidden-import=webdriver_manager --hidden-import=schedule --hidden-import=pyperclip --hidden-import=tkinter --collect-all=selenium --collect-all=webdriver_manager --noconfirm --clean run.py

# 4. 한글 이름으로 복사
copy dist\BandAutoPoster.exe "dist\네이버밴드자동포스팅.exe"
```

### 3단계: 빌드 결과 확인

```bash
# dist 폴더 확인
dir dist

# 다음 파일들이 있어야 합니다:
# BandAutoPoster.exe (약 50-70 MB)
# 네이버밴드자동포스팅.exe (복사본)
```

### 4단계: .exe 테스트

```bash
# dist 폴더로 이동
cd dist

# 실행 테스트
BandAutoPoster.exe
```

**테스트 체크리스트:**
- [ ] 프로그램이 정상적으로 실행됨
- [ ] GUI 창이 열림
- [ ] 채팅방 추가 가능
- [ ] 포스트 추가 가능
- [ ] 설정 저장 가능
- [ ] Chrome 실행 가능

### 5단계: 사용 설명서 준비

이미 `사용설명서.txt` 파일이 프로젝트에 있습니다!

```bash
# 확인
type 사용설명서.txt
```

### 6단계: GitHub Release 생성

#### 6-1. GitHub 웹사이트 접속

1. 브라우저에서 https://github.com/rpaakdi1-spec/naver-band-auto-poster 열기
2. 로그인 확인

#### 6-2. Release 페이지 이동

1. 오른쪽 사이드바에서 **"Releases"** 클릭
2. **"Create a new release"** 또는 **"Draft a new release"** 버튼 클릭

#### 6-3. 태그 생성

**"Choose a tag" 입력란:**
```
v5.0.0
```

> 💡 버전 규칙: v{major}.{minor}.{patch}
> - v5.0.0 = 웹 버전 추가
> - v5.0.1 = 버그 수정
> - v5.1.0 = 새 기능 추가

**"Target" 선택:**
- `main` 브랜치 선택 (기본값)

#### 6-4. 릴리스 정보 입력

**Release title (제목):**
```
네이버밴드 자동포스팅 v5.0.0 - 웹 버전 지원
```

**Description (설명):**

```markdown
## 🎉 v5.0.0 주요 업데이트

### 새로운 기능
- 🌐 **웹 버전 추가**: Streamlit 기반 브라우저 앱
- 📱 **모바일 지원**: 같은 Wi-Fi에서 모바일 접속 가능
- 🎨 **모던 UI**: 깔끔한 웹 인터페이스
- 🔄 **실시간 업데이트**: 1초마다 자동 새로고침

### 개선 사항
- ⏱️ 실시간 카운트다운 타이머
- 🎯 채팅방 별명 및 선택적 포스팅
- 📅 날짜+시간 스케줄링
- 🔧 세션 안정성 개선

### 실행 방법

#### 1️⃣ 웹 버전 (추천)
```bash
git clone https://github.com/rpaakdi1-spec/naver-band-auto-poster.git
cd naver-band-auto-poster
run_web.bat  # Windows
# 또는
python3 run_web.py  # Mac/Linux
```

#### 2️⃣ .exe 파일 (Python 불필요)
1. 아래에서 `네이버밴드자동포스팅.exe` 다운로드
2. 더블클릭 실행
3. 끝!

#### 3️⃣ 데스크톱 GUI
```bash
git clone https://github.com/rpaakdi1-spec/naver-band-auto-poster.git
cd naver-band-auto-poster
pip install -r requirements.txt
python run.py
```

### 📖 문서
- [빠른 시작 가이드](https://github.com/rpaakdi1-spec/naver-band-auto-poster/blob/main/WEB_QUICK_START.md)
- [웹 버전 가이드](https://github.com/rpaakdi1-spec/naver-band-auto-poster/blob/main/WEB_VERSION_GUIDE.md)
- [3가지 방법 비교](https://github.com/rpaakdi1-spec/naver-band-auto-poster/blob/main/3_WAYS_GUIDE.md)

### ⚠️ 주의사항
- Windows 10/11 64-bit 필요 (.exe 파일)
- Chrome 브라우저 설치 필요
- 네이버 이용약관 준수

### 🐛 알려진 이슈
- 없음

---

**Full Changelog**: https://github.com/rpaakdi1-spec/naver-band-auto-poster/compare/v4.2.0...v5.0.0
```

#### 6-5. 파일 업로드

**"Attach binaries by dropping them here or selecting them" 영역에 드래그 앤 드롭:**

1. `dist/네이버밴드자동포스팅.exe`
2. `사용설명서.txt`

또는 **클릭해서 파일 선택**

**업로드할 파일 목록:**
- ✅ `네이버밴드자동포스팅.exe` (필수)
- ✅ `사용설명서.txt` (권장)
- ⭐ `BandAutoPoster.exe` (선택사항, 영문명)

#### 6-6. 릴리스 옵션 설정

- ✅ **"Set as the latest release"** 체크 (최신 릴리스로 설정)
- ❌ **"Set as a pre-release"** 체크 해제 (정식 릴리스)

#### 6-7. 릴리스 발행

**"Publish release"** 버튼 클릭! 🎉

---

## ✅ 완료 확인

### 1. 릴리스 페이지 확인

https://github.com/rpaakdi1-spec/naver-band-auto-poster/releases/latest

다음을 확인:
- [ ] v5.0.0 태그가 최신 릴리스로 표시됨
- [ ] 제목과 설명이 올바르게 표시됨
- [ ] 파일이 다운로드 가능함

### 2. 다운로드 테스트

1. 릴리스 페이지에서 `네이버밴드자동포스팅.exe` 클릭
2. 다운로드 확인
3. 새 폴더에 저장
4. 실행 테스트
5. 정상 작동 확인

### 3. README 업데이트 (선택사항)

릴리스 URL을 README에 추가:

```bash
# 저장소 루트로 이동
cd C:\path\to\naver-band-auto-poster

# README.md 편집
notepad README.md
```

**추가할 내용:**
```markdown
### 방법 2: .exe 파일 💻 (Python 불필요)

**다운로드**: [최신 릴리스](https://github.com/rpaakdi1-spec/naver-band-auto-poster/releases/latest)

1. `네이버밴드자동포스팅.exe` 다운로드
2. 더블클릭 실행
3. 끝!
```

**커밋 및 푸시:**
```bash
git add README.md
git commit -m "docs: Add download link to latest release"
git push origin main
```

---

## 📊 릴리스 후 체크리스트

- [ ] 릴리스가 https://github.com/rpaakdi1-spec/naver-band-auto-poster/releases/latest 에서 보임
- [ ] .exe 파일 다운로드 가능
- [ ] 다운로드한 .exe 정상 실행
- [ ] Windows Defender 경고 무시하고 실행 가능
- [ ] 프로그램 모든 기능 정상 작동
- [ ] README에 다운로드 링크 추가 (선택사항)
- [ ] 사용자에게 알림 (선택사항)

---

## 🔧 문제 해결

### ❌ "빌드 실패: PyInstaller를 찾을 수 없습니다"

```bash
pip install pyinstaller --upgrade
```

### ❌ "빌드 실패: 모듈을 찾을 수 없습니다"

```bash
pip install -r requirements.txt --upgrade --force-reinstall
```

### ❌ ".exe 파일이 생성되지 않았습니다"

1. `build_exe_debug.bat` 실행
2. 오류 메시지 확인
3. [BUILD_TROUBLESHOOTING.md](BUILD_TROUBLESHOOTING.md) 참조

### ❌ "GitHub Release 생성 실패: 권한 오류"

- 저장소에 쓰기 권한이 있는지 확인
- 저장소 소유자이거나 collaborator여야 함

### ❌ "파일 업로드 실패: 파일이 너무 큽니다"

- GitHub Release는 파일당 2GB까지 지원
- .exe 파일은 보통 50-100MB이므로 문제없음
- 네트워크 연결 확인

---

## 💡 팁

### 자동 릴리스 노트 생성

GitHub의 **"Generate release notes"** 버튼 클릭하면:
- 이전 릴리스 이후의 모든 커밋 자동 나열
- Pull Request 링크 자동 추가
- 기여자 목록 자동 생성

### 릴리스 초안 저장

릴리스를 바로 발행하지 않고 **"Save draft"**로 저장 가능:
- 나중에 편집 가능
- 다른 사람에게 리뷰 요청 가능
- 준비되면 **"Publish release"**로 발행

### 여러 파일 업로드

한 번에 여러 파일 업로드 가능:
```
네이버밴드자동포스팅.exe
BandAutoPoster.exe
사용설명서.txt
config.example.json
```

---

## 🎓 추가 자료

- **GitHub Releases 공식 문서**: https://docs.github.com/en/repositories/releasing-projects-on-github
- **PyInstaller 공식 문서**: https://pyinstaller.org/
- **빌드 가이드**: [BUILD_EXE_GUIDE.md](BUILD_EXE_GUIDE.md)
- **문제 해결**: [BUILD_TROUBLESHOOTING.md](BUILD_TROUBLESHOOTING.md)

---

## 🎉 완료!

이제 사용자들이 GitHub Release에서 .exe 파일을 다운로드하여 바로 사용할 수 있습니다!

**릴리스 URL**: https://github.com/rpaakdi1-spec/naver-band-auto-poster/releases/latest

**다운로드 링크**: 
```
https://github.com/rpaakdi1-spec/naver-band-auto-poster/releases/latest/download/네이버밴드자동포스팅.exe
```

---

💡 **요약**:
1. `build_exe_fixed.bat` 실행
2. `dist/네이버밴드자동포스팅.exe` 확인
3. GitHub Release 생성
4. 파일 업로드
5. 발행!
