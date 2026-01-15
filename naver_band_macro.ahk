; ======================================================
; 네이버밴드 자동 포스팅 매크로 (AutoHotkey v2)
; ======================================================
; 사용법:
; 1. AutoHotkey v2 설치: https://www.autohotkey.com/
; 2. 이 파일을 .ahk로 저장
; 3. 더블클릭으로 실행
; 4. F1 키를 누르면 자동 포스팅 시작
; 5. F2 키를 누르면 중지
; ======================================================

#Requires AutoHotkey v2.0
#SingleInstance Force

; ========== 설정 (여기를 수정하세요) ==========
NAVER_ID := "your_naver_id"              ; 네이버 아이디
NAVER_PW := "your_password"              ; 네이버 비밀번호
BAND_URL := "https://band.us/band/xxxxx" ; 밴드 URL

; 포스팅할 내용들
Posts := [
    "첫 번째 게시글 내용입니다.",
    "두 번째 게시글 내용입니다.",
    "세 번째 게시글 내용입니다."
]

INTERVAL_MINUTES := 30    ; 포스팅 간격 (분)
RANDOM_DELAY := 5         ; 랜덤 딜레이 (분)
START_HOUR := 9          ; 시작 시간 (24시간 형식)
END_HOUR := 22           ; 종료 시간 (24시간 형식)
; ============================================

global isRunning := false
global currentPostIndex := 1
global chrome := ""

; 트레이 아이콘 메뉴
A_IconTip := "네이버밴드 자동 포스팅 매크로`nF1: 시작 | F2: 중지"

; ========== 단축키 설정 ==========
F1:: StartAutoPost()
F2:: StopAutoPost()
F3:: PostOnce()

; ========== 함수 정의 ==========

StartAutoPost() {
    global isRunning
    if isRunning {
        MsgBox "이미 실행 중입니다!", "알림"
        return
    }
    
    isRunning := true
    MsgBox "자동 포스팅을 시작합니다!`n`n간격: " INTERVAL_MINUTES "분`n랜덤 딜레이: " RANDOM_DELAY "분`n활성 시간: " START_HOUR ":00 ~ " END_HOUR ":00`n`nF2를 눌러 중지할 수 있습니다.", "시작"
    
    ; 첫 실행
    PostOnce()
    
    ; 주기적 실행
    SetTimer PostOnce, INTERVAL_MINUTES * 60000
}

StopAutoPost() {
    global isRunning
    if !isRunning {
        MsgBox "실행 중이 아닙니다.", "알림"
        return
    }
    
    isRunning := false
    SetTimer PostOnce, 0
    MsgBox "자동 포스팅을 중지했습니다.", "중지"
}

PostOnce() {
    ; 시간대 체크
    currentHour := A_Hour + 0
    if (currentHour < START_HOUR || currentHour > END_HOUR) {
        ToolTip "활성 시간이 아닙니다. (" A_Hour "시)"
        SetTimer () => ToolTip(), -3000
        return
    }
    
    ; Chrome이 실행 중인지 확인
    if !WinExist("ahk_exe chrome.exe") {
        Run "chrome.exe " BAND_URL
        Sleep 5000
    }
    
    ; 밴드 페이지로 이동
    if WinExist("ahk_exe chrome.exe") {
        WinActivate
        Send "^l"  ; 주소창 선택
        Sleep 500
        Send BAND_URL "{Enter}"
        Sleep 3000
    }
    
    ; 다음 포스트 선택
    global currentPostIndex, Posts
    postContent := Posts[currentPostIndex]
    currentPostIndex := Mod(currentPostIndex, Posts.Length) + 1
    
    ; 게시글 작성 영역 찾기 (Tab 키로 이동)
    Send "{Tab}"
    Sleep 500
    
    ; 내용 입력
    Send postContent
    Sleep 1000
    
    ; 등록 버튼 (Tab으로 이동 후 Enter)
    Send "{Tab}{Tab}{Enter}"
    
    ToolTip "포스팅 완료: " SubStr(postContent, 1, 30) "..."
    SetTimer () => ToolTip(), -3000
    
    ; 랜덤 딜레이
    if (RANDOM_DELAY > 0) {
        randomDelay := Random(0, RANDOM_DELAY * 60)
        Sleep randomDelay * 1000
    }
}

; ========== 시작 메시지 ==========
MsgBox "
(
네이버밴드 자동 포스팅 매크로 시작!

단축키:
  F1: 자동 포스팅 시작
  F2: 자동 포스팅 중지
  F3: 즉시 1회 포스팅

설정을 수정하려면 스크립트 파일을 편집하세요.
)", "네이버밴드 자동 포스팅", "Iconi"
