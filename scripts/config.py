import os
from pathlib import Path

# --- Directory Settings ---
BASE_DIR = Path(__file__).resolve().parent.parent
PRIMARY_DATA_DIR = BASE_DIR / "primary_data"
SECONDARY_DATA_DIR = BASE_DIR / "secondary_data"
INTERIM_REPORTS_DIR = BASE_DIR / "interim_reports"
LOGS_DIR = BASE_DIR / "logs"

for _dir in [PRIMARY_DATA_DIR, SECONDARY_DATA_DIR, INTERIM_REPORTS_DIR, LOGS_DIR]:
    _dir.mkdir(parents=True, exist_ok=True)

# --- API Keys (Secrets에서 가져오며, 줄바꿈/공백 자동 제거) ---
NEWS_API_KEY = os.environ.get("NEWS_API_KEY", "").strip()
LLM_API_KEY = os.environ.get("LLM_API_KEY", "").strip()
NOTION_API_KEY = os.environ.get("NOTION_API_KEY", "").strip()
NOTION_DATABASE_ID = os.environ.get("NOTION_DATABASE_ID", "").strip()
NOTION_BRIEFING_PAGE_ID = os.environ.get("NOTION_BRIEFING_PAGE_ID", "").strip()

# --- Application Settings ---
TARGET_SECTORS = ["경제", "과학기술(반도체)", "세계 경제", "전쟁"]
NEWS_QUERY_KEYWORD = "경제 OR 반도체 OR 전쟁 OR 세계경제"
