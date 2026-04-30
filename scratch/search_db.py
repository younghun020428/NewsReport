import requests
import sys
import os
sys.path.append(os.getcwd())
from scripts.config import NOTION_API_KEY

def search_briefing_db():
    url = "https://api.notion.com/v1/search"
    headers = {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }
    payload = {
        "query": "일일 경제 보고서",
        "filter": {
            "value": "database",
            "property": "object"
        }
    }
    
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        results = response.json().get("results", [])
        if not results:
            print("No database named '일일 경제 보고서' found.")
            return
        
        for db in results:
            title = db.get("title", [{}])[0].get("plain_text", "Unknown")
            print(f"Found DB: {title}, ID: {db['id']}")
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    search_briefing_db()
