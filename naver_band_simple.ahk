; ======================================================
; 네이버밴드 간편 포스팅 매크로 (AutoHotkey v2)
; ======================================================
; 이것은 매우 간단한 버전입니다!
; 
; 사용법:
; 1. AutoHotkey v2 설치: https://www.autohotkey.com/
; 2. 이 파일 더블클릭
; 3. Chrome에서 밴드 페이지를 열어두세요
; 4. Ctrl+Shift+P 를 누르면 자동으로 글이 올라갑니다!
; ======================================================

#Requires AutoHotkey v2.0

; ===== 여기에 포스팅할 내용을 입력하세요 =====
posts := [
    "안녕하세요! 첫 번째 글입니다.",
    "두 번째 게시글입니다.",
    "세 번째 내용입니다."
]
; ==========================================

global currentIndex := 1

; Ctrl+Shift+P: 포스팅 실행
^+p:: {
    global currentIndex, posts
    
    ; 현재 포스트 가져오기
    content := posts[currentIndex]
    currentIndex := Mod(currentIndex, posts.Length) + 1
    
    ; 클립보드에 복사
    A_Clipboard := content
    
    ; Chrome 활성화
    if WinExist("ahk_exe chrome.exe") {
        WinActivate
        Sleep 300
        
        ; 글쓰기 영역 클릭 (마우스 위치 조정 필요)
        Click 500, 300
        Sleep 500
        
        ; 붙여넣기
        Send "^v"
        Sleep 500
        
        ; Enter로 등록 (필요시 Tab으로 버튼 이동)
        Send "{Tab}{Tab}{Enter}"
        
        TrayTip "포스팅 완료!", SubStr(content, 1, 50), 1
    } else {
        MsgBox "Chrome을 먼저 실행하세요!"
    }
}

; Ctrl+Shift+Q: 종료
^+q:: ExitApp

MsgBox "
(
네이버밴드 간편 포스팅 매크로 시작!

사용법:
1. Chrome에서 밴드 페이지 열기
2. Ctrl+Shift+P - 포스팅 실행
3. Ctrl+Shift+Q - 프로그램 종료

매우 간단하게 사용할 수 있습니다!
)", "시작", "Iconi"
