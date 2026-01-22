# ✅ 날짜+시간 스케줄링 및 24시간 기본 설정 완료

## 📋 개요
스케줄 설정을 **날짜+시간** 형식으로 확장하고, 프로그램 시작 시 **현재 시간부터 24시간**을 기본값으로 자동 설정하는 기능을 추가했습니다.

## ✨ 새로운 기능

### 1. 📅 날짜+시간 스케줄링

#### 이전 형식 (시간만)
```
시작 시간: 09:00
종료 시간: 22:00

문제점:
- 날짜 지정 불가
- 하루 단위로만 제한
- 익일 종료 불가
- 장기 실행 불편
```

#### 새로운 형식 (날짜+시간)
```
시작 일시: 2026-01-22 09:00
종료 일시: 2026-01-23 09:00

장점:
✅ 정확한 날짜 지정
✅ 여러 날 실행 가능
✅ 익일 종료 가능
✅ 장기 캠페인 설정
```

### 2. ⏰ 24시간 자동 설정

#### 프로그램 시작 시 자동 설정
```
현재 시간: 2026-01-22 14:30

자동 설정:
  시작 일시: 2026-01-22 14:30  (현재 시간)
  종료 일시: 2026-01-23 14:30  (24시간 후)

결과:
→ 별도 설정 없이 즉시 사용 가능
→ 24시간 연속 실행
→ 편리한 기본값
```

### 3. 🔄 기존 설정 자동 마이그레이션

#### 호환성 유지
```
기존 설정 (HH:MM):
  start_time: "09:00"
  end_time: "22:00"

자동 변환:
  start_datetime: "2026-01-22 09:00"  (오늘 날짜 추가)
  end_datetime: "2026-01-22 22:00"   (오늘 날짜 추가)

→ 기존 사용자도 문제없이 사용
```

## 🔧 기술 구현

### 1. GUI 변경 (src/gui.py)

#### 날짜+시간 입력 필드
```python
# 시작 일시
ttk.Label(schedule_frame, text="시작 일시:").grid(row=1, column=0)
self.start_datetime_entry = ttk.Entry(schedule_frame, width=20)

# 현재 시간을 기본값으로
now = datetime.now()
default_start = now.strftime("%Y-%m-%d %H:%M")
self.start_datetime_entry.insert(0, default_start)

# 형식 안내
ttk.Label(schedule_frame, text="(YYYY-MM-DD HH:MM)", 
         font=("맑은 고딕", 8), foreground="gray").grid(...)

# 종료 일시 (24시간 후)
default_end = (now + timedelta(hours=24)).strftime("%Y-%m-%d %H:%M")
self.end_datetime_entry.insert(0, default_end)
```

#### 저장 시 형식 검증
```python
def save_config(self):
    # 날짜/시간 형식 검증
    try:
        datetime.strptime(self.start_datetime_entry.get(), "%Y-%m-%d %H:%M")
        datetime.strptime(self.end_datetime_entry.get(), "%Y-%m-%d %H:%M")
    except ValueError:
        raise ValueError("날짜/시간 형식이 올바르지 않습니다. (YYYY-MM-DD HH:MM)")
    
    # 설정 저장
    self.poster.config['schedule']['start_datetime'] = self.start_datetime_entry.get()
    self.poster.config['schedule']['end_datetime'] = self.end_datetime_entry.get()
```

#### 로드 시 마이그레이션
```python
def load_config(self):
    # 새로운 형식 우선
    if 'start_datetime' in config['schedule']:
        self.start_datetime_entry.insert(0, config['schedule']['start_datetime'])
    
    # 기존 형식 변환
    elif 'start_time' in config['schedule']:
        old_time = config['schedule']['start_time']  # "09:00"
        today = datetime.now().strftime("%Y-%m-%d")
        self.start_datetime_entry.insert(0, f"{today} {old_time}")
    
    # 기본값
    else:
        self.start_datetime_entry.insert(0, datetime.now().strftime("%Y-%m-%d %H:%M"))
```

### 2. 백엔드 로직 (src/band_poster.py)

#### 스케줄 범위 검증
```python
def is_within_schedule(self) -> bool:
    """현재 시간이 스케줄 범위 내인지 확인"""
    now = datetime.now()
    
    # 새로운 형식 (YYYY-MM-DD HH:MM) 지원
    if 'start_datetime' in self.config['schedule']:
        start_datetime = datetime.strptime(
            self.config['schedule']['start_datetime'], 
            "%Y-%m-%d %H:%M"
        )
        end_datetime = datetime.strptime(
            self.config['schedule']['end_datetime'], 
            "%Y-%m-%d %H:%M"
        )
        
        is_within = start_datetime <= now <= end_datetime
        
        if not is_within:
            self.logger.info(
                f"스케줄 범위 외: "
                f"현재 {now.strftime('%Y-%m-%d %H:%M')}, "
                f"시작 {start_datetime.strftime('%Y-%m-%d %H:%M')}, "
                f"종료 {end_datetime.strftime('%Y-%m-%d %H:%M')}"
            )
        
        return is_within
    
    # 기존 형식 (HH:MM) 호환성
    elif 'start_time' in self.config['schedule']:
        now_time = now.time()
        start_time = datetime.strptime(
            self.config['schedule']['start_time'], "%H:%M"
        ).time()
        end_time = datetime.strptime(
            self.config['schedule']['end_time'], "%H:%M"
        ).time()
        
        return start_time <= now_time <= end_time
    
    # 설정 없으면 항상 실행
    return True
```

#### 기본 설정 생성
```python
def _get_default_config(self) -> Dict:
    """기본 설정 반환"""
    # 현재 시간부터 24시간 후까지
    now = datetime.now()
    start_datetime = now.strftime("%Y-%m-%d %H:%M")
    end_datetime = (now + timedelta(hours=24)).strftime("%Y-%m-%d %H:%M")
    
    return {
        "chat_rooms": [],
        "posts": [],
        "schedule": {
            "interval_minutes": 30,
            "random_delay_minutes": 5,
            "start_datetime": start_datetime,
            "end_datetime": end_datetime
        },
        ...
    }
```

### 3. 설정 파일 (config.example.json)

#### 새로운 형식
```json
{
  "schedule": {
    "interval_minutes": 30,
    "random_delay_minutes": 5,
    "start_datetime": "2026-01-22 09:00",
    "end_datetime": "2026-01-23 09:00",
    "_comment_datetime": "날짜+시간 형식 (YYYY-MM-DD HH:MM)"
  }
}
```

## 📊 사용 예시

### 시나리오 1: 프로그램 첫 실행
```
1. 프로그램 시작
   현재 시간: 2026-01-22 14:30

2. 자동 설정 확인
   ┌────────────────────────────────┐
   │ 시작 일시: 2026-01-22 14:30   │
   │ 종료 일시: 2026-01-23 14:30   │
   └────────────────────────────────┘

3. 즉시 사용 가능
   → 별도 설정 불필요
   → 24시간 동안 자동 실행
```

### 시나리오 2: 단기 캠페인 (3시간)
```
설정:
  시작 일시: 2026-01-22 15:00
  종료 일시: 2026-01-22 18:00

결과:
  → 15:00부터 18:00까지만 실행
  → 3시간 집중 포스팅
```

### 시나리오 3: 장기 캠페인 (7일)
```
설정:
  시작 일시: 2026-01-22 00:00
  종료 일시: 2026-01-29 00:00

결과:
  → 7일간 연속 실행
  → 주간 캠페인
  → 자동으로 7일 후 종료
```

### 시나리오 4: 야간 포스팅
```
설정:
  시작 일시: 2026-01-22 22:00
  종료 일시: 2026-01-23 06:00

결과:
  → 밤 10시부터 다음날 아침 6시까지
  → 익일 종료 가능
  → 8시간 야간 실행
```

### 시나리오 5: 주말만 실행
```
금요일 설정:
  시작 일시: 2026-01-24 18:00  (금요일 저녁)
  종료 일시: 2026-01-26 23:59  (일요일 밤)

결과:
  → 금요일 저녁부터 일요일 밤까지
  → 주말 집중 포스팅
```

## 💡 주요 개선 사항

### 1. 📅 정확한 날짜 지정
| 기능 | 이전 | 현재 |
|-----|------|------|
| 날짜 지정 | ❌ 불가 | ✅ 가능 |
| 여러 날 실행 | ❌ 불가 | ✅ 가능 |
| 익일 종료 | ❌ 불가 | ✅ 가능 |
| 장기 캠페인 | ❌ 어려움 | ✅ 쉬움 |

### 2. ⏰ 편리한 기본값
```
이전:
  시작: 09:00
  종료: 22:00
  → 아침 9시부터만 가능
  → 매일 수동 재설정 필요

현재:
  시작: 현재 시간
  종료: 24시간 후
  → 즉시 시작 가능
  → 자동 24시간 실행
```

### 3. 🔄 하위 호환성
```
기존 사용자:
  start_time: "09:00"
  end_time: "22:00"

자동 변환:
  → 오늘 날짜 + 시간
  → 문제없이 사용
  → 수동 변경 불필요
```

### 4. 🎯 유연한 스케줄링
```
단기:
  3시간: 15:00 → 18:00

중기:
  3일: 2026-01-22 → 2026-01-25

장기:
  1주일: 2026-01-22 → 2026-01-29

연속:
  24시간: 현재 → +24시간
```

## 🎬 실제 로그 예시

### 정상 실행
```
[14:30:00] 📂 설정 로드 완료
[14:30:00] ⏰ 스케줄 범위: 2026-01-22 14:30 ~ 2026-01-23 14:30
[14:30:00] ✅ 현재 시간이 스케줄 범위 내입니다
[14:30:00] 📨 포스팅 시작...
```

### 범위 외
```
[08:00:00] ⚠️ 스케줄 범위 외: 
           현재 2026-01-22 08:00,
           시작 2026-01-22 09:00,
           종료 2026-01-23 09:00
[08:00:00] ⏸️ 대기 중...
```

### 종료 시간 도달
```
[14:30:00] ⚠️ 스케줄 범위 외:
           현재 2026-01-23 14:31,
           시작 2026-01-22 14:30,
           종료 2026-01-23 14:30
[14:30:00] 🏁 스케줄 종료됨
```

## 📝 형식 안내

### 올바른 형식
```
✅ 2026-01-22 09:00
✅ 2026-12-31 23:59
✅ 2026-01-01 00:00

형식: YYYY-MM-DD HH:MM
  YYYY: 연도 (4자리)
  MM: 월 (01-12)
  DD: 일 (01-31)
  HH: 시 (00-23)
  MM: 분 (00-59)
```

### 잘못된 형식
```
❌ 2026-1-22 09:00     (월/일 1자리)
❌ 2026/01/22 09:00    (슬래시 사용)
❌ 22-01-2026 09:00    (순서 다름)
❌ 2026-01-22 9:00     (시 1자리)
❌ 2026-01-22 09       (분 누락)
```

## 🔮 향후 개선 계획

### 추가 예정 기능
- [ ] 캘린더 UI로 날짜 선택
- [ ] 시간대 (Timezone) 지원
- [ ] 반복 스케줄 (매주 월/수/금)
- [ ] 여러 스케줄 구간 설정
- [ ] 스케줄 프리셋 저장
- [ ] 휴일 제외 옵션

## 📝 커밋 정보

```
commit 88f01f6
Author: BandPoster Team
Date: 2026-01-22

feat: Add date+time scheduling with 24-hour default period
- Change schedule format from HH:MM to YYYY-MM-DD HH:MM
- Set default period to current time + 24 hours
- Add automatic migration from old format
- Support multi-day campaigns
- Add date/time format validation
- Improve schedule range checking with detailed logging
```

## 🎉 결론

**더 정확하고 유연한 스케줄링!**

1. 📅 **날짜+시간** - 정확한 기간 설정
2. ⏰ **24시간 기본값** - 즉시 사용 가능
3. 🔄 **자동 마이그레이션** - 기존 설정 호환
4. 🎯 **유연한 설정** - 단기/장기 모두 가능

**저장소**: https://github.com/rpaakdi1-spec/naver-band-auto-poster
**최신 커밋**: 88f01f6

---
**개발**: BandPoster Team
**날짜**: 2026-01-22
**버전**: 4.2.0
