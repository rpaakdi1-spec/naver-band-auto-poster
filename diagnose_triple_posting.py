#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
포스팅 중복 문제 진단 스크립트

사용자 시나리오:
- 포스트 1개 등록
- 채팅방 1개 등록
- 포스팅 실행
- 예상: 1번 포스팅
- 실제: 3번 포스팅
"""

import json
import os

def diagnose_posting_issue():
    """포스팅 중복 문제 진단"""
    print("=" * 80)
    print("📊 포스팅 중복 문제 진단")
    print("=" * 80)
    
    # 시나리오: 사용자가 보고한 상황
    test_post = "01/25일 20시 백암 - 양산 \n빠른당착 16p 42만\n010 5046 6242"
    
    print(f"\n🔍 테스트 포스트:")
    print(f"   {test_post[:50]}...")
    print(f"   (총 {len(test_post)}자, 줄바꿈 {test_post.count(chr(10))}개)")
    
    # config.json 확인
    config_path = "config/config.json"
    
    if not os.path.exists(config_path):
        print(f"\n⚠️ {config_path} 파일이 없습니다.")
        return
    
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    # 포스트 분석
    posts = config.get('posts', [])
    enabled_posts = [p for p in posts if p.get('enabled', True)]
    
    print(f"\n📝 등록된 포스트 분석:")
    print(f"   총 포스트 수: {len(posts)}개")
    print(f"   활성화된 포스트: {len(enabled_posts)}개")
    
    # 중복 포스트 체크
    post_contents = [p.get('content', '') for p in posts]
    from collections import Counter
    content_counts = Counter(post_contents)
    
    duplicates = {content: count for content, count in content_counts.items() if count > 1}
    
    if duplicates:
        print(f"\n⚠️ 중복된 포스트 발견!")
        print(f"=" * 80)
        for content, count in duplicates.items():
            print(f"\n중복 횟수: {count}회")
            print(f"내용 미리보기: {content[:50]}...")
            
            # 해당 포스트의 상세 정보
            matching_posts = [p for p in posts if p.get('content') == content]
            for i, post in enumerate(matching_posts, 1):
                print(f"  [{i}] 활성화: {'✅' if post.get('enabled', True) else '❌'}")
    else:
        print(f"   ✅ 중복된 포스트 없음")
    
    # 채팅방 분석
    chat_rooms = config.get('chat_rooms', [])
    enabled_rooms = [room for room in chat_rooms if room.get('enabled', True)]
    
    print(f"\n📱 등록된 채팅방 분석:")
    print(f"   총 채팅방 수: {len(chat_rooms)}개")
    print(f"   활성화된 채팅방: {len(enabled_rooms)}개")
    
    # 포스팅 예상 횟수 계산
    if enabled_posts and enabled_rooms:
        expected_posts_per_run = len(enabled_rooms)
        print(f"\n🎯 예상 포스팅 횟수 (1회 실행 시):")
        print(f"   활성화된 채팅방 × 1회 = {expected_posts_per_run}회")
        
        if len(enabled_posts) > 1:
            print(f"\n⚠️ 주의: 활성화된 포스트가 {len(enabled_posts)}개입니다.")
            print(f"   - 각 채팅방마다 다른 포스트가 전송될 수 있습니다.")
            print(f"   - 같은 내용을 보내려면 포스트를 1개만 등록하세요.")
    
    # 스케줄 분석
    schedule = config.get('schedule', {})
    interval = schedule.get('interval_minutes', 30)
    
    print(f"\n⏰ 스케줄 설정:")
    print(f"   포스팅 간격: {interval}분")
    print(f"   랜덤 딜레이: {schedule.get('random_delay_minutes', 5)}분")
    
    # 중복 포스팅 가능성 분석
    print(f"\n" + "=" * 80)
    print("🔍 중복 포스팅 원인 분석:")
    print("=" * 80)
    
    possible_causes = []
    
    # 원인 1: 중복 포스트 등록
    if duplicates:
        possible_causes.append({
            'cause': '같은 포스트가 여러 번 등록됨',
            'count': max(content_counts.values()),
            'solution': 'GUI/웹에서 중복된 포스트를 삭제하세요.'
        })
    
    # 원인 2: 여러 채팅방
    if len(enabled_rooms) > 1:
        possible_causes.append({
            'cause': f'활성화된 채팅방이 {len(enabled_rooms)}개입니다',
            'count': len(enabled_rooms),
            'solution': '각 채팅방에 1번씩 포스팅됩니다. 의도한 동작일 수 있습니다.'
        })
    
    # 원인 3: 여러 포스트
    if len(enabled_posts) > 1:
        possible_causes.append({
            'cause': f'활성화된 포스트가 {len(enabled_posts)}개입니다',
            'count': len(enabled_posts),
            'solution': '순환/랜덤 방식으로 각 채팅방마다 다른 포스트가 전송됩니다.'
        })
    
    if not possible_causes:
        print("✅ 명확한 원인을 찾을 수 없습니다.")
        print("   config.json 파일 내용을 확인하거나 로그를 제공해주세요.")
    else:
        for i, cause_info in enumerate(possible_causes, 1):
            print(f"\n{i}. {cause_info['cause']}")
            print(f"   → 예상 포스팅 횟수: {cause_info['count']}회")
            print(f"   → 해결 방법: {cause_info['solution']}")
    
    # 권장 조치
    print(f"\n" + "=" * 80)
    print("💡 권장 조치:")
    print("=" * 80)
    
    if duplicates:
        print("1. 중복된 포스트 삭제:")
        print("   - GUI: 포스트 관리 → 중복 항목 선택 → [✖ 삭제]")
        print("   - 웹: 포스트 관리 → 중복 항목의 [🗑] 클릭")
    
    if len(enabled_posts) > 1:
        print(f"\n2. 포스트 수 확인:")
        print(f"   - 같은 내용을 모든 채팅방에 보내려면 포스트 1개만 등록")
        print(f"   - 현재: {len(enabled_posts)}개 활성화됨")
    
    if len(enabled_rooms) > 1:
        print(f"\n3. 채팅방 수 확인:")
        print(f"   - 1개 채팅방에만 보내려면 나머지 채팅방 체크 해제")
        print(f"   - 현재: {len(enabled_rooms)}개 활성화됨")
        print(f"   - 각 채팅방에 1번씩 포스팅됩니다 (정상 동작)")
    
    print(f"\n" + "=" * 80)
    print("📋 상세 정보:")
    print("=" * 80)
    print(f"등록된 포스트 목록:")
    for i, post in enumerate(posts, 1):
        status = "✅ 활성" if post.get('enabled', True) else "❌ 비활성"
        content = post.get('content', '')
        preview = content[:40] + "..." if len(content) > 40 else content
        preview = preview.replace('\n', '\\n')
        print(f"  {i}. [{status}] {preview}")
    
    print(f"\n등록된 채팅방 목록:")
    for i, room in enumerate(chat_rooms, 1):
        status = "✅ 활성" if room.get('enabled', True) else "❌ 비활성"
        name = room.get('name', '이름없음')
        print(f"  {i}. [{status}] {name}")
    
    print(f"\n" + "=" * 80)

if __name__ == "__main__":
    diagnose_posting_issue()
