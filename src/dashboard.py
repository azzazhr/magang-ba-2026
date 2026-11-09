import pandas as pd

def get_summary_metrics(conn, model_version=None):
    """Mengambil 5 metrik utama berdasarkan struktur tabel aktual."""
    
    # 1. Total Unggahan / Total Komentar dasar
    try:
        total_posts = pd.read_sql("SELECT COUNT(DISTINCT comment_id) FROM comments", conn).iloc[0, 0]
    except Exception:
        total_posts = 0

    # 2. Komentar Layak (Total komentar)
    try:
        total_eligible = pd.read_sql("SELECT COUNT(*) FROM comments", conn).iloc[0, 0]
    except Exception:
        total_eligible = 0

    # 3. Komentar Diprediksi
    pred_sql = "SELECT COUNT(DISTINCT comment_id) FROM predictions"
    try:
        total_predicted = pd.read_sql(pred_sql, conn).iloc[0, 0]
    except Exception:
        total_predicted = 0

    # 4. Komentar Terverifikasi unik
    try:
        total_verified = pd.read_sql("SELECT COUNT(DISTINCT comment_id) FROM verification_history", conn).iloc[0, 0]
    except Exception:
        total_verified = 0

    # 5. Persentase Verifikasi
    verif_pct = (total_verified / total_predicted * 100) if total_predicted > 0 else 0.0

    return {
        "total_posts": total_posts,
        "total_eligible": total_eligible,
        "total_predicted": total_predicted,
        "total_verified": total_verified,
        "verif_pct": verif_pct
    }

def get_latest_verifications_df(conn):
    """Mengambil dataframe label verifikasi terbaru per komentar."""
    query = """
        WITH RankedVerification AS (
            SELECT comment_id, new_label, verified_at,
                   ROW_NUMBER() OVER(PARTITION BY comment_id ORDER BY verified_at DESC) as rn
            FROM verification_history
        )
        SELECT c.comment_id, c.text_original, v.new_label AS label
        FROM comments c
        JOIN RankedVerification v ON c.comment_id = v.comment_id AND v.rn = 1
    """
    return pd.read_sql(query, conn)

def get_latest_predictions_df(conn, model_version=None):
    """Mengambil dataframe prediksi model terbaru."""
    try:
        cols = pd.read_sql("PRAGMA table_info(predictions)", conn)['name'].tolist()
        label_col = 'predicted_label' if 'predicted_label' in cols else 'label'
    except Exception:
        label_col = 'predicted_label'

    query = f"""
        SELECT c.comment_id, c.text_original, p.{label_col} AS label
        FROM comments c
        JOIN predictions p ON c.comment_id = p.comment_id
    """
    return pd.read_sql(query, conn)
