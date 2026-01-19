# 네이버밴드 자동 포스팅 프로그램

[![Build Windows EXE](https://github.com/rpaakdi1-spec/naver-band-auto-poster/actions/workflows/build-exe.yml/badge.svg)](https://github.com/rpaakdi1-spec/naver-band-auto-poster/actions/workflows/build-exe.yml)
[![GitHub release](https://img.shields.io/github/v/release/rpaakdi1-spec/naver-band-auto-poster)](https://github.com/rpaakdi1-spec/naver-band-auto-poster/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

네이버밴드 PC버전의 채팅방에 설정한 시간에 따라 주기적으로 글을 자동 포스팅하는 프로그램입니다.

## 🚀 빠른 시작 (Python 없이 실행)

### ⭐ 방법 1: EXE 파일 사용 (추천)

**Python 설치 없이 바로 실행!**

1. **Releases**에서 `네이버밴드_자동포스팅.exe` 다운로드
2. 더블클릭으로 바로 실행!
3. GUI에서 설정 입력 후 사용

> 📥 [Releases 페이지에서 다운로드](https://github.com/rpaakdi1-spec/naver-band-auto-poster/releases)

### 방법 2: 원클릭 실행 스크립트

**Python이 설치되어 있다면:**

1. 프로젝트 다운로드
2. `실행.bat` 더블클릭
3. 자동으로 필요한 패키지 설치 후 실행!

---

## 💻 수동 설치 (개발자용)

### 시스템 요구사항

- Python 3.8 이상
- Chrome 브라우저
- Windows/macOS/Linux

### 설치 방법

```bash
# 1. 프로젝트 다운로드
git clone https://github.com/rpaakdi1-spec/naver-band-auto-poster.git
cd naver-band-auto-poster

# 2. 패키지 설치
pip install -r requirements.txt

# 3. 실행
python run.py
```

---

## 🎯 주요 기능

- 🤖 **자동 로그인**: 네이버 계정 자동 로그인
- ⏰ **스케줄 포스팅**: 설정한 시간 간격으로 자동 포스팅
- 📝 **다중 포스트 관리**: 여러 개의 포스팅 내용을 등록하고 관리
- 🔄 **순환/랜덤 포스팅**: 포스트를 순환 또는 랜덤으로 선택
- 🎯 **시간대 설정**: 포스팅 활성 시간대 설정 (예: 09:00 ~ 22:00)
- 🎲 **랜덤 딜레이**: 자연스러운 포스팅을 위한 랜덤 딜레이
- 🖥️ **GUI 인터페이스**: 사용하기 쉬운 그래픽 인터페이스
- 📊 **로깅**: 모든 활동 로그 기록

---

## 📖 사용 방법

### GUI 실행 후

1. **로그인 정보 입력**
   - 네이버 ID
   - 비밀번호
   - 밴드 URL (예: https://band.us/band/12345678)

2. **스케줄 설정**
   - 포스팅 간격 (분)
   - 랜덤 딜레이 (분)
   - 시작 시간 (HH:MM 형식)
   - 종료 시간 (HH:MM 형식)

3. **포스팅 내용 추가**
   - 포스트 내용 입력란에 내용 작성
   - "추가" 버튼 클릭
   - 여러 개의 포스트 등록 가능

4. **설정 저장**
   - "설정 저장" 버튼 클릭
   - config/config.json 파일에 저장됨

5. **실행**
   - "시작" 버튼: 자동 포스팅 시작
   - "중지" 버튼: 자동 포스팅 중지
   - "수동 실행" 버튼: 즉시 한 번 포스팅

---

## 🔧 EXE 파일 직접 빌드하기

직접 EXE 파일을 만들고 싶다면:

### Windows에서:

```bash
# 방법 1: 자동 빌드
build_exe.bat 더블클릭

# 방법 2: 수동 빌드
pip install pyinstaller
pyinstaller --clean --noconfirm build_exe.spec
```

빌드 완료 후 `dist/네이버밴드_자동포스팅.exe` 생성됨

자세한 내용: [BUILD_EXE_GUIDE.md](BUILD_EXE_GUIDE.md)

---

## 📁 프로젝트 구조

```
naver-band-auto-poster/
├── src/
│   ├── band_poster.py      # 자동화 엔진
│   └── gui.py              # GUI 인터페이스
├── config/
│   └── config.example.json # 설정 예제
├── requirements.txt        # 필요 패키지
├── run.py                  # 실행 스크립트
├── 실행.bat                # 원클릭 실행 (Windows)
├── build_exe.bat           # EXE 빌드 스크립트
└── README.md              # 사용 설명서
```

---

## ⚙️ 설정 파일

`config/config.json`:

```json
{
  "naver_id": "your_naver_id",
  "naver_password": "your_naver_password",
  "band_url": "https://band.us/band/xxxxx",
  "posts": [
    {
      "content": "첫 번째 게시글 내용입니다.",
      "enabled": true
    }
  ],
  "schedule": {
    "interval_minutes": 30,
    "random_delay_minutes": 5,
    "start_time": "09:00",
    "end_time": "22:00"
  },
  "settings": {
    "headless": false,
    "auto_login": true,
    "rotate_posts": true,
    "log_level": "INFO"
  }
}
```

---

## ❓ 문제 해결

### Q: EXE 실행 시 Windows Defender 경고

A: "추가 정보" > "실행" 클릭 (안전한 파일입니다)

### Q: Python 설치 없이 사용하고 싶어요

A: Releases에서 EXE 파일 다운로드하거나 직접 빌드하세요

### Q: tkinter 오류 발생 시

A: Python 재설치 또는 `sudo apt-get install python3-tk` (Linux)

### Q: Chrome Driver 오류

A: Chrome 브라우저 설치 필요 (자동으로 드라이버 다운로드됨)

### Q: [WinError 193] Win32 응용 프로그램 오류 ⚠️ 중요

**증상**: `[WinError 193] %1은(는) 올바른 Win32 응용 프로그램이 아닙니다`

**원인**: WebDriver Manager 캐시 손상

**🚀 즉시 해결 (추천)**:
```cmd
긴급수정_실행.bat 더블클릭
```

**해결 방법** (아래 중 하나 선택):

1. **원클릭 수정 (최우선 추천)** ⭐⭐⭐
   - `긴급수정_실행.bat` 파일 더블클릭
   - 자동으로 캐시 정리 → 프로그램 재시작

2. **자동 정리 스크립트**
   ```bash
   # Python 스크립트 실행
   python clear_cache.py
   
   # 또는 배치 파일 더블클릭
   clear_cache.bat
   ```

3. **수동 정리**
   - Windows 탐색기에서 `C:\Users\사용자명\.wdm` 폴더 삭제
   - 프로그램 재실행

4. **자세한 가이드**: [CHROMEDRIVER_FIX.md](CHROMEDRIVER_FIX.md) 참조

**최신 코드 사용 중이라면**:
- 프로그램이 자동으로 3가지 방법 시도
- 1) ChromeDriverManager 자동 수정
- 2) Selenium Manager 폴백
- 3) 캐시 자동 정리 후 재시도

### Q: 로그인 실패

A: 네이버 2단계 인증 해제 또는 CAPTCHA 수동 입력

---

## ⚠️ 주의사항

⚠️ **중요**: 이 프로그램은 교육 목적으로 제작되었습니다.

- 네이버 이용약관을 준수하여 사용하세요
- 과도한 자동화는 계정 제재를 받을 수 있습니다
- 적절한 포스팅 간격을 설정하세요 (최소 30분 권장)
- 로그인 정보는 안전하게 관리하세요

---

## 📄 라이선스

MIT License

---

## 🤝 기여

버그 리포트나 기능 제안은 [Issues](https://github.com/rpaakdi1-spec/naver-band-auto-poster/issues)에 등록해주세요.

---

## 📝 변경 이력

### v1.0.0 (2026-01-15)
- 초기 버전 릴리스
- GUI 인터페이스 추가
- 자동 로그인 기능
- 스케줄 포스팅 기능
- 다중 포스트 관리
- EXE 빌드 지원 추가
