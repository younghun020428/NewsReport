import requests
import json
import sys
import os
sys.path.append(os.getcwd())
from scripts.config import NOTION_API_KEY, NOTION_DATABASE_ID

def check_latest_entries():
    url = f"https://api.notion.com/v1/databases/{NOTION_DATABASE_ID}/query"
    headers = {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }
    
    # 최근 5개 항목 조회
    payload = {
        "page_size": 5,
        "sorts": [
            {
                "timestamp": "created_time",
                "direction": "descending"
            }
        ]
    }
    
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        results = response.json().get("results", [])
        print(f"Total entries found: {len(results)}")
        for i, page in enumerate(results):
            props = page.get("properties", {})
            title = ""
            title_prop = props.get("제목", {}).get("title", [])
            if title_prop:
                title = title_prop[0].get("text", {}).get("content", "")
            
            date = ""
            date_prop = props.get("날짜", {}).get("date", {})
            if date_prop:
                date = date_prop.get("start", "")
                
            print(f"{i+1}. [{date}] {title}")
    else:
        print(f"Error: {response.status_code} - {response.text}")

if __name__ == "__main__":
    check_latest_entries()
