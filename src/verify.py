import sqlite3
from datetime import datetime

VALID = {"positif", "negatif", "netral"}

def current_label(conn, comment_id):
    """
    Mengambil label terbaru untuk suatu komentar.
    Mengecek apakah sudah pernah dikoreksi di verification_history,
    jika belum, mengambil dari tabel predictions.
    """
    cursor = conn.cursor()
    
    # 1. Cek apakah ada riwayat verifikasi sebelumnya
    cursor.execute("""
        SELECT new_label FROM verification_history 
        WHERE comment_id = ? 
        ORDER BY verified_at DESC LIMIT 1
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

    # Masukkan data koreksi baru ke tabel verification_history
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
        datetime.now().isoformat(timespec="seconds")
    ))
    
    conn.commit()
