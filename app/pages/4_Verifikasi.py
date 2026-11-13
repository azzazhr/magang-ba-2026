import sys
from pathlib import Path

# Menambahkan direktori root proyek ke sys.path secara dinamis
root_dir = Path(__file__).resolve().parent.parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
from src.queries import latest_predictions
from src.verify import add_verification, current_label

st.set_page_config(page_title="Verifikasi & Detail Prediksi", page_icon="🔍", layout="wide")

st.title("🔍 Halaman Verifikasi & Detail Prediksi")
st.write("Gunakan halaman ini untuk memverifikasi detail prediksi, konteks unggahan, dan melakukan koreksi label secara transparan.")

# Koneksi ke database SQLite
def get_connection():
    return sqlite3.connect("data/sentiment.db")

conn = get_connection()

# ==========================================
# ATURAN FORMAT SKOR
# ==========================================
def score_text(score, score_type):
    if score_type in ["probabilitas_softmax", "softmax"]:
        return f"Probabilitas model (belum dikalibrasi): {score:.2f}"
    if score_type == "margin_svm":
        return f"Skor margin SVM: {score:.2f} (bukan probabilitas)"
    if score is not None:
        return f"Skor: {score:.2f} (Tipe: {score_type})"
    return "Skor tidak tersedia"

# Fungsi helper platform
def get_platform_info(comment_id):
    if comment_id.startswith("IG-"):
        return "Instagram"
    elif comment_id.startswith("YT-"):
        return "YouTube"
    elif comment_id.startswith("TT-"):
        return "TikTok"
    return "Media Sosial Lainnya"

# ==========================================
# 1. SIDEBAR FILTER
# ==========================================
st.sidebar.header("Filter Verifikasi")
try:
    versions_df = pd.read_sql("SELECT DISTINCT model_version FROM predictions", conn)
    model_versions = versions_df['model_version'].tolist() if not versions_df.empty else []
except Exception:
    model_versions = []

selected_version = st.sidebar.selectbox("Pilih Versi Model", [None] + model_versions)

df_latest = latest_predictions(conn, selected_version)

if df_latest.empty:
    st.warning("Belum ada data prediksi yang tersimpan di database untuk versi ini.")
else:
    # ==========================================
    # 2. TABEL RINGKAS DI HALAMAN UTAMA
    # ==========================================
    st.subheader("1. Ringkasan Tabel Prediksi Terbaru")
    display_df = df_latest[['comment_id', 'predicted_label', 'score', 'model_version']]
    st.dataframe(display_df, use_container_width=True)

    # ==========================================
    # 3. PANEL DETAIL KOMENTAR & FORM KOREKSI
    # ==========================================
    st.subheader("2. Panel Detail Komentar & Koreksi")
    selected_id = st.selectbox("Pilih Comment ID untuk melihat detail lengkap:", df_latest['comment_id'].tolist())

    if selected_id:
        row = df_latest[df_latest['comment_id'] == selected_id].iloc[0]
        platform_name = get_platform_info(row['comment_id'])

        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**Comment ID:** `{row['comment_id']}`")
            st.markdown(f"**Prediksi Model:** `{row['predicted_label']}`")
            
            # Tampilkan label aktif saat ini (bisa dari prediksi awal atau riwayat koreksi)
            active_label = current_label(conn, row['comment_id'])
            st.markdown(f"**Label Saat Ini:** `{active_label}`")

            formatted_score = score_text(row['score'], row['score_type'])
            st.markdown(f"**Jenis Skor:** {formatted_score}")
        with col2:
            st.markdown(f"**Versi Model:** `{row['model_version']}`")
            st.markdown(f"**Waktu Prediksi:** `{row['predicted_at']}`")

        st.markdown("**Teks Asli Komentar:**")
        st.info(row['text_original'] if pd.notna(row['text_original']) else "Teks tidak tersedia")

        st.write(f"Platform: **{platform_name}** | Sumber Data: Internal Dataset (`{row['comment_id']}`)")

        # ==========================================
        # FORM KOREKSI
        # ==========================================
        st.markdown("### 📝 Formulir Koreksi Label")
        
        with st.form("correction_form"):
            col_f1, col_f2 = st.columns(2)
            with col_f1:
                new_label = st.selectbox("Pilih Label Baru:", ["positif", "negatif", "netral"])
            with col_f2:
                reviewer_id = st.selectbox("ID Pemeriksa:", ["reviewer_azza", "reviewer_01", "reviewer_02"])
            
            reason = st.text_area("Alasan Koreksi (Minimal 5 karakter):", placeholder="Tuliskan alasan mengapa label ini dikoreksi...")
            
            submitted = st.form_submit_button("Simpan Koreksi")
            
            if submitted:
                try:
                    prediction_id = int(row['id']) if 'id' in row and pd.notna(row['id']) else 1
                    add_verification(
                        conn=conn,
                        comment_id=row['comment_id'],
                        prediction_id=prediction_id,
                        new_label=new_label,
                        reason=reason,
                        reviewer_id=reviewer_id
                    )
                    timestamp_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    st.success(f"Koreksi berhasil disimpan pada {timestamp_now}! Label baru: **{new_label}** (Pemeriksa: {reviewer_id})")
                except ValueError as ve:
                    st.error(f"Validasi Gagal: {ve}")
                except Exception as e:
                    st.error(f"Terjadi kesalahan pada basis data: {e}")

        # ==========================================
        # 📜 TAMBAHAN LANGKAH 1 HARI 23: TABEL RIWAYAT
        # ==========================================
        st.markdown("---")
        st.subheader("📜 Riwayat Koreksi Komentar Ini")

        verification_columns = pd.read_sql(
            "PRAGMA table_info(verification_history)", conn
        )["name"].tolist()
        history_order = (
            "history_id DESC, verified_at DESC"
            if "history_id" in verification_columns
            else "verified_at DESC"
        )
        if {"previous_label", "new_label", "reason", "reviewer_id"} <= set(verification_columns):
            history_query = """
                SELECT verified_at AS 'Waktu',
                       previous_label || ' → ' || new_label AS 'Perubahan Label',
                       reason AS 'Alasan',
                       reviewer_id AS 'Reviewer'
                FROM verification_history
                WHERE comment_id = ?
                ORDER BY {history_order}
            """
        else:
            history_query = """
                SELECT verified_at AS 'Waktu',
                       label AS 'Perubahan Label',
                       '-' AS 'Alasan',
                       '-' AS 'Reviewer'
                FROM verification_history
                WHERE comment_id = ?
                ORDER BY {history_order}
            """
        df_history = pd.read_sql(
            history_query.format(history_order=history_order),
            conn,
            params=(selected_id,),
        )

        if not df_history.empty:
            st.dataframe(df_history, use_container_width=True)
        else:
            st.info("Belum ada riwayat koreksi untuk komentar ini.")

conn.close()
