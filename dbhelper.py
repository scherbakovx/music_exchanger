import sqlite3
import datetime
from typing import Optional


class DBHelper:

    def __init__(self, dbname="music_exchanger.sqlite") -> None:
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname, check_same_thread=False)

    def setup(self) -> None:
        stmt = "CREATE TABLE IF NOT EXISTS playlist_urls (url TEXT, user_id INT, added TEXT)"
        self.conn.execute(stmt)
        self.conn.commit()

        stmt = """
        CREATE TABLE IF NOT EXISTS requested_playlist_urls (url TEXT, user_id INT, requested TEXT, message_id INT)
        """
        self.conn.execute(stmt)
        self.conn.commit()

    def check_if_user_could_get_playlist_url(self, user_id: int) -> bool:
        current_datetime = datetime.datetime.now().strftime('%Y-%m-%d')
        stmt = "SELECT COUNT(*) FROM requested_playlist_urls WHERE user_id == %d AND DATE(requested) >= '%s'" % (
            user_id,
            current_datetime
        )
        for row in self.conn.execute(stmt):
            if row[0] > 0:
                return False
        return True

    def check_if_user_could_add_playlist_url(self, user_id: int) -> bool:
        current_datetime = datetime.datetime.now().strftime('%Y-%m-%d')
        stmt = "SELECT COUNT(*) FROM playlist_urls WHERE user_id == %d AND DATE(added) >= '%s'" % (
            user_id,
            current_datetime
        )
        for row in self.conn.execute(stmt):
            if row[0] > 0:
                return False
        return True

    def add_playlist_url_from_user(self, playlist_url: str, user_id: int) -> None:
        current_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        stmt = "INSERT INTO playlist_urls (url, user_id, added) VALUES ('%s', %d, '%s')" % (
            playlist_url, user_id, current_datetime
        )
        self.conn.execute(stmt)
        self.conn.commit()

    def get_random_playlist_url_for_user(self, user_id: int) -> Optional[str]:
        stmt = "SELECT url FROM playlist_urls WHERE user_id != %d ORDER BY RANDOM() LIMIT 1;" % user_id
        for row in self.conn.execute(stmt):
            return row[0]
        return None

    def add_info_about_requested_url(self, playlist_url: str, user_id: int, message_id: int) -> None:
        current_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        stmt = "INSERT INTO requested_playlist_urls (url, user_id, requested, message_id) VALUES ('%s', %d, '%s', '%d')" % (
            playlist_url, user_id, current_datetime, message_id
        )
        self.conn.execute(stmt)
        self.conn.commit()
