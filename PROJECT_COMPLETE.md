# ✅ 네이버밴드 자동 포스팅 프로그램 완성!

## 🎉 프로젝트 생성 완료

**GitHub 저장소**: https://github.com/rpaakdi1-spec/naver-band-auto-poster

깨끗하게 새로 시작한 네이버밴드 자동 포스팅 프로그램이 완성되었습니다!

---

## 📦 프로젝트 구조

```
naver-band-auto-poster/
├── src/
│   ├── __init__.py           # 패키지 초기화
│   ├── band_poster.py        # 핵심 포스팅 엔진
│   └── gui.py                # GUI 인터페이스
├── config/
│   └── config.example.json   # 설정 예시 파일
├── logs/                     # 로그 디렉토리 (자동 생성)
├── requirements.txt          # Python 패키지 목록
├── run.py                    # 메인 실행 파일
├── .gitignore               # Git 무시 파일
└── README.md                # 프로젝트 문서
```

---

## 🎯 주요 기능

### 기본 자동 포스팅
- ✅ **자동 로그인**: 네이버 계정 자동 로그인
- ✅ **스케줄 포스팅**: 설정한 시간 간격으로 자동 포스팅
- ✅ **다중 포스트 관리**: 여러 개의 포스팅 내용을 등록하고 관리
- ✅ **순환/랜덤 포스팅**: 포스트를 순환 또는 랜덤으로 선택
- ✅ **시간대 설정**: 포스팅 활성 시간대 설정 (예: 09:00 ~ 22:00)
- ✅ **랜덤 딜레이**: 자연스러운 포스팅을 위한 랜덤 딜레이
- ✅ **GUI 인터페이스**: 사용하기 쉬운 그래픽 인터페이스
- ✅ **로깅**: 모든 활동 로그 기록

---

## 🚀 설치 및 실행

### 1. 저장소 클론

```bash
git clone https://github.com/rpaakdi1-spec/naver-band-auto-poster.git
cd naver-band-auto-poster
```

### 2. 패키지 설치

```bash
pip install -r requirements.txt
```

필요한 패키지:
- `selenium==4.16.0` - 웹 자동화
- `webdriver-manager==4.0.1` - Chrome 드라이버 자동 관리
- `schedule==1.2.1` - 스케줄링
- `pyperclip==1.8.2` - 클립보드 관리

### 3. 프로그램 실행

```bash
python run.py
```

---

## 📖 사용 방법

### GUI에서 설정하기

1. **로그인 정보 입력**
   - 네이버 ID 입력
   - 비밀번호 입력
   - 밴드 URL 입력 (예: https://band.us/band/12345678)

2. **스케줄 설정**
   - 포스팅 간격(분): 기본 30분
   - 랜덤 딜레이(분): 기본 5분
   - 시작 시간: 09:00
   - 종료 시간: 22:00

3. **포스팅 내용 추가**
   - 포스트 내용 입력란에 내용 작성
   - "추가" 버튼 클릭하여 목록에 추가
   - 여러 개의 포스트 등록 가능

4. **설정 저장**
   - "설정 저장" 버튼 클릭
   - `config/config.json` 파일에 저장됨

5. **실행**
   - **시작** 버튼: 자동 포스팅 시작
   - **중지** 버튼: 자동 포스팅 중지
   - **수동 실행** 버튼: 즉시 한 번 포스팅

---

## ⚙️ 설정 파일 예시

`config/config.json`:

```json
{
  "naver_id": "your_id",
  "naver_password": "your_password",
  "band_url": "https://band.us/band/xxxxx",
  "posts": [
    {
      "content": "첫 번째 게시글 내용입니다.",
      "enabled": true
    },
    {
      "content": "두 번째 게시글 내용입니다.",
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
    "rotate_posts": true,
    "log_level": "INFO"
  }
}
```

---

## 💻 코드 구조

### `src/band_poster.py` - 핵심 엔진

주요 클래스와 메서드:

```python
class BandPoster:
    def init_driver()           # Chrome 드라이버 초기화
    def login()                 # 네이버 로그인
    def navigate_to_band()      # 밴드 페이지 이동
    def post_message(content)   # 메시지 포스팅
    def get_next_post()         # 다음 포스트 가져오기
    def is_within_schedule()    # 스케줄 시간 확인
    def run_once()              # 한 번 실행
```

### `src/gui.py` - GUI 인터페이스

주요 기능:
- Tkinter 기반 그래픽 인터페이스
- 설정 입력 및 저장
- 포스트 관리 (추가/삭제)
- 실시간 로그 표시
- 시작/중지/수동 실행 버튼

---

## 📊 로깅

모든 활동은 자동으로 로그 파일에 기록됩니다:

```
logs/band_poster_YYYYMMDD.log
```

로그 내용:
- 드라이버 초기화
- 로그인 시도 및 결과
- 포스팅 시도 및 결과
- 오류 메시지
- 스케줄 정보

---

## ⚠️ 주의사항

### 사용 시 유의사항

- ⚠️ **네이버 이용약관** 준수
- ⚠️ **계정 제재** 방지를 위한 적절한 간격 설정
- ⚠️ **최소 30분 이상** 포스팅 간격 권장
- ⚠️ **로그인 정보** 안전하게 관리
- ⚠️ **과도한 사용** 자제

### 보안

- `config/config.json` 파일은 `.gitignore`에 포함되어 있음
- 비밀번호를 코드에 하드코딩하지 마세요
- 공개 저장소에 설정 파일을 올리지 마세요

---

## 🐛 문제 해결

### Chrome 드라이버 오류

**문제**: Chrome 드라이버를 찾을 수 없음

**해결**: 
```bash
pip install --upgrade webdriver-manager
```

### 로그인 실패

**원인**:
- 네이버 2단계 인증 활성화
- CAPTCHA 발생
- 잘못된 계정 정보

**해결**:
- 2단계 인증 해제
- CAPTCHA 수동 입력
- 계정 정보 확인

### 포스팅 실패

**원인**:
- 밴드 페이지 구조 변경
- 네트워크 오류
- 권한 부족

**해결**:
- 로그 파일 확인
- 밴드 URL 확인
- 수동으로 밴드 접속 테스트

---

## 🔧 개발자 정보

### 기술 스택

- **Python** 3.8+
- **Selenium** 4.16.0 - 웹 자동화
- **Tkinter** - GUI 프레임워크
- **Schedule** - 작업 스케줄링
- **WebDriver Manager** - 드라이버 자동 관리

### 코드 스타일

- PEP 8 준수
- Type hints 사용
- Docstring 포함
- 에러 핸들링

---

## 📈 향후 개발 계획

- [ ] 이미지 첨부 기능
- [ ] 여러 밴드 동시 관리
- [ ] 웹 대시보드
- [ ] 통계 및 분석
- [ ] 데이터베이스 연동
- [ ] API 서버 모드

---

## 🤝 기여하기

버그 리포트나 기능 제안:
https://github.com/rpaakdi1-spec/naver-band-auto-poster/issues

Pull Request 환영합니다!

---

## 📄 라이선스

MIT License

---

## 🎉 완성!

깨끗하게 새로 시작한 네이버밴드 자동 포스팅 프로그램이 완성되었습니다!

### Git 커밋 정보

```
Commit: 8cd28b7
Message: feat: Complete rewrite - Naver Band Auto Poster
Branch: main
```

### GitHub 저장소

https://github.com/rpaakdi1-spec/naver-band-auto-poster

---

**즐거운 코딩 되세요! 🚀**
