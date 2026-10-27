import os
import streamlit as st
import pandas as pd
import sys

# Menambahkan path src agar dapat diimpor secara aman
try:
    current_dir = os.path.dirname(os.path.abspath(__file__))
except NameError:
    current_dir = os.getcwd()

sys.path.append(os.path.abspath(os.path.join(current_dir, '../../')))
from src.db import get_conn, init_db
from src.queries import filter_comments

st.title("Eksplorasi & Filter Data Komentar")
st.write("Gunakan panel filter di sidebar sebelah kiri untuk menyaring data secara dinamis.")

init_db()

# --- KONTROL FILTER DI SIDEBAR ---
st.sidebar.header("Filter Data Lanjutan")

# Ambil koneksi database terlebih dahulu untuk memuat platform unik secara dinamis
conn = get_conn()
try:
    df_all = pd.read_sql("SELECT DISTINCT platform FROM comments", conn)
    available_platforms = df_all['platform'].dropna().unique().tolist()
    if not available_platforms:
        available_platforms = ["Instagram", "YouTube", "Twitter", "TikTok"]
except Exception:
    available_platforms = ["Instagram", "YouTube", "Twitter", "TikTok"]

# 1. Filter Platform (menggunakan multiselect agar TikTok dan lainnya bisa dipilih)
platforms_selected = st.sidebar.multiselect(
    "Pilih Platform:",
    available_platforms,
    default=available_platforms
)

# 2. Filter Rentang Tanggal
date_from = st.sidebar.date_input("Dari Tanggal:", value=None)
date_to = st.sidebar.date_input("Sampai Tanggal:", value=None)

# 3. Filter Kategori Konten
categories_selected = st.sidebar.multiselect(
    "Pilih Kategori:",
    ["Sosial", "Ekonomi", "Pendidikan"],
    default=[]
)

# 4. Filter Kata Kunci
keyword = st.sidebar.text_input("Kata Kunci Teks:", "")

# Konversi input menjadi argumen (None jika kosong)
platforms_arg = platforms_selected if platforms_selected else None
categories_arg = categories_selected if categories_selected else None
date_from_arg = date_from if date_from else None
date_to_arg = date_to if date_to else None
keyword_arg = keyword if keyword else None

# Eksekusi fungsi filter_comments dengan koneksi yang sama
df_res = filter_comments(
    conn,
    platforms=platforms_arg,
    date_from=date_from_arg,
    date_to=date_to_arg,
    categories=categories_arg,
    keyword=keyword_arg
)
conn.close()

# --- TAMPILAN UTAMA ---
count = len(df_res)
st.subheader(f"Ditemukan {count} Komentar")

if count > 0:
    st.dataframe(df_res, use_container_width=True)
else:
    st.info("Tidak ada data yang cocok dengan kriteria filter tersebut.")
