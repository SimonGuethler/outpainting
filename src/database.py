import sqlite3
from dataclasses import dataclass
from typing import List, Optional

DB_FILE = 'sqlite.db'


@dataclass
class Entry:
    id: int
    prompt: str
    source: str
    image: str
    date: str


class Database:
    def __init__(self):
        self.conn = sqlite3.connect(DB_FILE)
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                prompt TEXT,
                source TEXT,
                image TEXT,
                date TEXT
            )
        ''')

    def add_entry(self, prompt: str, source: str, image: str, date: str) -> None:
        print(f"Adding entry: {prompt}, {date}, {source}, {image}")
        self.conn.execute('''
            INSERT INTO entries (prompt, source, image, date)
            VALUES (?, ?, ?, ?)
        ''', (prompt, source, image, date))
        self.conn.commit()

    def get_all_entries(self) -> List[Entry]:
        cursor = self.conn.execute('SELECT * FROM entries')
        rows = cursor.fetchall()
        entries = []
        for row in rows:
            entry = Entry(id=row[0], prompt=row[1], source=row[2], image=row[3], date=row[4])
            entries.append(entry)
        return entries

    def get_entry_by_id(self, id: int) -> Optional[Entry]:
        cursor = self.conn.execute('SELECT * FROM entries WHERE id = ?', (id,))
        entry = cursor.fetchone()
        if entry is None:
            return None
        return Entry(id=entry[0], prompt=entry[1], source=entry[2], image=entry[3], date=entry[4])

    def delete_all_entries(self) -> None:
        self.conn.execute('DELETE FROM entries')
        self.conn.commit()

    def close_connection(self) -> None:
        self.conn.close()
