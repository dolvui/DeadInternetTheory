import sqlite3
import json
from datetime import datetime

class VideoDB:
    def __init__(self, path="videos.db"):
        self.conn = sqlite3.connect(path)
        self._create_tables()

    def _create_tables(self):
        c = self.conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                scraped_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        c.execute("""
            CREATE TABLE IF NOT EXISTS videos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                --user_id INTEGER,
                video_url TEXT UNIQUE,
                file_path TEXT,
                downloaded_at TEXT DEFAULT CURRENT_TIMESTAMP,
                metadata TEXT,
                isPosted BOOLEAN DEFAULT FALSE
                --FOREIGN KEY(user_id) REFERENCES users(id)
            )
        """)
        self.conn.commit()

    def add_user(self, username):
        c = self.conn.cursor()
        c.execute("INSERT OR IGNORE INTO users (username,scraped_at) VALUES (?,NULL)", (username,))
        self.conn.commit()

    def video_exists(self, video_url):
        c = self.conn.cursor()
        c.execute("SELECT id FROM videos WHERE video_url = ?", (video_url,))
        return c.fetchone() is not None

    def add_video(self, url, path, metadata=None):
        c = self.conn.cursor()
        c.execute("""
            INSERT OR IGNORE INTO videos (video_url, file_path, metadata,downloaded_at)
            VALUES (?, ?, ?, FALSE)
        """, (url, path, json.dumps(metadata)))
        self.conn.commit()

    def get_all_users(self):
        c = self.conn.cursor()
        c.execute("SELECT username,scraped_at FROM users")
        return [row for row in c.fetchall()]

    def get_not_scraped_users(self):
        c = self.conn.cursor()
        c.execute('SELECT username,scraped_at FROM users where scraped_at is NULL')
        #c.execute("UPDATE users SET scraped_at = NULL")
        #self.conn.commit()
        return [str(row[0]) for row in c.fetchall()]

    def user_get_scrap(self,username):
        c = self.conn.cursor()
        c.execute('UPDATE users SET scraped_at = CURRENT_TIMESTAMP WHERE username = ?', (username,))

    def user_done(self,username):
        c = self.conn.cursor()
        c.execute("UPDATE users SET scraped_at = CURRENT_TIMESTAMP WHERE username = ?", (username,))
        self.conn.commit()

    def users_done(self,usernames):
        for username in usernames:
            self.user_done(username)

    def get_videos(self):
        c = self.conn.cursor()
        c.execute("SELECT * FROM videos")
        return [row for row in c.fetchall()]

    def get_videos_not_publish(self):
        c = self.conn.cursor()
        c.execute("SELECT id,file_path,isPosted FROM videos WHERE isPosted IS FALSE")
        return [row for row in c.fetchall()]

    def mark_video_posted(self,video_id):
        c = self.conn.cursor()
        c.execute("UPDATE videos SET isPosted = TRUE WHERE id = ?",(video_id,))
        self.conn.commit()

    def bite(self):
        c = self.conn.cursor()

        c.execute("DROP TABLE IF EXISTS videos;")
        self.conn.commit()