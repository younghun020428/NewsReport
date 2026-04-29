import sys
from pathlib import Path
import importlib

# Add current directory to path to ensure modules can be imported
sys.path.append(str(Path(__file__).parent))

fetch_news_module = importlib.import_module("01_fetch_news")
filter_module = importlib.import_module("02_filter_summarize")
update_notion_module = importlib.import_module("03_update_notion")
cleanup_module = importlib.import_module("04_cleanup_notion")

import psutil

def check_battery_status():
    battery = psutil.sensors_battery()
    if battery is None:
        return True, "배터리 정보를 확인할 수 없습니다. (데스크탑 등)"
    
    percent = battery.percent
    power_plugged = battery.power_plugged
    
    if power_plugged:
        return True, f"전원이 연결되어 있습니다. (배터리: {percent} %)"
    
    if percent >= 70:
        return True, f"배터리 잔량이 충분합니다. ({percent} %)"
    
    return False, f"배터리 잔량이 부족하여 실행을 스킵합니다. (현재: {percent} %, 기준: 70 %)"

def run_pipeline():
    print("=== 뉴스 큐레이션 및 알림 파이프라인 시작 ===")
    
    # 배터리 체크
    can_run, message = check_battery_status()
    print(f"상태 확인: {message}")
    if not can_run:
        print("파이프라인 실행 조건을 만족하지 않습니다.")
        return

    articles = fetch_news_module.fetch_news()
    if not articles:
        print("수집된 뉴스가 없어 파이프라인을 종료합니다.")
        return
    fetch_news_module.save_raw_data(articles)
    
    # 2. Generate Macro Report (보고서 생성 및 키워드 추출)
    # 02번 필터링 단계에서 보고서 키워드를 사용하기 위해 순서를 앞으로 당김
    generate_macro_module = importlib.import_module("05_generate_macro_report")
    generate_macro_module.process_macro_report()
    
    # 3. Filter and Summarize (보고서 키워드 기반 필터링)
    filter_module.process_data()
    
    # 4. Update Notion (개별 뉴스 - 키워드 포함)
    update_notion_module.upload_data()
    
    # 5. Cleanup Old Articles
    cleanup_module.cleanup_old_articles()
    
    # 6. Upload Macro Report to Notion
    upload_macro_module = importlib.import_module("06_upload_report_to_notion")
    upload_macro_module.process_upload()
    
    print("=== 뉴스 큐레이션 및 알림 파이프라인 완료 ===")

if __name__ == "__main__":
    run_pipeline()
