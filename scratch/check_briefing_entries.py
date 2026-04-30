import requests
import sys
import os
sys.path.append(os.getcwd())
from scripts.config import NOTION_API_KEY, NOTION_BRIEFING_PAGE_ID

def check_briefing_entries():
    # NOTION_BRIEFING_PAGE_ID는 데이터베이스 ID임
    url = f"https://api.notion.com/v1/databases/{NOTION_BRIEFING_PAGE_ID}/query"
    headers = {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }
    
    response = requests.post(url, headers=headers)
    if response.status_code == 200:
        results = response.json().get("results", [])
        print(f"Found {len(results)} briefing reports.")
        for i, page in enumerate(results):
            props = page.get("properties", {})
            # '페이지' 속성이 제목(title) 타입임
            title = ""
            title_prop = props.get("페이지", {}).get("title", [])
            if title_prop:
                title = title_prop[0].get("text", {}).get("content", "")
            try:
                print(f"{i+1}. {repr(title)} (ID: {page['id']})")
            except:
                print(f"{i+1}. [Title Error] (ID: {page['id']})")
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    check_briefing_entries()
