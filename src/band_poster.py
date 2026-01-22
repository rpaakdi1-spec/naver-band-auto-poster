"""
네이버밴드 자동 포스팅 엔진 (다중 채팅방 지원)
"""

import os
import glob
import json
import time
import random
import logging
from datetime import datetime
from typing import List, Dict, Optional

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager


class BandPoster:
    """네이버밴드 자동 포스팅 클래스 (다중 채팅방)"""
    
    def __init__(self, config_path: str = "config/config.json"):
        self.config_path = config_path
        self.config = self._load_config()
        self.driver = None
        self.current_post_index = 0
        self.current_chat_index = 0
        self.is_logged_in = False
        self._setup_logging()
        
    def _setup_logging(self):
        """로깅 설정"""
        os.makedirs('logs', exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(
                    f'logs/band_poster_{datetime.now().strftime("%Y%m%d")}.log',
                    encoding='utf-8'
                ),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def _load_config(self) -> Dict:
        """설정 파일 로드"""
        if not os.path.exists(self.config_path):
            return self._get_default_config()
        
        with open(self.config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _get_default_config(self) -> Dict:
        """기본 설정 반환"""
        return {
            "chat_urls": [],
            "posts": [],
            "schedule": {
                "interval_minutes": 30,
                "random_delay_minutes": 5,
                "start_time": "09:00",
                "end_time": "22:00"
            },
            "settings": {
                "rotate_posts": True,
                "rotate_chats": True,
                "log_level": "INFO",
                "wait_after_post": 2,
                "wait_between_chats": 3
            }
        }
    
    def save_config(self):
        """설정 저장"""
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, ensure_ascii=False, indent=2)
        self.logger.info("설정 파일 저장 완료")
    
    def init_driver(self):
        """Chrome 드라이버 초기화"""
        try:
            chrome_options = Options()
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
            chrome_options.add_argument('--log-level=3')
            chrome_options.add_argument('--disable-logging')
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            # ChromeDriverManager로 드라이버 경로 가져오기
            driver_path = ChromeDriverManager().install()
            
            # 올바른 chromedriver.exe 경로 찾기
            if not driver_path.endswith('.exe'):
                driver_dir = os.path.dirname(driver_path)
                exe_files = glob.glob(os.path.join(driver_dir, '**', 'chromedriver.exe'), recursive=True)
                
                if exe_files:
                    driver_path = exe_files[0]
                    self.logger.info(f"ChromeDriver 경로: {driver_path}")
                else:
                    parent_dir = os.path.dirname(driver_dir)
                    exe_files = glob.glob(os.path.join(parent_dir, '**', 'chromedriver.exe'), recursive=True)
                    if exe_files:
                        driver_path = exe_files[0]
                        self.logger.info(f"ChromeDriver 경로: {driver_path}")
                    else:
                        raise FileNotFoundError("chromedriver.exe를 찾을 수 없습니다")
            
            service = Service(driver_path)
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            self.logger.info("Chrome 드라이버 초기화 완료")
            
        except Exception as e:
            self.logger.error(f"Chrome 드라이버 초기화 실패: {str(e)}")
            raise
    
    def start_chrome_and_wait_for_login(self) -> bool:
        """Chrome 실행하고 수동 로그인 대기"""
        try:
            self.logger.info("Chrome 브라우저 실행 중...")
            
            # 밴드 메인 페이지로 이동
            self.driver.get("https://band.us")
            
            self.logger.info("=" * 60)
            self.logger.info("🌐 Chrome 브라우저가 실행되었습니다")
            self.logger.info("📝 수동 로그인을 진행해주세요:")
            self.logger.info("   1. 열린 Chrome 브라우저에서 밴드에 로그인")
            self.logger.info("   2. 로그인 완료 후 프로그램으로 돌아와서")
            self.logger.info("   3. Enter 키를 눌러주세요")
            self.logger.info("=" * 60)
            
            # 사용자 입력 대기
            input("\n✅ 로그인 완료 후 Enter를 눌러주세요...")
            
            # 로그인 확인
            current_url = self.driver.current_url
            if "band.us" in current_url:
                self.is_logged_in = True
                self.logger.info("✅ 로그인 확인 완료")
                return True
            else:
                self.logger.warning("⚠️ 밴드 페이지가 아닙니다. 계속 진행합니다...")
                return True
                
        except Exception as e:
            self.logger.error(f"Chrome 실행 중 오류: {str(e)}")
            return False
    
    def post_to_chat(self, chat_url: str, content: str) -> bool:
        """특정 채팅방에 메시지 포스팅"""
        try:
            self.logger.info(f"📨 채팅방 이동: {chat_url}")
            
            # 채팅방 URL로 이동
            self.driver.get(chat_url)
            time.sleep(self.config['settings'].get('wait_between_chats', 3))
            
            # 채팅 입력창 찾기 (여러 선택자 시도)
            input_selectors = [
                "//textarea[@placeholder='메시지를 입력하세요']",
                "//textarea[contains(@class, 'chatInput')]",
                "//div[@contenteditable='true']",
                "//textarea[contains(@placeholder, '메시지')]",
                "//input[@type='text' and contains(@placeholder, '메시지')]"
            ]
            
            input_element = None
            for selector in input_selectors:
                try:
                    input_element = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, selector))
                    )
                    if input_element:
                        self.logger.info(f"✅ 입력창 찾음: {selector}")
                        break
                except TimeoutException:
                    continue
            
            if not input_element:
                self.logger.error("❌ 채팅 입력창을 찾을 수 없습니다")
                return False
            
            # 입력창 클릭
            input_element.click()
            time.sleep(0.5)
            
            # 메시지 입력
            input_element.send_keys(content)
            time.sleep(1)
            
            # Enter 키로 전송 또는 전송 버튼 클릭
            send_button_selectors = [
                "//button[contains(text(), '전송')]",
                "//button[contains(@class, 'sendBtn')]",
                "//button[@type='submit']"
            ]
            
            send_button = None
            for selector in send_button_selectors:
                try:
                    send_button = self.driver.find_element(By.XPATH, selector)
                    if send_button and send_button.is_displayed():
                        self.logger.info(f"✅ 전송 버튼 찾음: {selector}")
                        break
                except NoSuchElementException:
                    continue
            
            if send_button:
                # 전송 버튼 클릭
                send_button.click()
            else:
                # Enter 키로 전송
                input_element.send_keys(Keys.RETURN)
            
            time.sleep(self.config['settings'].get('wait_after_post', 2))
            
            self.logger.info(f"✅ 채팅방 포스팅 완료: {chat_url}")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ 채팅방 포스팅 오류: {str(e)}")
            return False
    
    def get_next_post(self) -> Optional[str]:
        """다음 포스팅할 글 가져오기"""
        enabled_posts = [p for p in self.config['posts'] if p.get('enabled', True)]
        
        if not enabled_posts:
            self.logger.warning("활성화된 포스트가 없습니다")
            return None
        
        if self.config['settings'].get('rotate_posts', True):
            # 순환 방식
            post = enabled_posts[self.current_post_index % len(enabled_posts)]
            self.current_post_index += 1
        else:
            # 랜덤 방식
            post = random.choice(enabled_posts)
        
        return post['content']
    
    def get_next_chat_url(self) -> Optional[str]:
        """다음 채팅방 URL 가져오기"""
        chat_urls = self.config.get('chat_urls', [])
        
        if not chat_urls:
            self.logger.warning("채팅방 URL이 없습니다")
            return None
        
        if self.config['settings'].get('rotate_chats', True):
            # 순환 방식
            url = chat_urls[self.current_chat_index % len(chat_urls)]
            self.current_chat_index += 1
        else:
            # 랜덤 방식
            url = random.choice(chat_urls)
        
        return url
    
    def post_to_all_chats(self, content: str) -> Dict[str, bool]:
        """모든 채팅방에 메시지 포스팅"""
        results = {}
        chat_urls = self.config.get('chat_urls', [])
        
        self.logger.info(f"📢 {len(chat_urls)}개 채팅방에 포스팅 시작")
        
        for i, chat_url in enumerate(chat_urls, 1):
            self.logger.info(f"\n[{i}/{len(chat_urls)}] 채팅방 포스팅 중...")
            success = self.post_to_chat(chat_url, content)
            results[chat_url] = success
            
            # 마지막 채팅방이 아니면 대기
            if i < len(chat_urls):
                wait_time = self.config['settings'].get('wait_between_chats', 3)
                self.logger.info(f"⏱️ {wait_time}초 대기 중...")
                time.sleep(wait_time)
        
        # 결과 요약
        success_count = sum(1 for v in results.values() if v)
        self.logger.info(f"\n✅ 포스팅 완료: {success_count}/{len(chat_urls)} 성공")
        
        return results
    
    def is_within_schedule(self) -> bool:
        """현재 시간이 스케줄 범위 내인지 확인"""
        now = datetime.now().time()
        start_time = datetime.strptime(self.config['schedule']['start_time'], "%H:%M").time()
        end_time = datetime.strptime(self.config['schedule']['end_time'], "%H:%M").time()
        
        return start_time <= now <= end_time
    
    def run_once(self) -> bool:
        """한 번 실행"""
        if not self.is_within_schedule():
            self.logger.info("스케줄 시간이 아닙니다")
            return False
        
        try:
            # 드라이버 초기화
            if not self.driver:
                self.init_driver()
            
            # 로그인
            if not self.is_logged_in:
                if not self.start_chrome_and_wait_for_login():
                    self.logger.error("로그인 실패")
                    return False
            
            # 다음 포스트 가져오기
            content = self.get_next_post()
            if not content:
                self.logger.warning("포스팅할 내용이 없습니다")
                return False
            
            # 모든 채팅방에 포스팅
            results = self.post_to_all_chats(content)
            
            # 성공 여부 확인
            success = any(results.values())
            
            if success:
                # 랜덤 딜레이
                random_delay = random.randint(
                    0, 
                    self.config['schedule'].get('random_delay_minutes', 5) * 60
                )
                self.logger.info(f"⏱️ 다음 포스팅까지 {random_delay}초 대기")
                time.sleep(random_delay)
            
            return success
                
        except Exception as e:
            self.logger.error(f"실행 중 오류: {str(e)}")
            return False
    
    def close(self):
        """리소스 정리"""
        if self.driver:
            self.driver.quit()
            self.logger.info("드라이버 종료")


if __name__ == "__main__":
    poster = BandPoster()
    
    try:
        poster.run_once()
    except KeyboardInterrupt:
        print("\n프로그램 종료")
    finally:
        poster.close()
