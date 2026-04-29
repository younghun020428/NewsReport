import os
from notion_client import Client

notion = Client(auth="ntn_j16731676731mfrvCc7A78r8Wd5RfbDodyEi2nWZTZl3JT")
db_id = "350063ba-8339-8185-9ec8-000bb36262dd"

db = notion.databases.retrieve(database_id="1d577291-099e-43c0-a855-1fb90ad6e2b2")
import pprint
pprint.pprint(db)
