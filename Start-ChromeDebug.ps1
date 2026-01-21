# Naver Band Safe Macro - Chrome Debug Mode Launcher
# PowerShell script with full UTF-8 support

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "네이버밴드 안전 타이핑 매크로" -ForegroundColor Cyan
Write-Host "Chrome 디버깅 모드 실행 도구" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Find Chrome path
$chromePaths = @(
    "${env:ProgramFiles}\Google\Chrome\Application\chrome.exe",
    "${env:ProgramFiles(x86)}\Google\Chrome\Application\chrome.exe",
    "$env:LOCALAPPDATA\Google\Chrome\Application\chrome.exe"
)

$chromePath = $null
foreach ($path in $chromePaths) {
    if (Test-Path $path) {
        $chromePath = $path
        break
    }
}

if (-not $chromePath) {
    Write-Host "[오류] Chrome을 찾을 수 없습니다." -ForegroundColor Red
    Write-Host "Chrome을 설치하거나 경로를 수동으로 지정하세요." -ForegroundColor Yellow
    Read-Host "계속하려면 Enter를 누르세요"
    exit 1
}

Write-Host "[확인] Chrome 찾음: $chromePath" -ForegroundColor Green
Write-Host ""

# Configuration
$userDataDir = "$env:USERPROFILE\chrome_dev_session"
$debugPort = 9222

Write-Host "[설정]" -ForegroundColor Yellow
Write-Host "   - 디버깅 포트: $debugPort"
Write-Host "   - 데이터 디렉토리: $userDataDir"
Write-Host ""

# Check for existing Chrome processes
$chromeProcesses = Get-Process chrome -ErrorAction SilentlyContinue

if ($chromeProcesses) {
    Write-Host "[경고] Chrome이 이미 실행 중입니다." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Chrome을 완전히 종료하고 다시 시도하시겠습니까?"
    Write-Host "1. 예 - Chrome 종료 후 디버깅 모드로 실행"
    Write-Host "2. 아니오 - 현재 실행 중인 Chrome 사용 시도"
    Write-Host ""
    
    $choice = Read-Host "선택하세요 (1 또는 2)"
    
    if ($choice -eq "1") {
        Write-Host ""
        Write-Host "Chrome 종료 중..." -ForegroundColor Yellow
        Stop-Process -Name chrome -Force -ErrorAction SilentlyContinue
        Start-Sleep -Seconds 2
        Write-Host "[완료] Chrome 종료 완료" -ForegroundColor Green
        Write-Host ""
    }
}

Write-Host "[실행] Chrome을 디버깅 모드로 실행합니다..." -ForegroundColor Cyan
Write-Host ""
Write-Host "+-----------------------------------------------------------+"
Write-Host "| Chrome이 실행되면:                                        |"
Write-Host "| 1. 네이버에 로그인하세요                                  |"
Write-Host "| 2. 네이버밴드 채팅방으로 이동하세요                       |"
Write-Host "| 3. 다른 PowerShell 창에서 매크로를 실행하세요             |"
Write-Host "|    python src/safe_band_macro.py --test                   |"
Write-Host "+-----------------------------------------------------------+"
Write-Host ""

# Launch Chrome
$arguments = "--remote-debugging-port=$debugPort --user-data-dir=`"$userDataDir`""
Start-Process -FilePath $chromePath -ArgumentList $arguments

Write-Host ""
Write-Host "[완료] Chrome 디버깅 모드 실행 완료!" -ForegroundColor Green
Write-Host ""
Write-Host "[다음 단계]" -ForegroundColor Yellow
Write-Host "   1. Chrome에서 네이버밴드 로그인 및 채팅방 열기"
Write-Host "   2. 새 PowerShell 또는 CMD 창 열기"
Write-Host "   3. 매크로 실행: python src/safe_band_macro.py --test"
Write-Host ""

Read-Host "계속하려면 Enter를 누르세요"
