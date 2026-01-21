"""
네이버밴드 안전 타이핑 매크로
Chrome 디버깅 모드를 사용하여 기존 로그인 세션 활용
"""

import os
import json
import time
import random
import logging
from datetime import datetime
from typing import List, Dict, Optional

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

try:
    import pyperclip
    HAS_PYPERCLIP = True
except ImportError:
    HAS_PYPERCLIP = False
    print("⚠️ pyperclip이 설치되지 않았습니다. 한글 입력이 제한될 수 있습니다.")
    print("설치: pip install pyperclip")


class SafeBandTypingMacro:
    """네이버밴드 안전 타이핑 매크로 클래스"""
    
    def __init__(self, debug_port: int = 9222, config_path: str = None):
        """
        크롬 디버깅 모드에 연결
        
        Args:
            debug_port: Chrome 디버깅 포트 (기본: 9222)
            config_path: 설정 파일 경로 (선택사항)
        
        사용 전 Chrome을 디버깅 모드로 실행해야 합니다:
        Windows: chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chrome_dev_session"
        Mac: /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222 --user-data-dir="/tmp/chrome_dev_session"
        Linux: google-chrome --remote-debugging-port=9222 --user-data-dir="/tmp/chrome_dev_session"
        """
        self.debug_port = debug_port
        self.config_path = config_path
        self.driver = None
        self.wait = None
        self.send_count = 0
        self.config = self._load_config() if config_path else {}
        
        # 로깅 설정
        self._setup_logging()
        
        # 드라이버 연결
        self._connect_to_chrome()
        
    def _setup_logging(self):
        """로깅 설정"""
        os.makedirs('logs', exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(
                    f'logs/safe_macro_{datetime.now().strftime("%Y%m%d")}.log',
                    encoding='utf-8'
                ),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def _load_config(self) -> Dict:
        """설정 파일 로드"""
        if self.config_path and os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                self.logger.warning(f"설정 파일 로드 실패: {e}")
        return {}
        
    def _connect_to_chrome(self):
        """크롬 디버깅 세션에 연결"""
        try:
            chrome_options = Options()
            chrome_options.add_experimental_option(
                "debuggerAddress", 
                f"127.0.0.1:{self.debug_port}"
            )
            
            self.driver = webdriver.Chrome(options=chrome_options)
            self.wait = WebDriverWait(self.driver, 15)
            
            self.logger.info(f"✅ 크롬 디버깅 세션에 연결 완료 (포트: {self.debug_port})")
            self.logger.info(f"현재 URL: {self.driver.current_url}")
            
        except Exception as e:
            error_msg = f"""
❌ 크롬 연결 실패: {e}

Chrome을 디버깅 모드로 먼저 실행해야 합니다:

Windows:
chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\\chrome_dev_session"

Mac:
/Applications/Google\\ Chrome.app/Contents/MacOS/Google\\ Chrome --remote-debugging-port=9222 --user-data-dir="/tmp/chrome_dev_session"

Linux:
google-chrome --remote-debugging-port=9222 --user-data-dir="/tmp/chrome_dev_session"
"""
            self.logger.error(error_msg)
            raise
            
    def find_chat_input(self) -> Optional[object]:
        """
        채팅 입력창 찾기 (다중 선택자 지원)
        
        Returns:
            입력창 엘리먼트 또는 None
        """
        # 밴드 채팅 입력창 선택자들
        selectors = [
            # 채팅 입력창
            "textarea.commentWrite",
            "textarea[placeholder*='메시지']",
            "textarea[placeholder*='댓글']",
            "textarea._chatInput",
            "textarea.uCommentWrite",
            
            # contenteditable div
            "div[contenteditable='true']",
            "div.chatInput[contenteditable='true']",
            
            # 게시글 작성
            "textarea[placeholder*='게시글']",
            "textarea[placeholder*='작성']",
            
            # 일반적인 입력창
            ".chatInput textarea",
            ".writeForm textarea",
            "textarea.writeTextarea"
        ]
        
        self.logger.info("채팅 입력창 검색 중...")
        
        for selector in selectors:
            try:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                for element in elements:
                    if element.is_displayed() and element.is_enabled():
                        self.logger.info(f"✅ 입력창 발견: {selector}")
                        return element
            except Exception as e:
                self.logger.debug(f"선택자 {selector} 시도 실패: {e}")
                continue
        
        self.logger.error("❌ 채팅 입력창을 찾을 수 없습니다")
        self.logger.info("💡 페이지를 확인하거나 수동으로 입력창을 클릭해보세요")
        return None
        
    def human_like_typing(self, element, text: str) -> bool:
        """
        사람처럼 자연스러운 타이핑
        
        Args:
            element: 입력창 엘리먼트
            text: 입력할 텍스트
            
        Returns:
            성공 여부
        """
        try:
            # 입력창 포커스
            self.logger.info("입력창에 포커스 중...")
            element.click()
            time.sleep(random.uniform(0.5, 1.2))
            
            # 기존 내용 지우기
            element.send_keys(Keys.CONTROL, 'a')
            time.sleep(0.2)
            element.send_keys(Keys.BACK_SPACE)
            time.sleep(0.5)
            
            # 한글 입력 처리
            if HAS_PYPERCLIP:
                # 클립보드 활용 (한글 입력에 안전)
                self.logger.info("클립보드를 통한 입력 사용")
                pyperclip.copy(text)
                time.sleep(random.uniform(0.3, 0.8))
                element.send_keys(Keys.CONTROL, 'v')
            else:
                # 직접 타이핑 (영문/숫자만 권장)
                self.logger.info("직접 타이핑 사용")
                for char in text:
                    element.send_keys(char)
                    # 자연스러운 타이핑 속도
                    time.sleep(random.uniform(0.05, 0.15))
            
            # 검토하는 시간 (중요!)
            review_time = random.uniform(2.0, 4.0)
            self.logger.info(f"⏰ {review_time:.1f}초 검토 중...")
            time.sleep(review_time)
            
            return True
            
        except Exception as e:
            self.logger.error(f"타이핑 중 오류: {e}")
            return False
            
    def send_message(self, message: str, auto_send: bool = False) -> bool:
        """
        메시지 입력 및 전송
        
        Args:
            message: 전송할 메시지
            auto_send: 자동 전송 여부 (False 권장)
            
        Returns:
            성공 여부
        """
        try:
            self.logger.info("=" * 60)
            self.logger.info(f"메시지 전송 시작 (#{self.send_count + 1})")
            self.logger.info("=" * 60)
            
            # 입력창 찾기
            input_box = self.find_chat_input()
            if not input_box:
                return False
            
            # 타이핑
            if not self.human_like_typing(input_box, message):
                return False
                
            self.logger.info("✅ 메시지 입력 완료")
            
            # 전송 처리
            if auto_send:
                self.logger.warning("⚠️ 자동 전송 모드")
                input_box.send_keys(Keys.ENTER)
                self.logger.info("📤 자동 전송 완료")
            else:
                self.logger.info("⏸️ 수동 전송 대기 중...")
                self.logger.info("💡 Enter 키를 직접 눌러서 전송하세요")
                
            self.send_count += 1
            return True
            
        except Exception as e:
            self.logger.error(f"❌ 전송 실패: {e}")
            return False
            
    def generate_varied_message(self, base_template: str, 
                               add_timestamp: bool = True,
                               add_prefix: bool = True) -> str:
        """
        스팸 방지를 위한 메시지 변형
        
        Args:
            base_template: 기본 템플릿
            add_timestamp: 시간 추가 여부
            add_prefix: 접두어 추가 여부
            
        Returns:
            변형된 메시지
        """
        now = datetime.now()
        timestamp = now.strftime("%H:%M")
        
        result = base_template
        
        # 접두어 추가
        if add_prefix:
            prefixes = ["🚛", "📦", "[긴급]", "【화물】", "★수배★", "🔔", "📢"]
            prefix = random.choice(prefixes)
            result = f"{prefix} {result}"
        
        # 타임스탬프 추가
        if add_timestamp:
            suffixes = [
                f"({timestamp} 현재)",
                f"- {timestamp} 업데이트",
                f"※{timestamp}※",
                f"[{timestamp}]",
                f"\n\n⏰ {timestamp} 업데이트"
            ]
            suffix = random.choice(suffixes)
            result = f"{result}\n\n{suffix}"
        
        return result
        
    def run_continuous(self, 
                      base_message: str,
                      interval_minutes: int = 5,
                      max_sends: int = 20,
                      auto_send: bool = False,
                      vary_message: bool = True) -> None:
        """
        연속 전송 (신중하게 사용)
        
        Args:
            base_message: 기본 메시지
            interval_minutes: 전송 간격 (분)
            max_sends: 최대 전송 횟수
            auto_send: 자동 전송 여부
            vary_message: 메시지 변형 여부
        """
        self.logger.info("🔄 연속 전송 모드 시작")
        self.logger.info(f"📊 설정: {interval_minutes}분 간격, 최대 {max_sends}회")
        self.logger.info(f"⚠️ 자동 전송: {'ON' if auto_send else 'OFF'}")
        
        try:
            while self.send_count < max_sends:
                # 메시지 준비
                if vary_message:
                    message = self.generate_varied_message(base_message)
                else:
                    message = base_message
                
                # 전송
                success = self.send_message(message, auto_send=auto_send)
                
                if success:
                    self.logger.info(f"📊 진행률: {self.send_count}/{max_sends}")
                else:
                    self.logger.warning("⚠️ 전송 실패, 다음 시도까지 대기")
                
                # 마지막 전송이 아니면 대기
                if self.send_count < max_sends:
                    # 랜덤 간격 추가 (±30초)
                    wait_seconds = interval_minutes * 60 + random.randint(-30, 30)
                    next_time = datetime.now().timestamp() + wait_seconds
                    next_time_str = datetime.fromtimestamp(next_time).strftime('%H:%M:%S')
                    
                    self.logger.info(f"⏰ 다음 전송 예정: {next_time_str} ({wait_seconds}초 후)")
                    time.sleep(wait_seconds)
                    
        except KeyboardInterrupt:
            self.logger.info("\n⏹️ 사용자가 중단했습니다")
        except Exception as e:
            self.logger.error(f"❌ 실행 중 오류: {e}")
        finally:
            self.logger.info("=" * 60)
            self.logger.info(f"🏁 총 {self.send_count}회 전송 완료")
            self.logger.info("=" * 60)
            
    def get_current_page_info(self) -> Dict:
        """
        현재 페이지 정보 가져오기
        
        Returns:
            페이지 정보 딕셔너리
        """
        try:
            info = {
                'url': self.driver.current_url,
                'title': self.driver.title,
                'is_band': 'band.us' in self.driver.current_url
            }
            return info
        except Exception as e:
            self.logger.error(f"페이지 정보 가져오기 실패: {e}")
            return {}
            
    def close(self):
        """리소스 정리"""
        if self.driver:
            self.logger.info("⚠️ 드라이버를 종료하지 않습니다 (디버깅 세션 유지)")
            self.logger.info("Chrome 창을 수동으로 닫아주세요")
            # self.driver.quit()  # 디버깅 세션이므로 종료하지 않음
            

def create_freight_message(
    truck_type: str = "5톤 윙바디",
    pickup_location: str = "경기 이천",
    pickup_time: str = "오후 2시",
    dropoff_location: str = "부산 강서구",
    dropoff_time: str = "내일 오전",
    cargo_info: str = "파렛트 화물 15개",
    price: str = "45만원",
    payment: str = "현금/인수증",
    contact: str = "010-1234-5678"
) -> str:
    """
    화물 정보 메시지 생성
    
    Returns:
        포맷된 화물 정보 메시지
    """
    message = f"""{truck_type} 화물 수배

📍 상차: {pickup_location} ({pickup_time})
📍 하차: {dropoff_location} ({dropoff_time})
📦 화물: {cargo_info}
💰 운임: {price} ({payment})

연락: {contact}"""
    
    return message


# 사용 예시 및 테스트
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='네이버밴드 안전 타이핑 매크로')
    parser.add_argument('--port', type=int, default=9222, help='Chrome 디버깅 포트')
    parser.add_argument('--test', action='store_true', help='테스트 모드 (1회만 실행)')
    parser.add_argument('--auto-send', action='store_true', help='자동 전송 활성화')
    parser.add_argument('--interval', type=int, default=5, help='전송 간격 (분)')
    parser.add_argument('--max-sends', type=int, default=20, help='최대 전송 횟수')
    
    args = parser.parse_args()
    
    try:
        # 매크로 초기화
        print("\n" + "=" * 60)
        print("네이버밴드 안전 타이핑 매크로")
        print("=" * 60 + "\n")
        
        macro = SafeBandTypingMacro(debug_port=args.port)
        
        # 현재 페이지 확인
        page_info = macro.get_current_page_info()
        print(f"현재 페이지: {page_info.get('title', 'Unknown')}")
        print(f"URL: {page_info.get('url', 'Unknown')}")
        
        if not page_info.get('is_band'):
            print("\n⚠️ 경고: 현재 네이버밴드 페이지가 아닙니다")
            print("💡 Chrome에서 네이버밴드 채팅방으로 이동해주세요\n")
        
        # 화물 정보 템플릿
        freight_template = create_freight_message()
        
        print("\n" + "-" * 60)
        print("전송할 메시지:")
        print("-" * 60)
        print(freight_template)
        print("-" * 60 + "\n")
        
        if args.test:
            # 테스트 모드: 1회만 실행
            print("🧪 테스트 모드: 1회만 전송합니다\n")
            macro.send_message(freight_template, auto_send=args.auto_send)
        else:
            # 연속 전송 모드
            confirmation = input(f"연속 전송을 시작하시겠습니까? (최대 {args.max_sends}회, {args.interval}분 간격) [y/N]: ")
            if confirmation.lower() == 'y':
                macro.run_continuous(
                    freight_template,
                    interval_minutes=args.interval,
                    max_sends=args.max_sends,
                    auto_send=args.auto_send
                )
            else:
                print("취소되었습니다")
                
    except KeyboardInterrupt:
        print("\n\n프로그램을 종료합니다...")
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if 'macro' in locals():
            macro.close()
