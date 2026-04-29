import os
import json
from datetime import datetime
from notion_client import Client
from config import SECONDARY_DATA_DIR, NOTION_API_KEY, NOTION_DATABASE_ID

def update_notion_db(articles):
    print(f"[{datetime.now().isoformat()}] Notion 업데이트 시작")
    
    if not NOTION_API_KEY or not NOTION_DATABASE_ID:
        print("Notion 설정이 누락되었습니다.")
        return
        
    notion = Client(auth=NOTION_API_KEY)
    
    for article in articles:
        title = article.get("title", "제목 없음")
        summary = article.get("summary", "요약 없음")
        url = article.get("url", "")
        # 섹터명에서 쉼표(,)를 제거하여 노션 에러 방지
        sector = article.get("sector", "기타").replace(",", " ").strip()
        
        try:
            notion.pages.create(
                parent={"database_id": NOTION_DATABASE_ID},
                properties={
                    "제목": {"title": [{"text": {"content": title}}]},
                    "섹터": {"select": {"name": sector}},
                    "수집일": {"select": {"name": datetime.now().strftime("%Y-%m-%d")}},
                    "요약": {"rich_text": [{"text": {"content": summary}}]},
                    "URL": {"url": url},
                    "날짜": {"date": {"start": datetime.now().isoformat()}},
                    "보고서_키워드": {
                        "multi_select": [{"name": kw.replace(",", " ")} for kw in article.get("matched_keywords", [])]
                    }
                }
            )
            print(f"Notion 페이지 생성 완료: {title}")
        except Exception as e:
            print(f"Notion API 업데이트 에러: {e}")

def upload_data():
    today_str = datetime.now().strftime("%Y%m%d")
    input_file = SECONDARY_DATA_DIR / f"filtered_news_{today_str}.json"
    if not input_file.exists(): return
    with open(input_file, "r", encoding="utf-8-sig") as f:
        articles = json.load(f)
    update_notion_db(articles)

if __name__ == "__main__":
    upload_data()
