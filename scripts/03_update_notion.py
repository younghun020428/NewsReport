import os
import json
from notion_client import Client
from config import NOTION_API_KEY, NOTION_DATABASE_ID, get_now_kst

def update_notion_database(results):
    """
    요약된 뉴스 리스트를 노션 데이터베이스에 페이지로 추가합니다.
    """
    if not results:
        print("업데이트할 뉴스가 없습니다.")
        return

    notion = Client(auth=NOTION_API_KEY)
    now = get_now_kst()
    today_iso = now.date().isoformat()
    
    success_count = 0
    for item in results:
        try:
            notion.pages.create(
                parent={"database_id": NOTION_DATABASE_ID},
                properties={
                    "제목": {"title": [{"text": {"content": item.get("title", "제목 없음")}}]},
                    "날짜": {"date": {"start": today_iso}},
                    "섹터": {"select": {"name": item.get("sector", "미분류")}},
                    "요약": {"rich_text": [{"text": {"content": item.get("summary", "내용 없음")}}]},
                    "URL": {"url": item.get("url", "")}
                }
            )
            success_count += 1
        except Exception as e:
            print(f"노션 페이지 생성 중 오류 발생: {e}")
            
    print(f"[{now.isoformat()}] {success_count}개의 뉴스를 노션 데이터베이스에 업데이트했습니다.")

def upload_data():
    today_str = get_now_kst().strftime("%Y%m%d")
    from pathlib import Path
    filtered_file = Path(__file__).parent.parent / "secondary_data" / f"filtered_news_{today_str}.json"
    
    if filtered_file.exists():
        with open(filtered_file, "r", encoding="utf-8-sig") as f:
            results = json.load(f)
        update_notion_database(results)
    else:
        print(f"요약 데이터 파일이 없습니다: {filtered_file}")

if __name__ == "__main__":
    upload_data()
