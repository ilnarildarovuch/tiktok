import sqlite3
import random
from contextlib import contextmanager

class Databaser:
    def __init__(self, db_name='database.db'):
        self.db_name = db_name
        self._create_table()

    @contextmanager
    def get_connection(self):
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()

    def _create_table(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS videos (
                                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                desc TEXT,
                                likes INT,
                                author_name TEXT)''')
            conn.commit()

    def get_random_video(self, history=None):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if history:
                cursor.execute('''
                    SELECT * FROM videos 
                    WHERE id NOT IN ({})
                    ORDER BY RANDOM() 
                    LIMIT 1
                '''.format(','.join(['?']*len(history))), history)
            else:
                cursor.execute('SELECT * FROM videos ORDER BY RANDOM() LIMIT 1')
            video = cursor.fetchone()
            return dict(video) if video else None

    def add_video(self, desc, author_name, video_id=None):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if video_id is None:
                cursor.execute('''INSERT INTO videos (desc, likes, author_name) 
                VALUES (?, 0, ?)''', (desc, author_name))
            else:
                cursor.execute('''INSERT OR REPLACE INTO videos (id, desc, likes, author_name)
                VALUES (?, ?, 0, ?)
                ''', (video_id, desc, author_name))
            conn.commit()

    def get_video(self, video_id):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM videos WHERE id = ?', (video_id,))
            r = cursor.fetchone()
            return dict(r) if r else None

    def change_video(self, video_id, desc=None, author_name=None):
        with self.connection:
            cursor = self.connection.cursor()
        
            old = self.get_video(video_id)

            if desc is None:
                desc = old['desc']
            if author_name is None:
                author_name = old['author_name']

            cursor.execute('UPDATE videos SET desc = ?, author_name = ? WHERE id = ?', (desc, author_name, video_id))
            self.connection.commit()

    def like_video(self, video_id):
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute('UPDATE videos SET likes = likes + 1 WHERE id = ?', (video_id,))

    def get_videos(self):
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute('SELECT * FROM videos ORDER BY likes')
            videos = cursor.fetchall()

            videos = list(map(dict, videos))

            return videos
    
    def get_random_video(self, history=None):
        with self.connection:
            if history is None:
                history = []

            cursor = self.connection.cursor()
            cursor.execute('SELECT Count(*) FROM videos')
            mx = cursor.fetchone()['Count(*)']

            rng = set(range(1, mx + 1)) - set(history)

            if not rng:
                return None

            print(rng, list(history))

            video_id = random.choice(list(rng))

            return self.get_video(video_id)


if __name__ == '__main__':
    db = Databaser()
    db.add_video('env', 'eleday', 3)
    db.add_video('hello world', 'eleday', 4)
    db.add_video('Скачать картинку', 'eleday', 5)
    db.add_video('Matplotlib', 'eleday', 6)
    db.add_video('qr', 'eleday', 7)
    db.add_video('Скриншот', 'eleday', 8)
    db.add_video('sqlite', 'eleday', 9)
    db.add_video('excel', 'eleday', 10)
