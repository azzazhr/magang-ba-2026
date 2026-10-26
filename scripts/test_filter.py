import sqlite3
import pandas as pd
from src.queries import filter_comments

# 1. Buka koneksi ke database SQLite
conn = sqlite3.connect("data/app.db")

print("=" * 60)
print("HASIL PENGUJIAN KUERI MANUAL (VALIDASI HARI 14)")
print("=" * 60)

# --- Kombinasi 1: Satu Platform + Rentang Tanggal/Bulan ---
df_comb1 = filter_comments(
    conn, 
    platforms=["Instagram"], 
    date_from="2026-09-01", 
    date_to="2026-09-30"
)
print(f"1. Kombinasi 1 (Instagram + Sept 2026): Ditemukan {len(df_comb1)} baris")

# --- Kombinasi 2: Dua Kategori Konten Sekaligus ---
df_comb2 = filter_comments(
    conn, 
    categories=["Sosial", "Ekonomi"]
)
print(f"2. Kombinasi 2 (Kategori Sosial & Ekonomi): Ditemukan {len(df_comb2)} baris")

# --- Kombinasi 3: Kata Kunci Spesifik + Platform Tertentu ---
df_comb3 = filter_comments(
    conn, 
    platforms=["Instagram"], 
    keyword="bantuan"
)
print(f"3. Kombinasi 3 (Kata kunci 'bantuan' di Instagram): Ditemukan {len(df_comb3)} baris")

print("=" * 60)

# 2. Tutup koneksi database
conn.close()
