"""
네이버밴드 자동 포스팅 GUI (다중 채팅방)
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import schedule
import time
from src.band_poster import BandPoster


class BandPosterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("네이버밴드 자동 포스팅 (다중 채팅방)")
        self.root.geometry("900x800")
        
        self.poster = BandPoster()
        self.is_running = False
        self.schedule_thread = None
        
        self.create_widgets()
        self.load_config()
        
    def create_widgets(self):
        """GUI 위젯 생성"""
        # 메인 프레임
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 안내 메시지
        info_frame = ttk.LabelFrame(main_frame, text="ℹ️ 사용 안내", padding="10")
        info_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        info_text = """
🌐 Chrome이 자동으로 실행되며, 로그인은 브라우저에서 수동으로 진행합니다.
📨 여러 채팅방 URL을 추가하면 순차적으로 메시지를 전송합니다.
⏰ 스케줄 설정으로 자동 포스팅이 가능합니다.
        """
        info_label = ttk.Label(info_frame, text=info_text.strip(), foreground="blue", justify=tk.LEFT)
        info_label.grid(row=0, column=0, sticky=tk.W)
        
        # 채팅방 URL 관리
        chat_frame = ttk.LabelFrame(main_frame, text="📱 채팅방 URL 관리", padding="10")
        chat_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(chat_frame, text="채팅방 URL:").grid(row=0, column=0, sticky=tk.W)
        self.chat_url_entry = ttk.Entry(chat_frame, width=60)
        self.chat_url_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5)
        
        chat_btn_frame = ttk.Frame(chat_frame)
        chat_btn_frame.grid(row=1, column=0, columnspan=2, pady=5)
        
        ttk.Button(chat_btn_frame, text="추가", command=self.add_chat_url).pack(side=tk.LEFT, padx=2)
        ttk.Button(chat_btn_frame, text="삭제", command=self.remove_chat_url).pack(side=tk.LEFT, padx=2)
        ttk.Button(chat_btn_frame, text="전체 삭제", command=self.clear_chat_urls).pack(side=tk.LEFT, padx=2)
        ttk.Button(chat_btn_frame, text="🔄 채팅방 불러오기", command=self.fetch_chat_rooms).pack(side=tk.LEFT, padx=2)
        
        # 채팅방 목록
        ttk.Label(chat_frame, text="등록된 채팅방:").grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=(10, 5))
        
        chat_list_frame = ttk.Frame(chat_frame)
        chat_list_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
        self.chat_listbox = tk.Listbox(chat_list_frame, height=8)
        self.chat_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        chat_scrollbar = ttk.Scrollbar(chat_list_frame, orient=tk.VERTICAL, command=self.chat_listbox.yview)
        chat_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.chat_listbox.config(yscrollcommand=chat_scrollbar.set)
        
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
        
        ttk.Label(schedule_frame, text="시작 시간:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.start_time_entry = ttk.Entry(schedule_frame, width=15)
        self.start_time_entry.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        self.start_time_entry.insert(0, "09:00")
        
        ttk.Label(schedule_frame, text="종료 시간:").grid(row=1, column=2, sticky=tk.W, padx=(20, 0), pady=5)
        self.end_time_entry = ttk.Entry(schedule_frame, width=15)
        self.end_time_entry.grid(row=1, column=3, sticky=tk.W, padx=5, pady=5)
        self.end_time_entry.insert(0, "22:00")
        
        ttk.Label(schedule_frame, text="채팅방 간격(초):").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.chat_interval_entry = ttk.Entry(schedule_frame, width=15)
        self.chat_interval_entry.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
        self.chat_interval_entry.insert(0, "3")
        
        # 포스트 관리
        post_frame = ttk.LabelFrame(main_frame, text="📝 포스트 관리", padding="10")
        post_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        ttk.Label(post_frame, text="포스트 내용:").grid(row=0, column=0, sticky=tk.W)
        
        self.post_text = scrolledtext.ScrolledText(post_frame, width=70, height=6)
        self.post_text.grid(row=1, column=0, columnspan=2, pady=5)
        
        ttk.Button(post_frame, text="추가", command=self.add_post).grid(row=2, column=0, pady=5)
        ttk.Button(post_frame, text="삭제", command=self.remove_post).grid(row=2, column=1, pady=5)
        
        # 포스트 목록
        self.post_listbox = tk.Listbox(post_frame, height=4)
        self.post_listbox.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        post_scrollbar = ttk.Scrollbar(post_frame, orient=tk.VERTICAL, command=self.post_listbox.yview)
        post_scrollbar.grid(row=3, column=2, sticky=(tk.N, tk.S))
        self.post_listbox.config(yscrollcommand=post_scrollbar.set)
        
        # 설정
        settings_frame = ttk.LabelFrame(main_frame, text="⚙️ 설정", padding="10")
        settings_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        self.rotate_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(settings_frame, text="포스트 순환 (체크 해제 시 랜덤)", 
                       variable=self.rotate_var).grid(row=0, column=0, sticky=tk.W, padx=5)
        
        self.rotate_chat_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(settings_frame, text="채팅방 순환 (체크 해제 시 랜덤)", 
                       variable=self.rotate_chat_var).grid(row=0, column=1, sticky=tk.W, padx=5)
        
        # 버튼
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="설정 저장", command=self.save_config).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="시작", command=self.start_posting).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="중지", command=self.stop_posting).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="수동 실행", command=self.manual_post).pack(side=tk.LEFT, padx=5)
        
        # 상태 표시
        self.status_label = ttk.Label(main_frame, text="상태: 대기 중", foreground="blue")
        self.status_label.grid(row=6, column=0, columnspan=2, pady=5)
        
        # 로그
        log_frame = ttk.LabelFrame(main_frame, text="📋 로그", padding="10")
        log_frame.grid(row=7, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, width=70, height=8, state=tk.DISABLED)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 그리드 가중치 설정
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(3, weight=1)
        main_frame.rowconfigure(7, weight=1)
        
    def log(self, message):
        """로그 메시지 추가"""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
        
    def add_chat_url(self):
        """채팅방 URL 추가"""
        url = self.chat_url_entry.get().strip()
        if not url:
            messagebox.showwarning("경고", "채팅방 URL을 입력하세요.")
            return
        
        if not url.startswith("https://"):
            messagebox.showwarning("경고", "올바른 URL을 입력하세요. (https://로 시작)")
            return
        
        self.poster.config.setdefault('chat_urls', [])
        self.poster.config['chat_urls'].append(url)
        
        # 리스트박스에 추가 (짧게 표시)
        display_url = url if len(url) <= 60 else url[:57] + "..."
        self.chat_listbox.insert(tk.END, display_url)
        
        self.chat_url_entry.delete(0, tk.END)
        self.log(f"채팅방 추가: {url}")
        
    def remove_chat_url(self):
        """채팅방 URL 삭제"""
        selection = self.chat_listbox.curselection()
        if not selection:
            messagebox.showwarning("경고", "삭제할 채팅방을 선택하세요.")
            return
        
        index = selection[0]
        url = self.poster.config['chat_urls'][index]
        self.poster.config['chat_urls'].pop(index)
        self.chat_listbox.delete(index)
        self.log(f"채팅방 삭제: {url}")
        
    def clear_chat_urls(self):
        """모든 채팅방 URL 삭제"""
        if not messagebox.askyesno("확인", "모든 채팅방을 삭제하시겠습니까?"):
            return
        
        self.poster.config['chat_urls'] = []
        self.chat_listbox.delete(0, tk.END)
        self.log("모든 채팅방 삭제됨")
    
    def fetch_chat_rooms(self):
        """채팅방 목록 자동 불러오기"""
        self.log("🔄 채팅방 목록 불러오는 중...")
        self.status_label.config(text="상태: 채팅방 불러오는 중...", foreground="orange")
        
        def fetch_thread():
            try:
                # 드라이버 초기화
                if not self.poster.driver:
                    self.poster.init_driver()
                
                # 로그인 확인
                if not self.poster.is_logged_in:
                    if not self.poster.start_chrome_and_wait_for_login():
                        self.log("❌ 로그인 실패")
                        self.status_label.config(text="상태: 로그인 실패", foreground="red")
                        messagebox.showerror("오류", "로그인이 필요합니다.")
                        return
                
                # 채팅방 목록 가져오기
                chat_list = self.poster.fetch_chat_list()
                
                if not chat_list:
                    self.log("⚠️ 채팅방을 찾을 수 없습니다")
                    self.status_label.config(text="상태: 채팅방 없음", foreground="orange")
                    messagebox.showwarning("알림", "채팅방을 찾을 수 없습니다.\n\n수동으로 URL을 추가하거나,\n브라우저에서 채팅 탭을 확인 후 다시 시도하세요.")
                    return
                
                # 기존 목록에 추가
                added_count = 0
                for chat in chat_list:
                    url = chat['url']
                    name = chat['name']
                    
                    # 중복 확인
                    if url not in self.poster.config.get('chat_urls', []):
                        self.poster.config.setdefault('chat_urls', [])
                        self.poster.config['chat_urls'].append(url)
                        
                        # 리스트박스에 추가
                        display_text = f"{name} - {url[:40]}..." if len(url) > 40 else f"{name} - {url}"
                        self.chat_listbox.insert(tk.END, display_text)
                        
                        added_count += 1
                        self.log(f"✅ 추가: {name}")
                
                self.log(f"✅ 총 {added_count}개의 채팅방이 추가되었습니다")
                self.status_label.config(text=f"상태: {added_count}개 채팅방 추가됨", foreground="green")
                messagebox.showinfo("완료", f"{added_count}개의 채팅방이 추가되었습니다!")
                
            except Exception as e:
                self.log(f"❌ 오류: {str(e)}")
                self.status_label.config(text="상태: 오류 발생", foreground="red")
                messagebox.showerror("오류", f"채팅방 목록을 불러오는 중 오류가 발생했습니다:\n\n{str(e)}")
        
        threading.Thread(target=fetch_thread, daemon=True).start()
        
    def load_config(self):
        """설정 로드"""
        config = self.poster.config
        
        # 채팅방 URL 로드
        for url in config.get('chat_urls', []):
            display_url = url if len(url) <= 60 else url[:57] + "..."
            self.chat_listbox.insert(tk.END, display_url)
        
        schedule = config.get('schedule', {})
        self.interval_entry.delete(0, tk.END)
        self.interval_entry.insert(0, schedule.get('interval_minutes', 30))
        
        self.delay_entry.delete(0, tk.END)
        self.delay_entry.insert(0, schedule.get('random_delay_minutes', 5))
        
        self.start_time_entry.delete(0, tk.END)
        self.start_time_entry.insert(0, schedule.get('start_time', '09:00'))
        
        self.end_time_entry.delete(0, tk.END)
        self.end_time_entry.insert(0, schedule.get('end_time', '22:00'))
        
        settings = config.get('settings', {})
        self.chat_interval_entry.delete(0, tk.END)
        self.chat_interval_entry.insert(0, settings.get('wait_between_chats', 3))
        
        self.rotate_var.set(settings.get('rotate_posts', True))
        self.rotate_chat_var.set(settings.get('rotate_chats', True))
        
        # 포스트 목록 로드
        for post in config.get('posts', []):
            if post.get('enabled', True):
                content = post['content'][:50] + "..." if len(post['content']) > 50 else post['content']
                self.post_listbox.insert(tk.END, content)
        
    def save_config(self):
        """설정 저장"""
        self.poster.config['schedule']['interval_minutes'] = int(self.interval_entry.get())
        self.poster.config['schedule']['random_delay_minutes'] = int(self.delay_entry.get())
        self.poster.config['schedule']['start_time'] = self.start_time_entry.get()
        self.poster.config['schedule']['end_time'] = self.end_time_entry.get()
        
        self.poster.config['settings']['wait_between_chats'] = int(self.chat_interval_entry.get())
        self.poster.config['settings']['rotate_posts'] = self.rotate_var.get()
        self.poster.config['settings']['rotate_chats'] = self.rotate_chat_var.get()
        
        self.poster.save_config()
        self.log("설정이 저장되었습니다.")
        messagebox.showinfo("저장 완료", "설정이 저장되었습니다.")
        
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
        
        display_content = content[:50] + "..." if len(content) > 50 else content
        self.post_listbox.insert(tk.END, display_content)
        
        self.post_text.delete("1.0", tk.END)
        self.log(f"포스트 추가: {display_content}")
        
    def remove_post(self):
        """포스트 삭제"""
        selection = self.post_listbox.curselection()
        if not selection:
            messagebox.showwarning("경고", "삭제할 포스트를 선택하세요.")
            return
        
        index = selection[0]
        self.poster.config['posts'].pop(index)
        self.post_listbox.delete(index)
        self.log(f"포스트 삭제: 인덱스 {index}")
        
    def start_posting(self):
        """자동 포스팅 시작"""
        if self.is_running:
            messagebox.showinfo("알림", "이미 실행 중입니다.")
            return
        
        if not self.poster.config.get('chat_urls'):
            messagebox.showwarning("경고", "채팅방 URL을 먼저 추가하세요.")
            return
        
        if not self.poster.config['posts']:
            messagebox.showwarning("경고", "포스트를 먼저 추가하세요.")
            return
        
        self.is_running = True
        self.status_label.config(text="상태: 실행 중", foreground="green")
        self.log("자동 포스팅 시작")
        
        # 스케줄 설정
        interval = self.poster.config['schedule']['interval_minutes']
        schedule.every(interval).minutes.do(self.poster.run_once)
        
        # 스케줄 실행 스레드
        self.schedule_thread = threading.Thread(target=self.run_schedule, daemon=True)
        self.schedule_thread.start()
        
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
        schedule.clear()
        self.status_label.config(text="상태: 중지됨", foreground="red")
        self.log("자동 포스팅 중지")
        
    def manual_post(self):
        """수동 포스팅"""
        if not self.poster.config.get('chat_urls'):
            messagebox.showwarning("경고", "채팅방 URL을 먼저 추가하세요.")
            return
        
        if not self.poster.config['posts']:
            messagebox.showwarning("경고", "포스트를 먼저 추가하세요.")
            return
        
        self.log("수동 포스팅 시작...")
        self.status_label.config(text="상태: 포스팅 중...", foreground="orange")
        
        def post_thread():
            try:
                success = self.poster.run_once()
                if success:
                    self.log("✅ 수동 포스팅 완료")
                    self.status_label.config(text="상태: 완료", foreground="green")
                else:
                    self.log("❌ 수동 포스팅 실패")
                    self.status_label.config(text="상태: 실패", foreground="red")
            except Exception as e:
                self.log(f"❌ 오류: {str(e)}")
                self.status_label.config(text="상태: 오류 발생", foreground="red")
                messagebox.showerror("오류", f"포스팅 중 오류가 발생했습니다:\n\n{str(e)}")
        
        threading.Thread(target=post_thread, daemon=True).start()


def main():
    root = tk.Tk()
    app = BandPosterGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
