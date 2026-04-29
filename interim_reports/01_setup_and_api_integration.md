# 중간 보고서: 뉴스 큐레이션 봇 초기 설정 및 News API 연동

## 개요
사용자(교수님)가 제공한 NewsAPI.org API Key를 활용하여 봇의 초기 환경을 구축하고 첫 번째 데이터 수집 테스트를 완료하였습니다.

## 주요 작업 내용
1. **프로젝트 구조 생성**: `primary_data`, `secondary_data`, `interim_reports`, `logs`, `scripts` 디렉토리 구조 셋업
2. **스크립트 초안 작성**:
   - `config.py`: 환경 변수 및 설정 관리 파일 (News API 키 연동)
   - `01_fetch_news.py`: NewsAPI.org `/v2/everything` 엔드포인트를 호출하여 `TARGET_SECTORS` 키워드로 검색
   - `02_filter_summarize.py`: (추후 Gemini API 연동을 위한 초안 작성)
   - `03_update_notion.py`: (추후 Notion 연동을 위한 초안 작성)
   - `00_main_pipeline.py`: 전체 실행 스크립트 작성
3. **패키지 설치 및 테스트**:
   - 필수 패키지(`requests`, `google-generativeai`, `notion-client`) 설치 완료
   - `01_fetch_news.py` 테스트 실행 성공 (100건의 기사 정상 수집 확인)

## 향후 진행 사항
- 사용자가 LLM API Key 및 Notion API Key/Database ID를 제공하면 `02` 및 `03` 스크립트를 실제 API와 연동하고 테스트할 예정입니다.
- 뉴스 요약 로직 및 시스템 프롬프트(학술적 톤 등)를 세부 조정할 예정입니다.
