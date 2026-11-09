import sqlite3
import pandas as pd

def filter_comments(conn, platform=None, category=None, start_date=None, end_date=None, label=None, label_source=None, keyword=None):
    """
    Fungsi filter_comments yang aman dari error kolom hilang (seperti post_id).
    """
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(comments);")
    columns_in_db = [col[1] for col in cursor.fetchall()]
    
    # Pilih kolom yang dipastikan ada di database
    cols_to_select = ["comment_id", "text_original", "sentiment_label as model_label"]
    if "platform" in columns_in_db:
        cols_to_select.append("platform")
    if "content_category" in columns_in_db:
        cols_to_select.append("content_category")
    if "commented_at" in columns_in_db:
        cols_to_select.append("commented_at")
    if "is_eligible" in columns_in_db:
        cols_to_select.append("is_eligible")
        
    query = f"SELECT {', '.join(cols_to_select)} FROM comments c WHERE 1=1"
    params = []
    
    if platform and platform != "Semua" and "platform" in columns_in_db:
        query += " AND c.platform = ?"
        params.append(platform)
        
    if category and category != "Semua" and "content_category" in columns_in_db:
        query += " AND c.content_category = ?"
        params.append(category)
        
    if keyword and keyword.strip() != "":
        query += " AND c.text_original LIKE ?"
        params.append(f"%{keyword.strip()}%")
        
    # Baca data utama
    df = pd.read_sql(query, conn, params=params)
    
    # Ambil label verifikasi secara terpisah jika tabelnya ada
    try:
        df_verif = pd.read_sql("SELECT comment_id, label as verified_label FROM verification_history", conn)
        if not df_verif.empty:
            df = df.merge(df_verif, on="comment_id", how="left")
    except Exception:
        df['verified_label'] = None

    # Filter berdasarkan label sentimen & sumbernya
    if label and label != "Semua":
        target_label = label.lower()
        if label_source == "Prediksi model":
            if 'model_label' in df.columns:
                df = df[df['model_label'].astype(str).str.lower() == target_label]
        elif label_source == "Label verifikasi":
            if 'verified_label' in df.columns:
                df = df[df['verified_label'].astype(str).str.lower() == target_label]
                
    return df
