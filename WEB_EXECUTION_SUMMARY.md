# 웹 버전 실행 방법 완벽 가이드 🌐

## 🎯 목차

1. [30초 빠른 시작](#30초-빠른-시작) ⭐
2. [상세 설명](#상세-설명)
3. [문제 해결](#문제-해결)
4. [추가 팁](#추가-팁)

---

## 30초 빠른 시작 ⭐

### Windows 사용자

```bash
# 터미널/명령 프롬프트에서 실행
git clone https://github.com/rpaakdi1-spec/naver-band-auto-poster.git
cd naver-band-auto-poster
run_web.bat
```

**또는 파일 탐색기에서:**
1. `naver-band-auto-poster` 폴더 열기
2. `run_web.bat` 더블클릭
3. 완료! 🎉

### Mac/Linux 사용자

```bash
git clone https://github.com/rpaakdi1-spec/naver-band-auto-poster.git
cd naver-band-auto-poster
python3 run_web.py
```

### 실행 후

브라우저가 자동으로 열리고 다음 주소로 접속됩니다:
```
http://localhost:8501
```

---

## 상세 설명

### 1단계: 저장소 다운로드

**Git이 설치되어 있는 경우:**

```bash
git clone https://github.com/rpaakdi1-spec/naver-band-auto-poster.git
cd naver-band-auto-poster
```

**Git이 없는 경우:**

1. https://github.com/rpaakdi1-spec/naver-band-auto-poster 방문
2. 초록색 "Code" 버튼 클릭
3. "Download ZIP" 선택
4. 압축 해제 후 폴더로 이동

### 2단계: 실행

#### 방법 A: 자동 스크립트 (추천)

**Windows:**
```bash
run_web.bat
```

**Mac/Linux:**
```bash
python3 run_web.py
```

이 스크립트는 자동으로:
- ✅ Streamlit이 설치되어 있는지 확인
- ✅ 없으면 자동으로 설치
- ✅ 웹 서버 시작
- ✅ 브라우저 자동으로 열기

#### 방법 B: 수동 실행

```bash
# 1. 패키지 설치
pip install -r requirements.txt

# 2. Streamlit 실행
streamlit run streamlit_app.py
```

#### 방법 C: 직접 Streamlit 명령

```bash
# Streamlit만 설치
pip install streamlit

# 실행
streamlit run streamlit_app.py
```

### 3단계: 접속

실행 후 터미널에 다음과 같이 표시됩니다:

```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.1.100:8501
```

- **Local URL**: 같은 컴퓨터에서 접속
- **Network URL**: 같은 Wi-Fi의 다른 기기에서 접속 (모바일, 태블릿 등)

---

## 문제 해결

### ❌ "python 명령을 찾을 수 없습니다"

**문제**: Python이 설치되지 않았거나 PATH에 없습니다.

**해결:**

1. Python 설치 확인
   ```bash
   python --version
   # 또는
   python3 --version
   ```

2. Python 설치 (필요한 경우)
   - **Windows**: https://python.org/downloads/
   - **Mac**: `brew install python3`
   - **Linux**: `sudo apt install python3` (Ubuntu/Debian)

### ❌ "Streamlit을 찾을 수 없습니다"

**문제**: Streamlit이 설치되지 않았습니다.

**해결:**

```bash
pip install streamlit
# 또는
pip3 install streamlit
```

그 다음 다시 실행:
```bash
python run_web.py
```

### ❌ "브라우저가 자동으로 열리지 않습니다"

**문제**: 브라우저 자동 실행 실패

**해결:**

터미널에 표시된 주소를 수동으로 브라우저에 입력:
```
http://localhost:8501
```

### ❌ "포트가 이미 사용 중입니다" (Address already in use)

**문제**: 8501 포트가 다른 프로그램에서 사용 중

**해결 방법 1**: 다른 포트 사용

```bash
streamlit run streamlit_app.py --server.port 8502
```

브라우저 주소: `http://localhost:8502`

**해결 방법 2**: 기존 프로세스 종료

**Windows:**
```bash
netstat -ano | findstr :8501
taskkill /PID <PID번호> /F
```

**Mac/Linux:**
```bash
lsof -i :8501
kill -9 <PID>
```

### ❌ "ModuleNotFoundError: No module named 'selenium'"

**문제**: 필요한 패키지가 설치되지 않았습니다.

**해결:**

```bash
pip install -r requirements.txt
```

또는 개별 설치:
```bash
pip install selenium webdriver-manager schedule pyperclip streamlit
```

### ❌ 웹 페이지가 로딩되지 않습니다

**해결:**

1. 페이지 새로고침 (F5 또는 Ctrl+R)
2. 캐시 삭제 후 새로고침 (Ctrl+Shift+R)
3. 다른 브라우저에서 시도
4. 서버 재시작:
   - Ctrl+C로 종료
   - 다시 `run_web.bat` 또는 `python run_web.py` 실행

---

## 추가 팁

### 💡 네트워크에서 접속하기

같은 Wi-Fi 네트워크의 다른 기기(모바일, 태블릿)에서 접속:

```bash
# --server.address 옵션 추가
streamlit run streamlit_app.py --server.address 0.0.0.0
```

터미널에 표시되는 **Network URL**을 다른 기기에서 입력:
```
http://192.168.1.100:8501
```

### 💡 자동 브라우저 열림 비활성화

```bash
streamlit run streamlit_app.py --server.headless true
```

### 💡 포트 변경

```bash
streamlit run streamlit_app.py --server.port 9000
```

### 💡 서버 종료

터미널에서:
```
Ctrl + C
```

### 💡 백그라운드 실행

**Windows (PowerShell):**
```powershell
Start-Process -NoNewWindow -FilePath "streamlit" -ArgumentList "run streamlit_app.py"
```

**Mac/Linux:**
```bash
nohup streamlit run streamlit_app.py &
```

종료:
```bash
pkill -f streamlit
```

---

## 📱 모바일 접속 방법

1. **PC와 모바일이 같은 Wi-Fi에 연결**

2. **Network URL 확인**
   - PC 터미널에서 `Network URL` 찾기
   - 예: `http://192.168.1.100:8501`

3. **모바일 브라우저에서 접속**
   - 주소창에 Network URL 입력
   - 터치 최적화된 웹 UI 사용 가능!

4. **QR 코드로 접속 (선택사항)**
   ```bash
   # QR 코드 생성 (터미널에 표시)
   pip install qrcode[pil]
   python -c "import qrcode; qr = qrcode.QRCode(); qr.add_data('http://192.168.1.100:8501'); qr.print_ascii()"
   ```

---

## 🔧 고급 설정

### Streamlit 설정 파일

`.streamlit/config.toml` 파일을 생성하여 기본 설정 변경:

```toml
[server]
port = 8501
address = "0.0.0.0"
headless = false

[browser]
gatherUsageStats = false

[theme]
primaryColor = "#FF4B4B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"
```

### 환경 변수로 설정

```bash
# 포트 설정
export STREAMLIT_SERVER_PORT=8502

# 헤드리스 모드
export STREAMLIT_SERVER_HEADLESS=true

# 실행
streamlit run streamlit_app.py
```

---

## 📖 관련 문서

- 🚀 **[빠른 시작 가이드](WEB_QUICK_START.md)** - 초보자 필독!
- 📚 **[웹 버전 상세 가이드](WEB_VERSION_GUIDE.md)** - 모든 기능 설명
- 🆚 **[3가지 방법 비교](3_WAYS_GUIDE.md)** - 웹/데스크톱/.exe 비교
- 📖 **[메인 README](README.md)** - 프로젝트 전체 개요

---

## ✅ 체크리스트

실행 전 확인사항:

- [ ] Python 3.8 이상 설치됨
- [ ] Git 설치됨 (또는 ZIP 다운로드)
- [ ] 저장소 다운로드 완료
- [ ] Chrome 브라우저 설치됨
- [ ] 인터넷 연결 확인
- [ ] 8501 포트가 사용 가능

실행 후 확인사항:

- [ ] 브라우저가 열림
- [ ] `http://localhost:8501` 접속 가능
- [ ] 웹 페이지가 정상 표시됨
- [ ] 채팅방 추가 가능
- [ ] 포스트 추가 가능
- [ ] 설정 저장 가능

---

## 🎉 성공!

웹 버전이 정상적으로 실행되었다면 축하합니다!

이제 다음 단계로:
1. 채팅방 URL 추가
2. 포스트 내용 작성
3. 스케줄 설정
4. 시작 버튼 클릭!

**저장소**: https://github.com/rpaakdi1-spec/naver-band-auto-poster

---

💡 **가장 간단한 방법 요약**:

Windows: `run_web.bat` 더블클릭
Mac/Linux: `python3 run_web.py`

끝! 🚀
