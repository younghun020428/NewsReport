import os
import json
import requests
from datetime import datetime
from google import genai
from config import NOTION_API_KEY, NOTION_BRIEFING_PAGE_ID, LLM_API_KEY, SECONDARY_DATA_DIR

def fetch_today_report_and_extract_keywords():
    print(f"[{datetime.now().isoformat()}] Notion에서 오늘자 보고서 읽기 시작")
    
    headers = {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }
    
    today_str = datetime.now().strftime("%Y-%m-%d")
    target_title = f"[거시경제 브리핑] {today_str}"
    
    # 1. 하위 페이지 목록 조회
    url = f"https://api.notion.com/v1/blocks/{NOTION_BRIEFING_PAGE_ID}/children"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    children = response.json().get("results", [])
    
    report_page_id = None
    for child in children:
        if child.get("type") == "child_page":
            if child["child_page"]["title"] == target_title:
                report_page_id = child["id"]
                break
    
    if not report_page_id:
        print(f"오늘자 보고서를 찾을 수 없습니다: {target_title}")
        return
        
    print(f"보고서 페이지 발견: {report_page_id}")
    
    # 2. 페이지 내용(블록) 가져오기
    url = f"https://api.notion.com/v1/blocks/{report_page_id}/children"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    blocks = response.json().get("results", [])
    
    text_content = []
    for block in blocks:
        block_type = block.get("type")
        if block_type in ["paragraph", "heading_1", "heading_2", "heading_3"]:
            rich_text = block[block_type].get("rich_text", [])
            for rt in rich_text:
                text_content.append(rt.get("plain_text", ""))
                
    full_text = "\n".join(text_content)
    print(f"보고서 텍스트 추출 완료 ({len(full_text)}자)")
    
    # 3. 키워드 추출 (gemini-2.0-flash-exp 또는 working model)
    client = genai.Client(api_key=LLM_API_KEY)
    
    keyword_prompt = f"""
다음 거시경제 브리핑 보고서에서 오늘 시장에서 가장 중요한 핵심 키워드를 10개 추출하라.
키워드는 특정 기업명, 지표명, 국가명, 정책 이름, 원자재명 등 구체적인 명사여야 한다.
반드시 JSON 배열 형식으로만 반환하라. 예: ["연준", "TSMC", "원달러환율", "반도체", "금리인하"]

보고서 내용:
{full_text[:4000]}
"""

    try:
        # 이전에 작동했던 gemini-2.5-flash 시도 (실제로는 flash-latest 계열일 가능성 높음)
        response = client.models.generate_content(
            model="gemini-2.5-flash", 
            contents=keyword_prompt,
        )
        result = response.text.strip()
        if result.startswith("```json"):
            result = result[7:].rstrip("```").strip()
        elif result.startswith("```"):
            result = result[3:].rstrip("```").strip()
        keywords = json.loads(result)
        
        today_file_str = datetime.now().strftime("%Y%m%d")
        keywords_file = SECONDARY_DATA_DIR / f"report_keywords_{today_file_str}.json"
        with open(keywords_file, "w", encoding="utf-8-sig") as f:
            json.dump(keywords, f, ensure_ascii=False, indent=2)
            
        print(f"키워드 추출 및 저장 완료: {keywords}")
        return True
    except Exception as e:
        print(f"키워드 추출 실패: {e}")
        return False

if __name__ == "__main__":
    fetch_today_report_and_extract_keywords()
