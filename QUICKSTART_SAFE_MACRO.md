# 🚀 안전 매크로 빠른 시작 가이드

네이버밴드 안전 타이핑 매크로를 5분 안에 시작하세요!

---

## ⚡ 3단계로 시작하기

### 1️⃣ 패키지 설치

```bash
pip install selenium webdriver-manager pyperclip
```

### 2️⃣ Chrome 디버깅 모드 실행

**Windows:**
```cmd
start_chrome_debug.bat
```

**Mac/Linux:**
```bash
# Mac
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=9222 \
  --user-data-dir="/tmp/chrome_dev_session"

# Linux
google-chrome --remote-debugging-port=9222 \
  --user-data-dir="/tmp/chrome_dev_session"
```

### 3️⃣ 네이버밴드 준비 & 실행

1. 디버깅 Chrome에서 네이버 로그인
2. 네이버밴드 채팅방 열기
3. 매크로 실행:

```bash
# 테스트 (1회만)
python src/safe_band_macro.py --test

# 또는 대화형 예시
python examples_safe_macro.py
```

---

## 💡 간단 사용 예시

```python
from src.safe_band_macro import SafeBandTypingMacro, create_freight_message

# 매크로 초기화
macro = SafeBandTypingMacro()

# 화물 정보 생성
msg = create_freight_message(
    truck_type="5톤 윙바디",
    pickup_location="서울 강남구",
    dropoff_location="부산 해운대구",
    contact="010-1234-5678"
)

# 전송 (수동 Enter)
macro.send_message(msg)
```

---

## 🎯 주요 명령어

| 명령어 | 설명 |
|--------|------|
| `--test` | 테스트 모드 (1회만) |
| `--interval 5` | 5분 간격 |
| `--max-sends 10` | 최대 10회 |
| `--auto-send` | 자동 전송 (⚠️) |

### 사용 예시:

```bash
# 10분 간격, 5회 전송
python src/safe_band_macro.py --interval 10 --max-sends 5

# 자동 전송 테스트 (위험!)
python src/safe_band_macro.py --test --auto-send
```

---

## ⚠️ 중요 안전 수칙

✅ **권장사항:**
- 수동 전송 모드 사용 (`--auto-send` 없이)
- 최소 5분 이상 간격
- 메시지 변형 활성화
- 하루 최대 20회 이하

❌ **금지사항:**
- 1분 이하 짧은 간격
- 동일 메시지 반복
- 100회 이상 연속
- 스팸성 콘텐츠

---

## 🐛 문제 해결

### "크롬 연결 실패"
👉 Chrome을 디버깅 모드로 다시 실행

### "입력창을 찾을 수 없습니다"
👉 네이버밴드 채팅방이 열려있는지 확인

### 한글 입력 안됨
👉 `pip install pyperclip` 설치

---

## 📚 더 알아보기

- 📖 [상세 가이드](SAFE_MACRO_GUIDE.md)
- 💻 [사용 예시](examples_safe_macro.py)
- 🏠 [메인 README](README.md)

---

**🎉 준비 완료! 안전하게 사용하세요.**
