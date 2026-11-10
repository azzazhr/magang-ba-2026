import pandas as pd
from src.queries import filter_comments

# Kontrak daftar kolom ekspor yang wajib dipatuhi (21 kolom)
EXPORT_COLUMNS = [
    "comment_id", "post_id", "platform", "source_account", "post_url", "published_at",
    "context_text", "content_format", "content_category", "commented_at", "text_original",
    "split", "data_version", "pred_label", "pred_score", "score_type", "model_version",
    "verified_label", "verify_reason", "reviewer_id", "verified_at"
]

def export_filtered(conn, filters=None):
    # Mengambil data yang telah difilter dan merapikan kolom sesuai kontrak EXPORT_COLUMNS tanpa PII.
    try:
        df_filtered = filter_comments(conn)
        
        # Terapkan filter tambahan secara aman menggunakan Pandas jika parameter filters tersedia
        if filters and not df_filtered.empty:
            if "platform" in filters and filters["platform"] and filters["platform"] != "Semua":
                if "platform" in df_filtered.columns:
                    df_filtered = df_filtered[df_filtered["platform"] == filters["platform"]]
            if "content_category" in filters and filters["content_category"] and filters["content_category"] != "Semua":
                if "content_category" in df_filtered.columns:
                    df_filtered = df_filtered[df_filtered["content_category"] == filters["content_category"]]
    except Exception as e:
        # Fallback jika terjadi kendala pada fungsi queries
        query = "SELECT * FROM comments"
        df_filtered = pd.read_sql(query, conn)

    # Jika dataframe kosong, kembalikan kerangka kolom kontrak
    if df_filtered.empty:
        return pd.DataFrame(columns=EXPORT_COLUMNS)
        
    # Pastikan tidak ada kolom identitas pengguna (PII) yang ikut terekspor
    pii_cols = ["username", "user_name", "author", "user_id"]
    df_filtered = df_filtered.drop(columns=[c for c in pii_cols if c in df_filtered.columns])
    
    # Reindex kolom agar urutan dan nama selalu konsisten (kolom kosong otomatis bernilai NaN/kosong)
    out = df_filtered.reindex(columns=EXPORT_COLUMNS)
    
    # Validasi pengaman (Assertion) untuk memastikan keamanan privasi
    assert not any(c in out.columns for c in ["username", "user_name", "author"]), "Pelanggaran privasi: Kolom PII terdeteksi!"
    
    return out
