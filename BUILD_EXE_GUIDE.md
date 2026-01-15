# EXE 파일로 변환하기

## 방법 1: 자동 빌드 스크립트 (Windows)

1. `build_exe.bat` 파일을 더블클릭
2. 빌드 완료 후 `dist\네이버밴드_자동포스팅.exe` 생성됨
3. EXE 파일을 바탕화면으로 복사해서 사용

## 방법 2: 수동 빌드

```bash
pip install -r requirements.txt
pip install pyinstaller
pyinstaller --clean --noconfirm build_exe.spec
```

## 빌드 후

- `dist/네이버밴드_자동포스팅.exe` 파일이 생성됩니다
- 이 파일만 있으면 **Python 설치 없이** 바로 실행 가능!
- 다른 PC에서도 실행 가능 (Chrome 브라우저만 필요)

## 주의사항

- EXE 파일 크기: 약 100-150MB
- 첫 실행 시 Windows Defender가 경고할 수 있음 (안전함)
- Chrome 브라우저는 별도로 설치 필요
- config 폴더가 자동 생성됨

## 실행 방법

1. `네이버밴드_자동포스팅.exe` 더블클릭
2. GUI 창에서 설정 입력
3. "시작" 버튼으로 자동 포스팅 시작!
