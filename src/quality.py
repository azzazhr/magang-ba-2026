import pandas as pd

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
