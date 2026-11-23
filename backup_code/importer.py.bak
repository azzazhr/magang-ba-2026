import pandas as pd
import sqlite3

def import_posts(conn, df):
    """Mengimpor data posts ke database SQLite"""
    ok, skipped, rejected = 0, 0, []
    for r in df.itertuples():
        if pd.isna(r.post_id):
            rejected.append((str(getattr(r, 'Index', 'Unknown')), "Post ID kosong"))
            continue

        try:
            cur = conn.cursor()
            cur.execute("""
                INSERT OR IGNORE INTO posts (post_id, platform, published_at, text_content)
                VALUES (?, ?, ?, ?)
            """, (
                str(r.post_id),
                str(getattr(r, 'platform', 'Unknown')),
                str(getattr(r, 'published_at', '')),
                str(getattr(r, 'text_content', ''))
            ))
            if cur.rowcount == 1:
                ok += 1
            else:
                skipped += 1
        except Exception as e:
            rejected.append((str(r.post_id), str(e)))

    conn.commit()
    return {"diterima": ok, "dilewati": skipped, "ditolak": rejected}

def import_comments(conn, df):
    """Mengimpor data comments ke database SQLite dengan validasi foreign key (post_id)"""
    ok, skipped, rejected = 0, 0, []
    for r in df.itertuples():
        if pd.isna(r.comment_id) or pd.isna(r.post_id):
            rejected.append((str(getattr(r, 'comment_id', 'Unknown')), "Comment ID atau Post ID kosong"))
            continue

        # Periksa apakah unggahan induk (post_id) ada di database
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM posts WHERE post_id = ?", (str(r.post_id),))
        if cur.fetchone() is None:
            rejected.append((str(r.comment_id), "Q09: unggahan sumber tidak ditemukan"))
            continue

        try:
            cur.execute("""
                INSERT OR IGNORE INTO comments
                (comment_id, post_id, text_content, text_original, text_hash, published_at, status_eksklusi, alasan_eksklusi, split)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                str(r.comment_id),
                str(r.post_id),
                str(getattr(r, 'text_content', '')),
                str(getattr(r, 'text_original', '')),
                str(getattr(r, 'text_hash', '')),
                str(getattr(r, 'published_at', '')),
                str(getattr(r, 'status_eksklusi', 'Aktif')),
                str(getattr(r, 'alasan_eksklusi', 'Lolos')),
                str(getattr(r, 'split', 'train'))
            ))
            if cur.rowcount == 1:
                ok += 1
            else:
                skipped += 1
        except Exception as e:
            rejected.append((str(r.comment_id), str(e)))

    conn.commit()
    return {"diterima": ok, "dilewati": skipped, "ditolak": rejected}
