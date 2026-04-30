import os
import json
import google.generativeai as genai
from config import SECONDARY_DATA_DIR, LLM_API_KEY, get_now_kst

def filter_and_summarize(articles):
    """
    수집된 기사들을 필터링하고 요약합니다.
    """
    if not articles:
        return []

    # Gemini API 설정
    genai.configure(api_key=LLM_API_KEY)
    
    # 모델 설정 (최신 gemini-2.0-flash 사용)
    model = genai.GenerativeModel('gemini-2.0-flash')
    
    summarized_results = []
    
    prompt_template = """
    아래는 수집된 뉴스 기사의 목록입니다. 
    이 중 '경제', '반도체', '세계 경제', '전쟁'과 관련된 중요한 기사만 선택하여 
    핵심 내용을 한국어로 요약해 주세요. 
    
    출력 형식은 JSON 리스트로 해주세요:
    [
        {"title": "기사 제목", "summary": "3줄 이내 요약", "sector": "분류", "url": "원문 링크"},
        ...
    ]
    
    뉴스 기사:
    {articles_text}
    """
    
    # 실제 구현에서는 기사가 많을 경우 나누어서 처리해야 할 수 있습니다.
    # 여기서는 상위 15개 기사만 샘플로 처리합니다.
    sample_articles = articles[:15]
    articles_text = ""
    for idx, art in enumerate(sample_articles):
        articles_text += f"{idx+1}. 제목: {art.get('title')}\n내용: {art.get('description')}\n링크: {art.get('url')}\n\n"
    
    try:
        response = model.generate_content(prompt_template.format(articles_text=articles_text))
        
        # 응답에서 JSON 추출 (마크다운 태그 제거 등)
        text_response = response.text
        if "```json" in text_response:
            text_response = text_response.split("```json")[1].split("```")[0]
        elif "```" in text_response:
            text_response = text_response.split("```")[1].split("```")[0]
            
        summarized_results = json.loads(text_response.strip())
        print(f"[{get_now_kst().isoformat()}] {len(summarized_results)}개의 기사를 요약했습니다.")
        return summarized_results
    except Exception as e:
        print(f"[{get_now_kst().isoformat()}] AI 요약 중 오류 발생: {e}")
        return []

def save_summarized_data(results):
    now = get_now_kst()
    today_str = now.strftime("%Y%m%d")
    filename = SECONDARY_DATA_DIR / f"filtered_news_{today_str}.json"
    
    with open(filename, "w", encoding="utf-8-sig") as f:
        json.dump(results, f, ensure_ascii=False, indent=4)
    print(f"[{now.isoformat()}] 요약 데이터 저장 완료: {filename}")
    return filename

def process_data():
    today_str = get_now_kst().strftime("%Y%m%d")
    from pathlib import Path
    raw_file = Path(__file__).parent.parent / "primary_data" / f"raw_news_{today_str}.json"
    
    if raw_file.exists():
        with open(raw_file, "r", encoding="utf-8-sig") as f:
            articles = json.load(f)
        results = filter_and_summarize(articles)
        save_summarized_data(results)
    else:
        print(f"원본 파일이 없습니다: {raw_file}")

if __name__ == "__main__":
    process_data()
