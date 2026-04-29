import os
from datetime import datetime, timedelta
from notion_client import Client
from config import NOTION_API_KEY, NOTION_DATABASE_ID

import requests

def cleanup_old_articles():
    """
    Notion 데이터베이스에서 10일 이상 지난 기사를 찾아 삭제(Archive)합니다.
    """
    print(f"[{datetime.now().isoformat()}] 오래된 기사 정리(Cleanup) 시작")
    
    if NOTION_API_KEY == "YOUR_NOTION_API_KEY" or NOTION_DATABASE_ID == "YOUR_NOTION_DATABASE_ID":
        print("Notion API 키 또는 Database ID가 설정되지 않아 정리를 건너뜁니다.")
        return
        
    # 10일 전 날짜 계산 (ISO 8601 포맷)
    ten_days_ago = (datetime.utcnow() - timedelta(days=10)).isoformat() + "Z"
    
    headers = {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }
    
    try:
        # created_time이 10일 이전인 항목 쿼리 (직접 HTTP 호출)
        url = f"https://api.notion.com/v1/databases/{NOTION_DATABASE_ID}/query"
        payload = {
            "filter": {
                "timestamp": "created_time",
                "created_time": {
                    "before": ten_days_ago
                }
            }
        }
        
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        
        results = data.get("results", [])
        if not results:
            print("10일 이상 지난 기사가 없습니다.")
            return
            
        print(f"총 {len(results)}개의 오래된 기사를 삭제(Archive)합니다.")
        
        # 각 페이지를 Archived 처리
        for page in results:
            page_id = page["id"]
            patch_url = f"https://api.notion.com/v1/pages/{page_id}"
            patch_payload = {"archived": True}
            requests.patch(patch_url, headers=headers, json=patch_payload)
            
        print(f"[{datetime.now().isoformat()}] 오래된 기사 삭제 완료")
        
    except Exception as e:
        print(f"Notion API 삭제(Cleanup) 에러: {e}")

if __name__ == "__main__":
    cleanup_old_articles()
