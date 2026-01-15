# 네이버밴드 자동 포스팅 프로그램

네이버밴드 PC버전의 채팅방에 설정한 시간에 따라 주기적으로 글을 자동 포스팅하는 프로그램입니다.

## 주요 기능

- 🤖 **자동 로그인**: 네이버 계정 자동 로그인
- ⏰ **스케줄 포스팅**: 설정한 시간 간격으로 자동 포스팅
- 📝 **다중 포스트 관리**: 여러 개의 포스팅 내용을 등록하고 관리
- 🔄 **순환/랜덤 포스팅**: 포스트를 순환 또는 랜덤으로 선택
- 🎯 **시간대 설정**: 포스팅 활성 시간대 설정 (예: 09:00 ~ 22:00)
- 🎲 **랜덤 딜레이**: 자연스러운 포스팅을 위한 랜덤 딜레이
- 🖥️ **GUI 인터페이스**: 사용하기 쉬운 그래픽 인터페이스
- 📊 **로깅**: 모든 활동 로그 기록

## 시스템 요구사항

- Python 3.8 이상
- Chrome 브라우저
- Windows/macOS/Linux

## 설치 방법

### 1. Python 설치

먼저 Python 3.8 이상이 설치되어 있는지 확인하세요.

```bash
python --version
```

### 2. 프로젝트 다운로드

```bash
git clone <repository-url>
cd naver-band-auto-poster
```

### 3. 가상환경 생성 (권장)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 4. 패키지 설치

```bash
pip install -r requirements.txt
```

## 사용 방법

### GUI 버전 (권장)

```bash
python run.py
```

또는

```bash
python src/gui.py
```

### 설정 방법

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

### 커맨드라인 버전

```bash
python src/band_poster.py
```

설정 파일을 먼저 작성해야 합니다:

```bash
cp config/config.example.json config/config.json
# config/config.json 파일을 편집하여 설정 입력
```

## 설정 파일 구조

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
    "headless": false,
    "auto_login": true,
    "rotate_posts": true,
    "log_level": "INFO"
  }
}
```

### 설정 옵션 설명

- **naver_id**: 네이버 아이디
- **naver_password**: 네이버 비밀번호
- **band_url**: 밴드 URL
- **posts**: 포스팅할 내용 리스트
  - **content**: 게시글 내용
  - **enabled**: 활성화 여부
- **schedule**: 스케줄 설정
  - **interval_minutes**: 포스팅 간격 (분)
  - **random_delay_minutes**: 랜덤 딜레이 범위 (분)
  - **start_time**: 포스팅 시작 시간
  - **end_time**: 포스팅 종료 시간
- **settings**: 기타 설정
  - **headless**: 백그라운드 실행 여부
  - **auto_login**: 자동 로그인 여부
  - **rotate_posts**: 순환 포스팅 여부 (false면 랜덤)
  - **log_level**: 로그 레벨 (DEBUG/INFO/WARNING/ERROR)

## 로그 확인

로그 파일은 `logs/` 디렉토리에 날짜별로 저장됩니다:

```
logs/band_poster_20240115.log
```

## 문제 해결

### 로그인 실패

- 네이버 ID/비밀번호가 정확한지 확인
- 2단계 인증이 설정되어 있다면 임시로 해제
- CAPTCHA가 나타나는 경우 수동으로 해결 필요

### 포스팅 실패

- 밴드 URL이 정확한지 확인
- 밴드 접근 권한이 있는지 확인
- 로그 파일에서 자세한 오류 확인

### Chrome 드라이버 오류

프로그램이 자동으로 Chrome 드라이버를 다운로드합니다. 인터넷 연결을 확인하세요.

## 주의사항

⚠️ **중요**: 이 프로그램은 교육 목적으로 제작되었습니다.

- 네이버 이용약관을 준수하여 사용하세요
- 과도한 자동화는 계정 제재를 받을 수 있습니다
- 적절한 포스팅 간격을 설정하세요 (최소 30분 권장)
- 로그인 정보는 안전하게 관리하세요

## 라이선스

MIT License

## 기여

버그 리포트나 기능 제안은 이슈로 등록해주세요.

## 변경 이력

### v1.0.0 (2024-01-15)
- 초기 버전 릴리스
- GUI 인터페이스 추가
- 자동 로그인 기능
- 스케줄 포스팅 기능
- 다중 포스트 관리
