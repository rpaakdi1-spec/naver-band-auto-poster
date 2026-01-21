# 네이버밴드 안전 타이핑 매크로 사용 가이드

## 🎯 개요

기존 Chrome 브라우저의 로그인 세션을 활용하여 안전하게 네이버밴드에 메시지를 전송하는 매크로입니다.

### ✨ 주요 특징

- **기존 세션 활용**: 로그인된 Chrome 세션을 사용하여 안전
- **자연스러운 타이핑**: 사람처럼 타이핑하여 자동화 감지 방지
- **한글 지원**: pyperclip을 통한 안정적인 한글 입력
- **메시지 변형**: 스팸 방지를 위한 자동 메시지 변형
- **수동/자동 전송**: 안전한 수동 전송 또는 자동 전송 선택 가능

---

## 🚀 빠른 시작

### 1단계: Chrome 디버깅 모드로 실행

매크로를 사용하기 전에 Chrome을 디버깅 모드로 실행해야 합니다.

#### Windows

```cmd
"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\chrome_dev_session"
```

또는 바로가기 만들기:
1. Chrome 바로가기 우클릭 → 속성
2. 대상 끝에 추가: ` --remote-debugging-port=9222 --user-data-dir="C:\chrome_dev_session"`

#### Mac

```bash
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222 --user-data-dir="/tmp/chrome_dev_session"
```

#### Linux

```bash
google-chrome --remote-debugging-port=9222 --user-data-dir="/tmp/chrome_dev_session"
```

### 2단계: 네이버밴드 로그인

디버깅 모드로 실행된 Chrome에서:
1. 네이버에 로그인
2. 네이버밴드 접속
3. 메시지를 보낼 채팅방 또는 밴드 열기

### 3단계: 매크로 실행

```bash
# 테스트 모드 (1회만 실행)
python src/safe_band_macro.py --test

# 연속 전송 모드
python src/safe_band_macro.py --interval 5 --max-sends 10

# 자동 전송 모드 (위험!)
python src/safe_band_macro.py --test --auto-send
```

---

## 📖 상세 사용법

### 기본 사용

```python
from src.safe_band_macro import SafeBandTypingMacro

# 매크로 초기화
macro = SafeBandTypingMacro(debug_port=9222)

# 메시지 전송 (수동 Enter)
message = "안녕하세요! 테스트 메시지입니다."
macro.send_message(message, auto_send=False)

# 매크로 종료
macro.close()
```

### 화물 정보 메시지 생성

```python
from src.safe_band_macro import create_freight_message

# 화물 정보 생성
freight_msg = create_freight_message(
    truck_type="5톤 윙바디",
    pickup_location="경기 이천",
    pickup_time="오후 2시",
    dropoff_location="부산 강서구",
    dropoff_time="내일 오전",
    cargo_info="파렛트 화물 15개",
    price="45만원",
    payment="현금/인수증",
    contact="010-1234-5678"
)

macro.send_message(freight_msg)
```

### 연속 전송

```python
# 5분 간격으로 최대 20회 전송
macro.run_continuous(
    base_message=freight_msg,
    interval_minutes=5,
    max_sends=20,
    auto_send=False,  # 수동 전송 (안전)
    vary_message=True  # 메시지 변형
)
```

---

## ⚙️ 명령줄 옵션

| 옵션 | 기본값 | 설명 |
|------|--------|------|
| `--port` | 9222 | Chrome 디버깅 포트 |
| `--test` | False | 테스트 모드 (1회만 실행) |
| `--auto-send` | False | 자동 전송 활성화 |
| `--interval` | 5 | 전송 간격 (분) |
| `--max-sends` | 20 | 최대 전송 횟수 |

### 사용 예시

```bash
# 1. 테스트 전송 (수동 Enter)
python src/safe_band_macro.py --test

# 2. 10분 간격으로 5회 전송
python src/safe_band_macro.py --interval 10 --max-sends 5

# 3. 자동 전송 (위험!)
python src/safe_band_macro.py --test --auto-send

# 4. 다른 포트 사용
python src/safe_band_macro.py --port 9223 --test
```

---

## 🔧 고급 기능

### 1. 메시지 변형

스팸 방지를 위해 메시지를 자동으로 변형합니다:

```python
# 기본 메시지
base = "5톤 윙바디 화물 수배\n상차: 서울\n하차: 부산"

# 변형된 메시지
varied = macro.generate_varied_message(
    base_template=base,
    add_timestamp=True,  # 시간 추가
    add_prefix=True      # 이모지 접두어 추가
)

# 결과 예시:
# 🚛 5톤 윙바디 화물 수배
# 상차: 서울
# 하차: 부산
# 
# (14:23 현재)
```

### 2. 커스텀 입력창 선택자

특정 입력창을 찾을 수 없는 경우:

```python
# 수동으로 입력창 지정
from selenium.webdriver.common.by import By

input_box = macro.driver.find_element(By.CSS_SELECTOR, "your-custom-selector")
macro.human_like_typing(input_box, "메시지 내용")
```

### 3. 페이지 정보 확인

```python
info = macro.get_current_page_info()
print(f"현재 URL: {info['url']}")
print(f"페이지 제목: {info['title']}")
print(f"밴드 페이지인가: {info['is_band']}")
```

---

## 📦 필요한 패키지

```bash
pip install selenium webdriver-manager pyperclip
```

### pyperclip 설치 (한글 입력 필수)

```bash
# Windows/Mac
pip install pyperclip

# Linux (추가 패키지 필요)
sudo apt-get install xclip  # 또는 xsel
pip install pyperclip
```

---

## ⚠️ 주의사항

### 안전 수칙

1. **수동 전송 권장**: `auto_send=False`로 설정하여 직접 Enter 입력
2. **적절한 간격**: 최소 5분 이상 간격 설정
3. **스팸 방지**: 메시지 변형 기능 활용
4. **계정 보호**: 과도한 사용 자제

### 금지 사항

⛔ **하지 말아야 할 것:**
- 1분 이하의 짧은 간격 설정
- 동일한 메시지 반복 전송
- 100회 이상 연속 전송
- 스팸성 콘텐츠 전송

### 법적 책임

⚠️ **중요**: 이 도구는 교육 목적으로 제작되었습니다.
- 네이버 이용약관을 준수하세요
- 스팸 또는 불법 활동에 사용하지 마세요
- 사용으로 인한 모든 책임은 사용자에게 있습니다

---

## 🐛 문제 해결

### Q1: "크롬 연결 실패" 오류

**원인**: Chrome이 디버깅 모드로 실행되지 않음

**해결**:
1. 모든 Chrome 프로세스 종료
2. 디버깅 모드로 Chrome 재실행
3. 포트 번호 확인 (기본: 9222)

### Q2: "채팅 입력창을 찾을 수 없습니다"

**원인**: 입력창 선택자가 페이지와 맞지 않음

**해결**:
1. Chrome DevTools (F12) 열기
2. 입력창 요소 검사
3. CSS 선택자 확인
4. `find_chat_input()` 메서드 수정

### Q3: 한글 입력이 안 됨

**원인**: pyperclip 미설치 또는 클립보드 접근 불가

**해결**:
```bash
# pyperclip 설치
pip install pyperclip

# Linux의 경우
sudo apt-get install xclip
```

### Q4: "포트가 이미 사용 중" 오류

**해결**:
```bash
# 다른 포트 사용
python src/safe_band_macro.py --port 9223 --test
```

Chrome 실행 시에도 동일한 포트 지정:
```bash
chrome.exe --remote-debugging-port=9223 --user-data-dir="C:\chrome_dev_session"
```

---

## 📊 로그 확인

모든 활동은 로그 파일에 기록됩니다:

```
logs/safe_macro_YYYYMMDD.log
```

로그 내용:
- 연결 상태
- 메시지 전송 결과
- 오류 정보
- 타이밍 정보

---

## 🔄 업데이트

### v1.0.0 (2026-01-21)
- 초기 버전 릴리스
- Chrome 디버깅 모드 지원
- 자연스러운 타이핑 구현
- 한글 입력 지원
- 메시지 변형 기능
- 연속 전송 모드

---

## 📞 지원

문제가 발생하면:
1. 로그 파일 확인
2. Chrome DevTools 콘솔 확인
3. 이슈 등록

---

## 📄 라이선스

MIT License - 교육 목적으로 자유롭게 사용 가능
