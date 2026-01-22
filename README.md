# 네이버밴드 자동 포스팅 프로그램 (다중 채팅방)

네이버밴드 여러 채팅방에 동시에 메시지를 자동 포스팅하는 프로그램입니다.

## 🎯 주요 기능

- 🌐 **Chrome 자동 실행**: Chrome 브라우저가 자동으로 실행됩니다
- 👤 **수동 로그인**: 브라우저에서 직접 로그인 (보안 강화)
- 📱 **다중 채팅방 지원**: 여러 채팅방에 동시 포스팅
- ⏰ **스케줄 포스팅**: 설정한 시간 간격으로 자동 포스팅
- 📝 **다중 포스트 관리**: 여러 개의 포스팅 내용을 등록하고 관리
- 🔄 **순환/랜덤 포스팅**: 포스트를 순환 또는 랜덤으로 선택
- 🎯 **시간대 설정**: 포스팅 활성 시간대 설정 (예: 09:00 ~ 22:00)
- 🎲 **랜덤 딜레이**: 자연스러운 포스팅을 위한 랜덤 딜레이
- 🖥️ **GUI 인터페이스**: 사용하기 쉬운 그래픽 인터페이스
- 📊 **로깅**: 모든 활동 로그 기록

## 🚀 빠른 시작

### 설치

```bash
# 저장소 클론
git clone https://github.com/rpaakdi1-spec/naver-band-auto-poster.git
cd naver-band-auto-poster

# 패키지 설치
pip install -r requirements.txt
```

### 실행

```bash
# GUI 프로그램 실행
python run.py
```

## 📖 사용 방법

### 1️⃣ 채팅방 URL 추가

GUI에서 "채팅방 URL 관리" 섹션에 채팅방 URL을 추가합니다:

```
예시:
https://www.band.us/band/54748329/chat/CevDKF
https://www.band.us/band/50213411/chat/CiD8Bg
https://www.band.us/band/71531986/chat/CYEcnV
```

- URL 입력 후 "추가" 버튼 클릭
- 여러 개의 채팅방 URL을 등록할 수 있습니다
- 삭제/전체 삭제 버튼으로 관리

### 2️⃣ 스케줄 설정

- **포스팅 간격 (분)**: 포스팅 반복 주기 (기본: 30분)
- **랜덤 딜레이 (분)**: 포스팅 후 랜덤 대기 (기본: 5분)
- **시작/종료 시간**: 포스팅 활성 시간대 (기본: 09:00 ~ 22:00)
- **채팅방 간격 (초)**: 채팅방 간 대기 시간 (기본: 3초)

### 3️⃣ 포스팅 내용 추가

- 포스트 내용 입력란에 메시지 작성
- "추가" 버튼 클릭
- 여러 개의 포스트 등록 가능
- 순환 또는 랜덤 선택 가능

### 4️⃣ 설정 저장

- "설정 저장" 버튼 클릭
- `config/config.json` 파일에 저장됨

### 5️⃣ 실행

**수동 실행 (권장)**:
1. "수동 실행" 버튼 클릭
2. Chrome 브라우저 자동 실행
3. 브라우저에서 밴드 로그인 (수동)
4. 콘솔에서 Enter 키 입력
5. 모든 채팅방에 자동 포스팅

**자동 실행**:
- "시작" 버튼: 스케줄에 따라 자동 포스팅
- "중지" 버튼: 자동 포스팅 중지

## ⚙️ 설정 파일

`config/config.json` 예시:

```json
{
  "chat_urls": [
    "https://www.band.us/band/54748329/chat/CevDKF",
    "https://www.band.us/band/50213411/chat/CiD8Bg",
    "https://www.band.us/band/71531986/chat/CYEcnV"
  ],
  "posts": [
    {
      "content": "안녕하세요! 첫 번째 메시지입니다.",
      "enabled": true
    },
    {
      "content": "두 번째 메시지 내용입니다.",
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
    "rotate_chats": true,
    "log_level": "INFO",
    "wait_after_post": 2,
    "wait_between_chats": 3
  }
}
```

## 🔄 동작 방식

### 포스팅 프로세스

```
1. Chrome 실행 및 로그인 (수동)
   ↓
2. 포스트 선택 (순환 또는 랜덤)
   ↓
3. 첫 번째 채팅방 이동
   ↓
4. 메시지 입력 및 전송
   ↓
5. 3초 대기 (설정값)
   ↓
6. 다음 채팅방 이동
   ↓
7. 반복 (모든 채팅방 완료까지)
   ↓
8. 랜덤 딜레이 (0~5분)
   ↓
9. 다음 포스팅 대기
```

### 순환 vs 랜덤

**포스트 순환**:
- ✅ 체크: 포스트를 순서대로 사용
- ❌ 해제: 포스트를 랜덤으로 선택

**채팅방 순환**:
- ✅ 체크: 채팅방을 순서대로 방문
- ❌ 해제: 채팅방을 랜덤으로 방문

## 🔒 보안 개선

이 프로그램은 자동 로그인 기능을 제거하고 **수동 로그인**을 사용합니다:

- ✅ 로그인 정보를 저장하지 않음
- ✅ 브라우저에서 직접 로그인
- ✅ 2단계 인증 지원
- ✅ 보안 강화

## ⚠️ 주의사항

- 네이버 이용약관을 준수하여 사용하세요
- 과도한 자동화는 계정 제재를 받을 수 있습니다
- 적절한 포스팅 간격을 설정하세요 (최소 30분 권장)
- 채팅방 간격은 최소 3초 이상 설정하세요
- 스팸으로 간주되지 않도록 주의하세요

## 📝 사용 예시

### 예시 1: 20개 채팅방에 하루 3회 포스팅

```json
{
  "chat_urls": [
    "https://www.band.us/band/...",
    // ... 20개 URL
  ],
  "schedule": {
    "interval_minutes": 480,  // 8시간마다
    "random_delay_minutes": 30,
    "start_time": "09:00",
    "end_time": "21:00"
  }
}
```

### 예시 2: 5개 채팅방에 시간당 1회 포스팅

```json
{
  "chat_urls": [
    "https://www.band.us/band/...",
    // ... 5개 URL
  ],
  "schedule": {
    "interval_minutes": 60,  // 1시간마다
    "random_delay_minutes": 10,
    "start_time": "09:00",
    "end_time": "18:00"
  }
}
```

## 📄 라이선스

MIT License

## 🤝 기여

버그 리포트나 기능 제안은 Issues에 등록해주세요.

## 🔗 GitHub

https://github.com/rpaakdi1-spec/naver-band-auto-poster

---

**v2.0 업데이트**: 다중 채팅방 지원 추가 🎉
