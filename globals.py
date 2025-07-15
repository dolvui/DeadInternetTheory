import json

import monkeydb

SESSIONS_PATH = None
db = None

def init(sessions_file):
    global SESSIONS_PATH
    with open(sessions_file, 'r', encoding='utf-8') as json_file:
        SESSIONS_PATH = json.load(json_file)
    global db
    db = monkeydb.monkeyDB(SESSIONS_PATH["database"])