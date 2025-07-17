import sqlite3
import json

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
                videoPath TEXT default NULL,
                sound_design TEXT default NULL
            )
        """)

        c.execute("""
                  CREATE TABLE IF NOT EXISTS account
                  (
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      session_path TEXT UNIQUE,
                      credit INTEGER default 0
                  )
                  """)

        self.conn.commit()

    def add_idea_video(self, prompt, voix, sound,description):
        c = self.conn.cursor()
        c.execute("INSERT OR IGNORE INTO monkeys (prompt,voix,sound_design,description) VALUES (?,?,?,?)", (prompt, voix,sound, description))
        self.conn.commit()

    def add_genrerate_video(self,id,path):
        c = self.conn.cursor()
        c.execute("UPDATE monkeys SET videoPath = ? WHERE id = ?", (path,id))
        self.conn.commit()

    def get_generate_video(self):
        c = self.conn.cursor()
        c.execute("SELECT * FROM monkeys WHERE videoPath IS NOT NULL AND isPost IS FALSE")
        return c.fetchone()

    def get_not_generate_video(self):
        c = self.conn.cursor()
        c.execute("SELECT * FROM monkeys WHERE videoPath IS NULL")
        return c.fetchone()

    def fill_database_form_json(self,path):
        with open(path , 'r' , encoding='utf-8') as json_file:
            data = json.load(json_file)
            for i in range(0,len(data)):
                idea = data[i]
                self.add_idea_video(idea['prompt'], idea['voice'], idea['sound_ambience'],idea['description'])

    def update_or_create_account(self,session_path,credit):
        c = self.conn.cursor()
        c.execute("INSERT INTO account (session_path, credit) VALUES (?, ?) ON CONFLICT(session_path) DO UPDATE SET credit = excluded.credit;",(session_path,credit))
        self.conn.commit()

    def find_sufficient_account(self,needed_credit):
        c = self.conn.cursor()
        c.execute("SELECT session_path FROM account where credit >= ?",(needed_credit,))
        return [str(row[0]) for row in c.fetchall()]

    def mark_video_as_posted(self,video_id):
        c = self.conn.cursor()
        c.execute("UPDATE monkeys SET isPost = TRUE WHERE id = ?", (video_id,))
        self.conn.commit()

    def set_video_path(self,video_path,video_id):
        c = self.conn.cursor()
        c.execute("UPDATE monkeys SET videoPath = ? WHERE id = ?", (video_path,video_id))
        self.conn.commit()

    def update_account_credit(self,account,price):
        c = self.conn.cursor()
