import requests
import json
import os
import sys

# scripts 폴더를 경로에 추가
sys.path.append(os.path.join(os.getcwd(), "scripts"))

try:
    from config import NOTION_API_KEY, NOTION_DATABASE_ID
except ImportError:
    # 만약 scripts 폴더 안에서 실행 중이라면
    from config import NOTION_API_KEY, NOTION_DATABASE_ID

def check_via_requests():
    url = f"https://api.notion.com/v1/databases/{NOTION_DATABASE_ID}"
    headers = {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        db = response.json()
        props = db.get("properties", {})
        print("Properties found via Requests:")
        # 인코딩 문제 방지를 위해 유니코드 이스케이프 출력
        for p in props.keys():
            print(f" - '{p}' (repr: {repr(p)})")
        
        if "보고서_키워드" in props:
            print("\nSUCCESS: '보고서_키워드' exists!")
        else:
            # 부분 일치 확인
            matches = [p for p in props.keys() if "보고서" in p or "키워드" in p]
            if matches:
                print(f"\nPARTIAL MATCHES: {matches}")
            print("\nFAILED: '보고서_키워드' not found.")
    else:
        print(f"Error: {response.status_code} - {response.text}")

if __name__ == "__main__":
    with open("scripts/prop_check_utf8.txt", "w", encoding="utf-8") as f:
        sys.stdout = f
        check_via_requests()
        sys.stdout = sys.__stdout__
