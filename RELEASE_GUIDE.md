# 📦 GitHub Release 배포 가이드

## 🎯 목표

GitHub Releases를 통해 `.exe` 파일을 배포하여 사용자가 쉽게 다운로드할 수 있도록 합니다.

## 📋 사전 준비

### 1단계: 실행 파일 빌드

**Windows에서:**

```bash
# 프로젝트 폴더로 이동
cd naver-band-auto-poster

# 최신 코드로 업데이트
git pull origin main

# 빌드 실행
build_exe.bat
```

**또는:**

```bash
python build_exe.py
```

### 빌드 결과 확인:

```
프로젝트/
└── dist/
    └── 네이버밴드자동포스팅.exe  ← 이 파일을 업로드!
```

## 🚀 GitHub Release 생성 방법

### 방법 1: GitHub 웹 인터페이스 (추천)

#### Step 1: Releases 페이지로 이동

1. GitHub 저장소로 이동: https://github.com/rpaakdi1-spec/naver-band-auto-poster
2. 오른쪽 사이드바에서 **"Releases"** 클릭
3. **"Create a new release"** 또는 **"Draft a new release"** 버튼 클릭

#### Step 2: 릴리스 정보 입력

**태그 버전:**
```
v4.2.0
```

**릴리스 제목:**
```
네이버밴드 자동포스팅 v4.2.0 - 독립 실행 파일 지원
```

**설명 (Description):**
```markdown
## 🎉 주요 기능

### 새로운 기능
- 🚀 **독립 실행 파일 지원**: 파이썬 설치 없이 실행 가능한 .exe 파일
- 🎯 **채팅방 별명 및 선택적 포스팅**: 체크박스로 포스팅할 채팅방 선택
- 📅 **날짜+시간 스케줄링**: 24시간 자동 설정
- ⏱️ **실시간 카운트다운**: 다음 포스팅까지 남은 시간 표시
- 🖥️ **개선된 UI**: 좌우 분할 레이아웃

### 개선 사항
- ✅ 세션 안정성 개선 (invalid session id 오류 해결)
- ✅ 카운트다운 타이머 정확도 향상
- ✅ 채팅방 닫기 로직 최적화

## 📥 다운로드

### Windows 사용자 (추천)
**`네이버밴드자동포스팅.exe`** 파일을 다운로드하여 바로 실행하세요!

- ✅ 파이썬 설치 불필요
- ✅ 패키지 설치 불필요
- ✅ 더블클릭만 하면 실행

### 개발자 / 소스 코드 사용자
아래 "Source code" 링크에서 다운로드하거나:
\`\`\`bash
git clone https://github.com/rpaakdi1-spec/naver-band-auto-poster.git
cd naver-band-auto-poster
pip install -r requirements.txt
python run.py
\`\`\`

## 🚀 빠른 시작

1. **다운로드**: `네이버밴드자동포스팅.exe` 다운로드
2. **실행**: 파일 더블클릭
3. **설정**:
   - 채팅방 URL 추가 (별명 지정 가능)
   - 포스팅할 내용 추가
   - 스케줄 설정 (시작/종료 일시)
4. **시작**: [시작] 버튼 클릭
5. **로그인**: Chrome 브라우저에서 밴드 로그인
6. **자동 포스팅 시작!** ✨

## 📖 상세 사용법

자세한 사용법은 [README.md](https://github.com/rpaakdi1-spec/naver-band-auto-poster/blob/main/README.md)를 참고하세요.

## ⚙️ 시스템 요구사항

- **운영체제**: Windows 10 또는 11 (64-bit)
- **브라우저**: Google Chrome (최신 버전)
- **인터넷**: 첫 실행 시 ChromeDriver 다운로드 필요
- **Python**: ❌ 설치 불필요!

## 🐛 알려진 이슈

- 일부 백신 프로그램에서 오탐지 가능 (정상 파일입니다)
- 첫 실행 시 Windows Defender 경고 가능 (실행 허용 필요)

## 📝 변경 사항 (Changelog)

### v4.2.0 (2026-01-22)
- feat: 독립 실행 파일(.exe) 빌드 지원 추가
- feat: 채팅방 별명 및 체크박스 선택 기능
- feat: 날짜+시간 스케줄링 (24시간 자동 설정)
- feat: 실시간 카운트다운 타이머
- feat: 좌우 분할 UI 레이아웃
- fix: 세션 안정성 개선 (채팅방 닫기 로직 최적화)
- fix: 카운트다운 즉시 표시
- docs: 빌드 가이드 및 사용 설명서 추가

### 이전 버전
- v4.1.0: UI 개선 및 카운트다운 기능
- v4.0.0: 채팅방 별명 및 선택적 포스팅
- v3.0.0: 고급 채팅방 검색
- v2.0.0: 다중 채팅방 지원

## 🔗 관련 링크

- [📖 사용 설명서](https://github.com/rpaakdi1-spec/naver-band-auto-poster/blob/main/README.md)
- [🔨 빌드 가이드](https://github.com/rpaakdi1-spec/naver-band-auto-poster/blob/main/BUILD_EXE_GUIDE.md)
- [🐛 이슈 리포트](https://github.com/rpaakdi1-spec/naver-band-auto-poster/issues)

## 💬 피드백

문제가 발생하거나 제안 사항이 있으시면 [Issues](https://github.com/rpaakdi1-spec/naver-band-auto-poster/issues)에 등록해주세요!

---

**⚠️ 주의사항**
- 네이버 이용약관을 준수하여 사용하세요
- 과도한 자동화는 계정 제재를 받을 수 있습니다
- 적절한 포스팅 간격을 설정하세요 (최소 30분 권장)
```

#### Step 3: 파일 업로드

1. 페이지 하단 **"Attach binaries"** 섹션으로 이동
2. **"Attach files by dragging & dropping, selecting or pasting them"** 영역으로 드래그
3. 다음 파일을 업로드:
   - ✅ `네이버밴드자동포스팅.exe` (필수)
   - ✅ `README.md` (선택)
   - ✅ `BUILD_EXE_GUIDE.md` (선택)

**또는** 파일을 직접 선택하여 업로드

#### Step 4: 릴리스 옵션 설정

- [ ] **Set as a pre-release** (베타 버전인 경우 체크)
- [x] **Set as the latest release** (최신 버전으로 설정)
- [ ] **Create a discussion for this release** (토론 생성 원하는 경우)

#### Step 5: 게시

**"Publish release"** 버튼 클릭!

---

### 방법 2: GitHub CLI 사용 (고급)

```bash
# GitHub CLI 설치 확인
gh --version

# 로그인 (처음 한 번만)
gh auth login

# 릴리스 생성 및 파일 업로드
gh release create v4.2.0 \
  dist/네이버밴드자동포스팅.exe \
  --title "네이버밴드 자동포스팅 v4.2.0 - 독립 실행 파일 지원" \
  --notes-file RELEASE_NOTES.md
```

---

## 📦 배포 체크리스트

릴리스 전 확인사항:

### 빌드 확인
- [ ] `build_exe.bat` 실행 성공
- [ ] `dist/네이버밴드자동포스팅.exe` 파일 생성 확인
- [ ] .exe 파일 실행 테스트
- [ ] 파이썬 미설치 환경에서 테스트

### 기능 테스트
- [ ] GUI 정상 실행
- [ ] Chrome 자동 실행
- [ ] 채팅방 추가/삭제
- [ ] 포스트 추가/삭제
- [ ] 수동 포스팅 테스트
- [ ] 자동 포스팅 테스트
- [ ] 설정 저장/로드

### 문서 확인
- [ ] README.md 업데이트
- [ ] 버전 번호 확인
- [ ] CHANGELOG 작성
- [ ] 스크린샷 준비 (선택)

### GitHub
- [ ] 최신 코드 푸시 완료
- [ ] 태그 버전 결정 (v4.2.0)
- [ ] 릴리스 노트 작성

---

## 📸 스크린샷 준비 (선택사항)

릴리스에 스크린샷을 추가하면 사용자 이해도가 높아집니다:

### 권장 스크린샷:
1. **메인 화면**: 프로그램 전체 UI
2. **채팅방 관리**: 채팅방 추가 화면
3. **포스트 관리**: 포스트 추가 화면
4. **실행 중**: 카운트다운 타이머 및 로그
5. **설정 화면**: 스케줄 설정

스크린샷을 Releases 설명에 추가:
```markdown
## 📸 스크린샷

### 메인 화면
![메인 화면](https://user-images.githubusercontent.com/.../main_screen.png)

### 실행 중
![실행 중](https://user-images.githubusercontent.com/.../running.png)
```

---

## 🔄 버전 업데이트 프로세스

### 1. 코드 수정
```bash
# 코드 작업
git add .
git commit -m "feat: 새로운 기능 추가"
git push origin main
```

### 2. 버전 업데이트
파일에서 버전 번호 변경:
- `README.md`
- `run.py` (상단 주석)
- `src/gui.py` (창 제목 또는 About)

### 3. 빌드
```bash
build_exe.bat
```

### 4. 테스트
```bash
dist\네이버밴드자동포스팅.exe
```

### 5. 릴리스 생성
GitHub Releases에서 새 릴리스 생성 및 .exe 업로드

---

## 🎯 릴리스 전략

### 버전 번호 규칙 (Semantic Versioning)

```
v{MAJOR}.{MINOR}.{PATCH}
```

- **MAJOR**: 큰 변경, 호환성 깨짐 (예: v5.0.0)
- **MINOR**: 새 기능 추가, 호환 유지 (예: v4.3.0)
- **PATCH**: 버그 수정, 작은 개선 (예: v4.2.1)

### 릴리스 주기

- **Beta**: `v4.2.0-beta.1`, `v4.2.0-beta.2` (테스트용)
- **Release Candidate**: `v4.2.0-rc.1` (거의 완성)
- **Stable**: `v4.2.0` (정식 릴리스)

---

## 📊 릴리스 후 확인사항

### 1. 다운로드 링크 테스트
```
https://github.com/rpaakdi1-spec/naver-band-auto-poster/releases/latest
```

### 2. README 업데이트
```markdown
## 🚀 빠른 시작

### 방법 1: 실행 파일 다운로드 (추천)
[최신 릴리스 다운로드](https://github.com/rpaakdi1-spec/naver-band-auto-poster/releases/latest)
```

### 3. 사용자 피드백 모니터링
- GitHub Issues 확인
- 다운로드 횟수 추적
- 버그 리포트 대응

---

## 🔐 보안 고려사항

### 파일 무결성 확인

**SHA256 체크섬 생성:**

```powershell
# Windows PowerShell
Get-FileHash dist\네이버밴드자동포스팅.exe -Algorithm SHA256
```

릴리스 노트에 추가:
```markdown
## 🔐 파일 무결성

**SHA256:**
```
abc123def456...
```
```

### 바이러스 검사

릴리스 전 VirusTotal에서 검사:
1. https://www.virustotal.com 방문
2. .exe 파일 업로드
3. 결과 링크를 릴리스 노트에 추가

---

## 💡 팁

### Tip 1: 자동 릴리스 노트
GitHub는 커밋 메시지로부터 자동 릴리스 노트를 생성할 수 있습니다.

**"Generate release notes"** 버튼 클릭하면 자동 생성!

### Tip 2: 다운로드 배지
README.md에 다운로드 배지 추가:

```markdown
[![GitHub release](https://img.shields.io/github/v/release/rpaakdi1-spec/naver-band-auto-poster)](https://github.com/rpaakdi1-spec/naver-band-auto-poster/releases/latest)
[![Downloads](https://img.shields.io/github/downloads/rpaakdi1-spec/naver-band-auto-poster/total)](https://github.com/rpaakdi1-spec/naver-band-auto-poster/releases)
```

### Tip 3: 이전 버전 유지
- 최소 3개의 최신 릴리스 유지
- 오래된 버전은 아카이브 처리

---

## 🎉 완료!

이제 사용자가 다음과 같이 다운로드할 수 있습니다:

```
1. GitHub 저장소 방문
2. Releases 클릭
3. 최신 릴리스에서 "네이버밴드자동포스팅.exe" 다운로드
4. 더블클릭 실행!
```

**다운로드 링크:**
```
https://github.com/rpaakdi1-spec/naver-band-auto-poster/releases/latest
```

---

## 📞 도움이 필요하신가요?

- [GitHub Releases 공식 문서](https://docs.github.com/en/repositories/releasing-projects-on-github)
- [Semantic Versioning](https://semver.org/)
- [프로젝트 Issues](https://github.com/rpaakdi1-spec/naver-band-auto-poster/issues)
