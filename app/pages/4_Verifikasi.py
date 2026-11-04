import sys
from pathlib import Path

# Menambahkan direktori root proyek ke sys.path secara dinamis
root_dir = Path(__file__).resolve().parent.parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

import streamlit as st
import sqlite3
import pandas as pd
from src.queries import latest_predictions

st.title("🔍 Halaman Verifikasi & Detail Prediksi")
st.write("Gunakan halaman ini untuk memverifikasi detail prediksi, konteks unggahan, dan kecocokan skor model secara transparan.")

# Koneksi ke database SQLite
def get_connection():
    return sqlite3.connect("data/sentiment.db")

conn = get_connection()

# ==========================================
# ATURAN FORMAT SKOR (Langkah 2)
# ==========================================
def score_text(score, score_type):
    if score_type in ["probabilitas_softmax", "softmax"]:
        return f"Probabilitas model (belum dikalibrasi): {score:.2f}"
    if score_type == "margin_svm":
        return f"Skor margin SVM: {score:.2f} (bukan probabilitas)"
    if score is not None:
        return f"Skor: {score:.2f} (Tipe: {score_type})"
    return "Skor tidak tersedia"

# Fungsi helper untuk mendeteksi platform dari comment_id
def get_platform_info(comment_id):
    if comment_id.startswith("IG-"):
        return "Instagram", f"https://instagram.com/p/{comment_id}"
    elif comment_id.startswith("YT-"):
        return "YouTube", f"https://youtube.com/watch?v={comment_id}"
    elif comment_id.startswith("TT-"):
        return "TikTok", f"https://tiktok.com/@post/{comment_id}"
    return "Media Sosial Lainnya", "(URL tidak tersedia)"

# ==========================================
# 1. SIDEBAR FILTER (Langkah 2)
# ==========================================
st.sidebar.header("Filter Verifikasi")
try:
    versions_df = pd.read_sql("SELECT DISTINCT model_version FROM predictions", conn)
    model_versions = versions_df['model_version'].tolist() if not versions_df.empty else []
except Exception:
    model_versions = []

selected_version = st.sidebar.selectbox("Pilih Versi Model", [None] + model_versions)

# Ambil data terbaru menggunakan fungsi latest_predictions
df_latest = latest_predictions(conn, selected_version)

if df_latest.empty:
    st.warning("Belum ada data prediksi yang tersimpan di database untuk versi ini.")
else:
    # ==========================================
    # 2. TABEL RINGKAS DI HALAMAN UTAMA (Langkah 2)
    # ==========================================
    st.subheader("1. Ringkasan Tabel Prediksi Terbaru")
    display_df = df_latest[['comment_id', 'predicted_label', 'score', 'model_version']]
    st.dataframe(display_df, use_container_width=True)

    # ==========================================
    # 3. PANEL DETAIL KOMENTAR (Langkah 3 & 4)
    # ==========================================
    st.subheader("2. Panel Detail Komentar")
    selected_id = st.selectbox("Pilih Comment ID untuk melihat detail lengkap:", df_latest['comment_id'].tolist())

    if selected_id:
        row = df_latest[df_latest['comment_id'] == selected_id].iloc[0]
        
        # Deteksi platform secara otomatis berdasarkan ID
        platform_name, platform_url = get_platform_info(row['comment_id'])

        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**Comment ID:** `{row['comment_id']}`")
            st.markdown(f"**Prediksi Model:** `{row['predicted_label']}`")
            
            formatted_score = score_text(row['score'], row['score_type'])
            st.markdown(f"**Jenis Skor:** {formatted_score}")
        with col2:
            st.markdown(f"**Versi Model:** `{row['model_version']}`")
            st.markdown(f"**Waktu Prediksi:** `{row['predicted_at']}`")

        st.markdown("**Teks Asli Komentar:**")
        st.info(row['text_original'] if pd.notna(row['text_original']) else "Teks tidak tersedia")

        st.markdown("**Konteks Unggahan:**")
        st.write(f"Platform: **{platform_name}** | URL Terkait: [{platform_url}]({platform_url})")

conn.close()
