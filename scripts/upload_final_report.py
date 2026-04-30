import os
import sys
from pathlib import Path

# scripts 폴더를 경로에 추가하여 config를 불러올 수 있게 함
sys.path.append(str(Path(__file__).resolve().parent))

from notion_client import Client
from config import NOTION_API_KEY, NOTION_BRIEFING_PAGE_ID

def upload_system_report_to_notion():
    if not NOTION_API_KEY or not NOTION_BRIEFING_PAGE_ID:
        print("Notion 설정이 누락되었습니다.")
        return

    notion = Client(auth=NOTION_API_KEY)
    
    # 보고서 파일 읽기
    report_path = "시스템_최종_보고서.md"
    if not os.path.exists(report_path):
        print(f"파일을 찾을 수 없습니다: {report_path}")
        return

    with open(report_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 노션 페이지 생성
    title = "📘 뉴스 큐레이션 시스템 최종 운영 보고서"
    
    # 텍스트를 2000자 단위로 분할하여 블록 생성
    chunks = [content[i:i+1900] for i in range(0, len(content), 1900)]
    blocks = []
    for chunk in chunks:
        blocks.append({
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{"type": "text", "text": {"content": chunk}}]
            }
        })

    try:
        new_page = notion.pages.create(
            parent={"database_id": NOTION_BRIEFING_PAGE_ID},
            properties={
                "페이지": {"title": [{"text": {"content": title}}]}
            },
            children=blocks[:100] # 최대 블록 수 제한 고려
        )
        print(f"SUCCESS: Notion report uploaded! URL: {new_page['url']}")
    except Exception as e:
        print(f"FAILED: Notion upload error: {e}")

if __name__ == "__main__":
    upload_system_report_to_notion()
