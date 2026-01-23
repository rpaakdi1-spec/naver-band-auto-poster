"""
네이버밴드 자동 포스팅 웹 애플리케이션 (Streamlit)
"""

import streamlit as st
import time
import schedule
from datetime import datetime, timedelta
from src.band_poster import BandPoster
import threading

# 페이지 설정
st.set_page_config(
    page_title="네이버밴드 자동 포스팅",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 세션 상태 초기화
if 'poster' not in st.session_state:
    st.session_state.poster = BandPoster()
    st.session_state.is_running = False
    st.session_state.next_post_time = None
    st.session_state.logs = []

def log_message(message):
    """로그 메시지 추가"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    st.session_state.logs.append(f"[{timestamp}] {message}")
    # 최근 100개만 유지
    if len(st.session_state.logs) > 100:
        st.session_state.logs = st.session_state.logs[-100:]

def add_chat_room(name, url):
    """채팅방 추가"""
    if not url:
        st.warning("⚠️ 채팅방 URL을 입력하세요.")
        return False
    
    if not url.startswith("https://"):
        st.warning("⚠️ 올바른 URL을 입력하세요. (https://로 시작)")
        return False
    
    if not name:
        name = f"채팅방{len(st.session_state.poster.config.get('chat_rooms', [])) + 1}"
    
    st.session_state.poster.config.setdefault('chat_rooms', [])
    st.session_state.poster.config['chat_rooms'].append({
        'name': name,
        'url': url,
        'enabled': True
    })
    
    log_message(f"✅ 채팅방 추가: [{name}] {url}")
    return True

def add_post(content):
    """포스트 추가"""
    if not content.strip():
        st.warning("⚠️ 포스트 내용을 입력하세요.")
        return False
    
    st.session_state.poster.config['posts'].append({
        'content': content,
        'enabled': True
    })
    
    log_message(f"✅ 포스트 추가: {content[:50]}...")
    return True

def save_config():
    """설정 저장"""
    try:
        st.session_state.poster.save_config()
        log_message("✅ 설정 저장 완료")
        st.success("✅ 설정이 저장되었습니다!")
        return True
    except Exception as e:
        log_message(f"❌ 설정 저장 실패: {str(e)}")
        st.error(f"❌ 설정 저장 실패: {str(e)}")
        return False

def start_posting():
    """자동 포스팅 시작"""
    enabled_chats = [room for room in st.session_state.poster.config.get('chat_rooms', []) 
                     if room.get('enabled', True)]
    
    if not enabled_chats:
        st.warning("⚠️ 활성화된 채팅방이 없습니다. 채팅방을 추가하고 체크하세요.")
        return
    
    if not st.session_state.poster.config['posts']:
        st.warning("⚠️ 포스트를 먼저 추가하세요.")
        return
    
    st.session_state.is_running = True
    log_message("▶ 자동 포스팅 시작")
    
    # 다음 포스팅 시간 설정
    interval = st.session_state.poster.config['schedule']['interval_minutes']
    st.session_state.next_post_time = datetime.now() + timedelta(minutes=interval)
    
    st.success("▶ 자동 포스팅이 시작되었습니다!")

def stop_posting():
    """자동 포스팅 중지"""
    st.session_state.is_running = False
    st.session_state.next_post_time = None
    schedule.clear()
    log_message("⏸ 자동 포스팅 중지")
    st.info("⏸ 자동 포스팅이 중지되었습니다.")

def manual_post():
    """수동 포스팅"""
    enabled_chats = [room for room in st.session_state.poster.config.get('chat_rooms', []) 
                     if room.get('enabled', True)]
    
    if not enabled_chats:
        st.warning("⚠️ 활성화된 채팅방이 없습니다.")
        return
    
    if not st.session_state.poster.config['posts']:
        st.warning("⚠️ 포스트를 먼저 추가하세요.")
        return
    
    log_message("🚀 수동 포스팅 시작...")
    
    with st.spinner("포스팅 중..."):
        try:
            success = st.session_state.poster.run_once()
            if success:
                log_message("✅ 수동 포스팅 완료!")
                st.success("✅ 포스팅이 완료되었습니다!")
            else:
                log_message("❌ 수동 포스팅 실패")
                st.error("❌ 포스팅에 실패했습니다.")
        except Exception as e:
            log_message(f"❌ 오류: {str(e)}")
            st.error(f"❌ 오류가 발생했습니다: {str(e)}")

# ===== 메인 UI =====

st.title("📱 네이버밴드 자동 포스팅")

# 안내 메시지
st.info("""
🌐 Chrome이 자동으로 실행되며, 로그인은 브라우저에서 수동으로 진행합니다.  
📨 여러 채팅방을 추가하고 체크박스로 포스팅할 채팅방을 선택하세요.  
⏰ 스케줄 설정으로 자동 포스팅이 가능합니다.
""")

# 사이드바: 설정
with st.sidebar:
    st.header("⚙️ 설정")
    
    # 스케줄 설정
    st.subheader("📅 스케줄 설정")
    
    interval_minutes = st.number_input(
        "포스팅 간격 (분)",
        min_value=1,
        max_value=1440,
        value=st.session_state.poster.config['schedule'].get('interval_minutes', 30),
        help="포스팅 반복 주기 (분)"
    )
    
    random_delay = st.number_input(
        "랜덤 딜레이 (분)",
        min_value=0,
        max_value=60,
        value=st.session_state.poster.config['schedule'].get('random_delay_minutes', 5),
        help="포스팅 후 랜덤 대기 시간 (분)"
    )
    
    # 날짜+시간 입력
    now = datetime.now()
    
    start_datetime = st.text_input(
        "시작 일시",
        value=st.session_state.poster.config['schedule'].get('start_datetime', now.strftime("%Y-%m-%d %H:%M")),
        help="형식: YYYY-MM-DD HH:MM"
    )
    
    end_datetime = st.text_input(
        "종료 일시",
        value=st.session_state.poster.config['schedule'].get('end_datetime', 
                                                              (now + timedelta(hours=24)).strftime("%Y-%m-%d %H:%M")),
        help="형식: YYYY-MM-DD HH:MM"
    )
    
    chat_interval = st.number_input(
        "채팅방 간 대기 (초)",
        min_value=1,
        max_value=60,
        value=st.session_state.poster.config['settings'].get('wait_between_chats', 3),
        help="채팅방 간 대기 시간 (초)"
    )
    
    st.divider()
    
    # 추가 설정
    st.subheader("🔧 추가 설정")
    
    rotate_posts = st.checkbox(
        "포스트 순환",
        value=st.session_state.poster.config['settings'].get('rotate_posts', True),
        help="체크: 순서대로 / 해제: 랜덤"
    )
    
    rotate_chats = st.checkbox(
        "채팅방 순환",
        value=st.session_state.poster.config['settings'].get('rotate_chats', True),
        help="체크: 순서대로 / 해제: 랜덤"
    )
    
    st.divider()
    
    # 설정 저장 버튼
    if st.button("💾 설정 저장", use_container_width=True):
        # 설정 업데이트
        st.session_state.poster.config['schedule']['interval_minutes'] = interval_minutes
        st.session_state.poster.config['schedule']['random_delay_minutes'] = random_delay
        st.session_state.poster.config['schedule']['start_datetime'] = start_datetime
        st.session_state.poster.config['schedule']['end_datetime'] = end_datetime
        st.session_state.poster.config['settings']['wait_between_chats'] = chat_interval
        st.session_state.poster.config['settings']['rotate_posts'] = rotate_posts
        st.session_state.poster.config['settings']['rotate_chats'] = rotate_chats
        
        save_config()

# 메인 컨텐츠: 2열 레이아웃
col1, col2 = st.columns(2)

# 좌측: 채팅방 관리
with col1:
    st.header("📱 채팅방 관리")
    
    with st.form("add_chat_form"):
        chat_name = st.text_input("별명", placeholder="예: 메인 채팅방")
        chat_url = st.text_input("채팅방 URL", placeholder="https://band.us/band/.../chat/...")
        
        col_a, col_b = st.columns([1, 1])
        with col_a:
            if st.form_submit_button("✚ 추가", use_container_width=True):
                if add_chat_room(chat_name, chat_url):
                    st.rerun()
        
        with col_b:
            if st.form_submit_button("🗑 전체 삭제", use_container_width=True):
                st.session_state.poster.config['chat_rooms'] = []
                log_message("🗑 모든 채팅방 삭제됨")
                st.rerun()
    
    st.subheader("✓ 등록된 채팅방")
    
    chat_rooms = st.session_state.poster.config.get('chat_rooms', [])
    
    if not chat_rooms:
        st.info("등록된 채팅방이 없습니다.")
    else:
        for idx, room in enumerate(chat_rooms):
            col_check, col_info, col_del = st.columns([0.5, 3, 0.5])
            
            with col_check:
                enabled = st.checkbox(
                    "활성",
                    value=room.get('enabled', True),
                    key=f"chat_{idx}",
                    label_visibility="collapsed"
                )
                room['enabled'] = enabled
            
            with col_info:
                st.text(f"[{room.get('name', '이름없음')}]")
                st.caption(room.get('url', '')[:60] + "...")
            
            with col_del:
                if st.button("🗑", key=f"del_chat_{idx}"):
                    st.session_state.poster.config['chat_rooms'].pop(idx)
                    log_message(f"🗑 채팅방 삭제: {room.get('name', '')}")
                    st.rerun()

# 우측: 포스트 관리
with col2:
    st.header("📝 포스트 관리")
    
    with st.form("add_post_form"):
        post_content = st.text_area("포스트 내용", height=100, placeholder="포스팅할 내용을 입력하세요...")
        
        col_a, col_b = st.columns([1, 1])
        with col_a:
            if st.form_submit_button("✚ 추가", use_container_width=True):
                if add_post(post_content):
                    st.rerun()
        
        with col_b:
            if st.form_submit_button("🗑 전체 삭제", use_container_width=True):
                st.session_state.poster.config['posts'] = []
                log_message("🗑 모든 포스트 삭제됨")
                st.rerun()
    
    st.subheader("✓ 등록된 포스트")
    
    posts = st.session_state.poster.config.get('posts', [])
    
    if not posts:
        st.info("등록된 포스트가 없습니다.")
    else:
        for idx, post in enumerate(posts):
            col_check, col_info, col_del = st.columns([0.5, 3, 0.5])
            
            with col_check:
                enabled = st.checkbox(
                    "활성",
                    value=post.get('enabled', True),
                    key=f"post_{idx}",
                    label_visibility="collapsed"
                )
                post['enabled'] = enabled
            
            with col_info:
                content = post.get('content', '')
                display = content[:50] + "..." if len(content) > 50 else content
                st.text(display)
            
            with col_del:
                if st.button("🗑", key=f"del_post_{idx}"):
                    st.session_state.poster.config['posts'].pop(idx)
                    log_message(f"🗑 포스트 삭제")
                    st.rerun()

# 실행 버튼
st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("▶ 시작", use_container_width=True, type="primary", disabled=st.session_state.is_running):
        start_posting()
        st.rerun()

with col2:
    if st.button("⏸ 중지", use_container_width=True, disabled=not st.session_state.is_running):
        stop_posting()
        st.rerun()

with col3:
    if st.button("🚀 수동 실행", use_container_width=True):
        manual_post()

# 상태 표시
st.divider()

status_col1, status_col2 = st.columns(2)

with status_col1:
    if st.session_state.is_running:
        st.success("▶ 실행 중")
        
        if st.session_state.next_post_time:
            remaining = st.session_state.next_post_time - datetime.now()
            if remaining.total_seconds() > 0:
                hours = int(remaining.total_seconds() // 3600)
                minutes = int((remaining.total_seconds() % 3600) // 60)
                seconds = int(remaining.total_seconds() % 60)
                
                if hours > 0:
                    countdown_text = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
                else:
                    countdown_text = f"{minutes:02d}:{seconds:02d}"
                
                st.metric("다음 포스팅까지", countdown_text)
                st.caption(f"다음 포스팅: {st.session_state.next_post_time.strftime('%H:%M:%S')}")
            else:
                st.info("포스팅 중...")
    else:
        st.info("⏸ 대기 중")

with status_col2:
    st.metric("등록된 채팅방", len(st.session_state.poster.config.get('chat_rooms', [])))
    st.metric("등록된 포스트", len(st.session_state.poster.config.get('posts', [])))

# 로그
st.divider()
st.subheader("📋 로그")

log_container = st.container(height=300)
with log_container:
    if st.session_state.logs:
        for log in reversed(st.session_state.logs[-50:]):  # 최근 50개만 표시
            st.text(log)
    else:
        st.info("로그가 없습니다.")

# 자동 새로고침 (실행 중일 때)
if st.session_state.is_running:
    time.sleep(1)
    st.rerun()
