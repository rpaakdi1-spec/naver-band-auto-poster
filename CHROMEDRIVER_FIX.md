# ChromeDriver 오류 해결 가이드

## 문제 설명
```
[WinError 193] %1은(는) 올바른 Win32 응용 프로그램이 아닙니다
```

이 오류는 WebDriver Manager가 잘못된 파일(THIRD_PARTY_NOTICES)을 실행 파일로 인식할 때 발생합니다.

## 해결 방법

### 방법 1: 캐시 삭제 (가장 간단) ⭐ 추천

WebDriver Manager의 캐시를 삭제하고 다시 다운로드합니다:

1. **Windows 탐색기**에서 다음 경로로 이동:
   ```
   C:\Users\WITHUS\.wdm
   ```

2. `.wdm` 폴더를 **완전히 삭제**

3. 프로그램을 다시 실행하면 자동으로 올바른 드라이버를 다운로드합니다.

### 방법 2: 명령 프롬프트로 캐시 삭제

```cmd
# 명령 프롬프트(CMD)를 관리자 권한으로 실행
rd /s /q "C:\Users\WITHUS\.wdm"
```

### 방법 3: Python 스크립트로 캐시 정리

프로젝트 폴더에 `clear_cache.py` 파일을 생성하여 실행:

```python
import os
import shutil

# WebDriver Manager 캐시 경로
cache_path = os.path.expanduser("~/.wdm")

if os.path.exists(cache_path):
    print(f"캐시 삭제 중: {cache_path}")
    shutil.rmtree(cache_path)
    print("캐시 삭제 완료!")
else:
    print("캐시 폴더가 없습니다.")
```

### 방법 4: 코드 수정 (이미 적용됨)

`src/band_poster.py`에 자동 복구 로직이 추가되었습니다:
- ChromeDriverManager 실패 시 Selenium Manager 자동 사용
- 잘못된 파일 경로 자동 수정

## 코드 변경 사항

기존 코드를 아래와 같이 개선했습니다:

```python
def _init_driver(self):
    """크롬 드라이버 초기화"""
    chrome_options = Options()
    
    # ... 옵션 설정 ...
    
    # ChromeDriverManager 캐시 문제 해결
    try:
        driver_path = ChromeDriverManager(cache_valid_range=1).install()
        
        # 잘못된 파일 경로 수정
        if 'THIRD_PARTY_NOTICES' in driver_path:
            import os
            driver_dir = os.path.dirname(driver_path)
            if os.path.exists(os.path.join(driver_dir, 'chromedriver.exe')):
                driver_path = os.path.join(driver_dir, 'chromedriver.exe')
            elif os.path.exists(os.path.join(os.path.dirname(driver_dir), 'chromedriver.exe')):
                driver_path = os.path.join(os.path.dirname(driver_dir), 'chromedriver.exe')
        
        service = Service(driver_path)
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        self.logger.error(f"ChromeDriverManager 오류: {str(e)}")
        self.logger.info("Selenium Manager로 자동 설치 시도 중...")
        # Selenium 4.6+ 의 자동 드라이버 관리 사용
        self.driver = webdriver.Chrome(options=chrome_options)
```

## 추가 확인 사항

### Chrome 브라우저 버전 확인

1. Chrome 브라우저 열기
2. 주소창에 입력: `chrome://settings/help`
3. 버전 확인 (예: 143.0.7499.192)

### Selenium 버전 확인

```cmd
pip show selenium
```

**권장 버전**: Selenium 4.6 이상

## 예방 조치

### 의존성 업데이트

```cmd
pip install --upgrade selenium webdriver-manager
```

### requirements.txt 업데이트

```txt
selenium>=4.16.0
webdriver-manager>=4.0.1
```

## 문제가 계속될 경우

1. **Python 재시작**: Python 인터프리터 완전히 종료 후 재실행
2. **Chrome 업데이트**: Chrome 브라우저를 최신 버전으로 업데이트
3. **관리자 권한**: 프로그램을 관리자 권한으로 실행
4. **방화벽/백신**: 일시적으로 비활성화하여 테스트

## 참고

- WebDriver Manager는 첫 실행 시 인터넷에서 ChromeDriver를 자동 다운로드합니다.
- 캐시 경로: `C:\Users\사용자명\.wdm\drivers\chromedriver\`
- Selenium 4.6+ 부터는 Selenium Manager가 내장되어 webdriver-manager 없이도 작동합니다.
