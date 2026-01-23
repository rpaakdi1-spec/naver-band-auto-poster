#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
네이버밴드 채팅 포스팅 제한 테스트

이 스크립트는 다양한 길이의 포스트를 생성하여
네이버밴드 채팅 시스템의 제한을 테스트합니다.
"""

def generate_test_posts():
    """다양한 길이의 테스트 포스트 생성"""
    
    print("=" * 80)
    print("네이버밴드 채팅 포스팅 제한 테스트")
    print("=" * 80)
    
    # 테스트 케이스 생성
    test_cases = [
        {
            'name': '짧은 포스트 (1줄)',
            'lines': 1,
            'content': "안녕하세요!"
        },
        {
            'name': '보통 포스트 (5줄)',
            'lines': 5,
            'content': "\n".join([f"라인 {i+1}" for i in range(5)])
        },
        {
            'name': '긴 포스트 (10줄)',
            'lines': 10,
            'content': "\n".join([f"라인 {i+1}: 테스트 내용입니다." for i in range(10)])
        },
        {
            'name': '매우 긴 포스트 (20줄)',
            'lines': 20,
            'content': "\n".join([f"라인 {i+1}: 이것은 테스트 메시지입니다." for i in range(20)])
        },
        {
            'name': '극도로 긴 포스트 (50줄)',
            'lines': 50,
            'content': "\n".join([f"라인 {i+1}: 네이버밴드 채팅 테스트" for i in range(50)])
        },
        {
            'name': '초대형 포스트 (100줄)',
            'lines': 100,
            'content': "\n".join([f"라인 {i+1}" for i in range(100)])
        },
    ]
    
    print("\n📊 테스트 케이스 요약:")
    print("=" * 80)
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n{i}. {test['name']}")
        print(f"   줄 수: {test['lines']}줄")
        print(f"   문자 수: {len(test['content'])}자")
        print(f"   줄바꿈 수: {test['content'].count(chr(10))}개")
        
        # 미리보기 (처음 3줄)
        lines = test['content'].split('\n')
        preview_lines = lines[:3]
        print(f"   미리보기:")
        for line in preview_lines:
            print(f"      {line}")
        if len(lines) > 3:
            print(f"      ... (외 {len(lines) - 3}줄)")
    
    # 일반적인 제한사항
    print("\n" + "=" * 80)
    print("📝 일반적인 웹 채팅 시스템 제한:")
    print("=" * 80)
    
    limits = {
        '카카오톡': {
            '줄 수': '제한 없음 (UI상 표시 제한)',
            '문자 수': '약 5,000자',
            '특징': 'Enter로 전송, Shift+Enter로 줄바꿈'
        },
        '라인 (LINE)': {
            '줄 수': '제한 없음',
            '문자 수': '약 10,000자',
            '특징': 'Enter로 전송, Shift+Enter로 줄바꿈'
        },
        '디스코드': {
            '줄 수': '제한 없음',
            '문자 수': '2,000자',
            '특징': 'Enter로 전송, Shift+Enter로 줄바꿈'
        },
        '슬랙 (Slack)': {
            '줄 수': '제한 없음',
            '문자 수': '약 40,000자',
            '특징': 'Enter로 전송, Shift+Enter로 줄바꿈'
        },
        '텔레그램': {
            '줄 수': '제한 없음',
            '문자 수': '4,096자',
            '특징': 'Enter로 줄바꿈, Ctrl+Enter로 전송'
        }
    }
    
    for platform, limit_info in limits.items():
        print(f"\n{platform}:")
        for key, value in limit_info.items():
            print(f"   {key}: {value}")
    
    # 네이버밴드 예상 제한
    print("\n" + "=" * 80)
    print("🎯 네이버밴드 예상 제한 (추정):")
    print("=" * 80)
    print("""
네이버밴드는 공식적으로 채팅 메시지 제한을 명시하지 않지만,
일반적인 웹 채팅 시스템의 패턴을 따를 것으로 예상됩니다:

1. 줄 수 제한
   - 이론적: 제한 없음
   - 실용적: 50~100줄까지 권장
   - 이유: UI 표시 및 성능 문제

2. 문자 수 제한
   - 예상: 2,000 ~ 10,000자
   - 권장: 2,000자 이내
   - 이유: 대부분의 웹 채팅은 2,000~10,000자 제한

3. 실제 테스트 필요
   - 정확한 제한은 실제 전송 테스트 필요
   - 서버 응답 확인 필요
   - 에러 메시지 분석 필요

4. 권장 사항
   ✅ 10줄 이내: 안전
   ⚠️ 10~50줄: 대부분 가능
   ❌ 50줄 이상: 권장하지 않음
   
   ✅ 500자 이내: 안전
   ⚠️ 500~2,000자: 대부분 가능
   ❌ 2,000자 이상: 권장하지 않음
    """)
    
    # 실용적 권장사항
    print("=" * 80)
    print("💡 실용적 권장사항:")
    print("=" * 80)
    print("""
1. 일반 메시지
   - 1~5줄
   - 100~300자
   - 가장 안전하고 읽기 편함

2. 공지사항
   - 5~10줄
   - 300~500자
   - 충분한 정보 전달 가능

3. 상세 안내
   - 10~20줄
   - 500~1,000자
   - 여전히 안전 범위

4. 긴 내용
   - 20줄 이상
   - 1,000자 이상
   - 가능하지만 여러 메시지로 나누기 권장
   - 이유:
     * 읽기 불편
     * 전송 실패 가능성
     * UI 렌더링 지연
    """)
    
    # 테스트 방법
    print("=" * 80)
    print("🧪 직접 테스트 방법:")
    print("=" * 80)
    print("""
1. 짧은 포스트부터 시작
   - 1줄 포스트로 테스트
   - 정상 전송 확인

2. 점진적으로 늘리기
   - 5줄, 10줄, 20줄 순서로 테스트
   - 각 단계에서 전송 성공 확인

3. 실패 시 확인사항
   - 에러 메시지
   - 서버 응답
   - 로그 파일 (logs/ 폴더)

4. 안전 범위 확인
   - 100% 성공하는 최대 줄 수
   - 권장 범위 설정
    """)
    
    print("=" * 80)

if __name__ == "__main__":
    generate_test_posts()
