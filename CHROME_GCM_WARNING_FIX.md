# Chrome GCM 경고 메시지 해결

## 🔍 문제

프로그램 실행 시 다음과 같은 에러 메시지가 출력됩니다:

```
[5628:15168:0122/133412.338:ERROR:google_apis\gcm\engine\registration_request.cc:292]
Registration response error message: DEPRECATED_ENDPOINT
```

## 📋 원인

- **Chrome 내부 동작**: Google Cloud Messaging (GCM) 서비스 등록 시도
- **Deprecated 엔드포인트**: 사용 중인 API 엔드포인트가 더 이상 사용되지 않음
- **Selenium과 무관**: Chrome 브라우저 자체의 내부 메시지

## ✅ 영향 없음

이 에러는 **프로그램 동작에 전혀 영향을 주지 않습니다**:

- ✅ Chrome 실행: 정상
- ✅ 로그인: 정상
- ✅ 포스팅: 정상
- ⚠️ 콘솔에 경고 메시지만 출력됨

## 🛠️ 해결 방법

### Chrome 옵션 추가

Chrome의 로그 레벨을 조정하여 불필요한 경고 메시지를 숨깁니다:

```python
chrome_options = Options()
chrome_options.add_argument('--log-level=3')  # FATAL만 표시
chrome_options.add_argument('--disable-logging')  # Chrome 로깅 비활성화
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
```

### 옵션 설명

| 옵션 | 설명 |
|------|------|
| `--log-level=3` | 로그 레벨을 3(FATAL)으로 설정하여 심각한 오류만 표시 |
| `--disable-logging` | Chrome 내부 로깅 비활성화 |
| `excludeSwitches: ["enable-logging"]` | 로깅 스위치 제외 |

### 로그 레벨

```
0 = INFO     (모든 정보)
1 = WARNING  (경고)
2 = ERROR    (에러)
3 = FATAL    (치명적 오류만)
```

## 📝 적용 결과

### 적용 전
```
[5628:15168:0122/133412.338:ERROR:google_apis\gcm\engine\registration_request.cc:292]
Registration response error message: DEPRECATED_ENDPOINT
[INFO] Chrome 드라이버 초기화 완료
...
```

### 적용 후
```
[INFO] Chrome 드라이버 초기화 완료
...
```

**깔끔한 콘솔 출력**으로 중요한 로그만 확인할 수 있습니다.

## 🔗 관련 정보

### 다른 Chrome 경고 메시지

다음과 같은 메시지들도 무시해도 됩니다:

```
DevTools listening on ws://...
USB: usb_device_handle_win.cc:...
Bluetooth: ...
```

이들은 모두 Chrome의 내부 동작 메시지이며 프로그램에 영향을 주지 않습니다.

### 추가 옵션

더 조용한 실행을 원한다면:

```python
chrome_options.add_argument('--silent')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--disable-software-rasterizer')
```

## ✅ 해결 완료

커밋 정보:
```
c603e2d fix: Suppress Chrome GCM deprecation warning messages
- Add --log-level=3 to show only FATAL errors
- Add --disable-logging to disable Chrome internal logging
- Add 'enable-logging' to excludeSwitches
- Resolves harmless GCM DEPRECATED_ENDPOINT warning
```

## 🚀 사용 방법

```bash
# 최신 코드 가져오기
git pull origin main

# 프로그램 실행
python run.py
```

이제 불필요한 경고 메시지 없이 깔끔한 콘솔 출력을 볼 수 있습니다! 🎉

---

**참고**: 만약 Chrome 관련 실제 오류가 발생한다면 `--log-level=1` 또는 `--log-level=2`로 변경하여 디버깅할 수 있습니다.
