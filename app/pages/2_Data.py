import os
import streamlit as st
import pandas as pd
import sys

# Menambahkan path src agar dapat diimpor
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from src.db import get_conn, init_db
from src.queries import search_comments

st.title("Pencarian Komentar & Eksplorasi Data")
st.write("Cari kata kunci pada isi komentar secara fleksibel (case-insensitive).")

init_db()

# Kotak pencarian
keyword = st.text_input("Masukkan kata kunci pencarian:", "")

if keyword:
    conn = get_conn()
    df_res = search_comments(conn, keyword)
    conn.close()
    
    count = len(df_res)
    st.write(f"Ditemukan {count} komentar")
    
    if count > 0:
        st.dataframe(df_res)
    else:
        st.info("Tidak ada komentar yang cocok dengan kata kunci tersebut.")
else:
    st.info("Silakan masukkan kata kunci di atas untuk mulai mencari.")
