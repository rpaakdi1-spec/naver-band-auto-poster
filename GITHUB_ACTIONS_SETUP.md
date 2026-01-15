# GitHub Actions 워크플로우 설정 가이드

## ⚠️ 중요 안내

GitHub App의 권한 제한으로 인해 워크플로우 파일(`.github/workflows/build-exe.yml`)은 자동으로 푸시되지 않았습니다.

수동으로 추가하려면 아래 단계를 따르세요.

---

## 📝 수동 설정 방법

### 옵션 1: GitHub 웹 인터페이스에서 추가

1. GitHub 저장소로 이동: https://github.com/rpaakdi1-spec/naver-band-auto-poster
2. "Add file" > "Create new file" 클릭
3. 파일 이름 입력: `.github/workflows/build-exe.yml`
4. 아래 내용을 복사하여 붙여넣기
5. "Commit new file" 클릭

### 옵션 2: 로컬에서 Git으로 추가

```bash
# 워크플로우 파일이 이미 생성되어 있습니다
git add .github/workflows/build-exe.yml
git commit -m "ci: add GitHub Actions workflow for automated builds"
git push origin main
```

---

## 📄 워크플로우 파일 내용

파일: `.github/workflows/build-exe.yml`

워크플로우 파일은 이미 로컬에 생성되어 있습니다:
- 위치: `/home/user/webapp/.github/workflows/build-exe.yml`
- 크기: 약 3.5KB

이 파일은 다음과 같은 기능을 제공합니다:

### 🔧 기능
- ✅ Windows EXE 자동 빌드
- ✅ Linux 실행 파일 자동 빌드
- ✅ 태그 푸시 시 자동 릴리스 생성
- ✅ 수동 워크플로우 실행 옵션
- ✅ 빌드 아티팩트 자동 업로드

### 🚀 사용 방법

1. **자동 빌드 (태그 푸시 시)**
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```
   → GitHub Actions가 자동으로 Windows/Linux 빌드를 생성하고 Release에 업로드합니다.

2. **수동 빌드**
   - GitHub 저장소 > "Actions" 탭
   - "Build Windows EXE" 워크플로우 선택
   - "Run workflow" 버튼 클릭

### 📦 빌드 결과

빌드 완료 후:
- **Artifacts**: Actions 탭에서 다운로드 가능
- **Releases**: 태그 푸시 시 자동 생성 (https://github.com/rpaakdi1-spec/naver-band-auto-poster/releases)

---

## 🔐 필요한 권한

워크플로우가 정상 작동하려면 다음 권한이 필요합니다:

- ✅ `actions: write` - 워크플로우 실행
- ✅ `contents: write` - 릴리스 생성
- ✅ `workflows: write` - 워크플로우 파일 수정 (선택사항)

기본적으로 GitHub Actions는 `GITHUB_TOKEN`을 사용하므로 추가 설정이 필요하지 않습니다.

---

## 🐛 문제 해결

### Q: 워크플로우가 실행되지 않습니다
**A**: 
1. "Actions" 탭이 활성화되어 있는지 확인
2. 저장소 Settings > Actions > General > "Allow all actions" 확인

### Q: 릴리스 생성이 실패합니다
**A**: 
1. 태그가 `v*` 형식인지 확인 (예: v1.0.0, v2.1.3)
2. Settings > Actions > General > Workflow permissions에서 "Read and write permissions" 선택

### Q: 빌드는 성공했는데 파일이 업로드되지 않습니다
**A**: 
1. Actions 탭에서 워크플로우 실행 로그 확인
2. "Upload artifact" 단계에서 오류 메시지 확인

---

## 📊 현재 상태

✅ **완료된 작업:**
- Linux 실행 파일 빌드 완료 (79MB)
- 빌드 문서 작성 완료
- 워크플로우 파일 생성 완료 (로컬)
- .gitignore 업데이트 완료

⏳ **대기 중인 작업:**
- GitHub에 워크플로우 파일 추가 (수동 작업 필요)
- 첫 번째 릴리스 태그 생성

---

## 🎯 다음 단계

1. **워크플로우 파일 추가** (위 방법 중 하나 선택)
2. **첫 릴리스 생성**:
   ```bash
   git tag v1.0.0 -m "First release"
   git push origin v1.0.0
   ```
3. **GitHub Actions 실행 확인** (Actions 탭)
4. **릴리스 다운로드** (Releases 페이지)

---

## 📞 지원

문제가 발생하면:
- GitHub Issues: https://github.com/rpaakdi1-spec/naver-band-auto-poster/issues
- 워크플로우 로그 확인: Actions 탭에서 실행 기록 확인
