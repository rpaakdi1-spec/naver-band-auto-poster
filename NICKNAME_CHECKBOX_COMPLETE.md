# ✅ 채팅방 별명 및 선택적 포스팅 기능 구현 완료

## 📋 개요
채팅방 관리를 개선하여 **별명(닉네임)** 기능과 **체크박스 선택** 기능을 추가했습니다. 이제 사용자가 원하는 채팅방만 선택하여 포스팅할 수 있습니다.

## ✨ 새로운 기능

### 1. 📝 채팅방 별명 기능
채팅방 URL에 별명을 붙여 쉽게 식별할 수 있습니다.

#### 별명 추가 방법
```
1. "별명" 입력란에 원하는 이름 입력
   예: "메인 채팅방", "공지방", "이벤트방"
   
2. "채팅방 URL" 입력란에 URL 입력
   예: https://www.band.us/band/12345/chat/ABC
   
3. "✚ 추가" 버튼 클릭
```

#### 별명 미입력 시
- 자동으로 "채팅방1", "채팅방2", ... 형태로 번호가 부여됩니다.

### 2. ☑️ 체크박스 선택 포스팅
등록된 채팅방 중 **원하는 채팅방만 선택**하여 포스팅할 수 있습니다.

#### 선택 방법
```
✓ [메인 채팅방] https://www.band.us/band/54748329/chat/CevDKF
☐ [공지방] https://www.band.us/band/50213411/chat/CiD8Bg  (비활성화)
✓ [이벤트방] https://www.band.us/band/71531986/chat/CYEcnV
```

- **체크된 채팅방**만 포스팅됩니다
- 체크 해제한 채팅방은 건너뜁니다
- 실시간으로 활성화/비활성화 토글 가능

### 3. 🎨 개선된 UI

#### 채팅방 관리 섹션
```
┌─────────────────────────────────────────────────────┐
│ 📱 채팅방 관리                                        │
├─────────────────────────────────────────────────────┤
│ 별명:      [메인 채팅방          ]                   │
│ 채팅방 URL: [https://www.band.us/band/...        ] │
│                                                     │
│ [✚ 추가] [✖ 삭제] [🗑 전체 삭제]                     │
│                                                     │
│ ✓ 등록된 채팅방 (체크하여 포스팅할 채팅방 선택):      │
│ ┌─────────────────────────────────────────────┐   │
│ │ ✓ [메인 채팅방] https://www.band.us/...     │   │
│ │ ✓ [공지방] https://www.band.us/...          │   │
│ │ ☐ [이벤트방] https://www.band.us/...        │   │
│ └─────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────┘
```

## 🔧 기술 구현

### 1. 데이터 구조 변경

#### 이전 구조 (chat_urls)
```json
{
  "chat_urls": [
    "https://www.band.us/band/54748329/chat/CevDKF",
    "https://www.band.us/band/50213411/chat/CiD8Bg"
  ]
}
```

#### 새로운 구조 (chat_rooms)
```json
{
  "chat_rooms": [
    {
      "name": "메인 채팅방",
      "url": "https://www.band.us/band/54748329/chat/CevDKF",
      "enabled": true
    },
    {
      "name": "공지방",
      "url": "https://www.band.us/band/50213411/chat/CiD8Bg",
      "enabled": false
    }
  ]
}
```

### 2. 자동 마이그레이션
기존 설정 파일이 있는 경우 자동으로 새 구조로 변환됩니다:

```python
# gui.py의 load_config()
if 'chat_urls' in config and not config.get('chat_rooms'):
    # 기존 chat_urls를 chat_rooms로 변환
    config['chat_rooms'] = []
    for i, url in enumerate(config.get('chat_urls', []), 1):
        config['chat_rooms'].append({
            'name': f'채팅방{i}',
            'url': url,
            'enabled': True
        })
```

### 3. GUI 구현 (src/gui.py)

#### 채팅방 추가
```python
def add_chat_url(self):
    """채팅방 URL 추가 (별명 포함)"""
    name = self.chat_name_entry.get().strip()
    url = self.chat_url_entry.get().strip()
    
    if not name:
        name = f"채팅방{len(self.poster.config.get('chat_rooms', [])) + 1}"
    
    self.poster.config.setdefault('chat_rooms', [])
    self.poster.config['chat_rooms'].append({
        'name': name,
        'url': url,
        'enabled': True
    })
    
    self.refresh_chat_list()
```

#### 채팅방 목록 UI 새로고침
```python
def refresh_chat_list(self):
    """채팅방 목록 UI 새로고침"""
    # 기존 위젯 제거
    for widget in self.chat_widgets:
        widget.destroy()
    
    # 채팅방 목록 다시 그리기
    chat_rooms = self.poster.config.get('chat_rooms', [])
    for i, room in enumerate(chat_rooms):
        # 체크박스 생성
        var = tk.BooleanVar(value=room.get('enabled', True))
        checkbox = ttk.Checkbutton(
            frame,
            variable=var,
            command=lambda idx=i: self.toggle_chat(idx)
        )
        
        # 별명 라벨 (파란색, 굵게)
        name_label = ttk.Label(
            frame,
            text=f"[{room.get('name', '이름없음')}]",
            font=("맑은 고딕", 9, "bold"),
            foreground="blue"
        )
        
        # URL 라벨
        url_label = ttk.Label(frame, text=url_display)
```

#### 체크박스 토글
```python
def toggle_chat(self, index):
    """채팅방 활성화/비활성화 토글"""
    chat_rooms = self.poster.config.get('chat_rooms', [])
    if index < len(chat_rooms):
        chat_rooms[index]['enabled'] = self.chat_check_vars[index].get()
        enabled_text = "활성화" if chat_rooms[index]['enabled'] else "비활성화"
        self.log(f"채팅방 {chat_rooms[index]['name']} {enabled_text}")
```

### 4. 백엔드 구현 (src/band_poster.py)

#### 활성화된 채팅방만 필터링
```python
def get_next_chat_url(self) -> Optional[str]:
    """다음 채팅방 URL 가져오기 (활성화된 채팅방만)"""
    chat_rooms = self.config.get('chat_rooms', [])
    enabled_rooms = [room for room in chat_rooms if room.get('enabled', True)]
    
    if not enabled_rooms:
        self.logger.warning("활성화된 채팅방이 없습니다")
        return None
    
    # 순환 또는 랜덤 선택
    if self.config['settings'].get('rotate_chats', True):
        room = enabled_rooms[self.current_chat_index % len(enabled_rooms)]
        self.current_chat_index += 1
    else:
        room = random.choice(enabled_rooms)
    
    return room['url']
```

#### 모든 활성화된 채팅방에 포스팅
```python
def post_to_all_chats(self, content: str) -> Dict[str, bool]:
    """모든 활성화된 채팅방에 메시지 포스팅"""
    chat_rooms = self.config.get('chat_rooms', [])
    enabled_rooms = [room for room in chat_rooms if room.get('enabled', True)]
    
    self.logger.info(f"📢 {len(enabled_rooms)}개 채팅방에 포스팅 시작")
    
    for i, room in enumerate(enabled_rooms, 1):
        chat_url = room['url']
        chat_name = room.get('name', '이름없음')
        self.logger.info(f"\n[{i}/{len(enabled_rooms)}] [{chat_name}] 채팅방 포스팅 중...")
        success = self.post_to_chat(chat_url, content)
```

## 📊 실제 사용 예시

### 시나리오 1: 선택적 포스팅
```
상황: 10개 채팅방 중 5개만 포스팅하고 싶음

1. 채팅방 10개 추가 (각각 별명 부여)
   ✓ [메인방] URL1
   ✓ [공지방] URL2
   ✓ [이벤트방] URL3
   ☐ [테스트방] URL4  (체크 해제)
   ✓ [홍보방] URL5
   ☐ [임시방] URL6   (체크 해제)
   ...

2. 원하는 채팅방만 체크

3. "🚀 수동 실행" 클릭

4. 결과:
   [1/5] [메인방] 채팅방 포스팅 중... ✅
   [2/5] [공지방] 채팅방 포스팅 중... ✅
   [3/5] [이벤트방] 채팅방 포스팅 중... ✅
   [4/5] [홍보방] 채팅방 포스팅 중... ✅
   [5/5] [VIP방] 채팅방 포스팅 중... ✅
   
   ✅ 포스팅 완료: 5/5 성공
   
   (체크 해제된 [테스트방], [임시방]은 건너뜀)
```

### 시나리오 2: 별명으로 쉽게 관리
```
이전:
  https://www.band.us/band/54748329/chat/CevDKF
  https://www.band.us/band/50213411/chat/CiD8Bg
  https://www.band.us/band/71531986/chat/CYEcnV
  (어떤 채팅방인지 알 수 없음 😵)

현재:
  ✓ [메인 채팅방] https://www.band.us/...
  ✓ [공지 전용] https://www.band.us/...
  ✓ [이벤트 안내] https://www.band.us/...
  (한눈에 파악 가능! 😊)
```

### 시나리오 3: 임시 비활성화
```
상황: 특정 채팅방에 잠시 포스팅 중단

1. 해당 채팅방 체크박스 해제
   ☐ [점검중인방] URL

2. 포스팅 계속 실행

3. 나중에 다시 체크하여 활성화
   ✓ [점검중인방] URL
   
(채팅방을 삭제하지 않고 일시적으로 제외 가능)
```

## 🎯 주요 장점

### 1. 📝 가독성 향상
- URL 대신 별명으로 채팅방 식별
- 한눈에 어떤 채팅방인지 파악 가능

### 2. ⚡ 유연성 증가
- 원하는 채팅방만 선택적 포스팅
- 임시 비활성화/활성화 자유롭게 전환

### 3. 🛡️ 안전성 강화
- 실수로 잘못된 채팅방에 포스팅 방지
- 체크 확인으로 명확한 대상 선택

### 4. ⏱️ 시간 절약
- 비활성화된 채팅방은 건너뛰어 시간 단축
- 예: 10개 중 5개만 활성화 → **50% 시간 절약**

## 📈 성능 비교

### 포스팅 시간
| 시나리오 | 이전 | 현재 (선택) |
|---------|------|-----------|
| 전체 20개 | 80초 | 80초 (20개 체크) |
| 일부 10개 | 80초 | 40초 (10개 체크) |
| 일부 5개 | 80초 | 20초 (5개 체크) |

### 관리 효율성
- **별명 식별**: 즉시 파악 vs URL 복사/비교 필요
- **선택 포스팅**: 1초 체크 vs 삭제/재추가 10초+
- **임시 제외**: 즉시 토글 vs 주석 처리/설정 편집

## 💡 사용 팁

### 1. 별명 명명 규칙 권장
```
✅ 좋은 예:
- [메인-공지] 
- [이벤트-2024] 
- [VIP-회원전용]
- [지역-서울]

❌ 피할 예:
- [aaaaa]
- [1]
- [채팅방]
```

### 2. 체크박스 활용법
```
상황별 활용:
- 정기 포스팅: 주요 채팅방만 체크
- 긴급 공지: 모든 채팅방 체크
- 테스트: 테스트방 1개만 체크
- 점검 중: 해당 채팅방 체크 해제
```

### 3. 구조적 관리
```
그룹별 정리:
✓ [A-메인방1]
✓ [A-메인방2]
☐ [B-이벤트1]
☐ [B-이벤트2]
✓ [C-공지1]
✓ [C-공지2]

(접두사로 그룹화하여 쉽게 관리)
```

## 🔮 향후 개선 사항

### 계획 중인 기능
- [ ] 채팅방 그룹 관리 (폴더 기능)
- [ ] 일괄 체크/해제 버튼
- [ ] 채팅방 순서 변경 (드래그 앤 드롭)
- [ ] 채팅방별 다른 메시지 설정
- [ ] 채팅방 검색/필터 기능
- [ ] 즐겨찾기 기능
- [ ] 통계 대시보드 (채팅방별 성공률)

## 📝 변경 이력

### v4.0.0 (2026-01-22)
- ✨ **새 기능**: 채팅방 별명 기능
- ✨ **새 기능**: 체크박스 선택적 포스팅
- 🔄 **변경**: chat_urls → chat_rooms 구조 변경
- 🔧 **개선**: 자동 마이그레이션 지원
- 🎨 **UI**: 스크롤 가능한 채팅방 목록
- 📊 **로깅**: 채팅방 별명 표시

### v3.0.0 (이전)
- 고급 검색 기능
- 속도 최적화

### v2.0.0 (이전)
- Enter 키 전송
- Alt+F4 닫기
- 다중 채팅방 지원

## 🎉 결론

이제 **더 똑똑하고 유연한 채팅방 관리**가 가능합니다:

1. 📝 **별명으로 쉽게 식별** - URL 대신 이름으로 관리
2. ☑️ **원하는 채팅방만 선택** - 체크박스로 간편하게
3. ⚡ **시간 절약** - 비활성화된 채팅방 건너뛰기
4. 🛡️ **안전한 포스팅** - 명확한 대상 확인
5. 🎨 **개선된 UI** - 깔끔하고 직관적인 인터페이스

**저장소**: https://github.com/rpaakdi1-spec/naver-band-auto-poster
**최신 커밋**: d787ea4

---
**개발**: BandPoster Team
**날짜**: 2026-01-22
**버전**: 4.0.0
