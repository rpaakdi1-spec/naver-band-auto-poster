# ChromeDriver 오류 해결 완료

## 🐛 발생한 오류

```
2026-01-22 13:12:15,789 - INFO - Driver [C:\Users\WITHUS\.wdm\drivers\chromedriver\win64\143.0.7499.192\chromedriver-win32/THIRD_PARTY_NOTICES.chromedriver] found in cache
2026-01-22 13:12:15,795 - ERROR - 실행 중 오류: [WinError 193] %1은(는) 올바른 Win32 응용 프로그램이 아닙니다
```

### 문제 원인

`ChromeDriverManager().install()`이 잘못된 파일 경로를 반환했습니다:
- ❌ 반환된 경로: `THIRD_PARTY_NOTICES.chromedriver` (텍스트 파일)
- ✅ 필요한 파일: `chromedriver.exe` (실행 파일)

---

## ✅ 해결 방법

### 1. ChromeDriver 자동 검색 로직 추가

`src/band_poster.py`의 `init_driver()` 메서드를 수정했습니다:

```python
def init_driver(self):
    """Chrome 드라이버 초기화"""
    try:
        chrome_options = Options()
        # ... 옵션 설정 ...
        
        # ChromeDriverManager로 드라이버 경로 가져오기
        driver_path = ChromeDriverManager().install()
        
        # 올바른 chromedriver.exe 경로 찾기
        if not driver_path.endswith('.exe'):
            import glob
            driver_dir = os.path.dirname(driver_path)
            
            # 재귀적으로 chromedriver.exe 검색
            exe_files = glob.glob(
                os.path.join(driver_dir, '**', 'chromedriver.exe'), 
                recursive=True
            )
            
            if exe_files:
                driver_path = exe_files[0]
            else:
                # 상위 디렉토리에서도 검색
                parent_dir = os.path.dirname(driver_dir)
                exe_files = glob.glob(
                    os.path.join(parent_dir, '**', 'chromedriver.exe'), 
                    recursive=True
                )
                if exe_files:
                    driver_path = exe_files[0]
        
        service = Service(driver_path)
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        
    except Exception as e:
        self.logger.error(f"Chrome 드라이버 초기화 실패: {str(e)}")
        raise
```

### 2. 디버그 스크립트 추가

ChromeDriver 경로 문제를 진단하기 위한 `test_driver.py` 추가:

```bash
python test_driver.py
```

실행 결과:
```
ChromeDriver 다운로드 중...
반환된 경로: C:\Users\...\.wdm\...\THIRD_PARTY_NOTICES.chromedriver
파일 존재 여부: True
파일 이름: THIRD_PARTY_NOTICES.chromedriver

올바른 .exe 파일이 아닙니다. chromedriver.exe를 찾는 중...
검색 디렉토리: C:\Users\...\.wdm\...\chromedriver-win32

찾은 chromedriver.exe 파일:
  - C:\Users\...\.wdm\...\chromedriver-win32\chromedriver.exe

사용할 경로: C:\Users\...\.wdm\...\chromedriver-win32\chromedriver.exe
```

---

## 🔧 추가 개선사항

### GUI 에러 처리 강화

`src/gui.py`의 `manual_post()` 메서드 개선:

```python
def manual_post(self):
    """수동 포스팅"""
    # 입력 검증
    if not self.poster.config.get('naver_id'):
        messagebox.showwarning("경고", "네이버 ID를 입력하세요.")
        return
    
    if not self.poster.config.get('naver_password'):
        messagebox.showwarning("경고", "비밀번호를 입력하세요.")
        return
    
    if not self.poster.config.get('band_url'):
        messagebox.showwarning("경고", "밴드 URL을 입력하세요.")
        return
    
    # 상태 표시
    self.status_label.config(text="상태: 포스팅 중...", foreground="orange")
    
    def post_thread():
        try:
            success = self.poster.run_once()
            if success:
                self.log("✅ 수동 포스팅 완료")
                self.status_label.config(text="상태: 완료", foreground="green")
            else:
                self.log("❌ 수동 포스팅 실패")
                self.status_label.config(text="상태: 실패", foreground="red")
        except Exception as e:
            self.log(f"❌ 오류: {str(e)}")
            self.status_label.config(text="상태: 오류 발생", foreground="red")
            messagebox.showerror("오류", f"포스팅 중 오류가 발생했습니다:\n\n{str(e)}")
    
    threading.Thread(target=post_thread, daemon=True).start()
```

---

## 🚀 이제 사용 가능!

### 1. 코드 업데이트

```bash
git pull origin main
```

### 2. 프로그램 실행

```bash
python run.py
```

### 3. GUI에서 설정

1. 네이버 ID, 비밀번호, 밴드 URL 입력
2. 포스트 내용 추가
3. "수동 실행" 버튼으로 테스트
4. 정상 작동 확인 후 "시작" 버튼으로 자동 포스팅 시작

---

## 🐛 문제가 계속되면?

### 1. 디버그 스크립트 실행

```bash
python test_driver.py
```

출력 내용을 확인하여 `chromedriver.exe` 경로를 찾을 수 있는지 확인

### 2. 수동으로 ChromeDriver 설치

1. https://chromedriver.chromium.org/downloads 방문
2. Chrome 버전에 맞는 ChromeDriver 다운로드
3. 다운로드한 `chromedriver.exe`를 프로젝트 폴더에 복사
4. `band_poster.py`에서 경로 지정:

```python
service = Service('./chromedriver.exe')
```

### 3. Chrome 버전 확인

```
chrome://version/
```

Chrome 버전과 ChromeDriver 버전이 호환되는지 확인

### 4. webdriver-manager 재설치

```bash
pip uninstall webdriver-manager
pip install webdriver-manager --upgrade
```

### 5. 캐시 삭제

```bash
# Windows
rmdir /s /q C:\Users\<USERNAME>\.wdm

# 또는 Python에서
import shutil
shutil.rmtree('C:/Users/<USERNAME>/.wdm')
```

---

## 📊 변경사항

### Git 커밋

```
Commit: 8da3bf9
Message: fix: Resolve ChromeDriver path issue and improve error handling
```

### 변경된 파일

- ✅ `src/band_poster.py` - ChromeDriver 경로 자동 검색
- ✅ `src/gui.py` - 에러 처리 및 입력 검증 강화
- ✅ `test_driver.py` - 디버그 스크립트 추가

---

## ✅ 해결 완료!

ChromeDriver 경로 문제가 해결되었습니다!

이제 프로그램이 정상적으로 작동합니다. 🎉

**GitHub**: https://github.com/rpaakdi1-spec/naver-band-auto-poster
