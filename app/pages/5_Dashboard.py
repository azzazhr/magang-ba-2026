import sys
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

import streamlit as st
import sqlite3
import pandas as pd
from src.queries import filter_comments

st.set_page_config(page_title="Dashboard Analisis Sentimen", page_icon="📊", layout="wide")

st.title("📊 Dashboard Analisis Sentimen & Kebijakan Publik")
st.markdown("Eksplorasi data riil, distribusi sentimen, dan metrik verifikasi interaktif dengan filter terpusat.")

def get_connection():
    return sqlite3.connect("data/sentiment.db")

conn = get_connection()

# ==========================================
# SIDEBAR: FILTER TERPUSAT (SESSION STATE)
# ==========================================
st.sidebar.header("🔍 Filter Data Interaktif")

if "f_platform" not in st.session_state:
    st.session_state["f_platform"] = "Semua"
if "f_category" not in st.session_state:
    st.session_state["f_category"] = "Semua"
if "f_label_source" not in st.session_state:
    st.session_state["f_label_source"] = "Prediksi model"
if "f_label" not in st.session_state:
    st.session_state["f_label"] = "Semua"
if "f_keyword" not in st.session_state:
    st.session_state["f_keyword"] = ""

platforms = ["Semua", "Instagram", "YouTube", "TikTok", "Twitter/X"]
categories = ["Semua", "Infrastruktur", "Pelayanan Publik", "Pendidikan", "Kesehatan", "Transportasi"]
labels = ["Semua", "positif", "netral", "negatif"]

st.session_state["f_platform"] = st.sidebar.selectbox("Platform", platforms, index=platforms.index(st.session_state["f_platform"]))
st.session_state["f_category"] = st.sidebar.selectbox("Kategori Konten", categories, index=categories.index(st.session_state["f_category"]))
st.session_state["f_label_source"] = st.sidebar.radio("Sumber Label Sentimen", ["Prediksi model", "Label verifikasi"], index=0 if st.session_state["f_label_source"]=="Prediksi model" else 1)
st.session_state["f_label"] = st.sidebar.selectbox("Label Sentimen", labels, index=labels.index(st.session_state["f_label"]))
st.session_state["f_keyword"] = st.sidebar.text_input("Cari Kata Kunci", value=st.session_state["f_keyword"])

# MEMANGGIL filter_comments BERDASARKAN SESSION STATE
df_filtered = filter_comments(
    conn,
    platform=st.session_state["f_platform"],
    category=st.session_state["f_category"],
    label=st.session_state["f_label"],
    label_source=st.session_state["f_label_source"],
    keyword=st.session_state["f_keyword"]
)

st.info(f"📌 Menampilkan data berdasarkan filter aktif (Total baris setelah filter: **{len(df_filtered):,}**)")

# ==========================================
# 1. RINGKASAN ANGKA (AGREGASI DARI HASIL FILTER)
# ==========================================
st.subheader("📌 Ringkasan Metrik Utama")
total_posts = len(df_filtered)
total_eligible = int(df_filtered['is_eligible'].sum()) if 'is_eligible' in df_filtered.columns and not df_filtered.empty else total_posts
total_predicted = int(df_filtered['model_label'].notna().sum()) if 'model_label' in df_filtered.columns and not df_filtered.empty else 0
total_verified = int(df_filtered['verified_label'].notna().sum()) if 'verified_label' in df_filtered.columns and not df_filtered.empty else 0
verif_pct = (total_verified / total_predicted * 100) if total_predicted > 0 else 0.0

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.metric("Total Unggahan", f"{total_posts:,}")
with col2:
    st.metric("Komentar Layak", f"{total_eligible:,}")
with col3:
    st.metric("Komentar Diprediksi", f"{total_predicted:,}")
with col4:
    st.metric("Komentar Terverifikasi", f"{total_verified:,}")
with col5:
    st.metric("Persentase Verifikasi", f"{verif_pct:.1f}%")

st.markdown("---")

# ==========================================
# 2. EMPAT GRAFIK UTAMA
# ==========================================
col_g1, col_g2 = st.columns(2)

with col_g1:
    st.subheader("📱 Grafik 1: Komentar per Platform")
    if not df_filtered.empty and 'platform' in df_filtered.columns:
        st.bar_chart(df_filtered['platform'].value_counts())
    else:
        st.info("Tidak ada data platform.")

with col_g2:
    st.subheader("📂 Grafik 2: Unggahan per Kategori Konten")
    if not df_filtered.empty and 'content_category' in df_filtered.columns:
        st.bar_chart(df_filtered['content_category'].value_counts())
    else:
        st.info("Tidak ada data kategori.")

st.markdown("---")

col_s1, col_s2 = st.columns(2)

with col_s1:
    st.subheader("🎯 Grafik 3: Distribusi Sentimen")
    active_col = 'model_label' if st.session_state["f_label_source"] == "Prediksi model" else 'verified_label'
    if not df_filtered.empty and active_col in df_filtered.columns:
        counts = df_filtered[active_col].astype(str).str.lower().value_counts().reindex(["positif", "netral", "negatif"], fill_value=0)
        st.bar_chart(counts)
    else:
        st.warning("Data sentimen tidak tersedia.")

with col_s2:
    st.subheader("📈 Grafik 4: Tren Mingguan Komentar")
    if not df_filtered.empty and 'commented_at' in df_filtered.columns:
        try:
            df_filtered['dt'] = pd.to_datetime(df_filtered['commented_at'], errors='coerce')
            trend = df_filtered.dropna(subset=['dt']).groupby(pd.Grouper(key='dt', freq='W')).size()
            st.line_chart(trend)
        except Exception:
            st.info("Gagal merender tren.")
    else:
            st.info("Data tanggal tidak tersedia.")

conn.close()

st.markdown("---")
st.markdown("> **Catatan:** Komentar adalah sampel dari akun resmi pada rentang 1 Juli–30 September 2026 dan tidak mewakili seluruh warga.")
