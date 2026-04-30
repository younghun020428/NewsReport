import os
import json
from google import genai
from google.genai import types
from config import PRIMARY_DATA_DIR, INTERIM_REPORTS_DIR, SECONDARY_DATA_DIR, LLM_API_KEY, get_now_kst


def generate_macro_report(articles):
    """
    뉴스 기사들을 기반으로 거시경제·시장 브리핑 보고서를 생성합니다.
    Google Search Grounding을 활성화하여 최신 정보를 보강합니다.
    """
    now = get_now_kst()
    print(f"[{now.isoformat()}] 매크로 브리핑 보고서 생성 시작")

    client = genai.Client(api_key=LLM_API_KEY)

    # 기사 제목과 요약을 모아서 컨텍스트 생성 (상위 50개 제한)
    context_lines = []
    for article in articles[:50]:
        title = article.get("title", "")
        desc = article.get("description", "")
        if title:
            context_lines.append(f"제목: {title}\n요약: {desc}")

    context_text = "\n\n".join(context_lines)

    prompt = f"""
당신은 "투자 판단 보조 분석가"입니다.
제공된 뉴스 기사 컨텍스트와 Google Search로 검색한 최신 정보를 바탕으로 오늘 기준의 거시경제·시장 브리핑 보고서를 작성하십시오.

중요 원칙:
- 반드시 제공된 최신 정보와 당신이 아는 최신 정보를 조합하여 작성하라.
- "무슨 일이 있었는지"보다 "왜 발생했고, 시장에 어떤 경로로 연결되는지"를 중점적으로 설명하라.
- 확정적 예언은 금지하며, 조건부 시나리오로 제시하라.
- 객관적이고 건조한 학술적 톤을 유지하고, 숫자와 단위(% 등) 사이는 한 칸 띄어 써라.

다음 형식을 정확히 지켜 마크다운으로 출력하라:

# 오늘의 거시경제·시장 브리핑

## 1. 핵심 한줄 요약
- 

## 2. 글로벌 거시경제 상황
- 미국:
- 중국:
- 유럽:
- 한국:

## 3. 금융시장 흐름
- 미국 증시:
- 한국 증시:
- 금리:
- 환율:
- 원자재:
- 주요 섹터:

## 4. 오늘 시장을 움직인 핵심 인과관계
- 

## 5. 투자 판단 시나리오
### 시나리오 A: 
### 시나리오 B: 
### 시나리오 C: 

## 6. 투자자가 오늘 체크할 포인트
- 

## 7. 결론
- 

## 8. 출처
- 종합된 뉴스 컨텍스트 및 시장 데이터

---
[제공된 최신 뉴스 컨텍스트]
{context_text}
"""

    try:
        # 모델명을 안정적인 2.0-flash로 수정
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                tools=[types.Tool(google_search=types.GoogleSearch())],
            )
        )
        result = response.text.strip()
        print(f"[{get_now_kst().isoformat()}] 매크로 브리핑 보고서 생성 완료 (Google Search Grounding 활성화)")
        return result
    except Exception as e:
        print(f"매크로 브리핑 생성 중 LLM API 호출 에러: {e}")
        return "# 오늘의 거시경제·시장 브리핑\n\n(생성 실패)"


def extract_report_keywords(client, report_markdown):
    """
    생성된 보고서에서 오늘의 핵심 키워드 10개를 추출합니다.
    """
    now = get_now_kst()
    print(f"[{now.isoformat()}] 보고서 핵심 키워드 추출 시작")

    keyword_prompt = f"""
다음 거시경제 브리핑 보고서에서 오늘 시장에서 가장 중요한 핵심 키워드를 10개 추출하라.
키워드는 특정 기업명, 지표명, 국가명, 정책 이름, 원자재명 등 구체적인 명사여야 한다.
반드시 JSON 배열 형식으로만 반환하라. 예: ["연준", "TSMC", "원달러환율", "반도체", "금리인하"]

보고서 내용:
{report_markdown[:3000]}
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=keyword_prompt,
        )
        result = response.text.strip()
        if result.startswith("```json"):
            result = result[7:].rstrip("```").strip()
        elif result.startswith("```"):
            result = result[3:].rstrip("```").strip()
        keywords = json.loads(result)
        print(f"[{get_now_kst().isoformat()}] 키워드 추출 완료: {keywords}")
        return keywords
    except Exception as e:
        print(f"키워드 추출 중 에러 (기본값 사용): {e}")
        return []


def process_macro_report():
    now = get_now_kst()
    today_str = now.strftime("%Y%m%d")
    input_file = PRIMARY_DATA_DIR / f"raw_news_{today_str}.json"
    output_file = INTERIM_REPORTS_DIR / f"macro_briefing_{today_str}.md"

    if not input_file.exists():
        print(f"입력 파일이 없습니다: {input_file}")
        return None

    with open(input_file, "r", encoding="utf-8-sig") as f:
        articles = json.load(f)

    client = genai.Client(api_key=LLM_API_KEY)
    report_markdown = generate_macro_report(articles)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(report_markdown)

    print(f"[{get_now_kst().isoformat()}] 매크로 브리핑 파일 저장 완료: {output_file}")

    keywords = extract_report_keywords(client, report_markdown)
    keywords_file = SECONDARY_DATA_DIR / f"report_keywords_{today_str}.json"
    with open(keywords_file, "w", encoding="utf-8-sig") as f:
        json.dump(keywords, f, ensure_ascii=False, indent=2)
    print(f"[{get_now_kst().isoformat()}] 키워드 파일 저장 완료: {keywords_file}")

    return output_file


if __name__ == "__main__":
    process_macro_report()
