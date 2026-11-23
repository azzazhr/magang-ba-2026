import os
import sqlite3
import csv
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DB_PATH = str(PROJECT_ROOT / "data" / "app.db")

def get_conn():
    """Membuat koneksi SQLite dengan mengaktifkan foreign_keys = ON"""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH, check_same_thread=False, timeout=30)
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
        commented_at TEXT,
        context_text TEXT,
        content_category TEXT,
        is_eligible INTEGER,
        status_eksklusi TEXT,
        alasan_eksklusi TEXT,
        split TEXT,
        FOREIGN KEY (post_id) REFERENCES posts(post_id)
    )
    """)

    comment_columns = {
        row[1]
        for row in cursor.execute("PRAGMA table_info(comments)").fetchall()
    }
    for column, column_type in (
        ("commented_at", "TEXT"),
        ("context_text", "TEXT"),
        ("content_category", "TEXT"),
        ("is_eligible", "INTEGER"),
    ):
        if column not in comment_columns:
            cursor.execute(
                f"ALTER TABLE comments ADD COLUMN {column} {column_type}"
            )

    cursor.execute("""
        UPDATE comments
        SET commented_at = published_at
        WHERE commented_at IS NULL OR TRIM(commented_at) = ''
    """)

    historical_comments = PROJECT_ROOT / "data" / "processed" / "comments_v0.csv"
    if historical_comments.exists():
        historical_dates = {}
        with historical_comments.open("r", encoding="utf-8-sig", newline="") as file:
            for row in csv.DictReader(file):
                comment_id = str(row.get("comment_id", "")).strip()
                date = str(row.get("published_at", "")).strip()
                if comment_id and date and comment_id not in historical_dates:
                    historical_dates[comment_id] = date

        cursor.executemany(
            """
            UPDATE comments
            SET commented_at = ?,
                published_at = COALESCE(NULLIF(published_at, ''), ?)
            WHERE comment_id = ?
            """,
            (
                (date, date, comment_id)
                for comment_id, date in historical_dates.items()
            ),
        )

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

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS predictions (
        prediction_id INTEGER PRIMARY KEY AUTOINCREMENT,
        comment_id TEXT NOT NULL,
        model_name TEXT,
        model_version TEXT,
        predicted_label TEXT,
        score REAL,
        score_type TEXT,
        predicted_at TEXT,
        run_id TEXT,
        FOREIGN KEY (comment_id) REFERENCES comments(comment_id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS verification_history (
        history_id INTEGER PRIMARY KEY AUTOINCREMENT,
        comment_id TEXT NOT NULL,
        prediction_id INTEGER,
        previous_label TEXT,
        new_label TEXT NOT NULL,
        reason TEXT,
        reviewer_id TEXT,
        verified_at TEXT NOT NULL,
        FOREIGN KEY (comment_id) REFERENCES comments(comment_id),
        FOREIGN KEY (prediction_id) REFERENCES predictions(prediction_id)
    )
    """)

    conn.commit()
    conn.close()
    print("Database SQLite dan 4 tabel berhasil diinisialisasi.")

if __name__ == "__main__":
    init_db()
