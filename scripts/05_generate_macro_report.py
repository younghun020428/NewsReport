import os
import json
import google.generativeai as genai
from config import SECONDARY_DATA_DIR, LLM_API_KEY, get_now_kst, MODEL_NAME

def generate_macro_report(results):
    """
    요약된 기사들을 바탕으로 거시 경제 브리핑 보고서를 생성합니다.
    """
    if not results:
        print("분석할 뉴스가 없습니다.")
        return ""

    # Gemini API 설정
    genai.configure(api_key=LLM_API_KEY)
    model = genai.GenerativeModel(MODEL_NAME)
    
    # 분석용 텍스트 구성
    context_text = ""
    for idx, item in enumerate(results):
        context_text += f"[{item.get('sector')}] {item.get('title')}\n- 요약: {item.get('summary')}\n\n"
    
    prompt = f"""
    당신은 전문 경제 분석가입니다. 아래 제공된 오늘의 주요 뉴스 요약본을 바탕으로 
    현재의 글로벌 거시 경제 상황을 분석하고 브리핑 보고서를 작성해 주세요.
    
    [오늘의 주요 뉴스 요약]
    {context_text}
    
    [보고서 포함 내용]
    1. 오늘 핵심 요약 (3줄)
    2. 부문별 상세 분석 (경제, 반도체, 세계 정세 등)
    3. 향후 시장 전망 및 주의사항
    4. 투자자 또는 의사결정자를 위한 제언
    
    보고서는 한국어로 전문적이고 신뢰감 있는 톤으로 작성해 주세요. 
    마크다운(Markdown) 형식을 사용하여 가독성 있게 구성해 주세요.
    """
    
    try:
        response = model.generate_content(prompt)
        report_content = response.text
        print(f"[{get_now_kst().isoformat()}] 거시 경제 보고서 생성이 완료되었습니다.")
        return report_content
    except Exception as e:
        print(f"[{get_now_kst().isoformat()}] 보고서 생성 중 오류 발생: {e}")
        return ""

def save_report(content):
    now = get_now_kst()
    today_str = now.strftime("%Y%m%d")
    filename = SECONDARY_DATA_DIR / f"macro_briefing_{today_str}.md"
    
    with open(filename, "w", encoding="utf-8-sig") as f:
        f.write(content)
    print(f"[{now.isoformat()}] 보고서 파일 저장 완료: {filename}")
    return filename

def process_macro_report():
    today_str = get_now_kst().strftime("%Y%m%d")
    from pathlib import Path
    raw_file = Path(__file__).parent.parent / "primary_data" / f"raw_news_{today_str}.json"
    
    if raw_file.exists():
        with open(raw_file, "r", encoding="utf-8-sig") as f:
            data = json.load(f)
        
        # 데이터 구조 파악 (리스트인지 'results' 키가 있는 딕셔너리인지)
        results = []
        if isinstance(data, list):
            results = data
        elif isinstance(data, dict):
            # 1. 알려진 키 확인
            for key in ["results", "articles", "news", "items"]:
                if key in data and isinstance(data[key], list):
                    results = data[key]
                    break
            
            # 2. 키를 못 찾았다면 딕셔너리 내의 첫 번째 리스트를 사용
            if not results:
                for key, value in data.items():
                    if isinstance(value, list):
                        results = value
                        break
                else:
                    # 3. 리스트가 전혀 없다면 단일 딕셔너리를 리스트화
                    results = [data]
        
        if not results:
            print(f"[{get_now_kst().isoformat()}] 분석할 뉴스를 데이터에서 찾을 수 없습니다. (Data keys: {list(data.keys()) if isinstance(data, dict) else 'Not a dict'})")
            return
            
        report = generate_macro_report(results)
        if report:
            save_report(report)
    else:
        print(f"요약 데이터 파일이 없습니다: {filtered_file}")

if __name__ == "__main__":
    process_macro_report()
