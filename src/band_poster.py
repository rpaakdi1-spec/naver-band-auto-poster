"""
네이버밴드 자동 포스팅 엔진 (다중 채팅방 지원)
"""

import os
import glob
import json
import time
import random
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
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
        # 현재 시간부터 24시간 후까지 기본 설정
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
            "settings": {
                "rotate_posts": True,
                "rotate_chats": True,
                "log_level": "INFO",
                "wait_after_post": 2,
                "wait_between_chats": 3,
                "fast_mode": False,
                "input_wait_timeout": 3
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
    
    def fetch_chat_list(self) -> List[Dict[str, str]]:
        """밴드 채팅방 목록 가져오기"""
        try:
            self.logger.info("📋 채팅방 목록 가져오는 중...")
            
            # 1. 밴드 홈 페이지로 이동
            self.logger.info("🌐 밴드 홈으로 이동: https://band.us/home")
            self.driver.get("https://band.us/home")
            time.sleep(3)
            
            # 2. 페이지 스크롤 (채팅방이 아래에 있을 수 있음)
            self.logger.info("📜 페이지 스크롤 중...")
            for i in range(3):
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(1)
            
            # 3. 맨 위로 다시 스크롤
            self.driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(1)
            
            chat_list = []
            
            # 4. CSS 선택자로 먼저 시도 (더 빠름)
            css_selectors = [
                "a[href*='/chat/']",
                "a[href*='/band/'][href*='/chat/']",
                ".chatList a",
                ".chatItem a",
                "[class*='chat'] a[href*='/chat/']"
            ]
            
            chat_elements = []
            for selector in css_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        self.logger.info(f"✅ 채팅방 링크 찾음 (CSS): {len(elements)}개 - {selector}")
                        chat_elements.extend(elements)
                        break
                except Exception as e:
                    continue
            
            # 5. CSS로 못 찾으면 XPath 시도
            if not chat_elements:
                self.logger.info("🔍 XPath로 재시도...")
                xpath_selectors = [
                    "//a[contains(@href, '/chat/')]",
                    "//a[contains(@class, 'chat') and contains(@href, '/band/')]",
                    "//div[contains(@class, 'chatList')]//a",
                    "//ul[contains(@class, 'chat')]//a[contains(@href, '/chat/')]",
                    "//div[contains(@class, 'chat')]//a[contains(@href, '/band/')]"
                ]
                
                for selector in xpath_selectors:
                    try:
                        elements = self.driver.find_elements(By.XPATH, selector)
                        if elements:
                            self.logger.info(f"✅ 채팅방 링크 찾음 (XPath): {len(elements)}개")
                            chat_elements.extend(elements)
                            break
                    except Exception as e:
                        continue
            
            # 6. JavaScript로 직접 찾기 (최후의 수단)
            if not chat_elements:
                self.logger.info("🔍 JavaScript로 재시도...")
                try:
                    js_code = """
                    var links = document.querySelectorAll('a');
                    var chatLinks = [];
                    for(var i = 0; i < links.length; i++) {
                        var href = links[i].href;
                        if(href && href.includes('/chat/') && href.includes('/band/')) {
                            chatLinks.push(links[i]);
                        }
                    }
                    return chatLinks;
                    """
                    elements = self.driver.execute_script(js_code)
                    if elements:
                        self.logger.info(f"✅ 채팅방 링크 찾음 (JavaScript): {len(elements)}개")
                        chat_elements = elements
                except Exception as e:
                    self.logger.error(f"JavaScript 실행 실패: {str(e)}")
            
            # 7. 중복 제거를 위한 set
            seen_urls = set()
            
            for element in chat_elements:
                try:
                    chat_url = element.get_attribute('href')
                    
                    # 유효한 채팅방 URL인지 확인
                    if chat_url and '/band/' in chat_url and '/chat/' in chat_url:
                        if chat_url not in seen_urls:
                            seen_urls.add(chat_url)
                            
                            # 채팅방 이름 가져오기
                            try:
                                chat_name = element.text.strip()
                                if not chat_name:
                                    chat_name = element.get_attribute('title') or element.get_attribute('aria-label') or "채팅방"
                            except:
                                chat_name = "채팅방"
                            
                            chat_list.append({
                                'url': chat_url,
                                'name': chat_name
                            })
                            
                            self.logger.info(f"  📁 {chat_name}: {chat_url}")
                            
                except Exception as e:
                    continue
            
            if not chat_list:
                # 8. 디버그 정보 출력
                self.logger.warning("⚠️ 채팅방을 찾을 수 없습니다.")
                self.logger.info("🔍 디버그 정보:")
                self.logger.info(f"   현재 URL: {self.driver.current_url}")
                
                # 페이지 소스에서 채팅 관련 텍스트 찾기
                try:
                    page_source = self.driver.page_source
                    if '/chat/' in page_source:
                        self.logger.info("   ✅ 페이지에 '/chat/' 텍스트 존재")
                    else:
                        self.logger.info("   ❌ 페이지에 '/chat/' 텍스트 없음")
                    
                    if '채팅' in page_source:
                        self.logger.info("   ✅ 페이지에 '채팅' 텍스트 존재")
                    else:
                        self.logger.info("   ❌ 페이지에 '채팅' 텍스트 없음")
                except:
                    pass
                
                self.logger.warning("💡 수동으로 URL을 추가하거나, 브라우저에서 채팅 탭을 확인 후 다시 시도하세요.")
            else:
                self.logger.info(f"✅ 총 {len(chat_list)}개의 채팅방을 찾았습니다")
            
            return chat_list
            
        except Exception as e:
            self.logger.error(f"❌ 채팅방 목록 가져오기 실패: {str(e)}")
            import traceback
            self.logger.error(traceback.format_exc())
            return []
    
    def fetch_chat_list_from_band(self, band_no: str) -> List[Dict[str, str]]:
        """특정 밴드의 채팅방 목록 가져오기"""
        try:
            self.logger.info(f"📋 밴드 {band_no}의 채팅방 목록 가져오는 중...")
            
            # 밴드 페이지로 이동
            band_url = f"https://band.us/band/{band_no}"
            self.driver.get(band_url)
            time.sleep(3)
            
            # 페이지 스크롤
            for i in range(2):
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(1)
            
            # 채팅 탭 클릭 시도
            chat_tab_selectors = [
                "a[href*='/chat']",
                "button:contains('채팅')",
                "//a[contains(text(), '채팅')]",
                "//button[contains(text(), '채팅')]",
                "//a[contains(@href, '/chat')]",
                "//div[contains(@class, 'menuItem')]//a[contains(text(), '채팅')]",
                "//li[contains(@class, 'menu')]//a[contains(text(), '채팅')]"
            ]
            
            for selector in chat_tab_selectors:
                try:
                    if selector.startswith('//'):
                        chat_tab = self.driver.find_element(By.XPATH, selector)
                    else:
                        chat_tab = self.driver.find_element(By.CSS_SELECTOR, selector)
                    
                    if chat_tab and chat_tab.is_displayed():
                        self.logger.info(f"🖱️ 채팅 탭 클릭: {selector}")
                        chat_tab.click()
                        time.sleep(2)
                        break
                except:
                    continue
            
            # 채팅방 목록 가져오기
            chat_list = []
            
            # CSS 선택자로 시도
            css_selectors = [
                f"a[href*='/band/{band_no}/chat/']",
                "a[href*='/chat/']",
                ".chatItem a",
                ".chatList a"
            ]
            
            chat_elements = []
            for selector in css_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        self.logger.info(f"✅ 채팅방 링크 찾음 (CSS): {len(elements)}개")
                        chat_elements = elements
                        break
                except:
                    continue
            
            # XPath로 시도
            if not chat_elements:
                xpath_selectors = [
                    f"//a[contains(@href, '/band/{band_no}/chat/')]",
                    "//a[contains(@href, '/chat/')]",
                    "//div[contains(@class, 'chatItem')]//a",
                    "//ul[contains(@class, 'chatList')]//a"
                ]
                
                for selector in xpath_selectors:
                    try:
                        elements = self.driver.find_elements(By.XPATH, selector)
                        if elements:
                            self.logger.info(f"✅ 채팅방 링크 찾음 (XPath): {len(elements)}개")
                            chat_elements = elements
                            break
                    except:
                        continue
            
            seen_urls = set()
            
            for element in chat_elements:
                try:
                    chat_url = element.get_attribute('href')
                    
                    if chat_url and f'/band/{band_no}/chat/' in chat_url:
                        if chat_url not in seen_urls:
                            seen_urls.add(chat_url)
                            
                            # 채팅방 이름
                            try:
                                chat_name = element.text.strip() or element.get_attribute('title') or element.get_attribute('aria-label') or "채팅방"
                            except:
                                chat_name = "채팅방"
                            
                            chat_list.append({
                                'url': chat_url,
                                'name': chat_name
                            })
                            
                            self.logger.info(f"  📁 {chat_name}: {chat_url}")
                except:
                    continue
            
            if not chat_list:
                self.logger.warning(f"⚠️ 밴드 {band_no}에서 채팅방을 찾을 수 없습니다")
                self.logger.info("💡 채팅 탭이 있는지, 채팅방이 생성되어 있는지 확인하세요.")
            else:
                self.logger.info(f"✅ 총 {len(chat_list)}개의 채팅방을 찾았습니다")
            
            return chat_list
            
        except Exception as e:
            self.logger.error(f"❌ 채팅방 목록 가져오기 실패: {str(e)}")
            import traceback
            self.logger.error(traceback.format_exc())
            return []
    
    def fetch_all_bands_and_chats(self) -> List[Dict[str, str]]:
        """모든 밴드를 찾아서 각 밴드의 채팅방 가져오기"""
        try:
            self.logger.info("🔍 모든 밴드와 채팅방 검색 중...")
            
            # 밴드 목록 페이지로 이동
            self.driver.get("https://band.us/home/bands")
            time.sleep(3)
            
            # 페이지 스크롤
            for i in range(3):
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(1)
            
            all_chats = []
            
            # 밴드 링크 찾기
            band_links = []
            band_selectors = [
                "a[href*='/band/']",
                "//a[contains(@href, '/band/')]"
            ]
            
            for selector in band_selectors:
                try:
                    if selector.startswith('//'):
                        elements = self.driver.find_elements(By.XPATH, selector)
                    else:
                        elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    
                    if elements:
                        self.logger.info(f"✅ 밴드 링크 찾음: {len(elements)}개")
                        band_links = elements
                        break
                except:
                    continue
            
            # 밴드 번호 추출
            band_numbers = set()
            for link in band_links:
                try:
                    href = link.get_attribute('href')
                    if href and '/band/' in href:
                        # URL에서 밴드 번호 추출
                        import re
                        match = re.search(r'/band/(\d+)', href)
                        if match:
                            band_no = match.group(1)
                            band_numbers.add(band_no)
                except:
                    continue
            
            self.logger.info(f"📊 발견된 밴드: {len(band_numbers)}개")
            
            # 각 밴드의 채팅방 가져오기
            for i, band_no in enumerate(band_numbers, 1):
                self.logger.info(f"\n[{i}/{len(band_numbers)}] 밴드 {band_no} 검색 중...")
                chats = self.fetch_chat_list_from_band(band_no)
                all_chats.extend(chats)
                time.sleep(1)  # 과부하 방지
            
            self.logger.info(f"\n✅ 총 {len(all_chats)}개의 채팅방을 찾았습니다")
            return all_chats
            
        except Exception as e:
            self.logger.error(f"❌ 밴드 및 채팅방 검색 실패: {str(e)}")
            import traceback
            self.logger.error(traceback.format_exc())
            return []
    
    def post_to_chat(self, chat_url: str, content: str) -> bool:
        """특정 채팅방에 메시지 포스팅"""
        try:
            self.logger.info(f"📨 채팅방 이동: {chat_url}")
            
            # 채팅방 URL로 이동
            self.driver.get(chat_url)
            
            # 빠른 모드 설정
            fast_mode = self.config['settings'].get('fast_mode', False)
            
            # 페이지 로드 대기
            if fast_mode:
                time.sleep(0.5)  # 빠른 모드: 0.5초
            else:
                wait_time = self.config['settings'].get('wait_between_chats', 3)
                time.sleep(max(1, wait_time - 1))  # 일반 모드: 최소 1초
            
            # 빠른 입력창 찾기 - CSS 선택자 우선 (XPath보다 빠름)
            input_element = None
            timeout = self.config['settings'].get('input_wait_timeout', 3)
            
            # 1단계: CSS 선택자로 빠르게 찾기 (가장 일반적인 패턴)
            css_selectors = [
                "textarea[placeholder*='메시지']",
                "textarea.chatInput",
                "textarea[name='message']",
                "div[contenteditable='true']",
                "input[placeholder*='메시지']"
            ]
            
            for selector in css_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for element in elements:
                        if element.is_displayed() and element.is_enabled():
                            input_element = element
                            self.logger.info(f"✅ 입력창 찾음 (CSS): {selector}")
                            break
                    if input_element:
                        break
                except:
                    continue
            
            # 2단계: CSS로 못 찾으면 XPath로 시도 (더 구체적)
            if not input_element:
                xpath_selectors = [
                    "//textarea[@placeholder='메시지를 입력하세요']",
                    "//textarea[contains(@class, 'chatInput')]",
                    "//textarea[contains(@placeholder, '메시지')]",
                    "//div[@contenteditable='true' and contains(@class, 'input')]"
                ]
                
                for selector in xpath_selectors:
                    try:
                        elements = self.driver.find_elements(By.XPATH, selector)
                        for element in elements:
                            if element.is_displayed() and element.is_enabled():
                                input_element = element
                                self.logger.info(f"✅ 입력창 찾음 (XPath): {selector}")
                                break
                        if input_element:
                            break
                    except:
                        continue
            
            # 3단계: 마지막으로 명시적 대기로 시도 (최소 대기 시간)
            if not input_element:
                try:
                    input_element = WebDriverWait(self.driver, timeout).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "textarea, input[type='text'], div[contenteditable='true']"))
                    )
                    self.logger.info("✅ 입력창 찾음 (대기)")
                except TimeoutException:
                    self.logger.error("❌ 채팅 입력창을 찾을 수 없습니다")
                    return False
            
            if not input_element:
                self.logger.error("❌ 채팅 입력창을 찾을 수 없습니다")
                return False
            
            # 입력창 클릭
            input_element.click()
            time.sleep(0.5)
            
            # 메시지 입력
            input_element.send_keys(content)
            time.sleep(0.5)
            
            # Enter 키로 전송
            self.logger.info("⌨️ Enter 키로 메시지 전송")
            input_element.send_keys(Keys.RETURN)
            
            time.sleep(self.config['settings'].get('wait_after_post', 2))
            
            # 채팅방은 닫지 않고 그대로 유지 (세션 안정성 확보)
            # 다음 채팅방으로 이동 시 자동으로 새 페이지 로드됨
            
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
        """다음 채팅방 URL 가져오기 (활성화된 채팅방만)"""
        # chat_rooms에서 enabled=True인 채팅방만 필터링
        chat_rooms = self.config.get('chat_rooms', [])
        enabled_rooms = [room for room in chat_rooms if room.get('enabled', True)]
        
        if not enabled_rooms:
            self.logger.warning("활성화된 채팅방이 없습니다")
            return None
        
        if self.config['settings'].get('rotate_chats', True):
            # 순환 방식
            room = enabled_rooms[self.current_chat_index % len(enabled_rooms)]
            self.current_chat_index += 1
        else:
            # 랜덤 방식
            room = random.choice(enabled_rooms)
        
        return room['url']
    
    def post_to_all_chats(self, content: str) -> Dict[str, bool]:
        """모든 활성화된 채팅방에 메시지 포스팅"""
        results = {}
        # 활성화된 채팅방만 필터링
        chat_rooms = self.config.get('chat_rooms', [])
        enabled_rooms = [room for room in chat_rooms if room.get('enabled', True)]
        
        self.logger.info(f"📢 {len(enabled_rooms)}개 채팅방에 포스팅 시작")
        
        for i, room in enumerate(enabled_rooms, 1):
            chat_url = room['url']
            chat_name = room.get('name', '이름없음')
            self.logger.info(f"\n[{i}/{len(enabled_rooms)}] [{chat_name}] 채팅방 포스팅 중...")
            success = self.post_to_chat(chat_url, content)
            results[chat_url] = success
            
            # 마지막 채팅방이 아니면 대기
            if i < len(enabled_rooms):
                wait_time = self.config['settings'].get('wait_between_chats', 3)
                self.logger.info(f"⏱️ {wait_time}초 대기 중...")
                time.sleep(wait_time)
        
        # 결과 요약
        success_count = sum(1 for v in results.values() if v)
        self.logger.info(f"\n✅ 포스팅 완료: {success_count}/{len(enabled_rooms)} 성공")
        
        return results
    
    def is_within_schedule(self) -> bool:
        """현재 시간이 스케줄 범위 내인지 확인"""
        now = datetime.now()
        
        # 새로운 형식 (YYYY-MM-DD HH:MM) 지원
        if 'start_datetime' in self.config['schedule'] and 'end_datetime' in self.config['schedule']:
            try:
                start_datetime = datetime.strptime(self.config['schedule']['start_datetime'], "%Y-%m-%d %H:%M")
                end_datetime = datetime.strptime(self.config['schedule']['end_datetime'], "%Y-%m-%d %H:%M")
                
                is_within = start_datetime <= now <= end_datetime
                
                if not is_within:
                    self.logger.info(f"스케줄 범위 외: 현재 {now.strftime('%Y-%m-%d %H:%M')}, 시작 {start_datetime.strftime('%Y-%m-%d %H:%M')}, 종료 {end_datetime.strftime('%Y-%m-%d %H:%M')}")
                
                return is_within
            except ValueError as e:
                self.logger.error(f"날짜/시간 형식 오류: {str(e)}")
                return False
        
        # 기존 형식 (HH:MM) 호환성 유지
        elif 'start_time' in self.config['schedule'] and 'end_time' in self.config['schedule']:
            now_time = now.time()
            start_time = datetime.strptime(self.config['schedule']['start_time'], "%H:%M").time()
            end_time = datetime.strptime(self.config['schedule']['end_time'], "%H:%M").time()
            
            return start_time <= now_time <= end_time
        
        # 설정이 없으면 항상 실행
        return True
    
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
