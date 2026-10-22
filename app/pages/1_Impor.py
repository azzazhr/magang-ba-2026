import streamlit as st
import pandas as pd
import sys
import os

# Menambahkan path src agar dapat diimpor
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from src.db import get_conn, init_db
from src.importer import import_posts, import_comments
from src.quality import check_required, check_rows, check_duplicates_and_conflicts

st.title("Impor Data v0 ke Database SQLite")
st.write("Unggah file CSV (Posts atau Comments) untuk dimasukkan ke dalam database aplikasi.")

# Pastikan tabel sudah terinisialisasi
init_db()

# Pilih jenis data yang akan diimpor
data_type = st.radio("Pilih Jenis Data:", ["Posts", "Comments"])
uploaded_file = st.file_uploader(f"Pilih file CSV {data_type}", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    
    # Validasi khusus jika memilih Comments
    if data_type == "Comments":
        # 1. Cek Kolom Wajib (check_required)
        missing_cols = check_required(df)
        if missing_cols:
            st.error(f"❌ File ditolak! Kolom wajib berikut hilang dari file: {', '.join(missing_cols)}")
            st.stop()
        else:
            st.success("✔ Kolom wajib lengkap.")
            
        # 2. Cek Baris Kosong / ID Kosong (check_rows)
        row_problems = check_rows(df)
        if row_problems:
            st.warning("⚠️ Ditemukan beberapa catatan masalah baris data:")
            df_prob = pd.DataFrame(row_problems, columns=["ID / Baris", "Masalah"])
            st.dataframe(df_prob)

        # 3. Cek Duplikasi di dalam file (Q03 & Q08)
        dup_in_file, dup_text, _, _ = check_duplicates_and_conflicts(df)
        if not dup_in_file.empty or not dup_text.empty:
            st.warning("⚠️ Peringatan Duplikasi Terdeteksi di dalam File:")
            if not dup_in_file.empty:
                st.write(f"- **Q03 (ID Duplikat):** Ditemukan {len(dup_in_file)} baris dengan `comment_id` ganda.")
            if not dup_text.empty:
                st.write(f"- **Q08 (Teks Duplikat per Post):** Ditemukan {len(dup_text)} baris dengan teks serupa pada pos yang sama.")

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
                
                # Ambil data existing dari database untuk pemeriksaan Q04 (konflik)
                existing_records = conn.execute("SELECT comment_id, text_hash FROM comments").fetchall()
                existing_dict = {r[0]: r[1] for r in existing_records} if existing_records else {}
                
                # Jalankan pemeriksaan terpadu (Q03, Q08, Q04)
                dup_in_file, dup_text, same, conflict = check_duplicates_and_conflicts(df, existing_dict)
                
                # Jalankan fungsi import utama
                res = import_comments(conn, df)
        conn.close()

        st.success("Impor selesai!")
        col1, col2, col3 = st.columns(3)
        col1.metric("Diterima", res["diterima"])
        col2.metric("Dilewati", res.get("dilewati", 0) + len(same))
        col3.metric("Ditolak", len(res["ditolak"]) + len(dup_in_file) + len(dup_text) + len(conflict))

        # Gabungkan daftar baris ditolak dengan temuan duplikat spesifik Hari 12
        all_rejected = list(res["ditolak"])
        for idx, row in dup_in_file.iterrows():
            all_rejected.append((row["comment_id"], "Q03: ID komentar duplikat di dalam file"))
        for idx, row in dup_text.iterrows():
            all_rejected.append((row["comment_id"], "Q08: Teks duplikat pada unggahan yang sama"))
        for idx, row in conflict.iterrows():
            all_rejected.append((row["comment_id"], "Q04: Konflik basis data (ID sama, isi berbeda)"))

        if all_rejected:
            st.warning("Daftar Baris Ditolak / Bermasalah:")
            df_rejected = pd.DataFrame(all_rejected, columns=["ID", "Alasan"])
            st.dataframe(df_rejected)
