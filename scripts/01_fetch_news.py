import os
import json
import requests
from datetime import datetime
from config import PRIMARY_DATA_DIR, NEWS_API_KEY, NEWS_QUERY_KEYWORD

def fetch_news(query=NEWS_QUERY_KEYWORD, api_key=NEWS_API_KEY):
    """
    뉴스 API를 호출하여 기사 목록을 가져옵니다.
    ※ 주의: 사용자님의 실제 News API(네이버, NewsAPI.org 등)에 맞게 엔드포인트와 파라미터를 수정해야 합니다.
    """
    print(f"[{datetime.now().isoformat()}] 뉴스 수집 시작: 검색어 '{query}'")
    
    url = f"https://newsapi.org/v2/everything?q={query}&apiKey={api_key}&language=ko&sortBy=publishedAt"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        articles = data.get("articles", [])
        print(f"[{datetime.now().isoformat()}] {len(articles)}개의 기사를 수집했습니다.")
        return articles
    except requests.exceptions.RequestException as e:
        print(f"[{datetime.now().isoformat()}] 뉴스 API 호출 중 오류 발생: {e}")
        return []

def save_raw_data(articles):
    today_str = datetime.now().strftime("%Y%m%d")
    filename = PRIMARY_DATA_DIR / f"raw_news_{today_str}.json"
    
    with open(filename, "w", encoding="utf-8-sig") as f:
        json.dump(articles, f, ensure_ascii=False, indent=4)
    print(f"[{datetime.now().isoformat()}] 원본 데이터 저장 완료: {filename}")
    return filename

if __name__ == "__main__":
    articles = fetch_news()
    if articles:
        save_raw_data(articles)
    else:
        print("수집된 뉴스가 없습니다.")
