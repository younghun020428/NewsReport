import os
from pathlib import Path
from datetime import datetime, timezone, timedelta

# --- Directory Settings ---
BASE_DIR = Path(__file__).resolve().parent.parent
PRIMARY_DATA_DIR = BASE_DIR / "primary_data"
SECONDARY_DATA_DIR = BASE_DIR / "secondary_data"
INTERIM_REPORTS_DIR = BASE_DIR / "interim_reports"
LOGS_DIR = BASE_DIR / "logs"

# Ensure directories exist (in case they were deleted)
for _dir in [PRIMARY_DATA_DIR, SECONDARY_DATA_DIR, INTERIM_REPORTS_DIR, LOGS_DIR]:
    _dir.mkdir(parents=True, exist_ok=True)

# --- Timezone Settings ---
KST = timezone(timedelta(hours=9))

def get_now_kst():
    """현재 한국 시간(KST)을 반환합니다."""
    return datetime.now(KST)

# --- API Keys (Secrets에서 가져오며, 기본값 유지) ---
NEWS_API_KEY = os.environ.get("NEWS_API_KEY", "0bf993096a7041d9bf852e78993c6213").strip()
LLM_API_KEY = os.environ.get("LLM_API_KEY", "AIzaSyBHSoLBKrAVNbapyHWWFRZXzaPWDo695b8").strip()
NOTION_API_KEY = os.environ.get("NOTION_API_KEY", "ntn_j16731676731mfrvCc7A78r8Wd5RfbDodyEi2nWZTZl3JT").strip()
NOTION_DATABASE_ID = os.environ.get("NOTION_DATABASE_ID", "1d577291-099e-43c0-a855-1fb90ad6e2b2").strip()
# 브리핑 보고서 전용 페이지: "일일 경제 보고서" 페이지의 하위 페이지로 생성됨
NOTION_BRIEFING_PAGE_ID = os.environ.get("NOTION_BRIEFING_PAGE_ID", "350063ba-8339-8087-a1b5-e72ea54e008a").strip()

# --- Application Settings ---
TARGET_SECTORS = [
    "경제",
    "과학기술(반도체)",
    "세계 경제",
    "전쟁"
]

# Query parameters for News API
NEWS_QUERY_KEYWORD = "경제 OR 반도체 OR 전쟁 OR 세계경제"
