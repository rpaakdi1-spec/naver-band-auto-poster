# 🎉 네이버밴드 안전 매크로 완성!

## 📦 추가된 파일들

### 핵심 파일
- ✅ `src/safe_band_macro.py` - 안전 타이핑 매크로 클래스
- ✅ `examples_safe_macro.py` - 5가지 사용 예시
- ✅ `start_chrome_debug.bat` - Chrome 디버깅 모드 실행
- ✅ `run_safe_macro.bat` - 매크로 실행 스크립트

### 문서
- ✅ `SAFE_MACRO_GUIDE.md` - 상세 사용 가이드
- ✅ `QUICKSTART_SAFE_MACRO.md` - 빠른 시작 가이드
- ✅ `README.md` - 업데이트됨 (v1.1.0 기능 추가)

### 설정
- ✅ `requirements.txt` - pyperclip 추가

---

## 🚀 사용 방법

### 1. Chrome 디버깅 모드 실행

```cmd
start_chrome_debug.bat
```

### 2. 네이버밴드 로그인 및 채팅방 열기

### 3. 매크로 실행

#### 옵션 A: 간단 테스트
```bash
python src/safe_band_macro.py --test
```

#### 옵션 B: 대화형 예시
```bash
python examples_safe_macro.py
```

#### 옵션 C: Windows 실행 스크립트
```cmd
run_safe_macro.bat
```

---

## ✨ 주요 기능

### 1. 안전한 자동화
- **Chrome 디버깅 모드**: 기존 로그인 세션 활용
- **자연스러운 타이핑**: 사람처럼 타이핑하여 감지 방지
- **수동 전송 기본**: 안전한 수동 Enter 방식

### 2. 한글 완벽 지원
- **pyperclip 활용**: 클립보드를 통한 안정적인 한글 입력
- **타이핑 시뮬레이션**: 자연스러운 입력 속도

### 3. 스팸 방지
- **메시지 변형**: 자동으로 시간, 이모지 추가
- **랜덤 딜레이**: 자연스러운 간격
- **간격 조절**: 최소 5분 권장

### 4. 편리한 기능
- **화물 정보 템플릿**: `create_freight_message()` 함수
- **연속 전송 모드**: 설정한 간격으로 자동 반복
- **로깅**: 모든 활동 기록

---

## 📝 사용 예시

### 예시 1: 단순 메시지 전송

```python
from src.safe_band_macro import SafeBandTypingMacro

macro = SafeBandTypingMacro()
macro.send_message("안녕하세요! 테스트입니다.")
```

### 예시 2: 화물 정보 전송

```python
from src.safe_band_macro import SafeBandTypingMacro, create_freight_message

macro = SafeBandTypingMacro()

freight_msg = create_freight_message(
    truck_type="5톤 윙바디",
    pickup_location="서울 강남구",
    pickup_time="오후 2시",
    dropoff_location="부산 해운대구",
    dropoff_time="내일 오전",
    cargo_info="파렛트 15개",
    price="45만원",
    contact="010-1234-5678"
)

macro.send_message(freight_msg)
```

### 예시 3: 연속 전송 (5분 간격)

```python
macro.run_continuous(
    base_message=freight_msg,
    interval_minutes=5,
    max_sends=10,
    auto_send=False,  # 수동 전송 (안전)
    vary_message=True  # 메시지 변형
)
```

---

## 🎯 명령줄 옵션

```bash
# 테스트 (1회만)
python src/safe_band_macro.py --test

# 10분 간격, 5회 전송
python src/safe_band_macro.py --interval 10 --max-sends 5

# 자동 전송 (위험!)
python src/safe_band_macro.py --test --auto-send

# 다른 포트 사용
python src/safe_band_macro.py --port 9223 --test
```

---

## ⚠️ 안전 수칙

### ✅ 해야 할 것
- ✅ 수동 전송 모드 사용 (기본값)
- ✅ 최소 5분 이상 간격
- ✅ 메시지 변형 활성화
- ✅ 하루 최대 20회 이하

### ❌ 하지 말아야 할 것
- ❌ 1분 이하 짧은 간격
- ❌ 동일 메시지 반복
- ❌ 100회 이상 연속
- ❌ 스팸성 콘텐츠

---

## 🐛 문제 해결

### 문제: "크롬 연결 실패" 오류
**해결:**
1. 모든 Chrome 프로세스 종료
2. `start_chrome_debug.bat` 실행
3. 매크로 다시 실행

### 문제: "채팅 입력창을 찾을 수 없습니다"
**해결:**
1. 네이버밴드 채팅방이 열려있는지 확인
2. 페이지 새로고침
3. 수동으로 입력창 클릭 후 재시도

### 문제: 한글 입력이 안됨
**해결:**
```bash
pip install pyperclip
```

Linux의 경우:
```bash
sudo apt-get install xclip
pip install pyperclip
```

---

## 📊 로그 확인

모든 활동은 자동으로 기록됩니다:

```
logs/safe_macro_YYYYMMDD.log
```

로그에서 확인 가능한 정보:
- 연결 상태
- 메시지 전송 결과
- 오류 정보
- 타이밍 정보

---

## 🔧 고급 기능

### 메시지 변형 커스터마이징

```python
# 타임스탬프만 추가
msg = macro.generate_varied_message(base, add_prefix=False)

# 이모지만 추가
msg = macro.generate_varied_message(base, add_timestamp=False)

# 둘 다 추가 (기본값)
msg = macro.generate_varied_message(base)
```

### 현재 페이지 정보 확인

```python
info = macro.get_current_page_info()
print(f"URL: {info['url']}")
print(f"제목: {info['title']}")
print(f"밴드 페이지: {info['is_band']}")
```

---

## 📚 문서

1. **[QUICKSTART_SAFE_MACRO.md](QUICKSTART_SAFE_MACRO.md)** - 빠른 시작 (5분)
2. **[SAFE_MACRO_GUIDE.md](SAFE_MACRO_GUIDE.md)** - 상세 가이드
3. **[examples_safe_macro.py](examples_safe_macro.py)** - 실행 가능한 예시
4. **[README.md](README.md)** - 전체 프로젝트 문서

---

## 🎓 학습 자료

### Chrome 디버깅 모드란?
Chrome을 원격 제어 가능한 모드로 실행하는 방법입니다.
- 기존 로그인 유지
- 여러 자동화 도구 연결 가능
- 개발자 도구 항상 접근 가능

### Selenium이란?
웹 브라우저를 자동화하는 도구입니다.
- 웹 페이지 자동 조작
- 테스트 자동화
- 웹 스크래핑

---

## 💡 팁과 트릭

### 팁 1: 화물 정보 템플릿 활용
```python
# 기본 정보만 입력하고 나머지는 기본값 사용
msg = create_freight_message(
    pickup_location="서울",
    dropoff_location="부산",
    contact="010-1234-5678"
)
```

### 팁 2: 여러 화물 정보를 리스트로 관리
```python
freights = [
    {"pickup": "서울", "dropoff": "부산", ...},
    {"pickup": "인천", "dropoff": "대전", ...},
]

for freight in freights:
    msg = create_freight_message(**freight)
    macro.send_message(msg)
    time.sleep(300)  # 5분 대기
```

### 팁 3: 안전한 테스트
```python
# 먼저 짧은 메시지로 테스트
macro.send_message("테스트")

# 정상 작동 확인 후 실제 메시지 사용
macro.send_message(actual_message)
```

---

## 🔐 보안 주의사항

### ⚠️ 중요
1. **로그인 정보 관리**: 코드에 직접 넣지 마세요
2. **공개 저장소**: 설정 파일을 .gitignore에 추가
3. **계정 보호**: 과도한 사용 자제
4. **이용약관**: 네이버 이용약관 준수

### 권장 사항
- 환경 변수 사용
- 설정 파일 암호화
- 접근 권한 관리
- 정기적인 비밀번호 변경

---

## 📞 지원

### 도움이 필요하신가요?

1. **문서 확인**: SAFE_MACRO_GUIDE.md
2. **예시 실행**: examples_safe_macro.py
3. **로그 확인**: logs/ 디렉토리
4. **이슈 등록**: GitHub Issues

---

## 🎉 완성!

축하합니다! 네이버밴드 안전 타이핑 매크로가 준비되었습니다.

### 다음 단계:
1. ✅ Chrome 디버깅 모드 실행
2. ✅ 네이버밴드 로그인
3. ✅ 매크로 테스트
4. ✅ 안전하게 사용하기

**안전하고 책임감 있게 사용하세요! 🙏**

---

## 📄 라이선스

MIT License - 교육 목적으로 자유롭게 사용 가능

⚠️ **주의**: 이 도구는 교육 목적으로 제작되었습니다.
사용으로 인한 모든 책임은 사용자에게 있습니다.
