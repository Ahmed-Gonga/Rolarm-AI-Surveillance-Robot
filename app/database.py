import sqlite3, time, json
from contextlib import contextmanager

class EventDatabase:
    def __init__(self, db_path):
        self.db_path = db_path
        self.init()

    @contextmanager
    def connect(self):
        con = sqlite3.connect(self.db_path)
        con.row_factory = sqlite3.Row
        try:
            yield con
            con.commit()
        finally:
            con.close()

    def init(self):
        with self.connect() as con:
            con.execute('''CREATE TABLE IF NOT EXISTS events(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ts REAL NOT NULL,
                type TEXT NOT NULL,
                severity TEXT NOT NULL,
                message TEXT NOT NULL,
                payload TEXT
            )''')
            con.execute('''CREATE TABLE IF NOT EXISTS known_people(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                images INTEGER DEFAULT 0,
                created_at REAL NOT NULL
            )''')

    def log(self, event_type, severity, message, payload=None):
        with self.connect() as con:
            con.execute('INSERT INTO events(ts,type,severity,message,payload) VALUES(?,?,?,?,?)',
                        (time.time(), event_type, severity, message, json.dumps(payload or {})))

    def recent_events(self, limit=50):
        with self.connect() as con:
            rows = con.execute('SELECT * FROM events ORDER BY id DESC LIMIT ?', (limit,)).fetchall()
        return [dict(r) for r in rows]

    def upsert_person(self, name, images):
        with self.connect() as con:
            con.execute('INSERT INTO known_people(name,images,created_at) VALUES(?,?,?) ON CONFLICT(name) DO UPDATE SET images=excluded.images',
                        (name, images, time.time()))

    def people(self):
        with self.connect() as con:
            rows = con.execute('SELECT * FROM known_people ORDER BY name').fetchall()
        return [dict(r) for r in rows]
