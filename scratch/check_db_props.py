import requests
import sys
import os
sys.path.append(os.getcwd())
from scripts.config import NOTION_API_KEY, NOTION_BRIEFING_PAGE_ID

def check_db_props():
    url = f"https://api.notion.com/v1/databases/{NOTION_BRIEFING_PAGE_ID}"
    headers = {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Notion-Version": "2022-06-28"
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        props = response.json().get("properties", {})
        print(f"Properties: {list(props.keys())}")
        for k, v in props.items():
            hex_name = ":".join(f"{ord(c):04x}" for c in k)
            print(f"Property hex: {hex_name}")
            if v.get("type") == "title":
                print(f"Title property name found. Hex: {hex_name}")
                # k를 변수에 저장해서 나중에 출력
                title_key = k
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    check_db_props()
