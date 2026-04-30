import requests
import sys
import os
sys.path.append(os.getcwd())
from scripts.config import NOTION_API_KEY

def inspect_page():
    page_id = "351063ba-8339-8188-a3e0-e06125b62036"
    url = f"https://api.notion.com/v1/pages/{page_id}"
    headers = {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Notion-Version": "2022-06-28"
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        print(f"Page ID: {data['id']}")
        print(f"Archived (Deleted): {data.get('archived')}")
        
        props = data.get("properties", {})
        for k, v in props.items():
            if v.get("type") == "title":
                title_list = v.get("title", [])
                if title_list:
                    print(f"Title: {title_list[0].get('plain_text')}")
                else:
                    print("Title: (Empty)")
            else:
                # 다른 속성 확인 (예: 날짜)
                pass
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    inspect_page()
