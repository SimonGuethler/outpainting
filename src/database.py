import sqlite3
from typing import List, Tuple, Optional

DB_FILE = 'sqlite.db'


class Database:
    def __init__(self):
        self.conn = sqlite3.connect(DB_FILE)
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                prompt TEXT,
                date TEXT,
                source TEXT,
                image TEXT
            )
        ''')

    def add_entry(self, prompt: str, date: str, source: str, image: str) -> None:
        print(f"Adding entry: {prompt}, {date}, {source}, {image}")
        self.conn.execute('''
            INSERT INTO entries (prompt, date, source, image)
            VALUES (?, ?, ?, ?)
        ''', (prompt, date, source, image))
        self.conn.commit()

    def get_all_entries(self) -> List[Tuple[int, str, str, str, str]]:
        cursor = self.conn.execute('SELECT * FROM entries')
        entries = cursor.fetchall()
        return entries

    def get_entry_by_id(self, id: int) -> Optional[Tuple[int, str, str, str, str]]:
        cursor = self.conn.execute('SELECT * FROM entries WHERE id = ?', (id,))
        entry = cursor.fetchone()
        return entry

    def delete_all_entries(self) -> None:
        self.conn.execute('DELETE FROM entries')
        self.conn.commit()

    def close_connection(self) -> None:
        self.conn.close()
