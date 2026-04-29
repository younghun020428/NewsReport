# AI Agent & Developer Guidelines: News Curation Bot

이 문서는 GitHub Copilot 또는 다른 AI 코딩 에이전트가 이 프로젝트의 구조와 의도를 이해하고 효율적으로 코딩을 지원할 수 있도록 돕는 가이드라인입니다.

## 1. 프로젝트 개요 (Project Overview)
- **목표**: 경제, 반도체, 세계 경제, 전쟁 등 특정 섹션의 뉴스를 수집하고, Gemini AI를 통해 요약한 뒤 노션(Notion) 데이터베이스에 자동 업데이트 및 일일 보고서를 생성하는 봇입니다.
- **주요 기술 스택**: Python 3.10+, Google Gemini API (google-generativeai), Notion API (notion-client), GitHub Actions.

## 2. 프로젝트 구조 (Project Structure)
AI 에이전트는 다음 디렉토리 구조를 준수해야 합니다.

- `scripts/`: 핵심 로직이 담긴 파이썬 스크립트
    - `00_main_pipeline.py`: 전체 프로세스를 제어하는 메인 실행 파일
    - `01_fetch_news.py`: 뉴스 API를 통해 원시 데이터 수집
    - `02_filter_summarize.py`: Gemini AI를 사용한 필터링 및 요약
    - `03_update_notion.py`: 노션 데이터베이스 업데이트
    - `05_generate_macro_report.py`: 뉴스 데이터를 기반으로 거시경제 보고서 생성
    - `config.py`: 모든 설정 및 환경 변수 관리
- `.github/workflows/`: 클라우드 자동 실행을 위한 CI/CD 설정
- `primary_data/`, `secondary_data/`: 데이터 처리를 위한 중간 저장소

## 3. 핵심 아키텍처 및 흐름 (Architecture & Flow)
AI가 코드를 수정할 때 다음 순서를 이해해야 합니다.
1. **데이터 수집**: `01_fetch_news.py`가 외부 API에서 뉴스를 가져와 `primary_data/`에 저장.
2. **AI 분석**: `02_filter_summarize.py`가 수집된 뉴스를 읽어 중요도를 판별하고 요약본 생성.
3. **노션 반영**: 요약된 내용을 `03_update_notion.py`를 통해 노션 DB의 각 섹션에 업로드.
4. **보고서 생성**: 전체 뉴스 맥락을 종합하여 `05_generate_macro_report.py`가 심층 분석 보고서 작성 및 노션 페이지 업데이트.

## 4. 환경 변수 및 보안 (Environment Variables)
모든 API 키는 직접 하드코딩하지 않고 `scripts/config.py`를 통해 환경 변수(`os.environ`)에서 읽어옵니다. 새로운 기능을 추가할 때도 이 방식을 유지해야 합니다.
- `NEWS_API_KEY`, `LLM_API_KEY`, `NOTION_API_KEY`, `NOTION_DATABASE_ID`, `NOTION_BRIEFING_PAGE_ID`

## 5. 코딩 스타일 및 규칙 (Coding Rules for AI)
1. **모듈화**: 각 단계는 독립적인 스크립트로 유지하며, 메인 파이프라인에서 호출하는 구조를 유지합니다.
2. **에러 핸들링**: 네트워크 요청이나 API 호출 실패 시 적절한 Logging을 남기고, 전체 프로세스가 중단되지 않도록 예외 처리를 수행합니다.
3. **경로 관리**: 모든 파일 경로는 `config.py`에 정의된 `BASE_DIR`을 기준으로 하는 상대 경로를 사용합니다.
4. **주석**: 복잡한 로직이나 API 인터페이스에는 반드시 한글 주석을 포함합니다.

## 6. 유지보수 및 확장 (Maintenance & Extension)
- **섹션 추가**: `config.py`의 `TARGET_SECTORS` 리스트를 수정하여 수집 대상을 확장할 수 있습니다.
- **클라우드 실행**: `.github/workflows/daily_report.yml`에 정의된 스케줄에 따라 실행되므로, 실행 환경 의존성(requirements.txt) 관리에 주의해야 합니다.
