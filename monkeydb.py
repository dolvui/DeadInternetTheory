import sqlite3
import json
from datetime import datetime

class monkeyDB:
    def __init__(self, path):
        self.conn = sqlite3.connect(path)
        self._create_tables()

    def _create_tables(self):
        c = self.conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS monkeys (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                 prompt TEXT default NULL,
                voix TEXT default NULL,
                isPost BOOLEAN default False,
                description TEXT default NULL,
                videoPath TEXT default NULL
            )
        """)
        self.conn.commit()

    def add_idea_video(self, prompt, voix, description):
        c = self.conn.cursor()
        c.execute("INSERT OR IGNORE INTO monkeys (prompt,voix,description) VALUES (?,?,?)", (prompt, voix, description))
        self.conn.commit()

    def add_genrerate_video(self,id,path):
        c = self.conn.cursor()
        c.execute("UPDATE monkeys SET videoPath = ? WHERE id = ?", (path,id))
        self.conn.commit()

    def get_not_posted_videos(self):
        c = self.conn.cursor()
        c.execute("SELECT * FROM monkeys WHERE videoPath IS NOT NULL")
        return c.fetchone() is not None

    def fill_database_form_json(self,path):
        with open(path , 'r' , encoding='utf-8') as json_file:
            data = json.load(json_file)
            for i in range(0,len(data)):
                idea = data[i]
                self.add_idea_video(idea['prompt'], idea['voix'], idea['description'])