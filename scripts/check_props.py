from notion_client import Client
from config import NOTION_API_KEY, NOTION_DATABASE_ID
import pprint

def check_props():
    notion = Client(auth=NOTION_API_KEY)
    try:
        db = notion.databases.retrieve(database_id=NOTION_DATABASE_ID)
        print("--- Database Properties ---")
        pprint.pprint(list(db.get("properties", {}).keys()))
        if "보고서_키워드" in db.get("properties", {}):
            print("\n성공: '보고서_키워드' 속성을 찾았습니다!")
            return True
        else:
            print("\n실패: '보고서_키워드' 속성이 아직 없습니다.")
            return False
    except Exception as e:
        print(f"에러 발생: {e}")
        return False

if __name__ == "__main__":
    check_props()
