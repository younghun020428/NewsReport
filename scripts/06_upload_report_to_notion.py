import os
import json
import requests
from datetime import datetime, timedelta, timezone
from notion_client import Client
from config import INTERIM_REPORTS_DIR, NOTION_API_KEY, NOTION_BRIEFING_PAGE_ID

BRIEFING_RETENTION_DAYS = 10


def chunk_text(text, max_length=2000):
    """텍스트를 최대 길이 단위로 자릅니다."""
    return [text[i:i+max_length] for i in range(0, len(text), max_length)]


def upload_macro_report(report_file_path):
    """
    생성된 매크로 브리핑 마크다운 파일을 Notion의 '일일 경제 보고서' 페이지 하위에
    날짜별 서브페이지로 업로드합니다.
    """
    print(f"[{datetime.now().isoformat()}] 브리핑 Notion 업로드 시작: {report_file_path}")

    if NOTION_API_KEY == "YOUR_NOTION_API_KEY":
        print("Notion API 키가 설정되지 않았습니다. 모의(Mock) 실행으로 종료합니다.")
        return

    notion = Client(auth=NOTION_API_KEY)

    with open(report_file_path, "r", encoding="utf-8") as f:
        markdown_content = f.read()

    today_str = datetime.now().strftime("%Y-%m-%d")
    title = f"[거시경제 브리핑] {today_str}"

    # 본문 내용을 2000자 단위로 잘라 Block 객체 배열로 변환
    blocks = []
    chunks = chunk_text(markdown_content)
    for chunk in chunks:
        blocks.append({
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {"content": chunk}
                    }
                ]
            }
        })

    try:
        # 데이터베이스의 제목 필드명이 '페이지'임을 확인했습니다.
        title_prop_name = "페이지"

        # '일일 경제 보고서' 데이터베이스에 항목으로 추가
        notion.pages.create(
            parent={"database_id": NOTION_BRIEFING_PAGE_ID},
            properties={
                title_prop_name: {
                    "title": [
                        {
                            "text": {"content": title}
                        }
                    ]
                }
            },
            children=blocks[:100]
        )
        print(f"Notion 브리핑 업로드 완료: {title} (필드명: {title_prop_name})")




    except Exception as e:
        print(f"Notion 브리핑 업로드 에러: {e}")


def cleanup_old_briefings():
    """
    '일일 경제 보고서' 페이지의 하위 서브페이지 중 생성 후 10일이 지난 것을 삭제(Archive)합니다.
    """
    print(f"[{datetime.now().isoformat()}] 오래된 브리핑 정리(Cleanup) 시작")

    if NOTION_API_KEY == "YOUR_NOTION_API_KEY":
        print("Notion API 키가 설정되지 않아 정리를 건너뜁니다.")
        return

    cutoff = datetime.now(timezone.utc) - timedelta(days=BRIEFING_RETENTION_DAYS)
    headers = {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }

    try:
        # '일일 경제 보고서' 하위의 모든 블록(페이지) 조회
        url = f"https://api.notion.com/v1/blocks/{NOTION_BRIEFING_PAGE_ID}/children"
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        results = data.get("results", [])
        deleted_count = 0

        for block in results:
            # 하위 child_page 타입만 처리
            if block.get("type") != "child_page":
                continue

            created_time_str = block.get("created_time", "")
            if not created_time_str:
                continue

            created_time = datetime.strptime(created_time_str, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=timezone.utc)
            if created_time < cutoff:
                page_id = block["id"]
                patch_url = f"https://api.notion.com/v1/pages/{page_id}"
                requests.patch(patch_url, headers=headers, json={"archived": True})
                print(f"  삭제됨: {block.get('child_page', {}).get('title', page_id)} ({created_time_str})")
                deleted_count += 1

        if deleted_count == 0:
            print("10일 이상 지난 브리핑 서브페이지가 없습니다.")
        else:
            print(f"[{datetime.now().isoformat()}] 총 {deleted_count}개의 오래된 브리핑 삭제 완료")

    except Exception as e:
        print(f"Notion 브리핑 Cleanup 에러: {e}")


def process_upload():
    today_str = datetime.now().strftime("%Y%m%d")
    report_file = INTERIM_REPORTS_DIR / f"macro_briefing_{today_str}.md"

    if not report_file.exists():
        print(f"업로드할 브리핑 파일이 없습니다: {report_file}")
        return

    # 오래된 브리핑 먼저 정리
    cleanup_old_briefings()

    # 오늘 브리핑 업로드
    upload_macro_report(report_file)
    print(f"[{datetime.now().isoformat()}] 브리핑 Notion 업로드 프로세스 완료")


if __name__ == "__main__":
    process_upload()
