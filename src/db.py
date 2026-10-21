import os
import sqlite3

DB_PATH = "data/app.db"

def get_conn():
    """Membuat koneksi SQLite dengan mengaktifkan foreign_keys = ON"""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def init_db():
    """Menginisialisasi 4 tabel utama pada database SQLite"""
    conn = get_conn()
    cursor = conn.cursor()

    # 1. Tabel posts (Unggahan)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS posts (
        post_id TEXT PRIMARY KEY,
        platform TEXT,
        published_at TEXT,
        text_content TEXT
    )
    """)

    # 2. Tabel comments (Komentar)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS comments (
        comment_id TEXT PRIMARY KEY,
        post_id TEXT,
        text_content TEXT,
        text_original TEXT,
        text_hash TEXT,
        published_at TEXT,
        status_eksklusi TEXT,
        alasan_eksklusi TEXT,
        split TEXT,
        FOREIGN KEY (post_id) REFERENCES posts(post_id)
    )
    """)

    # 3. Tabel annotators (Pemeriksa/Labeler)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS annotators (
        annotator_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    )
    """)

    # 4. Tabel annotations (Hasil Pelabelan)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS annotations (
        annotation_id INTEGER PRIMARY KEY AUTOINCREMENT,
        comment_id TEXT,
        annotator_id INTEGER,
        label TEXT,
        created_at TEXT,
        FOREIGN KEY (comment_id) REFERENCES comments(comment_id),
        FOREIGN KEY (annotator_id) REFERENCES annotators(annotator_id)
    )
    """)

    conn.commit()
    conn.close()
    print("Database SQLite dan 4 tabel berhasil diinisialisasi.")

if __name__ == "__main__":
    init_db()
