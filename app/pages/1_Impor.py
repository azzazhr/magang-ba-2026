import os
import streamlit as st
import pandas as pd
import sys

# Menambahkan path src agar dapat diimpor
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from src.db import get_conn, init_db
from src.importer import import_posts, import_comments
from src.quality import check_required, check_rows

st.title("Impor Data v0 ke Database SQLite")
st.write("Unggah file CSV (Posts atau Comments) untuk dimasukkan ke dalam database aplikasi.")

# Pastikan tabel sudah terinisialisasi
init_db()

# Pilih jenis data yang akan diimpor
data_type = st.radio("Jenis Data:", ["Posts", "Comments"])
uploaded_file = st.file_uploader(f"Pilih file CSV {data_type}", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    
    # Validasi khusus jika memilih Comments
    if data_type == "Comments":
        # 1. Cek Kolom Wajib (check_required)
        missing_cols = check_required(df)
        if missing_cols:
            st.error(f"❌ File ditolak! Kolom wajib berikut hilang dari file: {', '.join(missing_cols)}")
            st.stop() # Hentikan eksekusi jika kolom tidak lengkap
        else:
            st.success("✔ Kolom wajib lengkap.")
            
        # 2. Cek Baris Kosong / ID Kosong (check_rows)
        row_problems = check_rows(df)
        if row_problems:
            st.warning("⚠️ Ditemukan beberapa catatan masalah baris data:")
            df_prob = pd.DataFrame(row_problems, columns=["ID / Baris", "Masalah"])
            st.dataframe(df_prob)
    
    st.subheader("Pratinjau 5 Baris Pertama")
    st.dataframe(df.head(5))

    if st.button(f"Mulai Impor {data_type}"):
        conn = get_conn()
        with st.spinner("Sedang memproses impor data..."):
            if data_type == "Posts":
                res = import_posts(conn, df)
            else:
                # Gabungkan informasi split jika ada di manifest
                if "manifest_v0.csv" in os.listdir("data/splits") and "split" not in df.columns:
                    manifest = pd.read_csv("data/splits/manifest_v0.csv")
                    df = df.merge(manifest[["comment_id", "split"]], on="comment_id", how="left")
                res = import_comments(conn, df)
        conn.close()

        st.success("Impor selesai!")
        col1, col2, col3 = st.columns(3)
        col1.metric("Diterima", res["diterima"])
        col2.metric("Dilewati (Duplikat)", res["dilewati"])
        col3.metric("Ditolak", len(res["ditolak"]))

        if res["ditolak"]:
            st.warning("Daftar Baris Ditolak:")
            df_rejected = pd.DataFrame(res["ditolak"], columns=["ID", "Alasan"])
            st.dataframe(df_rejected)
