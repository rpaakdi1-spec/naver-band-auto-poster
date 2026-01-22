"""
네이버밴드 자동 포스팅 엔진
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
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager


class BandPoster:
    """네이버밴드 자동 포스팅 클래스"""
    
    def __init__(self, config_path: str = "config/config.json"):
        self.config_path = config_path
        self.config = self._load_config()
        self.driver = None
        self.current_post_index = 0
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
            "band_url": "",
            "posts": [],
            "schedule": {
                "interval_minutes": 30,
                "random_delay_minutes": 5,
                "start_time": "09:00",
                "end_time": "22:00"
            },
            "settings": {
                "rotate_posts": True,
                "log_level": "INFO"
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
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            # ChromeDriverManager로 드라이버 경로 가져오기
            driver_path = ChromeDriverManager().install()
            
            # 올바른 chromedriver.exe 경로 찾기
            if not driver_path.endswith('.exe'):
                # 디렉토리에서 chromedriver.exe 찾기
                import glob
                driver_dir = os.path.dirname(driver_path)
                exe_files = glob.glob(os.path.join(driver_dir, '**', 'chromedriver.exe'), recursive=True)
                
                if exe_files:
                    driver_path = exe_files[0]
                    self.logger.info(f"ChromeDriver 경로: {driver_path}")
                else:
                    # 상위 디렉토리에서 찾기
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
            
            # 밴드 URL이 있으면 밴드 페이지로, 없으면 밴드 메인으로
            if self.config.get('band_url'):
                self.driver.get(self.config['band_url'])
            else:
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
    
    def navigate_to_band(self) -> bool:
        """밴드 페이지로 이동"""
        try:
            self.logger.info(f"밴드 페이지 이동: {self.config['band_url']}")
            self.driver.get(self.config['band_url'])
            time.sleep(3)
            return True
        except Exception as e:
            self.logger.error(f"밴드 페이지 이동 실패: {str(e)}")
            return False
    
    def post_message(self, content: str) -> bool:
        """메시지 포스팅"""
        try:
            self.logger.info(f"포스팅 시작: {content[:50]}...")
            
            if not self.navigate_to_band():
                return False
            
            # 글쓰기 영역 찾기
            write_selectors = [
                "//textarea[@placeholder='게시글을 작성해보세요.']",
                "//textarea[contains(@class, 'writeForm')]",
                "//div[contains(@class, 'writeFormBtn')]"
            ]
            
            write_element = None
            for selector in write_selectors:
                try:
                    write_element = WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, selector))
                    )
                    if write_element:
                        break
                except TimeoutException:
                    continue
            
            if not write_element:
                self.logger.error("글쓰기 영역을 찾을 수 없습니다")
                return False
            
            # 글쓰기 영역 클릭
            write_element.click()
            time.sleep(1)
            
            # 본문 입력
            write_element.send_keys(content)
            time.sleep(1)
            
            # 등록 버튼 찾기 및 클릭
            submit_selectors = [
                "//button[contains(text(), '등록')]",
                "//button[contains(@class, 'submit')]"
            ]
            
            submit_element = None
            for selector in submit_selectors:
                try:
                    submit_element = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    if submit_element:
                        break
                except TimeoutException:
                    continue
            
            if not submit_element:
                self.logger.error("등록 버튼을 찾을 수 없습니다")
                return False
            
            submit_element.click()
            time.sleep(2)
            
            self.logger.info("포스팅 완료")
            return True
            
        except Exception as e:
            self.logger.error(f"포스팅 중 오류: {str(e)}")
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
            
            # 포스팅
            success = self.post_message(content)
            
            if success:
                # 랜덤 딜레이
                random_delay = random.randint(
                    0, 
                    self.config['schedule'].get('random_delay_minutes', 5) * 60
                )
                self.logger.info(f"다음 포스팅까지 {random_delay}초 대기")
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
