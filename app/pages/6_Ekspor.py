import streamlit as st
import sqlite3
import pandas as pd
import json
from datetime import datetime, timezone
import sys
import os

# Menambahkan direktori root proyek ke sys.path agar folder 'src' terbaca
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from src.export import export_filtered
from src.db import get_conn, init_db

st.set_page_config(page_title="Ekspor Data", page_icon="📥", layout="wide")

st.title("📥 Ekspor Data Analisis & Verifikasi")
st.markdown("Unduh dataset hasil saringan analisis sentimen dan validasi manual sesuai parameter filter aktif.")

# Koneksi database
def get_connection():
    init_db()
    return get_conn()

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
    st.subheader("🔍 Pratinjau 5 Baris Pertama")
    st.dataframe(df_export.head(5), use_container_width=True)

    # Susun Manifest / Metadata Ekspor (memenuhi TC-15)
    data_versions = (
        sorted(df_export["data_version"].dropna().astype(str).unique().tolist())
        if "data_version" in df_export.columns and not df_export["data_version"].dropna().empty
        else ["v0"]
    )
    model_versions = (
        sorted(df_export["model_version"].dropna().astype(str).unique().tolist())
        if "model_version" in df_export.columns and not df_export["model_version"].dropna().empty
        else ["T3_indobert_len64"]
    )

    manifest_data = {
        "exported_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "dataset_file": "dataset_sentiment_filtered.csv",
        "row_count": int(len(df_export)),
        "column_count": int(len(df_export.columns)),
        "columns": list(df_export.columns),
        "data_versions": data_versions,
        "model_versions": model_versions,
        "applied_filters": filters if filters else {"platform": "Semua", "content_category": "Semua"},
        "pii_included": False
    }

    manifest_json_str = json.dumps(manifest_data, indent=2, ensure_ascii=False)
    manifest_bytes = manifest_json_str.encode("utf-8")
    csv_bytes = df_export.to_csv(index=False).encode("utf-8")

    # Simpan salinan manifest ke folder exports/
    os.makedirs("exports", exist_ok=True)
    with open("exports/manifest_export_latest.json", "w", encoding="utf-8") as mf:
        mf.write(manifest_json_str)

    btn_col1, btn_col2 = st.columns(2)
    with btn_col1:
        st.download_button(
            label="📥 Unduh Berkas CSV (Filtered Export)",
            data=csv_bytes,
            file_name="dataset_sentiment_filtered.csv",
            mime="text/csv",
            help="Klik untuk mengunduh data dalam format CSV standar sesuai kontrak."
        )
    with btn_col2:
        st.download_button(
            label="📄 Unduh Manifest Metadata (JSON)",
            data=manifest_bytes,
            file_name="manifest_dataset_sentiment.json",
            mime="application/json",
            help="Klik untuk mengunduh metadata versi data, versi model, filter, dan jumlah baris."
        )

    with st.expander("🔍 Pratinjau Manifest / Metadata Ekspor (JSON)", expanded=True):
        st.json(manifest_data)
else:
    st.warning("Tidak ada data yang ditemukan berdasarkan kombinasi filter tersebut.")

