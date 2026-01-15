"""
네이버밴드 자동 포스팅 프로그램 GUI
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
import os
import threading
from datetime import datetime
import sys

# band_poster 모듈 임포트를 위한 경로 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from band_poster import NaverBandPoster


class BandPosterGUI:
    """네이버밴드 자동 포스팅 GUI 클래스"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("네이버밴드 자동 포스팅 프로그램")
        self.root.geometry("800x700")
        
        self.poster = None
        self.is_running = False
        self.config_path = "config/config.json"
        
        self._create_widgets()
        self._load_config()
        
    def _create_widgets(self):
        """위젯 생성"""
        
        # 메인 프레임
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 로그인 정보
        login_frame = ttk.LabelFrame(main_frame, text="로그인 정보", padding="10")
        login_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(login_frame, text="네이버 ID:").grid(row=0, column=0, sticky=tk.W, padx=5)
        self.id_entry = ttk.Entry(login_frame, width=30)
        self.id_entry.grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(login_frame, text="비밀번호:").grid(row=1, column=0, sticky=tk.W, padx=5)
        self.pw_entry = ttk.Entry(login_frame, width=30, show="*")
        self.pw_entry.grid(row=1, column=1, padx=5, pady=2)
        
        ttk.Label(login_frame, text="밴드 URL:").grid(row=2, column=0, sticky=tk.W, padx=5)
        self.band_url_entry = ttk.Entry(login_frame, width=50)
        self.band_url_entry.grid(row=2, column=1, columnspan=2, padx=5, pady=2, sticky=(tk.W, tk.E))
        
        # 스케줄 설정
        schedule_frame = ttk.LabelFrame(main_frame, text="스케줄 설정", padding="10")
        schedule_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(schedule_frame, text="포스팅 간격 (분):").grid(row=0, column=0, sticky=tk.W, padx=5)
        self.interval_entry = ttk.Entry(schedule_frame, width=10)
        self.interval_entry.grid(row=0, column=1, padx=5, pady=2, sticky=tk.W)
        self.interval_entry.insert(0, "30")
        
        ttk.Label(schedule_frame, text="랜덤 딜레이 (분):").grid(row=0, column=2, sticky=tk.W, padx=5)
        self.random_delay_entry = ttk.Entry(schedule_frame, width=10)
        self.random_delay_entry.grid(row=0, column=3, padx=5, pady=2, sticky=tk.W)
        self.random_delay_entry.insert(0, "5")
        
        ttk.Label(schedule_frame, text="시작 시간:").grid(row=1, column=0, sticky=tk.W, padx=5)
        self.start_time_entry = ttk.Entry(schedule_frame, width=10)
        self.start_time_entry.grid(row=1, column=1, padx=5, pady=2, sticky=tk.W)
        self.start_time_entry.insert(0, "09:00")
        
        ttk.Label(schedule_frame, text="종료 시간:").grid(row=1, column=2, sticky=tk.W, padx=5)
        self.end_time_entry = ttk.Entry(schedule_frame, width=10)
        self.end_time_entry.grid(row=1, column=3, padx=5, pady=2, sticky=tk.W)
        self.end_time_entry.insert(0, "22:00")
        
        # 설정
        settings_frame = ttk.LabelFrame(main_frame, text="기타 설정", padding="10")
        settings_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        self.headless_var = tk.BooleanVar()
        ttk.Checkbutton(settings_frame, text="백그라운드 실행 (Headless)", 
                       variable=self.headless_var).grid(row=0, column=0, sticky=tk.W, padx=5)
        
        self.rotate_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(settings_frame, text="순환 포스팅", 
                       variable=self.rotate_var).grid(row=0, column=1, sticky=tk.W, padx=5)
        
        # 포스팅 내용 관리
        posts_frame = ttk.LabelFrame(main_frame, text="포스팅 내용 관리", padding="10")
        posts_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        # 포스트 리스트
        list_frame = ttk.Frame(posts_frame)
        list_frame.grid(row=0, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.posts_listbox = tk.Listbox(list_frame, height=8, yscrollcommand=scrollbar.set)
        self.posts_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.posts_listbox.yview)
        
        # 포스트 입력
        ttk.Label(posts_frame, text="포스트 내용:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=(10, 0))
        self.post_text = scrolledtext.ScrolledText(posts_frame, height=5, width=60)
        self.post_text.grid(row=2, column=0, columnspan=3, padx=5, pady=5, sticky=(tk.W, tk.E))
        
        # 포스트 관리 버튼
        btn_frame = ttk.Frame(posts_frame)
        btn_frame.grid(row=3, column=0, columnspan=3, pady=5)
        
        ttk.Button(btn_frame, text="추가", command=self._add_post).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="수정", command=self._edit_post).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="삭제", command=self._delete_post).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="활성화/비활성화", command=self._toggle_post).pack(side=tk.LEFT, padx=2)
        
        # 제어 버튼
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=4, column=0, columnspan=2, pady=10)
        
        self.start_btn = ttk.Button(control_frame, text="시작", command=self._start, width=15)
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        self.stop_btn = ttk.Button(control_frame, text="중지", command=self._stop, width=15, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(control_frame, text="설정 저장", command=self._save_config, width=15).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="수동 실행", command=self._run_once, width=15).pack(side=tk.LEFT, padx=5)
        
        # 상태 표시
        status_frame = ttk.LabelFrame(main_frame, text="상태", padding="10")
        status_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        self.status_label = ttk.Label(status_frame, text="대기 중", foreground="blue")
        self.status_label.pack()
        
        # 그리드 가중치 설정
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(3, weight=1)
        posts_frame.columnconfigure(0, weight=1)
        posts_frame.rowconfigure(0, weight=1)
        
    def _load_config(self):
        """설정 로드"""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    
                # 로그인 정보
                self.id_entry.insert(0, config.get('naver_id', ''))
                self.pw_entry.insert(0, config.get('naver_password', ''))
                self.band_url_entry.insert(0, config.get('band_url', ''))
                
                # 스케줄
                schedule = config.get('schedule', {})
                self.interval_entry.delete(0, tk.END)
                self.interval_entry.insert(0, str(schedule.get('interval_minutes', 30)))
                
                self.random_delay_entry.delete(0, tk.END)
                self.random_delay_entry.insert(0, str(schedule.get('random_delay_minutes', 5)))
                
                self.start_time_entry.delete(0, tk.END)
                self.start_time_entry.insert(0, schedule.get('start_time', '09:00'))
                
                self.end_time_entry.delete(0, tk.END)
                self.end_time_entry.insert(0, schedule.get('end_time', '22:00'))
                
                # 설정
                settings = config.get('settings', {})
                self.headless_var.set(settings.get('headless', False))
                self.rotate_var.set(settings.get('rotate_posts', True))
                
                # 포스트
                self.posts = config.get('posts', [])
                self._refresh_posts_list()
                
        except Exception as e:
            messagebox.showerror("오류", f"설정 로드 실패: {str(e)}")
    
    def _save_config(self):
        """설정 저장"""
        try:
            config = {
                'naver_id': self.id_entry.get(),
                'naver_password': self.pw_entry.get(),
                'band_url': self.band_url_entry.get(),
                'posts': self.posts,
                'schedule': {
                    'interval_minutes': int(self.interval_entry.get()),
                    'random_delay_minutes': int(self.random_delay_entry.get()),
                    'start_time': self.start_time_entry.get(),
                    'end_time': self.end_time_entry.get()
                },
                'settings': {
                    'headless': self.headless_var.get(),
                    'auto_login': True,
                    'rotate_posts': self.rotate_var.get(),
                    'log_level': 'INFO'
                }
            }
            
            os.makedirs('config', exist_ok=True)
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
            
            messagebox.showinfo("성공", "설정이 저장되었습니다.")
            
        except Exception as e:
            messagebox.showerror("오류", f"설정 저장 실패: {str(e)}")
    
    def _refresh_posts_list(self):
        """포스트 리스트 새로고침"""
        self.posts_listbox.delete(0, tk.END)
        for i, post in enumerate(self.posts):
            status = "✓" if post.get('enabled', True) else "✗"
            content = post['content'][:50] + "..." if len(post['content']) > 50 else post['content']
            self.posts_listbox.insert(tk.END, f"{status} {i+1}. {content}")
    
    def _add_post(self):
        """포스트 추가"""
        content = self.post_text.get("1.0", tk.END).strip()
        if not content:
            messagebox.showwarning("경고", "포스트 내용을 입력하세요.")
            return
        
        self.posts.append({'content': content, 'enabled': True})
        self._refresh_posts_list()
        self.post_text.delete("1.0", tk.END)
        messagebox.showinfo("성공", "포스트가 추가되었습니다.")
    
    def _edit_post(self):
        """포스트 수정"""
        selection = self.posts_listbox.curselection()
        if not selection:
            messagebox.showwarning("경고", "수정할 포스트를 선택하세요.")
            return
        
        content = self.post_text.get("1.0", tk.END).strip()
        if not content:
            messagebox.showwarning("경고", "포스트 내용을 입력하세요.")
            return
        
        idx = selection[0]
        self.posts[idx]['content'] = content
        self._refresh_posts_list()
        self.post_text.delete("1.0", tk.END)
        messagebox.showinfo("성공", "포스트가 수정되었습니다.")
    
    def _delete_post(self):
        """포스트 삭제"""
        selection = self.posts_listbox.curselection()
        if not selection:
            messagebox.showwarning("경고", "삭제할 포스트를 선택하세요.")
            return
        
        if messagebox.askyesno("확인", "선택한 포스트를 삭제하시겠습니까?"):
            idx = selection[0]
            del self.posts[idx]
            self._refresh_posts_list()
            messagebox.showinfo("성공", "포스트가 삭제되었습니다.")
    
    def _toggle_post(self):
        """포스트 활성화/비활성화"""
        selection = self.posts_listbox.curselection()
        if not selection:
            messagebox.showwarning("경고", "포스트를 선택하세요.")
            return
        
        idx = selection[0]
        self.posts[idx]['enabled'] = not self.posts[idx].get('enabled', True)
        self._refresh_posts_list()
    
    def _start(self):
        """자동 포스팅 시작"""
        try:
            # 설정 저장
            self._save_config()
            
            # 상태 업데이트
            self.is_running = True
            self.start_btn.config(state=tk.DISABLED)
            self.stop_btn.config(state=tk.NORMAL)
            self.status_label.config(text="실행 중...", foreground="green")
            
            # 별도 스레드에서 실행
            thread = threading.Thread(target=self._run_poster, daemon=True)
            thread.start()
            
        except Exception as e:
            messagebox.showerror("오류", f"시작 실패: {str(e)}")
            self._stop()
    
    def _stop(self):
        """자동 포스팅 중지"""
        self.is_running = False
        if self.poster:
            self.poster.close()
            self.poster = None
        
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.status_label.config(text="중지됨", foreground="red")
    
    def _run_poster(self):
        """포스터 실행"""
        try:
            self.poster = NaverBandPoster(self.config_path)
            self.poster.start_scheduler()
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("오류", f"실행 중 오류: {str(e)}"))
            self.root.after(0, self._stop)
    
    def _run_once(self):
        """수동으로 한 번 실행"""
        try:
            self._save_config()
            
            self.status_label.config(text="수동 실행 중...", foreground="orange")
            
            def run():
                try:
                    poster = NaverBandPoster(self.config_path)
                    poster.run_once()
                    poster.close()
                    self.root.after(0, lambda: messagebox.showinfo("완료", "포스팅이 완료되었습니다."))
                except Exception as e:
                    self.root.after(0, lambda: messagebox.showerror("오류", f"수동 실행 실패: {str(e)}"))
                finally:
                    self.root.after(0, lambda: self.status_label.config(text="대기 중", foreground="blue"))
            
            thread = threading.Thread(target=run, daemon=True)
            thread.start()
            
        except Exception as e:
            messagebox.showerror("오류", f"수동 실행 실패: {str(e)}")


def main():
    """메인 함수"""
    root = tk.Tk()
    app = BandPosterGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
