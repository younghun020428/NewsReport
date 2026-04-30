import os
import json
from notion_client import Client
from config import SECONDARY_DATA_DIR, NOTION_API_KEY, NOTION_DATABASE_ID, get_now_kst

def update_notion_db(articles):
    """
    필터링된 기사 목록을 Notion 데이터베이스에 업데이트합니다.
    """
    now = get_now_kst()
    print(f"[{now.isoformat()}] Notion 업데이트 시작")
    
    if NOTION_API_KEY == "YOUR_NOTION_API_KEY" or NOTION_DATABASE_ID == "YOUR_NOTION_DATABASE_ID":
        print("Notion API 키 또는 Database ID가 설정되지 않았습니다. 모의(Mock) 실행으로 종료합니다.")
        return
        
    notion = Client(auth=NOTION_API_KEY)
    
    for article in articles:
        title = article.get("title", "제목 없음")
        summary = article.get("summary", "요약 없음")
        url = article.get("url", "")
        sector = article.get("sector", "기타")
        
        try:
            notion.pages.create(
                parent={"database_id": NOTION_DATABASE_ID},
                properties={
                    "제목": {
                        "title": [
                            {
                                "text": {
                                    "content": title
                                }
                            }
                        ]
                    },
                    "섹터": {
                        "select": {
                            "name": sector
                        }
                    },
                    "수집일": {
                        "select": {
                            "name": now.strftime("%Y-%m-%d")
                        }
                    },
                    "요약": {
                        "rich_text": [
                            {
                                "text": {
                                    "content": summary
                                }
                            }
                        ]
                    },
                    "URL": {
                        "url": url
                    },
                    "날짜": {
                        "date": {
                            "start": now.isoformat()
                        }
                    },
                    "보고서_키워드": {
                        "multi_select": [
                            {"name": kw} for kw in article.get("matched_keywords", [])
                        ]
                    }
                }
            )
            print(f"Notion 페이지 생성 완료: {title}")
        except Exception as e:
            print(f"Notion API 업데이트 에러: {e}")

def upload_data():
    now = get_now_kst()
    today_str = now.strftime("%Y%m%d")
    input_file = SECONDARY_DATA_DIR / f"filtered_news_{today_str}.json"
    
    if not input_file.exists():
        print(f"업데이트할 데이터 파일이 없습니다: {input_file}")
        return
        
    with open(input_file, "r", encoding="utf-8-sig") as f:
        articles = json.load(f)
        
    update_notion_db(articles)
    print(f"[{now.isoformat()}] Notion 업데이트 프로세스 완료")

if __name__ == "__main__":
    upload_data()
