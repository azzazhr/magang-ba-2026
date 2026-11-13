import sqlite3
from datetime import datetime

VALID = {"positif", "negatif", "netral"}

def _verification_columns(conn):
    return {
        row[1]
        for row in conn.execute("PRAGMA table_info(verification_history)")
    }


def _upgrade_history_table(conn, verification_columns):
    if not {"comment_id", "label", "verified_at"} <= verification_columns:
        return verification_columns
    if {"prediction_id", "previous_label", "new_label", "reason", "reviewer_id"} <= verification_columns:
        return verification_columns

    conn.execute("""
        CREATE TABLE verification_history_new (
            history_id INTEGER PRIMARY KEY AUTOINCREMENT,
            comment_id TEXT NOT NULL,
            prediction_id INTEGER,
            previous_label TEXT,
            new_label TEXT NOT NULL,
            reason TEXT,
            reviewer_id TEXT,
            verified_at TIMESTAMP NOT NULL
        )
    """)
    conn.execute("""
        INSERT INTO verification_history_new
        (comment_id, new_label, verified_at)
        SELECT comment_id, label, verified_at
        FROM verification_history
    """)
    conn.execute("DROP TABLE verification_history")
    conn.execute(
        "ALTER TABLE verification_history_new RENAME TO verification_history"
    )
    return _verification_columns(conn)


def current_label(conn, comment_id):
    """
    Mengambil label terbaru untuk suatu komentar.
    Mengecek apakah sudah pernah dikoreksi di verification_history,
    jika belum, mengambil dari tabel predictions.
    """
    cursor = conn.cursor()
    verification_columns = _verification_columns(conn)
    label_column = "new_label" if "new_label" in verification_columns else "label"
    order_columns = "history_id DESC, verified_at DESC" if "history_id" in verification_columns else "verified_at DESC"
    
    # 1. Cek apakah ada riwayat verifikasi sebelumnya
    cursor.execute(f"""
        SELECT {label_column} FROM verification_history
        WHERE comment_id = ?
        ORDER BY {order_columns} LIMIT 1
    """, (comment_id,))
    row = cursor.fetchone()
    if row:
        return row[0]
        
    # 2. Jika belum ada koreksi, ambil dari prediksi awal model
    cursor.execute("""
        SELECT predicted_label FROM predictions 
        WHERE comment_id = ? 
        ORDER BY predicted_at DESC LIMIT 1
    """, (comment_id,))
    row = cursor.fetchone()
    return row[0] if row else "netral"

def add_verification(conn, comment_id, prediction_id, new_label, reason, reviewer_id):
    """
    Memvalidasi input koreksi label, mengambil label sebelumnya,
    lalu memasukkannya ke tabel verification_history secara aman (INSERT).
    Tidak ada proses UPDATE pada tabel predictions agar data asli tetap terjaga.
    """
    # Validasi 1: Pastikan label baru valid (positif/negatif/netral)
    if new_label not in VALID:
        raise ValueError("Label harus positif, negatif, atau netral")
    
    # Validasi 2: Pastikan alasan diisi dan minimal 5 karakter
    if not reason or len(reason.strip()) < 5:
        raise ValueError("Alasan minimal 5 karakter")
        
    # Validasi 3: Pastikan ID pemeriksa wajib diisi
    if not reviewer_id:
        raise ValueError("ID pemeriksa wajib diisi")
        
    # Ambil label sebelumnya (bisa dari koreksi terakhir atau prediksi awal)
    prev = current_label(conn, comment_id)            

    verification_columns = _upgrade_history_table(
        conn, _verification_columns(conn)
    )
    verified_at = datetime.now().isoformat(timespec="seconds")

    if {"prediction_id", "previous_label", "new_label", "reason", "reviewer_id"} <= verification_columns:
        conn.execute("""
            INSERT INTO verification_history
            (comment_id, prediction_id, previous_label, new_label, reason, reviewer_id, verified_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            comment_id,
            prediction_id,
            prev,
            new_label,
            reason.strip(),
            reviewer_id,
            verified_at
        ))
    else:
        raise sqlite3.OperationalError(
            "Skema verification_history tidak didukung"
        )
    
    conn.commit()
