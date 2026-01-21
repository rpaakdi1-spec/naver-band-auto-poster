"""
네이버밴드 안전 매크로 사용 예시
"""

from src.safe_band_macro import SafeBandTypingMacro, create_freight_message


def example_single_message():
    """단일 메시지 전송 예시"""
    print("\n" + "=" * 60)
    print("예시 1: 단일 메시지 전송")
    print("=" * 60)
    
    # 매크로 초기화
    macro = SafeBandTypingMacro(debug_port=9222)
    
    # 간단한 메시지
    message = "안녕하세요! 테스트 메시지입니다."
    
    # 전송 (수동 Enter)
    macro.send_message(message, auto_send=False)
    
    print("\n✅ 메시지가 입력되었습니다. Enter를 눌러 전송하세요.")
    

def example_freight_message():
    """화물 정보 메시지 예시"""
    print("\n" + "=" * 60)
    print("예시 2: 화물 정보 메시지")
    print("=" * 60)
    
    # 매크로 초기화
    macro = SafeBandTypingMacro(debug_port=9222)
    
    # 화물 정보 생성
    freight_msg = create_freight_message(
        truck_type="5톤 윙바디",
        pickup_location="경기 이천시 부발읍",
        pickup_time="오후 2시",
        dropoff_location="부산광역시 강서구 녹산산단",
        dropoff_time="내일 오전 10시",
        cargo_info="파렛트 화물 15개 (약 8톤)",
        price="45만원",
        payment="현금/인수증",
        contact="010-1234-5678"
    )
    
    print("\n전송할 메시지:")
    print("-" * 60)
    print(freight_msg)
    print("-" * 60)
    
    # 전송
    macro.send_message(freight_msg, auto_send=False)
    
    print("\n✅ 화물 정보가 입력되었습니다. 확인 후 Enter를 눌러 전송하세요.")


def example_varied_messages():
    """변형된 메시지 여러 개 전송 예시"""
    print("\n" + "=" * 60)
    print("예시 3: 변형된 메시지 3회 전송")
    print("=" * 60)
    
    # 매크로 초기화
    macro = SafeBandTypingMacro(debug_port=9222)
    
    # 기본 메시지
    base_message = """5톤 카고 화물 수배

📍 상차: 서울 강남구 (오늘 오후 3시)
📍 하차: 대전 유성구 (내일 오전)
📦 화물: 박스 화물 200개
💰 운임: 35만원 (세금계산서)

연락처: 010-9876-5432"""
    
    # 3회 반복 전송
    for i in range(3):
        print(f"\n--- {i+1}회 전송 ---")
        
        # 메시지 변형
        varied_msg = macro.generate_varied_message(
            base_message,
            add_timestamp=True,
            add_prefix=True
        )
        
        print("전송할 메시지:")
        print(varied_msg)
        print()
        
        # 전송
        success = macro.send_message(varied_msg, auto_send=False)
        
        if success:
            print(f"✅ {i+1}번째 메시지 입력 완료. Enter를 눌러 전송하세요.")
            input("Enter를 누르고 다음 메시지로 진행...")
        else:
            print(f"❌ {i+1}번째 메시지 입력 실패")
            break


def example_continuous_mode():
    """연속 전송 모드 예시 (신중하게 사용)"""
    print("\n" + "=" * 60)
    print("예시 4: 연속 전송 모드")
    print("=" * 60)
    print("\n⚠️ 경고: 이 모드는 자동으로 반복 전송합니다.")
    print("스팸으로 간주될 수 있으니 신중하게 사용하세요.\n")
    
    confirmation = input("정말 실행하시겠습니까? (yes 입력): ")
    if confirmation.lower() != "yes":
        print("취소되었습니다.")
        return
    
    # 매크로 초기화
    macro = SafeBandTypingMacro(debug_port=9222)
    
    # 기본 메시지
    base_message = create_freight_message(
        truck_type="1톤 탑차",
        pickup_location="인천 남동구",
        pickup_time="오후 5시",
        dropoff_location="수원시 영통구",
        dropoff_time="저녁 8시",
        cargo_info="소형 박스 50개",
        price="15만원",
        payment="현금",
        contact="010-5555-6666"
    )
    
    # 연속 전송 (5분 간격, 최대 5회, 수동 전송)
    macro.run_continuous(
        base_message=base_message,
        interval_minutes=5,
        max_sends=5,
        auto_send=False,  # 수동 전송 (안전)
        vary_message=True  # 메시지 변형
    )


def example_multiple_freights():
    """여러 화물 정보 순차 전송 예시"""
    print("\n" + "=" * 60)
    print("예시 5: 여러 화물 정보 순차 전송")
    print("=" * 60)
    
    # 매크로 초기화
    macro = SafeBandTypingMacro(debug_port=9222)
    
    # 여러 화물 정보 리스트
    freights = [
        {
            "truck_type": "5톤 윙바디",
            "pickup_location": "경기 이천",
            "pickup_time": "오후 2시",
            "dropoff_location": "부산 강서구",
            "dropoff_time": "내일 오전",
            "cargo_info": "파렛트 15개",
            "price": "45만원",
            "payment": "현금",
            "contact": "010-1111-2222"
        },
        {
            "truck_type": "1톤 탑차",
            "pickup_location": "서울 강남구",
            "pickup_time": "오후 4시",
            "dropoff_location": "경기 성남시",
            "dropoff_time": "저녁 7시",
            "cargo_info": "박스 50개",
            "price": "12만원",
            "payment": "카드",
            "contact": "010-3333-4444"
        },
        {
            "truck_type": "3.5톤 카고",
            "pickup_location": "인천 남동구",
            "pickup_time": "오전 10시",
            "dropoff_location": "대전 유성구",
            "dropoff_time": "오후 3시",
            "cargo_info": "가구 10점",
            "price": "30만원",
            "payment": "세금계산서",
            "contact": "010-5555-6666"
        }
    ]
    
    # 각 화물 정보 전송
    for i, freight_info in enumerate(freights, 1):
        print(f"\n--- {i}번째 화물 정보 ---")
        
        # 화물 메시지 생성
        msg = create_freight_message(**freight_info)
        
        # 전송
        success = macro.send_message(msg, auto_send=False)
        
        if success:
            print(f"✅ {i}번째 화물 정보 입력 완료")
            if i < len(freights):
                input("Enter를 누르고 다음 화물 정보로 진행...")
        else:
            print(f"❌ {i}번째 화물 정보 입력 실패")
            break


def main():
    """메인 메뉴"""
    while True:
        print("\n" + "=" * 60)
        print("네이버밴드 안전 매크로 - 사용 예시")
        print("=" * 60)
        print("\n사용 가능한 예시:")
        print("1. 단일 메시지 전송")
        print("2. 화물 정보 메시지")
        print("3. 변형된 메시지 3회 전송")
        print("4. 연속 전송 모드 (⚠️ 신중하게)")
        print("5. 여러 화물 정보 순차 전송")
        print("0. 종료")
        
        choice = input("\n선택하세요 (0-5): ").strip()
        
        try:
            if choice == "1":
                example_single_message()
            elif choice == "2":
                example_freight_message()
            elif choice == "3":
                example_varied_messages()
            elif choice == "4":
                example_continuous_mode()
            elif choice == "5":
                example_multiple_freights()
            elif choice == "0":
                print("\n프로그램을 종료합니다.")
                break
            else:
                print("\n❌ 잘못된 선택입니다. 0-5 사이의 숫자를 입력하세요.")
        except KeyboardInterrupt:
            print("\n\n⏹️ 사용자가 중단했습니다.")
        except Exception as e:
            print(f"\n❌ 오류 발생: {e}")
            import traceback
            traceback.print_exc()
        
        input("\nEnter를 눌러 메뉴로 돌아가기...")


if __name__ == "__main__":
    try:
        print("""
╔════════════════════════════════════════════════════════════╗
║       네이버밴드 안전 타이핑 매크로 - 사용 예시         ║
╚════════════════════════════════════════════════════════════╝

⚠️ 사용 전 확인사항:
1. Chrome을 디버깅 모드로 실행했나요?
2. 네이버밴드에 로그인했나요?
3. 메시지를 보낼 채팅방을 열었나요?

Chrome 디버깅 모드 실행:
  Windows: start_chrome_debug.bat
  또는: chrome.exe --remote-debugging-port=9222
        """)
        
        input("준비되었으면 Enter를 누르세요...")
        main()
        
    except Exception as e:
        print(f"\n❌ 프로그램 오류: {e}")
        import traceback
        traceback.print_exc()
