import requests
import sys
import os
sys.path.append(os.getcwd())
from scripts.config import NOTION_API_KEY, NOTION_BRIEFING_PAGE_ID

def check_page_access():
    url = f"https://api.notion.com/v1/pages/{NOTION_BRIEFING_PAGE_ID}"
    headers = {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Notion-Version": "2022-06-28"
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        print(f"Success! Page found.")
        data = response.json()
        # 제목 추출 시도
        props = data.get("properties", {})
        # 페이지 제목은 'title' 필드에 있음
        for k, v in props.items():
            if v.get("type") == "title":
                title_list = v.get("title", [])
                if title_list:
                    print(f"Page Title: {title_list[0].get('plain_text')}")
    else:
        print(f"Error: {response.status_code}")
        print(f"Message: {response.json().get('message')}")

if __name__ == "__main__":
    check_page_access()
