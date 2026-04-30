import os
from notion_client import Client
from config import NOTION_API_KEY, NOTION_BRIEFING_PAGE_ID, get_now_kst

def markdown_to_notion_blocks(markdown_text):
    """
    간단한 마크다운 텍스트를 노션 블록으로 변환합니다.
    (실제로는 더 복잡한 파서가 필요할 수 있으나, 여기서는 기본적인 단락 처리를 수행합니다.)
    """
    blocks = []
    lines = markdown_text.split('\n')
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        if line.startswith('# '):
            blocks.append({"object": "block", "type": "heading_1", "heading_1": {"rich_text": [{"text": {"content": line[2:]}}]}})
        elif line.startswith('## '):
            blocks.append({"object": "block", "type": "heading_2", "heading_2": {"rich_text": [{"text": {"content": line[3:]}}]}})
        elif line.startswith('### '):
            blocks.append({"object": "block", "type": "heading_3", "heading_3": {"rich_text": [{"text": {"content": line[4:]}}]}})
        elif line.startswith('- ') or line.startswith('* '):
            blocks.append({"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"text": {"content": line[2:]}}]}})
        else:
            blocks.append({"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": line}}]}})
            
    return blocks

def upload_report_to_notion(report_content):
    """
    생성된 보고서를 노션 페이지의 하위 페이지로 업로드합니다.
    """
    if not report_content:
        return

    notion = Client(auth=NOTION_API_KEY)
    now = get_now_kst()
    today_str = now.strftime("%Y년 %m월 %d일")
    
    try:
        # 하위 페이지 생성 (데이터베이스 내에 생성)
        new_page = notion.pages.create(
            parent={"database_id": NOTION_BRIEFING_PAGE_ID},
            properties={
                "페이지": {"title": [{"text": {"content": f"{today_str} 경제 브리핑 보고서"}}]}
            }
        )
        
        # 페이지 내용(블록) 추가
        blocks = markdown_to_notion_blocks(report_content)
        # 노션 API는 한 번에 최대 100개의 블록까지 허용하므로 청크로 나누어 추가
        for i in range(0, len(blocks), 100):
            notion.blocks.children.append(
                block_id=new_page["id"],
                children=blocks[i:i+100]
            )
            
        print(f"[{get_now_kst().isoformat()}] 노션 보고서 업로드 완료: {new_page['url']}")
    except Exception as e:
        print(f"[{get_now_kst().isoformat()}] 노션 보고서 업로드 중 오류 발생: {e}")

def process_upload():
    today_str = get_now_kst().strftime("%Y%m%d")
    from pathlib import Path
    report_file = Path(__file__).parent.parent / "secondary_data" / f"macro_briefing_{today_str}.md"
    
    if report_file.exists():
        with open(report_file, "r", encoding="utf-8-sig") as f:
            content = f.read()
        upload_report_to_notion(content)
    else:
        print(f"보고서 파일이 없습니다: {report_file}")

if __name__ == "__main__":
    process_upload()
