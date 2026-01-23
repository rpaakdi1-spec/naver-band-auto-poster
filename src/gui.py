import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import time
import schedule
from datetime import datetime, timedelta
from src.band_poster import BandPoster

class BandPosterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("네이버 밴드 자동 포스팅")
        self.root.geometry("1200x900")
        
        self.poster = BandPoster()
        self.is_running = False
        self.schedule_thread = None
        self.next_post_time = None
        
        # 채팅방 체크박스 변수 리스트
        self.chat_check_vars = []
        self.chat_widgets = []
        
        self.setup_ui()
        self.load_config()
        
    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 안내 메시지
        info_frame = ttk.LabelFrame(main_frame, text="ℹ️ 사용 안내", padding="10")
        info_frame.grid(row=0, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        info_text = """
🌐 Chrome이 자동으로 실행되며, 로그인은 브라우저에서 수동으로 진행합니다.
📨 여러 채팅방을 추가하고 체크박스로 포스팅할 채팅방을 선택하세요.
⏰ 스케줄 설정으로 자동 포스팅이 가능합니다.
        """
        info_label = ttk.Label(info_frame, text=info_text.strip(), foreground="blue", justify=tk.LEFT)
        info_label.grid(row=0, column=0, sticky=tk.W)
        
        # 좌측: 채팅방 관리
        chat_frame = ttk.LabelFrame(main_frame, text="📱 채팅방 관리", padding="10")
        chat_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5, padx=(0, 5))
        
        # 별명 입력
        ttk.Label(chat_frame, text="별명:").grid(row=0, column=0, sticky=tk.W, padx=5)
        self.chat_name_entry = ttk.Entry(chat_frame, width=20)
        self.chat_name_entry.grid(row=0, column=1, sticky=tk.W, padx=5, pady=2)
        
        # URL 입력
        ttk.Label(chat_frame, text="채팅방 URL:").grid(row=1, column=0, sticky=tk.W, padx=5)
        self.chat_url_entry = ttk.Entry(chat_frame, width=40)
        self.chat_url_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5, pady=2)
        
        chat_btn_frame = ttk.Frame(chat_frame)
        chat_btn_frame.grid(row=2, column=0, columnspan=2, pady=5)
        
        ttk.Button(chat_btn_frame, text="✚ 추가", command=self.add_chat_url, width=10).pack(side=tk.LEFT, padx=2)
        ttk.Button(chat_btn_frame, text="✖ 삭제", command=self.remove_chat_url, width=10).pack(side=tk.LEFT, padx=2)
        ttk.Button(chat_btn_frame, text="🗑 전체 삭제", command=self.clear_chat_urls, width=12).pack(side=tk.LEFT, padx=2)
        
        # 채팅방 목록
        ttk.Label(chat_frame, text="✓ 등록된 채팅방 (체크하여 선택):").grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=(10, 5), padx=5)
        
        # 스크롤 가능한 채팅방 목록
        chat_list_container = ttk.Frame(chat_frame)
        chat_list_container.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        chat_canvas = tk.Canvas(chat_list_container, height=400, bg="white")
        chat_scrollbar = ttk.Scrollbar(chat_list_container, orient="vertical", command=chat_canvas.yview)
        self.chat_checkboxes_frame = ttk.Frame(chat_canvas)
        
        self.chat_checkboxes_frame.bind(
            "<Configure>",
            lambda e: chat_canvas.configure(scrollregion=chat_canvas.bbox("all"))
        )
        
        chat_canvas.create_window((0, 0), window=self.chat_checkboxes_frame, anchor="nw")
        chat_canvas.configure(yscrollcommand=chat_scrollbar.set)
        
        chat_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        chat_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        chat_frame.columnconfigure(1, weight=1)
        chat_frame.rowconfigure(4, weight=1)
        
        # 우측: 포스트 관리
        post_frame = ttk.LabelFrame(main_frame, text="📝 포스트 관리", padding="10")
        post_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5, padx=(5, 0))
        
        ttk.Label(post_frame, text="포스트 내용:").grid(row=0, column=0, sticky=tk.W)
        
        self.post_text = scrolledtext.ScrolledText(post_frame, width=50, height=5)
        self.post_text.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=5)
        
        post_btn_frame = ttk.Frame(post_frame)
        post_btn_frame.grid(row=2, column=0)
        
        ttk.Button(post_btn_frame, text="✚ 추가", command=self.add_post, width=10).pack(side=tk.LEFT, padx=5)
        ttk.Button(post_btn_frame, text="✖ 삭제", command=self.remove_post, width=10).pack(side=tk.LEFT, padx=5)
        
        ttk.Label(post_frame, text="✓ 등록된 포스트:").grid(row=3, column=0, sticky=tk.W, pady=(10, 5))
        
        post_list_frame = ttk.Frame(post_frame)
        post_list_frame.grid(row=4, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.post_listbox = tk.Listbox(post_list_frame, height=20)
        self.post_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        post_scrollbar = ttk.Scrollbar(post_list_frame, orient=tk.VERTICAL, command=self.post_listbox.yview)
        post_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.post_listbox.config(yscrollcommand=post_scrollbar.set)
        
        post_frame.columnconfigure(0, weight=1)
        post_frame.rowconfigure(4, weight=1)
        
        # 스케줄 설정
        schedule_frame = ttk.LabelFrame(main_frame, text="⏰ 스케줄 설정", padding="10")
        schedule_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(schedule_frame, text="포스팅 간격(분):").grid(row=0, column=0, sticky=tk.W)
        self.interval_entry = ttk.Entry(schedule_frame, width=15)
        self.interval_entry.grid(row=0, column=1, sticky=tk.W, padx=5)
        self.interval_entry.insert(0, "30")
        
        ttk.Label(schedule_frame, text="랜덤 딜레이(분):").grid(row=0, column=2, sticky=tk.W, padx=(20, 0))
        self.delay_entry = ttk.Entry(schedule_frame, width=15)
        self.delay_entry.grid(row=0, column=3, sticky=tk.W, padx=5)
        self.delay_entry.insert(0, "5")
        
        ttk.Label(schedule_frame, text="시작 일시:").grid(row=1, column=0, sticky=tk.W, pady=5)
        
        start_frame = ttk.Frame(schedule_frame)
        start_frame.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        
        self.start_datetime_entry = ttk.Entry(start_frame, width=20)
        self.start_datetime_entry.pack(side=tk.LEFT)
        
        ttk.Label(start_frame, text="(YYYY-MM-DD HH:MM)", font=("맑은 고딕", 8), foreground="gray").pack(side=tk.LEFT, padx=(5, 0))
        
        # 현재 시간을 기본값으로 설정
        now = datetime.now()
        default_start = now.strftime("%Y-%m-%d %H:%M")
        self.start_datetime_entry.insert(0, default_start)
        
        ttk.Label(schedule_frame, text="종료 일시:").grid(row=1, column=2, sticky=tk.W, padx=(20, 0), pady=5)
        
        end_frame = ttk.Frame(schedule_frame)
        end_frame.grid(row=1, column=3, sticky=tk.W, padx=5, pady=5)
        
        self.end_datetime_entry = ttk.Entry(end_frame, width=20)
        self.end_datetime_entry.pack(side=tk.LEFT)
        
        ttk.Label(end_frame, text="(YYYY-MM-DD HH:MM)", font=("맑은 고딕", 8), foreground="gray").pack(side=tk.LEFT, padx=(5, 0))
        
        # 24시간 후를 기본값으로 설정
        default_end = (now + timedelta(hours=24)).strftime("%Y-%m-%d %H:%M")
        self.end_datetime_entry.insert(0, default_end)
        
        ttk.Label(schedule_frame, text="채팅방 간 대기(초):").grid(row=2, column=0, sticky=tk.W)
        self.chat_interval_entry = ttk.Entry(schedule_frame, width=15)
        self.chat_interval_entry.grid(row=2, column=1, sticky=tk.W, padx=5)
        self.chat_interval_entry.insert(0, "3")
        
        # 설정
        settings_frame = ttk.LabelFrame(main_frame, text="⚙️ 설정", padding="10")
        settings_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        self.rotate_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(settings_frame, text="포스트 순환 (체크 해제 시 랜덤)", 
                       variable=self.rotate_var).grid(row=0, column=0, sticky=tk.W, padx=5)
        
        self.rotate_chat_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(settings_frame, text="채팅방 순환 (체크 해제 시 랜덤)", 
                       variable=self.rotate_chat_var).grid(row=0, column=1, sticky=tk.W, padx=5)
        
        # 다음 포스팅 카운터
        counter_frame = ttk.LabelFrame(main_frame, text="⏱️ 다음 포스팅", padding="10")
        counter_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        self.countdown_label = ttk.Label(
            counter_frame, 
            text="대기 중", 
            font=("맑은 고딕", 14, "bold"),
            foreground="gray"
        )
        self.countdown_label.pack(pady=5)
        
        self.next_post_info_label = ttk.Label(
            counter_frame,
            text="",
            font=("맑은 고딕", 9),
            foreground="blue"
        )
        self.next_post_info_label.pack()
        
        # 버튼
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="💾 설정 저장", command=self.save_config, width=12).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="▶ 시작", command=self.start_posting, width=12).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="⏸ 중지", command=self.stop_posting, width=12).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="🚀 수동 실행", command=self.manual_post, width=12).pack(side=tk.LEFT, padx=5)
        
        # 상태 표시
        self.status_label = ttk.Label(main_frame, text="상태: 대기 중", foreground="blue", font=("맑은 고딕", 10, "bold"))
        self.status_label.grid(row=6, column=0, columnspan=2, pady=5)
        
        # 로그
        log_frame = ttk.LabelFrame(main_frame, text="📋 로그", padding="10")
        log_frame.grid(row=7, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, width=100, height=12, state=tk.DISABLED)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        # 그리드 가중치 설정
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=2)  # 채팅방/포스트 영역
        main_frame.rowconfigure(7, weight=1)  # 로그 영역
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # 카운터 업데이트 시작
        self.update_countdown()
        
    def update_countdown(self):
        """다음 포스팅까지 카운트다운 업데이트"""
        if self.is_running and self.next_post_time:
            now = datetime.now()
            remaining = self.next_post_time - now
            
            if remaining.total_seconds() > 0:
                hours = int(remaining.total_seconds() // 3600)
                minutes = int((remaining.total_seconds() % 3600) // 60)
                seconds = int(remaining.total_seconds() % 60)
                
                if hours > 0:
                    countdown_text = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
                else:
                    countdown_text = f"{minutes:02d}:{seconds:02d}"
                
                self.countdown_label.config(
                    text=countdown_text,
                    foreground="green"
                )
                
                next_time_str = self.next_post_time.strftime("%H:%M:%S")
                self.next_post_info_label.config(
                    text=f"다음 포스팅 예정: {next_time_str}"
                )
            else:
                self.countdown_label.config(
                    text="포스팅 중...",
                    foreground="orange"
                )
        else:
            self.countdown_label.config(
                text="대기 중",
                foreground="gray"
            )
            self.next_post_info_label.config(text="")
        
        # 1초마다 업데이트
        self.root.after(1000, self.update_countdown)
        
    def log(self, message):
        """로그 메시지 추가"""
        self.log_text.config(state=tk.NORMAL)
        timestamp = time.strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
        
    def refresh_chat_list(self):
        """채팅방 목록 UI 새로고침"""
        # 기존 위젯 제거
        for widget in self.chat_widgets:
            widget.destroy()
        self.chat_widgets.clear()
        self.chat_check_vars.clear()
        
        # 채팅방 목록 다시 그리기
        chat_rooms = self.poster.config.get('chat_rooms', [])
        for i, room in enumerate(chat_rooms):
            frame = ttk.Frame(self.chat_checkboxes_frame)
            frame.pack(fill=tk.X, padx=5, pady=2)
            
            var = tk.BooleanVar(value=room.get('enabled', True))
            self.chat_check_vars.append(var)
            
            checkbox = ttk.Checkbutton(
                frame,
                text="",
                variable=var,
                command=lambda idx=i: self.toggle_chat(idx)
            )
            checkbox.pack(side=tk.LEFT)
            
            name_label = ttk.Label(
                frame,
                text=f"[{room.get('name', '이름없음')}]",
                font=("맑은 고딕", 9, "bold"),
                foreground="blue"
            )
            name_label.pack(side=tk.LEFT, padx=(5, 10))
            
            url_text = room.get('url', '')
            url_display = url_text if len(url_text) <= 40 else url_text[:37] + "..."
            url_label = ttk.Label(frame, text=url_display, font=("맑은 고딕", 8))
            url_label.pack(side=tk.LEFT)
            
            self.chat_widgets.extend([frame, checkbox, name_label, url_label])
        
    def toggle_chat(self, index):
        """채팅방 활성화/비활성화 토글"""
        chat_rooms = self.poster.config.get('chat_rooms', [])
        if index < len(chat_rooms):
            chat_rooms[index]['enabled'] = self.chat_check_vars[index].get()
            enabled_text = "활성화" if chat_rooms[index]['enabled'] else "비활성화"
            self.log(f"채팅방 {chat_rooms[index]['name']} {enabled_text}")
        
    def add_chat_url(self):
        """채팅방 URL 추가"""
        name = self.chat_name_entry.get().strip()
        url = self.chat_url_entry.get().strip()
        
        if not url:
            messagebox.showwarning("경고", "채팅방 URL을 입력하세요.")
            return
        
        if not url.startswith("https://"):
            messagebox.showwarning("경고", "올바른 URL을 입력하세요. (https://로 시작)")
            return
        
        if not name:
            name = f"채팅방{len(self.poster.config.get('chat_rooms', [])) + 1}"
        
        # chat_rooms 구조로 변경
        self.poster.config.setdefault('chat_rooms', [])
        self.poster.config['chat_rooms'].append({
            'name': name,
            'url': url,
            'enabled': True
        })
        
        self.refresh_chat_list()
        
        self.chat_name_entry.delete(0, tk.END)
        self.chat_url_entry.delete(0, tk.END)
        self.log(f"✅ 채팅방 추가: [{name}] {url}")
        
    def remove_chat_url(self):
        """선택된 채팅방 삭제"""
        chat_rooms = self.poster.config.get('chat_rooms', [])
        if not chat_rooms:
            messagebox.showwarning("경고", "삭제할 채팅방이 없습니다.")
            return
        
        # 선택 대화상자
        dialog = tk.Toplevel(self.root)
        dialog.title("채팅방 삭제")
        dialog.geometry("500x400")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text="삭제할 채팅방을 선택하세요:", font=("맑은 고딕", 10, "bold")).pack(pady=10)
        
        listbox_frame = ttk.Frame(dialog)
        listbox_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        listbox = tk.Listbox(listbox_frame, selectmode=tk.MULTIPLE)
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(listbox_frame, orient=tk.VERTICAL, command=listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        listbox.config(yscrollcommand=scrollbar.set)
        
        for room in chat_rooms:
            listbox.insert(tk.END, f"[{room['name']}] {room['url']}")
        
        def confirm_delete():
            selections = listbox.curselection()
            if not selections:
                messagebox.showwarning("경고", "삭제할 채팅방을 선택하세요.")
                return
            
            # 역순으로 삭제 (인덱스 변경 방지)
            for index in sorted(selections, reverse=True):
                removed = chat_rooms.pop(index)
                self.log(f"🗑 채팅방 삭제: [{removed['name']}]")
            
            self.refresh_chat_list()
            dialog.destroy()
        
        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="삭제", command=confirm_delete, width=10).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="취소", command=dialog.destroy, width=10).pack(side=tk.LEFT, padx=5)
        
    def clear_chat_urls(self):
        """모든 채팅방 URL 삭제"""
        if not messagebox.askyesno("확인", "모든 채팅방을 삭제하시겠습니까?"):
            return
        
        self.poster.config['chat_rooms'] = []
        self.refresh_chat_list()
        self.log("🗑 모든 채팅방 삭제됨")
        
    def add_post(self):
        """포스트 추가"""
        content = self.post_text.get("1.0", tk.END).strip()
        if not content:
            messagebox.showwarning("경고", "포스트 내용을 입력하세요.")
            return
        
        self.poster.config['posts'].append({
            'content': content,
            'enabled': True
        })
        
        # 리스트박스에 추가
        display_content = content[:50] + "..." if len(content) > 50 else content
        self.post_listbox.insert(tk.END, f"✓ {display_content}")
        
        self.post_text.delete("1.0", tk.END)
        self.log(f"✅ 포스트 추가: {display_content}")
        
    def remove_post(self):
        """포스트 삭제"""
        selection = self.post_listbox.curselection()
        if not selection:
            messagebox.showwarning("경고", "삭제할 포스트를 선택하세요.")
            return
        
        index = selection[0]
        self.poster.config['posts'].pop(index)
        self.post_listbox.delete(index)
        self.log(f"🗑 포스트 삭제: 인덱스 {index}")
        
    def start_posting(self):
        """자동 포스팅 시작"""
        if self.is_running:
            messagebox.showinfo("알림", "이미 실행 중입니다.")
            return
        
        enabled_chats = [room for room in self.poster.config.get('chat_rooms', []) if room.get('enabled', True)]
        if not enabled_chats:
            messagebox.showwarning("경고", "활성화된 채팅방이 없습니다. 채팅방을 추가하고 체크하세요.")
            return
        
        if not self.poster.config['posts']:
            messagebox.showwarning("경고", "포스트를 먼저 추가하세요.")
            return
        
        self.is_running = True
        self.status_label.config(text="상태: ▶ 실행 중", foreground="green")
        self.log("▶ 자동 포스팅 시작")
        
        # 스케줄 초기화 (이전 스케줄 제거)
        schedule.clear()
        
        # 간격 설정
        interval = self.poster.config['schedule']['interval_minutes']
        
        # 다음 포스팅 시간을 먼저 설정 (카운트다운 표시용)
        self.next_post_time = datetime.now() + timedelta(minutes=interval)
        self.log(f"⏰ 첫 포스팅 후 다음 예정: {self.next_post_time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # 즉시 첫 포스팅 실행 (백그라운드)
        def first_post():
            self.log("🚀 첫 포스팅 실행 중...")
            try:
                success = self.poster.run_once()
                if success:
                    self.log(f"✅ 첫 포스팅 완료")
                else:
                    self.log(f"❌ 첫 포스팅 실패")
            except Exception as e:
                self.log(f"❌ 첫 포스팅 오류: {str(e)}")
            
            # 다음 포스팅 시간 재계산
            self.next_post_time = datetime.now() + timedelta(minutes=interval)
            self.log(f"⏰ 다음 포스팅: {self.next_post_time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # 첫 포스팅을 백그라운드에서 실행
        threading.Thread(target=first_post, daemon=True).start()
        
        # 스케줄 설정 (interval 분마다 실행)
        schedule.every(interval).minutes.do(self.scheduled_post)
        self.log(f"📅 스케줄 설정 완료: {interval}분마다 포스팅")
        
        # 스케줄 실행 스레드 (기존 스레드가 없을 때만 시작)
        if not self.schedule_thread or not self.schedule_thread.is_alive():
            self.schedule_thread = threading.Thread(target=self.run_schedule, daemon=True)
            self.schedule_thread.start()
            self.log("⚙️ 스케줄 실행 스레드 시작")
        
    def scheduled_post(self):
        """스케줄된 포스팅 실행"""
        if not self.is_running:
            self.log("⚠️ 중지됨 - 스케줄 포스팅 건너뜀")
            return
        
        self.log("📅 스케줄 포스팅 시작...")
        
        try:
            success = self.poster.run_once()
            if success:
                self.log("✅ 스케줄 포스팅 완료")
            else:
                self.log("❌ 스케줄 포스팅 실패")
        except Exception as e:
            self.log(f"❌ 스케줄 포스팅 오류: {str(e)}")
        
        # 다음 포스팅 시간 계산
        interval = self.poster.config['schedule']['interval_minutes']
        self.next_post_time = datetime.now() + timedelta(minutes=interval)
        self.log(f"⏰ 다음 포스팅 예정: {self.next_post_time.strftime('%Y-%m-%d %H:%M:%S')}")
        
    def run_schedule(self):
        """스케줄 실행"""
        while self.is_running:
            schedule.run_pending()
            time.sleep(1)
            
    def stop_posting(self):
        """자동 포스팅 중지"""
        if not self.is_running:
            messagebox.showinfo("알림", "실행 중이 아닙니다.")
            return
        
        self.is_running = False
        self.next_post_time = None
        schedule.clear()
        self.status_label.config(text="상태: ⏸ 중지됨", foreground="red")
        self.log("⏸ 자동 포스팅 중지")
        
    def manual_post(self):
        """수동 포스팅"""
        enabled_chats = [room for room in self.poster.config.get('chat_rooms', []) if room.get('enabled', True)]
        if not enabled_chats:
            messagebox.showwarning("경고", "활성화된 채팅방이 없습니다. 채팅방을 추가하고 체크하세요.")
            return
        
        if not self.poster.config['posts']:
            messagebox.showwarning("경고", "포스트를 먼저 추가하세요.")
            return
        
        self.status_label.config(text="상태: 🚀 수동 실행 중...", foreground="orange")
        self.log("🚀 수동 포스팅 시작...")
        
        def post_thread():
            try:
                success = self.poster.run_once()
                if success:
                    self.log("✅ 수동 포스팅 완료!")
                    self.status_label.config(text="상태: ✅ 완료", foreground="green")
                    messagebox.showinfo("완료", "포스팅이 완료되었습니다!")
                else:
                    self.log("❌ 수동 포스팅 실패")
                    self.status_label.config(text="상태: ❌ 실패", foreground="red")
                    messagebox.showerror("오류", "포스팅에 실패했습니다.")
            except Exception as e:
                self.log(f"❌ 오류: {str(e)}")
                self.status_label.config(text="상태: ❌ 오류", foreground="red")
                messagebox.showerror("오류", f"오류가 발생했습니다:\n{str(e)}")
        
        threading.Thread(target=post_thread, daemon=True).start()
        
    def save_config(self):
        """설정 저장"""
        try:
            # 스케줄 설정 저장
            self.poster.config['schedule']['interval_minutes'] = int(self.interval_entry.get())
            self.poster.config['schedule']['random_delay_minutes'] = int(self.delay_entry.get())
            self.poster.config['schedule']['start_datetime'] = self.start_datetime_entry.get()
            self.poster.config['schedule']['end_datetime'] = self.end_datetime_entry.get()
            
            # 날짜+시간 형식 검증
            try:
                datetime.strptime(self.start_datetime_entry.get(), "%Y-%m-%d %H:%M")
                datetime.strptime(self.end_datetime_entry.get(), "%Y-%m-%d %H:%M")
            except ValueError:
                raise ValueError("날짜/시간 형식이 올바르지 않습니다. (YYYY-MM-DD HH:MM)")
            
            # 채팅방 설정 저장
            self.poster.config['settings']['wait_between_chats'] = int(self.chat_interval_entry.get())
            self.poster.config['settings']['rotate_posts'] = self.rotate_var.get()
            self.poster.config['settings']['rotate_chats'] = self.rotate_chat_var.get()
            
            # 파일에 저장
            self.poster.save_config()
            
            self.log("💾 설정이 저장되었습니다.")
            self.status_label.config(text="상태: 💾 저장 완료", foreground="green")
            messagebox.showinfo("완료", "설정이 저장되었습니다.")
        except Exception as e:
            self.log(f"❌ 설정 저장 실패: {str(e)}")
            messagebox.showerror("오류", f"설정 저장 중 오류가 발생했습니다:\n{str(e)}")
        
    def load_config(self):
        """설정 로드"""
        config = self.poster.config
        
        # 스케줄 설정 로드
        self.interval_entry.delete(0, tk.END)
        self.interval_entry.insert(0, str(config['schedule'].get('interval_minutes', 30)))
        
        self.delay_entry.delete(0, tk.END)
        self.delay_entry.insert(0, str(config['schedule'].get('random_delay_minutes', 5)))
        
        # 날짜+시간 로드 (기존 시간 형식 마이그레이션)
        self.start_datetime_entry.delete(0, tk.END)
        if 'start_datetime' in config['schedule']:
            # 새로운 형식
            self.start_datetime_entry.insert(0, config['schedule'].get('start_datetime'))
        elif 'start_time' in config['schedule']:
            # 기존 형식 (HH:MM) -> 오늘 날짜 + 시간으로 변환
            old_time = config['schedule'].get('start_time', '09:00')
            today = datetime.now().strftime("%Y-%m-%d")
            self.start_datetime_entry.insert(0, f"{today} {old_time}")
        else:
            # 기본값: 현재 시간
            self.start_datetime_entry.insert(0, datetime.now().strftime("%Y-%m-%d %H:%M"))
        
        self.end_datetime_entry.delete(0, tk.END)
        if 'end_datetime' in config['schedule']:
            # 새로운 형식
            self.end_datetime_entry.insert(0, config['schedule'].get('end_datetime'))
        elif 'end_time' in config['schedule']:
            # 기존 형식 (HH:MM) -> 오늘 날짜 + 시간으로 변환
            old_time = config['schedule'].get('end_time', '22:00')
            today = datetime.now().strftime("%Y-%m-%d")
            self.end_datetime_entry.insert(0, f"{today} {old_time}")
        else:
            # 기본값: 24시간 후
            self.end_datetime_entry.insert(0, (datetime.now() + timedelta(hours=24)).strftime("%Y-%m-%d %H:%M"))
        
        self.chat_interval_entry.delete(0, tk.END)
        self.chat_interval_entry.insert(0, str(config['settings'].get('wait_between_chats', 3)))
        
        # 설정 로드
        self.rotate_var.set(config['settings'].get('rotate_posts', True))
        self.rotate_chat_var.set(config['settings'].get('rotate_chats', True))
        
        # 채팅방 목록 로드 (chat_urls -> chat_rooms 마이그레이션)
        if 'chat_urls' in config and not config.get('chat_rooms'):
            # 기존 chat_urls를 chat_rooms로 변환
            config['chat_rooms'] = []
            for i, url in enumerate(config.get('chat_urls', []), 1):
                config['chat_rooms'].append({
                    'name': f'채팅방{i}',
                    'url': url,
                    'enabled': True
                })
            # 기존 chat_urls 제거
            if 'chat_urls' in config:
                del config['chat_urls']
        
        self.refresh_chat_list()
        
        # 포스트 로드
        for post in config['posts']:
            if post.get('enabled', True):
                content = post['content']
                display_content = content[:50] + "..." if len(content) > 50 else content
                self.post_listbox.insert(tk.END, f"✓ {display_content}")
        
        self.log("📂 설정 로드 완료")

def main():
    root = tk.Tk()
    app = BandPosterGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
