import streamlit as st
import sqlite3
import pandas as pd
import sys
import os

# Menambahkan direktori root proyek ke sys.path agar folder 'src' terbaca
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from src.export import export_filtered

st.set_page_config(page_title="Ekspor Data", page_icon="📥", layout="wide")

st.title("📥 Ekspor Data Analisis & Verifikasi")
st.markdown("Unduh dataset hasil saringan analisis sentimen dan validasi manual sesuai parameter filter aktif.")

# Koneksi database
@st.cache_resource
def get_connection():
    return sqlite3.connect("data/sentiment.db", check_same_thread=False)

conn = get_connection()

# Sidebar Filter untuk Ekspor
st.sidebar.header("Filter Ekspor")
platform_opt = st.sidebar.selectbox("Pilih Platform", ["Semua", "Instagram", "YouTube", "TikTok", "Twitter"])
category_opt = st.sidebar.selectbox("Pilih Kategori", ["Semua", "Infrastruktur", "Layanan Publik", "Ekonomi", "Pendidikan"])

filters = {}
if platform_opt != "Semua":
    filters["platform"] = platform_opt
if category_opt != "Semua":
    filters["content_category"] = category_opt

# Ambil data menggunakan fungsi export_filtered
df_export = export_filtered(conn, filters=filters)

# Metrik ringkasan baris
col1, col2 = st.columns(2)
with col1:
    st.metric("Total Baris Data Siap Ekspor", f"{len(df_export):,}")
with col2:
    st.metric("Jumlah Kolom Kontrak", f"{len(df_export.columns)}")

if not df_export.empty:
    st.subheader("👀 Pratinjau 5 Baris Pertama")
    st.dataframe(df_export.head(5), use_container_width=True)

    # Konversi ke CSV untuk tombol unduh
    csv_bytes = df_export.to_csv(index=False).encode('utf-8')
    
    st.download_button(
        label="📥 Unduh Berkas CSV (Filtered Export)",
        data=csv_bytes,
        file_name="dataset_sentiment_filtered.csv",
        mime="text/csv",
        help="Klik untuk mengunduh data dalam format CSV standar sesuai kontrak."
    )
else:
    st.warning("⚠️ Tidak ada data yang ditemukan berdasarkan kombinasi filter tersebut.")
