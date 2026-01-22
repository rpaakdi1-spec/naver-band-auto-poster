## 🎉 주요 기능

### 새로운 기능
- 🚀 **독립 실행 파일 지원**: 파이썬 설치 없이 실행 가능한 .exe 파일
- 🎯 **채팅방 별명 및 선택적 포스팅**: 체크박스로 포스팅할 채팅방 선택
- 📅 **날짜+시간 스케줄링**: 24시간 자동 설정
- ⏱️ **실시간 카운트다운**: 다음 포스팅까지 남은 시간 표시
- 🖥️ **개선된 UI**: 좌우 분할 레이아웃

### 개선 사항
- ✅ 세션 안정성 개선 (invalid session id 오류 해결)
- ✅ 카운트다운 타이머 정확도 향상
- ✅ 채팅방 닫기 로직 최적화

## 📥 다운로드

### Windows 사용자 (추천)
**`네이버밴드자동포스팅.exe`** 파일을 다운로드하여 바로 실행하세요!

- ✅ 파이썬 설치 불필요
- ✅ 패키지 설치 불필요
- ✅ 더블클릭만 하면 실행

### 개발자 / 소스 코드 사용자
아래 "Source code" 링크에서 다운로드하거나:
```bash
git clone https://github.com/rpaakdi1-spec/naver-band-auto-poster.git
cd naver-band-auto-poster
pip install -r requirements.txt
python run.py
```

## 🚀 빠른 시작

1. **다운로드**: `네이버밴드자동포스팅.exe` 다운로드
2. **실행**: 파일 더블클릭
3. **설정**:
   - 채팅방 URL 추가 (별명 지정 가능)
   - 포스팅할 내용 추가
   - 스케줄 설정 (시작/종료 일시)
4. **시작**: [시작] 버튼 클릭
5. **로그인**: Chrome 브라우저에서 밴드 로그인
6. **자동 포스팅 시작!** ✨

## 📖 상세 사용법

자세한 사용법은 [README.md](https://github.com/rpaakdi1-spec/naver-band-auto-poster/blob/main/README.md)를 참고하세요.

## ⚙️ 시스템 요구사항

- **운영체제**: Windows 10 또는 11 (64-bit)
- **브라우저**: Google Chrome (최신 버전)
- **인터넷**: 첫 실행 시 ChromeDriver 다운로드 필요
- **Python**: ❌ 설치 불필요!

## 🐛 알려진 이슈

- 일부 백신 프로그램에서 오탐지 가능 (정상 파일입니다)
- 첫 실행 시 Windows Defender 경고 가능 (실행 허용 필요)

## 📝 변경 사항 (Changelog)

### v4.2.0 (2026-01-22)
- feat: 독립 실행 파일(.exe) 빌드 지원 추가
- feat: 채팅방 별명 및 체크박스 선택 기능
- feat: 날짜+시간 스케줄링 (24시간 자동 설정)
- feat: 실시간 카운트다운 타이머
- feat: 좌우 분할 UI 레이아웃
- fix: 세션 안정성 개선 (채팅방 닫기 로직 최적화)
- fix: 카운트다운 즉시 표시
- docs: 빌드 가이드 및 사용 설명서 추가

### 이전 버전
- v4.1.0: UI 개선 및 카운트다운 기능
- v4.0.0: 채팅방 별명 및 선택적 포스팅
- v3.0.0: 고급 채팅방 검색
- v2.0.0: 다중 채팅방 지원

## 🔗 관련 링크

- [📖 사용 설명서](https://github.com/rpaakdi1-spec/naver-band-auto-poster/blob/main/README.md)
- [🔨 빌드 가이드](https://github.com/rpaakdi1-spec/naver-band-auto-poster/blob/main/BUILD_EXE_GUIDE.md)
- [🐛 이슈 리포트](https://github.com/rpaakdi1-spec/naver-band-auto-poster/issues)

## 💬 피드백

문제가 발생하거나 제안 사항이 있으시면 [Issues](https://github.com/rpaakdi1-spec/naver-band-auto-poster/issues)에 등록해주세요!

---

**⚠️ 주의사항**
- 네이버 이용약관을 준수하여 사용하세요
- 과도한 자동화는 계정 제재를 받을 수 있습니다
- 적절한 포스팅 간격을 설정하세요 (최소 30분 권장)
