import sys
from pathlib import Path

# Tambahkan direktori root proyek ke sys.path paling awal
root_dir = Path(__file__).resolve().parent.parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

import os
import streamlit as st
import sqlite3
import pandas as pd
from src.predict import load_model, predict_and_store

st.set_page_config(page_title="Analisis Sentimen", page_icon="📊", layout="wide")

st.title("📊 Halaman Analisis Sentimen (Integrasi Model)")
st.write("Gunakan halaman ini untuk menjalankan inferensi model terpilih secara interaktif dan menyimpannya ke database.")

def get_connection():
    return sqlite3.connect("data/sentiment.db")

conn = get_connection()

# ==========================================
# 1. TAMPILKAN INFORMASI MODEL AKTIF
# ==========================================
st.subheader("1. Informasi Model Aktif")
try:
    clf, card = load_model()
    st.success(f"Model Aktif: **{card.get('model_id')}**")
    st.info(f"Versi/ID: `{card.get('experiment_id')}` | Max Length: `{card.get('max_length')}` | Score Type: `{card.get('score_type')}`")
except Exception as e:
    st.error(f"Gagal memuat model: {e}")
    st.stop()
# ==========================================
# 2. FILTER KOMENTAR & EKSEKUSI ANALISIS
# ==========================================
st.subheader("2. Filter Komentar untuk Dianalisis")

try:
    df_comments = pd.read_sql("SELECT comment_id, text_original, sentiment_label FROM comments", conn)
except Exception as e:
    st.error(f"Tabel 'comments' belum tersedia di database. Detail: {e}")
    df_comments = pd.DataFrame(columns=['comment_id', 'text_original', 'sentiment_label'])

source_filter = st.selectbox("Pilih Sumber Data", ["Semua Data", "Validation Set (Contoh)"])

if st.button("Jalankan Analisis"):
    if df_comments.empty:
        st.warning("Data komentar kosong. Harap pastikan tabel database sudah terisi.")
    else:
        with st.spinner("Sedang memproses prediksi model..."):
            sample_ids = df_comments['comment_id'].head(50).tolist()
            processed_count = predict_and_store(conn, sample_ids)
            
            st.success(f"Analisis selesai! Sebanyak **{processed_count} komentar** berhasil diproses dan disimpan.")
            st.info(f"Metadata tercatat dengan Model Version: `{card.get('experiment_id')}`")

# ==========================================
# 3. PRATINJAU HASIL PREDIKSI DARI DATABASE
# ==========================================
st.subheader("3. Pratinjau Hasil Prediksi Terbaru")
try:
    df_preds = pd.read_sql("""
        SELECT c.text_original, p.predicted_label, p.score, p.predicted_at, p.model_version
        FROM predictions p
        JOIN comments c ON p.comment_id = c.comment_id
        ORDER BY p.prediction_id DESC
        LIMIT 10
    """, conn)
    
    if not df_preds.empty:
        st.write("10 Riwayat Prediksi Terakhir:")
        st.dataframe(df_preds, use_container_width=True)
    else:
        st.info("Belum ada data prediksi yang tersimpan di database.")
except Exception as e:
    st.info("Menunggu eksekusi analisis pertama...")

conn.close()
