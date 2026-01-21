# Naver Band Safe Macro Runner
# PowerShell script with full UTF-8 support

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "네이버밴드 안전 타이핑 매크로 실행" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Check Python
try {
    $pythonVersion = python --version 2>&1
    Write-Host "[확인] Python 설치 확인: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "[오류] Python이 설치되어 있지 않습니다." -ForegroundColor Red
    Write-Host "https://www.python.org/downloads/ 에서 다운로드하세요." -ForegroundColor Yellow
    Read-Host "계속하려면 Enter를 누르세요"
    exit 1
}

Write-Host ""

# Check packages
Write-Host "[확인] 필요한 패키지 확인 중..." -ForegroundColor Yellow

$packages = @("selenium", "pyperclip")
foreach ($package in $packages) {
    $installed = pip show $package 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Host "   $package 설치 중..." -ForegroundColor Yellow
        pip install $package | Out-Null
    }
}

Write-Host "[완료] 패키지 확인 완료" -ForegroundColor Green
Write-Host ""

# Check Chrome debug mode
Write-Host "[확인] Chrome 디버깅 모드 확인 중..." -ForegroundColor Yellow

try {
    $response = Invoke-WebRequest -Uri "http://127.0.0.1:9222/json/version" -TimeoutSec 2 -ErrorAction Stop
    Write-Host "[확인] Chrome 디버깅 모드 실행 중" -ForegroundColor Green
} catch {
    Write-Host ""
    Write-Host "[경고] Chrome이 디버깅 모드로 실행되지 않았습니다!" -ForegroundColor Red
    Write-Host ""
    Write-Host "먼저 다음 명령으로 Chrome을 실행해야 합니다:" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "   .\Start-ChromeDebug.ps1" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "또는 start_chrome_debug_en.bat" -ForegroundColor Cyan
    Write-Host ""
    Read-Host "계속하려면 Enter를 누르세요"
    exit 1
}

Write-Host ""

# Main menu
function Show-Menu {
    Write-Host "============================================================" -ForegroundColor Cyan
    Write-Host "실행 모드 선택" -ForegroundColor Cyan
    Write-Host "============================================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "1. 테스트 모드 (1회만 실행, 수동 Enter)"
    Write-Host "2. 연속 전송 모드 (자동 반복)"
    Write-Host "3. 테스트 모드 (자동 전송 - 위험!)"
    Write-Host "4. 종료"
    Write-Host ""
}

do {
    Show-Menu
    $choice = Read-Host "선택하세요 (1-4)"
    
    switch ($choice) {
        "1" {
            Write-Host ""
            Write-Host "[실행] 테스트 모드 실행 (수동 전송)" -ForegroundColor Cyan
            Write-Host ""
            python src/safe_band_macro.py --test
            Write-Host ""
            Read-Host "계속하려면 Enter를 누르세요"
        }
        "2" {
            Write-Host ""
            Write-Host "[실행] 연속 전송 모드" -ForegroundColor Cyan
            Write-Host ""
            
            $interval = Read-Host "전송 간격(분, 기본 5)"
            if ([string]::IsNullOrWhiteSpace($interval)) { $interval = 5 }
            
            $maxSends = Read-Host "최대 전송 횟수(기본 20)"
            if ([string]::IsNullOrWhiteSpace($maxSends)) { $maxSends = 20 }
            
            $autoSend = Read-Host "자동 전송? (y/N, 기본 N)"
            
            Write-Host ""
            Write-Host "[설정]" -ForegroundColor Yellow
            Write-Host "   - 간격: $interval 분"
            Write-Host "   - 최대: $maxSends 회"
            Write-Host "   - 자동: $autoSend"
            Write-Host ""
            
            if ($autoSend -eq "y" -or $autoSend -eq "Y") {
                python src/safe_band_macro.py --interval $interval --max-sends $maxSends --auto-send
            } else {
                python src/safe_band_macro.py --interval $interval --max-sends $maxSends
            }
            
            Write-Host ""
            Read-Host "계속하려면 Enter를 누르세요"
        }
        "3" {
            Write-Host ""
            Write-Host "[경고] 자동 전송 테스트 모드 (위험!)" -ForegroundColor Red
            Write-Host ""
            
            $confirm = Read-Host "정말 실행하시겠습니까? (y/N)"
            if ($confirm -eq "y" -or $confirm -eq "Y") {
                Write-Host ""
                python src/safe_band_macro.py --test --auto-send
                Write-Host ""
            } else {
                Write-Host "취소되었습니다." -ForegroundColor Yellow
            }
            
            Read-Host "계속하려면 Enter를 누르세요"
        }
        "4" {
            Write-Host ""
            Write-Host "프로그램을 종료합니다." -ForegroundColor Yellow
            Write-Host ""
            break
        }
        default {
            Write-Host ""
            Write-Host "[오류] 잘못된 선택입니다. 1-4 사이의 숫자를 입력하세요." -ForegroundColor Red
            Write-Host ""
            Read-Host "계속하려면 Enter를 누르세요"
        }
    }
} while ($choice -ne "4")
