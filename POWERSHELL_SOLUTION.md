# Windows 배치 파일 인코딩 문제 - 최종 해결책

## 🔥 문제의 근본 원인

Windows 배치 파일(.bat)은 **CP949 인코딩**을 사용해야 하지만:
1. Git이 파일을 체크아웃할 때 UTF-8로 변환
2. 이모지와 특수문자가 CP949에서 지원되지 않음
3. 한글이 깨지면서 명령어가 제대로 실행되지 않음

## ✅ 최종 해결책: PowerShell 사용

Windows PowerShell은 **UTF-8을 완벽 지원**합니다!

### 🚀 새로운 실행 방법

#### 방법 1: PowerShell 직접 실행 (권장)

```powershell
# Chrome 디버깅 모드 실행
.\Start-ChromeDebug.ps1

# 매크로 실행
.\Start-SafeMacro.ps1
```

#### 방법 2: 배치 파일로 PowerShell 실행

```cmd
start_chrome.bat    # Chrome 디버깅 모드
run_macro.bat       # 매크로 실행
```

#### 방법 3: 영어 버전 배치 파일

```cmd
start_chrome_debug_en.bat    # 영어 버전 (인코딩 문제 없음)
```

## 📦 사용 가능한 파일들

### ✅ PowerShell 스크립트 (권장)
- **`Start-ChromeDebug.ps1`** - Chrome 디버깅 모드 실행 (한글 완벽 지원)
- **`Start-SafeMacro.ps1`** - 매크로 실행 (한글 완벽 지원)
- **`start_chrome.bat`** - PowerShell 스크립트 실행 도우미
- **`run_macro.bat`** - PowerShell 스크립트 실행 도우미

### ✅ 영어 배치 파일
- **`start_chrome_debug_en.bat`** - 영어 버전 (인코딩 문제 없음)

### ⚠️ 한글 배치 파일 (사용 비권장)
- `start_chrome_debug.bat` - 인코딩 문제 발생 가능
- `run_safe_macro.bat` - 인코딩 문제 발생 가능

## 🔧 PowerShell 실행 정책 설정

처음 PowerShell 스크립트를 실행할 때 오류가 발생하면:

```powershell
# PowerShell을 관리자 권한으로 실행 후
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

또는 일회성으로 실행:

```powershell
powershell -ExecutionPolicy Bypass -File Start-ChromeDebug.ps1
```

## 📝 사용 순서

### 1단계: Chrome 디버깅 모드 실행

**PowerShell (권장):**
```powershell
.\Start-ChromeDebug.ps1
```

**배치 파일:**
```cmd
start_chrome.bat
```

**영어 버전:**
```cmd
start_chrome_debug_en.bat
```

### 2단계: 네이버밴드 로그인

1. 실행된 Chrome에서 네이버 로그인
2. 네이버밴드 접속
3. 메시지를 보낼 채팅방 열기

### 3단계: 매크로 실행

**PowerShell (권장):**
```powershell
.\Start-SafeMacro.ps1
```

**배치 파일:**
```cmd
run_macro.bat
```

**Python 직접:**
```cmd
python src/safe_band_macro.py --test
```

## 💡 왜 PowerShell이 더 좋은가?

| 기능 | 배치 파일 (.bat) | PowerShell (.ps1) |
|------|------------------|-------------------|
| 한글 지원 | ❌ CP949 필요 | ✅ UTF-8 지원 |
| 이모지 지원 | ❌ 불가능 | ✅ 완벽 지원 |
| 색상 출력 | ❌ 제한적 | ✅ 다양한 색상 |
| 에러 처리 | ❌ 제한적 | ✅ 강력함 |
| 현대적 | ❌ 구식 | ✅ 최신 |

## 🔍 문제 해결

### Q: PowerShell 스크립트가 실행되지 않아요

**A:** 실행 정책을 변경하세요:
```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Q: 여전히 한글이 깨져요

**A:** PowerShell을 사용하세요:
```powershell
.\Start-ChromeDebug.ps1
```

### Q: PowerShell이 없어요

**A:** Windows 7 이상에는 기본 설치되어 있습니다.
- Windows + R → `powershell` 입력

### Q: 영어 버전을 사용하고 싶어요

**A:** 영어 배치 파일을 사용하세요:
```cmd
start_chrome_debug_en.bat
```

## 🎯 권장 사용법

```powershell
# 1. PowerShell 열기 (프로젝트 폴더에서)
cd C:\path\to\naver-band-auto-poster

# 2. Chrome 실행
.\Start-ChromeDebug.ps1

# 3. 네이버밴드 로그인 (Chrome에서)

# 4. 새 PowerShell 창에서 매크로 실행
.\Start-SafeMacro.ps1

# 또는 Python 직접 실행
python src/safe_band_macro.py --test
```

## 📚 참고

- PowerShell 스크립트는 **UTF-8 BOM** 인코딩으로 저장됨
- 한글, 이모지, 특수문자 모두 정상 작동
- Git에서도 문제없이 관리 가능

---

## 🎉 결론

**PowerShell 스크립트를 사용하세요!**

- ✅ 한글 완벽 지원
- ✅ 이모지 지원
- ✅ 색상 출력
- ✅ 인코딩 걱정 없음

더 이상 배치 파일의 인코딩 문제로 고생하지 마세요! 🚀
