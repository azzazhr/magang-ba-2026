import sys
from pathlib import Path

# Menambahkan root direktori proyek ke sys.path secara dinamis
root_dir = Path(__file__).resolve().parent.parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

import streamlit as st
import sqlite3
import pandas as pd
from src.dashboard import get_summary_metrics, get_latest_verifications_df, get_latest_predictions_df

st.set_page_config(page_title="Dashboard Analisis Sentimen", page_icon="📊", layout="wide")

st.title("📊 Dashboard Analisis Sentimen & Kebijakan Publik")
st.markdown("Eksplorasi data riil, distribusi sentimen, dan metrik verifikasi interaktif.")

# Koneksi ke database
def get_connection():
    return sqlite3.connect("data/sentiment.db")

conn = get_connection()

# ==========================================
# 1. RINGKASAN ANGKA (st.metric)
# ==========================================
st.subheader("📌 Ringkasan Metrik Utama")
metrics = get_summary_metrics(conn)

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.metric("Total Unggahan", f"{metrics['total_posts']:,}")
with col2:
    st.metric("Komentar Layak", f"{metrics['total_eligible']:,}")
with col3:
    st.metric("Komentar Diprediksi", f"{metrics['total_predicted']:,}")
with col4:
    st.metric("Komentar Terverifikasi", f"{metrics['total_verified']:,}")
with col5:
    st.metric("Persentase Verifikasi", f"{metrics['verif_pct']:.1f}%")

st.markdown("---")

# Memuat data riil dari database
df_comments = pd.read_sql("SELECT comment_id, text_original, sentiment_label, platform, content_category, commented_at FROM comments", conn)

# ==========================================
# 2. EMPAT GRAFIK UTAMA SESUAI PANDUAN
# ==========================================
col_g1, col_g2 = st.columns(2)

# Grafik 1: Jumlah komentar per platform (batang)
with col_g1:
    st.subheader("📱 Grafik 1: Komentar per Platform")
    if not df_comments.empty and 'platform' in df_comments.columns:
        platform_counts = df_comments['platform'].value_counts()
        st.bar_chart(platform_counts)
    else:
        st.info("Data platform tidak tersedia.")

# Grafik 2: Jumlah unggahan per kategori konten (batang)
with col_g2:
    st.subheader("📂 Grafik 2: Unggahan per Kategori Konten")
    if not df_comments.empty and 'content_category' in df_comments.columns:
        category_counts = df_comments['content_category'].value_counts()
        st.bar_chart(category_counts)
    else:
        st.info("Data kategori konten tidak tersedia.")

st.markdown("---")

# ==========================================
# 3. PILIHAN SUMBER LABEL & GRAFIK 3 (DISTRIBUSI SENTIMEN)
# ==========================================
st.subheader("🎯 Grafik 3: Distribusi Sentimen dengan Sumber Label")
src_label = st.radio(
    "Pilih Sumber Label Sentimen:", 
    ["Prediksi model", "Label verifikasi"]
)

if src_label == "Prediksi model":
    df_sentiment = get_latest_predictions_df(conn)
    label_source_desc = "Prediksi model"
else:
    df_sentiment = get_latest_verifications_df(conn)
    label_source_desc = "Label verifikasi (hanya komentar terverifikasi)"

n_count = len(df_sentiment)

col_s1, col_s2 = st.columns(2)

with col_s1:
    st.markdown(f"**Distribusi sentimen – {label_source_desc} (n = {n_count})**")
    if not df_sentiment.empty and 'label' in df_sentiment.columns:
        clean_labels = df_sentiment['label'].astype(str).str.lower()
        sentiment_counts = clean_labels.value_counts().reindex(["positif", "netral", "negatif"], fill_value=0)
        st.bar_chart(sentiment_counts)
    else:
        st.warning("Tidak ada data sentimen untuk sumber yang dipilih.")

# Grafik 4: Jumlah komentar per minggu berdasarkan commented_at (garis) - DIPERBAIKI
with col_s2:
    st.markdown("**Grafik 4: Tren Komentar per Minggu (berdasarkan commented_at)**")
    if not df_comments.empty and 'commented_at' in df_comments.columns:
        try:
            # Konversi kolom tanggal ke format datetime secara eksplisit & drop nilai NaT
            df_comments['commented_at_dt'] = pd.to_datetime(df_comments['commented_at'], errors='coerce')
            df_trend = df_comments.dropna(subset=['commented_at_dt'])
            
            if not df_trend.empty:
                # Groupby minggu untuk menghasilkan garis tren yang akurat
                weekly_trend = df_trend.groupby(pd.Grouper(key='commented_at_dt', freq='W')).size()
                st.line_chart(weekly_trend)
            else:
                st.warning("Format tanggal komentar tidak valid.")
        except Exception as e:
            st.error(f"Gagal memproses tren mingguan: {e}")
    else:
        st.info("Data tanggal komentar tidak tersedia.")

conn.close()

# ==========================================
# 4. CATATAN TETAP DI BAWAH DASHBOARD
# ==========================================
st.markdown("---")
st.markdown(
    "> **Catatan:** Komentar adalah sampel dari akun resmi pada rentang 1 Juli–30 September 2026 dan tidak mewakili seluruh warga."
)
