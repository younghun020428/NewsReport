from notion_client import Client
from config import NOTION_API_KEY, NOTION_DATABASE_ID
import pprint

def debug():
    notion = Client(auth=NOTION_API_KEY)
    
    print("1. Querying database entries...")
    try:
        pages = notion.databases.query(database_id=NOTION_DATABASE_ID, page_size=1)
        if pages['results']:
            props = pages['results'][0]['properties']
            print("\nFound Page Properties:")
            for p in props.keys():
                print(f" - '{p}'")
        else:
            print("No pages found in DB.")
            
        print("\n2. Retrieving database definition...")
        db = notion.databases.retrieve(database_id=NOTION_DATABASE_ID)
        if 'properties' in db:
            print("\nDB Definition Properties:")
            for p in db['properties'].keys():
                print(f" - '{p}'")
        else:
            print("DB definition did not contain 'properties'.")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    debug()
