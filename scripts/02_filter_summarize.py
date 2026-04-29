import os
import json
import google.generativeai as genai
from datetime import datetime
from config import PRIMARY_DATA_DIR, SECONDARY_DATA_DIR, LLM_API_KEY, TARGET_SECTORS


def load_report_keywords():
    """
    당일 거시경제 보고서에서 추출된 핵심 키워드를 로드합니다.
    파일이 없으면 빈 리스트를 반환합니다 (fallback: 기존 섹터 기반 필터 유지).
    """
    today_str = datetime.now().strftime("%Y%m%d")
    keywords_file = SECONDARY_DATA_DIR / f"report_keywords_{today_str}.json"
    if keywords_file.exists():
        with open(keywords_file, "r", encoding="utf-8-sig") as f:
            keywords = json.load(f)
        print(f"[{datetime.now().isoformat()}] 보고서 키워드 로드 성공 ({len(keywords)}개): {keywords}")
        return keywords
    else:
        print(f"[{datetime.now().isoformat()}] 보고서 키워드 파일 없음 → 섹터 기반 필터링으로 진행 ({keywords_file})")
        return []

def setup_llm():
    if LLM_API_KEY != "YOUR_LLM_API_KEY":
        genai.configure(api_key=LLM_API_KEY)
        return True
    return False

def filter_and_summarize(articles, report_keywords=None):
    """
    LLM을 사용하여 기사들을 필터링하고 요약합니다.
    report_keywords가 주어질 경우, 보고서와 연관된 기사를 우선 선별합니다.
    """
    print(f"[{datetime.now().isoformat()}] 필터링 및 요약 프로세스 시작 (총 {len(articles)}개 기사)")
    if report_keywords:
        print(f"  → 보고서 키워드 적용: {report_keywords}")
    
    filtered_articles = []
    has_api = setup_llm()
    
    if has_api:
        model = genai.GenerativeModel('gemini-2.5-flash')
    
    # 최소 10개의 기사를 수집할 때까지 반복
    for article in articles:
        if len(filtered_articles) >= 10:
            break
            
        title = article.get("title", "")
        description = article.get("description", "")

        # 보고서 키워드 힌트 구성
        if report_keywords:
            keyword_hint = (
                f"\n\n특히 오늘 거시경제 보고서의 핵심 키워드는 다음과 같다: {', '.join(report_keywords)}\n"
                "위 키워드와 직접 연관된 기사라면 relevant=true로 판단하라. "
                "연관 키워드가 있으면 matched_keywords 필드에 해당 키워드 목록(JSON 배열)을 포함하라."
            )
            return_format = (
                '{"relevant": true, "sector": "관련_섹터명", '
                '"summary": "3~4줄 요약문", "matched_keywords": ["키워드1", "키워드2"]}'
            )
        else:
            keyword_hint = ""
            return_format = '{"relevant": true, "sector": "관련_섹터명", "summary": "3~4줄 요약문"}'

        prompt = f"""
        다음 기사가 {', '.join(TARGET_SECTORS)}와(과) 같은 산업 섹터에 실질적인 영향을 미치는 핵심 기사인지 평가하십시오.{keyword_hint}
        관련이 없다면 JSON 형태로 {{"relevant": false}} 만 반환하십시오.
        관련이 있다면, JSON 형태로 {return_format} 을 반환하십시오.
        요약문은 객관적이고 건조한 학술적 톤으로 작성하십시오. (기호는 이탤릭체, 단위는 직립체, 숫자와 단위 사이 띄어쓰기 등 규정 준수)
        반드시 JSON 문자열만 반환하십시오.
        
        기사 제목: {title}
        본문/요약: {description}
        """
        
        if has_api:
            try:
                response = model.generate_content(prompt)
                result = response.text.strip()
                if result.startswith("```json"):
                    result = result[7:-3].strip()
                elif result.startswith("```"):
                    result = result[3:-3].strip()
                
                parsed = json.loads(result)
                if parsed.get("relevant"):
                    article["summary"] = parsed.get("summary", "")
                    article["sector"] = parsed.get("sector", "기타")
                    article["matched_keywords"] = parsed.get("matched_keywords", [])
                    filtered_articles.append(article)

            except Exception as e:
                print(f"LLM API 호출 에러: {e}")
            
            # Rate limit 방지 (15 RPM 제한 고려, 4.5초 대기)
            import time
            time.sleep(4.5)
        else:
            # Mock 로직: 제목에 타겟 섹터 키워드가 있으면 통과
            is_relevant = any(sector in title for sector in TARGET_SECTORS)
            if is_relevant:
                article["summary"] = f"(모의 요약) 이 기사는 {title}에 대한 내용을 담고 있으며, 산업 전반에 긍정적 영향을 미칠 것으로 예상됩니다."
                filtered_articles.append(article)
                
    return filtered_articles

def process_data():
    today_str = datetime.now().strftime("%Y%m%d")
    input_file = PRIMARY_DATA_DIR / f"raw_news_{today_str}.json"
    output_file = SECONDARY_DATA_DIR / f"filtered_news_{today_str}.json"
    
    if not input_file.exists():
        print(f"입력 파일이 없습니다: {input_file}")
        return None
        
    with open(input_file, "r", encoding="utf-8-sig") as f:
        articles = json.load(f)

    # 당일 보고서 키워드 로드 (없으면 빈 리스트 → 기존 필터 방식)
    report_keywords = load_report_keywords()
    filtered_articles = filter_and_summarize(articles, report_keywords=report_keywords)
    
    with open(output_file, "w", encoding="utf-8-sig") as f:
        json.dump(filtered_articles, f, ensure_ascii=False, indent=4)
        
    print(f"[{datetime.now().isoformat()}] 필터링 및 요약 완료 (저장된 기사 {len(filtered_articles)}개): {output_file}")
    return output_file

if __name__ == "__main__":
    process_data()
