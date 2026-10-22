import pandas as pd
import hashlib

# #Q01: Daftar kolom wajib (Required Columns) yang harus ada dalam file CSV komentar
REQUIRED_COMMENTS = [
    "comment_id",
    "post_id",
    "commented_at",
    "collected_at",
    "text_original",
    "eligibility_status",
    "data_version"
]

def hitung_hash_teks(teks):
    """Menghasilkan hash MD5 dari teks normalisasi (text_hash)."""
    if not isinstance(teks, str):
        return ""
    return hashlib.md5(teks.strip().lower().encode('utf-8')).hexdigest()

def check_required(df, required=REQUIRED_COMMENTS):
    """
    #Q01: Fungsi validasi kolom wajib.
    Mengembalikan daftar kolom wajib yang hilang dari DataFrame.
    Jika ada kolom yang kurang, seluruh file akan ditolak.
    """
    return sorted(set(required) - set(df.columns))

def check_rows(df):
    """
    #Q02 & #Q07: Fungsi validasi integritas baris data.
    - #Q02: Memeriksa apakah ada ID komentar yang kosong atau blank.
    - #Q07: Memeriksa apakah ada teks komentar asli yang kosong atau blank.
    """
    problems = []
    for r in df.itertuples():
        # #Q02: Periksa ID kosong
        comment_id_val = getattr(r, "comment_id", "")
        if not str(comment_id_val).strip():
            problems.append((r.Index, "Q02: ID kosong"))

        # #Q07: Periksa teks kosong
        text_val = getattr(r, "text_original", "")
        if not str(text_val).strip():
            ident = comment_id_val if str(comment_id_val).strip() else r.Index
            problems.append((ident, "Q07: teks kosong"))

    return problems

def check_duplicates_and_conflicts(df, existing_dict=None):
    """
    Pemeriksaan terpadu sesuai panduan Word:
    - #Q03: Duplikat ID di dalam file (dup_in_file)
    - #Q08: Teks duplikat pada unggahan yang sama memakai text_hash (dup_text)
    - #Q04: Data sudah ada / dilewati (same) & konflik basis data (conflict)
    """
    df_temp = df.copy()
    if "text_original" in df_temp.columns:
        df_temp["text_hash"] = df_temp["text_original"].map(hitung_hash_teks)
    else:
        df_temp["text_hash"] = ""

    # Q03: ID duplikat di dalam file
    dup_in_file = df_temp[df_temp.duplicated("comment_id", keep="first")] if "comment_id" in df_temp.columns else pd.DataFrame()

    # Q08: Teks duplikat pada unggahan yang sama (post_id & text_hash)
    if "post_id" in df_temp.columns and "text_hash" in df_temp.columns:
        dup_text = df_temp[df_temp.duplicated(["post_id", "text_hash"], keep="first")]
    else:
        dup_text = pd.DataFrame()

    same = pd.DataFrame()
    conflict = pd.DataFrame()

    # Q04: Pemeriksaan database (memakai existing_dict berformat {comment_id: text_hash})
    if existing_dict and isinstance(existing_dict, dict) and "comment_id" in df_temp.columns:
        same = df_temp[df_temp.comment_id.map(existing_dict.get) == df_temp.text_hash]
        conflict = df_temp[df_temp.comment_id.isin(existing_dict) & (df_temp.comment_id.map(existing_dict.get) != df_temp.text_hash)]

    return dup_in_file, dup_text, same, conflict
