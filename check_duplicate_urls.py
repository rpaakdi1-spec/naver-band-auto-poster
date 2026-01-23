#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
중복 URL 체크 스크립트

이 스크립트는 config.json에서 중복된 채팅방 URL을 찾아냅니다.
"""

import json
import os
from collections import Counter

def check_duplicate_urls():
    """config.json에서 중복 URL 체크"""
    config_path = "config/config.json"
    
    if not os.path.exists(config_path):
        print("⚠️ config/config.json 파일이 없습니다.")
        return
    
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    chat_rooms = config.get('chat_rooms', [])
    
    print("=" * 80)
    print("📊 채팅방 URL 중복 체크")
    print("=" * 80)
    print(f"총 등록된 채팅방: {len(chat_rooms)}개\n")
    
    # URL 리스트
    urls = [room.get('url') for room in chat_rooms if room.get('url')]
    
    # URL 빈도 계산
    url_counts = Counter(urls)
    
    # 중복 URL 찾기
    duplicates = {url: count for url, count in url_counts.items() if count > 1}
    
    if duplicates:
        print("⚠️ 중복된 URL 발견!")
        print("=" * 80)
        for url, count in duplicates.items():
            print(f"\n중복 횟수: {count}회")
            print(f"URL: {url}\n")
            
            # 해당 URL을 가진 채팅방 정보
            matching_rooms = [room for room in chat_rooms if room.get('url') == url]
            for i, room in enumerate(matching_rooms, 1):
                print(f"  [{i}] 채팅방 이름: {room.get('name', '이름없음')}")
                print(f"      활성화: {'✅' if room.get('enabled', True) else '❌'}")
        
        print("\n" + "=" * 80)
        print("🔧 해결 방법:")
        print("1. GUI 또는 웹 버전에서 중복된 채팅방을 삭제하세요.")
        print("2. 또는 config/config.json 파일을 직접 편집하세요.")
        print("3. 프로그램을 재시작하면 자동으로 중복이 제거됩니다.")
        print("=" * 80)
    else:
        print("✅ 중복된 URL이 없습니다!")
        print("=" * 80)
        print("\n📋 등록된 채팅방 목록:")
        for i, room in enumerate(chat_rooms, 1):
            status = "✅ 활성" if room.get('enabled', True) else "❌ 비활성"
            print(f"{i}. [{status}] {room.get('name', '이름없음')}")
            print(f"   URL: {room.get('url', 'URL 없음')[:60]}...")
        print("=" * 80)

if __name__ == "__main__":
    check_duplicate_urls()
