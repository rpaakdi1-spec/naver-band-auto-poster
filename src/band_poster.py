"""
네이버밴드 자동 포스팅 프로그램
"""

import os
import json
import time
import random
import logging
import schedule
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager


class NaverBandPoster:
    """네이버밴드 자동 포스팅 클래스"""
    
    def __init__(self, config_path: str = "config/config.json"):
        """
        초기화
        
        Args:
            config_path: 설정 파일 경로
        """
        self.config_path = config_path
        self.config = self._load_config()
        self.driver = None
        self.current_post_index = 0
        self.is_logged_in = False
        
        # 로깅 설정
        self._setup_logging()
        
    def _setup_logging(self):
        """로깅 설정"""
        log_level = getattr(logging, self.config['settings'].get('log_level', 'INFO'))
        
        # 로그 디렉토리 생성
        os.makedirs('logs', exist_ok=True)
        
        # 로거 설정
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(f'logs/band_poster_{datetime.now().strftime("%Y%m%d")}.log', encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def _load_config(self) -> Dict:
        """설정 파일 로드"""
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"설정 파일을 찾을 수 없습니다: {self.config_path}")
        
        with open(self.config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _init_driver(self):
        """크롬 드라이버 초기화"""
        chrome_options = Options()
        
        if self.config['settings'].get('headless', False):
            chrome_options.add_argument('--headless')
        
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        
        # 자동화 감지 우회
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # ChromeDriverManager 캐시 문제 해결
        try:
            # 캐시 디렉토리를 명시적으로 지정하고 최신 버전 강제 다운로드
            driver_path = ChromeDriverManager(cache_valid_range=1).install()
            
            # 잘못된 파일 경로 수정 (THIRD_PARTY_NOTICES 문제 해결)
            if 'THIRD_PARTY_NOTICES' in driver_path:
                import os
                driver_dir = os.path.dirname(driver_path)
                # chromedriver.exe 찾기
                if os.path.exists(os.path.join(driver_dir, 'chromedriver.exe')):
                    driver_path = os.path.join(driver_dir, 'chromedriver.exe')
                elif os.path.exists(os.path.join(os.path.dirname(driver_dir), 'chromedriver.exe')):
                    driver_path = os.path.join(os.path.dirname(driver_dir), 'chromedriver.exe')
            
            service = Service(driver_path)
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
        except Exception as e:
            self.logger.error(f"ChromeDriverManager 오류: {str(e)}")
            self.logger.info("Selenium Manager로 자동 설치 시도 중...")
            # Selenium 4.6+ 의 자동 드라이버 관리 사용
            self.driver = webdriver.Chrome(options=chrome_options)
        
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        self.logger.info("크롬 드라이버 초기화 완료")
    
    def login(self) -> bool:
        """
        네이버 로그인
        
        Returns:
            로그인 성공 여부
        """
        try:
            self.logger.info("네이버 로그인 시작")
            
            # 네이버 로그인 페이지 이동
            self.driver.get("https://nid.naver.com/nidlogin.login")
            time.sleep(2)
            
            # 아이디 입력
            id_input = self.driver.find_element(By.ID, "id")
            id_input.click()
            id_input.send_keys(self.config['naver_id'])
            time.sleep(0.5)
            
            # 비밀번호 입력
            pw_input = self.driver.find_element(By.ID, "pw")
            pw_input.click()
            pw_input.send_keys(self.config['naver_password'])
            time.sleep(0.5)
            
            # 로그인 버튼 클릭
            login_btn = self.driver.find_element(By.ID, "log.login")
            login_btn.click()
            
            time.sleep(3)
            
            # 로그인 성공 확인
            if "nid.naver.com" not in self.driver.current_url:
                self.is_logged_in = True
                self.logger.info("로그인 성공")
                return True
            else:
                self.logger.error("로그인 실패")
                return False
                
        except Exception as e:
            self.logger.error(f"로그인 중 오류 발생: {str(e)}")
            return False
    
    def navigate_to_band(self) -> bool:
        """
        밴드 페이지로 이동
        
        Returns:
            이동 성공 여부
        """
        try:
            self.logger.info(f"밴드 페이지로 이동: {self.config['band_url']}")
            self.driver.get(self.config['band_url'])
            time.sleep(3)
            return True
        except Exception as e:
            self.logger.error(f"밴드 페이지 이동 중 오류: {str(e)}")
            return False
    
    def post_message(self, content: str) -> bool:
        """
        메시지 포스팅
        
        Args:
            content: 포스팅할 내용
            
        Returns:
            포스팅 성공 여부
        """
        try:
            self.logger.info(f"포스팅 시작: {content[:50]}...")
            
            # 밴드 페이지로 이동
            if not self.navigate_to_band():
                return False
            
            # 글쓰기 영역 찾기 (여러 선택자 시도)
            write_selectors = [
                "//textarea[@placeholder='게시글을 작성해보세요.']",
                "//textarea[contains(@class, 'writeForm')]",
                "//div[contains(@class, 'writeFormBtn')]",
                "//button[contains(text(), '글쓰기')]",
                "//a[contains(@class, 'writeBtn')]"
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
            
            # 본문 입력 영역 찾기
            content_selectors = [
                "//textarea[@placeholder='게시글을 작성해보세요.']",
                "//div[@contenteditable='true']",
                "//textarea[contains(@class, 'content')]"
            ]
            
            content_element = None
            for selector in content_selectors:
                try:
                    content_element = WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, selector))
                    )
                    if content_element:
                        break
                except TimeoutException:
                    continue
            
            if not content_element:
                self.logger.error("본문 입력 영역을 찾을 수 없습니다")
                return False
            
            # 내용 입력
            content_element.click()
            time.sleep(0.5)
            content_element.send_keys(content)
            time.sleep(1)
            
            # 등록 버튼 찾기 및 클릭
            submit_selectors = [
                "//button[contains(text(), '등록')]",
                "//button[contains(@class, 'submit')]",
                "//a[contains(text(), '등록')]"
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
            self.logger.error(f"포스팅 중 오류 발생: {str(e)}")
            return False
    
    def get_next_post(self) -> Optional[str]:
        """
        다음 포스팅할 글 가져오기
        
        Returns:
            포스팅할 내용
        """
        enabled_posts = [post for post in self.config['posts'] if post.get('enabled', True)]
        
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
        """
        현재 시간이 스케줄 범위 내인지 확인
        
        Returns:
            스케줄 범위 내 여부
        """
        now = datetime.now().time()
        start_time = datetime.strptime(self.config['schedule']['start_time'], "%H:%M").time()
        end_time = datetime.strptime(self.config['schedule']['end_time'], "%H:%M").time()
        
        return start_time <= now <= end_time
    
    def run_once(self):
        """한 번 실행"""
        if not self.is_within_schedule():
            self.logger.info("스케줄 시간이 아닙니다")
            return
        
        try:
            # 드라이버 초기화
            if not self.driver:
                self._init_driver()
            
            # 로그인
            if not self.is_logged_in:
                if not self.login():
                    self.logger.error("로그인 실패")
                    return
            
            # 다음 포스트 가져오기
            content = self.get_next_post()
            if not content:
                self.logger.warning("포스팅할 내용이 없습니다")
                return
            
            # 포스팅
            success = self.post_message(content)
            
            if success:
                self.logger.info(f"포스팅 성공: {content[:50]}...")
                
                # 랜덤 딜레이
                random_delay = random.randint(0, self.config['schedule'].get('random_delay_minutes', 5) * 60)
                self.logger.info(f"다음 포스팅까지 {random_delay}초 대기")
                time.sleep(random_delay)
            else:
                self.logger.error("포스팅 실패")
                
        except Exception as e:
            self.logger.error(f"실행 중 오류: {str(e)}")
    
    def start_scheduler(self):
        """스케줄러 시작"""
        interval = self.config['schedule'].get('interval_minutes', 30)
        
        self.logger.info(f"스케줄러 시작 - {interval}분 간격")
        
        # 스케줄 등록
        schedule.every(interval).minutes.do(self.run_once)
        
        # 첫 실행
        self.run_once()
        
        # 스케줄 실행
        while True:
            schedule.run_pending()
            time.sleep(1)
    
    def close(self):
        """리소스 정리"""
        if self.driver:
            self.driver.quit()
            self.logger.info("드라이버 종료")


if __name__ == "__main__":
    try:
        poster = NaverBandPoster("config/config.json")
        poster.start_scheduler()
    except KeyboardInterrupt:
        print("\n프로그램을 종료합니다...")
        poster.close()
    except Exception as e:
        print(f"오류 발생: {str(e)}")
