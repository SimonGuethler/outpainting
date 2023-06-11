import os
import sqlite3
from dataclasses import dataclass
from typing import List, Optional

DB_FOLDER = 'outpainting'
DB_FILE = 'sqlite.db'


@dataclass
class Entry:
    id: int
    prompt: str
    source: str
    image: str
    date: str
    headline: str


class Database:
    def __init__(self):
        os.makedirs(DB_FOLDER, exist_ok=True)
        self.conn = sqlite3.connect(os.path.join(DB_FOLDER, DB_FILE))
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                prompt TEXT,
                source TEXT,
                image TEXT,
                date TEXT,
                headline TEXT
            )
        ''')

    def add_entry(self, prompt: str, source: str, image: str, date: str, headline: str) -> None:
        print(f"Adding entry: {prompt}, {source}, {image}, {date}, {headline}")
        self.conn.execute('''
            INSERT INTO entries (prompt, source, image, date, headline)
            VALUES (?, ?, ?, ?, ?)
        ''', (prompt, source, image, date, headline))
        self.conn.commit()

    def get_all_entries(self) -> List[Entry]:
        cursor = self.conn.execute('SELECT * FROM entries')
        rows = cursor.fetchall()
        entries = []
        for row in rows:
            entry = Entry(id=row[0], prompt=row[1], source=row[2], image=row[3], date=row[4], headline=row[5])
            entries.append(entry)
        return entries

    def get_entry_by_id(self, id: int) -> Optional[Entry]:
        cursor = self.conn.execute('SELECT * FROM entries WHERE id = ?', (id,))
        entry = cursor.fetchone()
        if entry is None:
            return None
        return Entry(id=entry[0], prompt=entry[1], source=entry[2], image=entry[3], date=entry[4], headline=entry[5])

    def delete_all_entries(self) -> None:
        self.conn.execute('DELETE FROM entries')
        self.conn.commit()

    def close_connection(self) -> None:
        self.conn.close()
