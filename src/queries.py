import pandas as pd


def infer_content_category(row):
    """Menentukan kategori konten komentar berdasarkan kata kunci pada teks terkait."""
    text = " ".join(
        ("" if pd.isna(row.get(column)) else str(row.get(column)))
        for column in ("context_text", "text_original", "text_content")
        if column in row
    ).lower()

    category_keywords = (
        ("Kesehatan", ("kesehatan", "rumah sakit", "puskesmas", "dokter", "obat", "bpjs")),
        ("Pendidikan", ("pendidikan", "sekolah", "kampus", "kuliah", "guru", "student", "lomba", "tahfidz")),
        ("Transportasi", ("transportasi", "jalan", "tol", "kereta", "bus", "angkot", "parkir", "mobilitas")),
        ("Infrastruktur", ("infrastruktur", "jembatan", "jalan", "bantuan air", "irigasi", "gedung", "banjir")),
        ("Pelayanan Publik", ("pelayanan", "pendaftaran", "layanan", "samsat", "kantor", "administrasi", "berkas", "surat")),
    )

    for category, keywords in category_keywords:
        if any(keyword in text for keyword in keywords):
            return category
    return "Pelayanan Publik"

def filter_comments(conn, platform=None, platforms=None, category=None, categories=None, 
                    start_date=None, date_from=None, end_date=None, date_to=None, 
                    label=None, label_source=None, keyword=None, **kwargs):
    """
    Fungsi filter_comments yang aman dari error keyword argument dan bebas nan.
    """
    selected_platforms = platforms if platforms is not None else platform
    if isinstance(selected_platforms, str):
        selected_platforms = [selected_platforms]
    selected_platforms = [
        value for value in (selected_platforms or []) if value and value != "Semua"
    ]

    selected_categories = categories if categories is not None else category
    if isinstance(selected_categories, str):
        selected_categories = [selected_categories]
    selected_categories = [
        value for value in (selected_categories or []) if value and value != "Semua"
    ]

    active_start = date_from if date_from is not None else start_date
    active_end = date_to if date_to is not None else end_date

    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    all_tables = [t[0] for t in cursor.fetchall()]

    # 1. Ambil seluruh data dari tabel comments (beserta platform dari posts jika ada)
    try:
        if "posts" in all_tables:
            query = """
                SELECT c.*, p.platform as post_platform
                FROM comments c
                LEFT JOIN posts p ON c.post_id = p.post_id
            """
        else:
            query = "SELECT c.* FROM comments c"
        df = pd.read_sql(query, conn)
    except Exception as e:
        print(f"Error reading comments: {e}")
        return pd.DataFrame()

    if df.empty:
        return df

    # 2. Normalisasi kolom platform
    if "platform" not in df.columns or df["platform"].isna().all():
        if "post_platform" in df.columns:
            df["platform"] = df["post_platform"]
        else:
            df["platform"] = "Instagram"

    # 3. Normalisasi teks agar tidak nan
    if "text_original" not in df.columns:
        df["text_original"] = None
    for column in ["text_original", "text_content", "context_text"]:
        if column in df.columns:
            df[column] = df[column].replace(
                r"^\s*(nan|none|null)?\s*$", pd.NA, regex=True
            )
    if "text_content" in df.columns:
        df["text_original"] = df["text_original"].fillna(df["text_content"])
    if "context_text" in df.columns:
        df["text_original"] = df["text_original"].fillna(df["context_text"])
    df["text_original"] = df["text_original"].fillna("Teks tidak tersedia")

    # 4. Normalisasi tanggal komentar
    df["commented_at"] = (
        df["commented_at"].copy()
        if "commented_at" in df.columns
        else pd.Series(pd.NA, index=df.index)
    )
    for col in ["published_at", "created_at"]:
        if col in df.columns:
            df["commented_at"] = df["commented_at"].fillna(df[col])
    if "commented_at" not in df.columns:
        df["commented_at"] = "2026-09-30"

    # Gunakan kategori yang tersimpan atau kategorikan data lama berdasarkan teks.
    if "content_category" not in df.columns:
        df["content_category"] = df.apply(infer_content_category, axis=1)
    else:
        df["content_category"] = df["content_category"].where(
            df["content_category"].notna()
            & df["content_category"].astype(str).str.strip().ne("")
            & df["content_category"].astype(str).str.lower().ne("nan"),
            pd.NA,
        )
        df["content_category"] = df["content_category"].fillna(
            df.apply(infer_content_category, axis=1)
        )

    if "is_eligible" not in df.columns:
        eligibility_column = (
            "status_eksklusi"
            if "status_eksklusi" in df.columns
            else "eligibility_status"
        )
        if eligibility_column in df.columns:
            df["is_eligible"] = df[eligibility_column].astype(str).str.lower().isin(
                ["aktif", "layak", "eligible", "lolos"]
            ).astype(int)
        else:
            df["is_eligible"] = 1
    else:
        eligibility_column = (
            "status_eksklusi"
            if "status_eksklusi" in df.columns
            else "eligibility_status"
        )
        eligible_by_status = (
            df[eligibility_column].astype(str).str.lower().isin(
                ["aktif", "layak", "eligible", "lolos"]
            ).astype(int)
            if eligibility_column in df.columns
            else pd.Series(1, index=df.index)
        )
        df["is_eligible"] = pd.to_numeric(
            df["is_eligible"], errors="coerce"
        ).fillna(eligible_by_status).astype(int)

    # 5. Terapkan Filter Platform
    if selected_platforms and "platform" in df.columns:
        df = df[df["platform"].isin(selected_platforms)]

    # 6. Terapkan Filter Kategori
    if selected_categories and "content_category" in df.columns:
        df = df[df["content_category"].isin(selected_categories)]

    # 7. Terapkan Filter Kata Kunci (Keyword)
    if keyword and keyword.strip() != "":
        kw = keyword.strip().lower()
        mask = df["text_original"].astype(str).str.lower().str.contains(kw, na=False)
        if "context_text" in df.columns:
            mask = mask | df["context_text"].astype(str).str.lower().str.contains(kw, na=False)
        df = df[mask]

    # 8. Gabungkan prediksi terbaru dan label verifikasi terbaru.
    if "predictions" in all_tables:
        prediction_query = """
            WITH ranked_predictions AS (
                SELECT comment_id, predicted_label,
                       ROW_NUMBER() OVER (
                           PARTITION BY comment_id
                           ORDER BY predicted_at DESC, prediction_id DESC
                       ) AS rn
                FROM predictions
            )
            SELECT comment_id, predicted_label AS model_label
            FROM ranked_predictions
            WHERE rn = 1
        """
        df_predictions = pd.read_sql(prediction_query, conn)
        df = df.merge(df_predictions, on="comment_id", how="left")
    else:
        df["model_label"] = None

    if "verification_history" in all_tables:
        verification_columns = pd.read_sql(
            "PRAGMA table_info(verification_history)", conn
        )["name"].tolist()
        verification_label_column = (
            "new_label" if "new_label" in verification_columns else "label"
        )
        verification_query = f"""
            WITH ranked_verifications AS (
                SELECT comment_id, {verification_label_column} AS verified_label,
                       ROW_NUMBER() OVER (
                           PARTITION BY comment_id
                           ORDER BY verified_at DESC
                       ) AS rn
                FROM verification_history
            )
            SELECT comment_id, verified_label
            FROM ranked_verifications
            WHERE rn = 1
        """
        df_verifications = pd.read_sql(verification_query, conn)
        df = df.merge(df_verifications, on="comment_id", how="left")
    else:
        df["verified_label"] = None

    for column in ["model_label", "verified_label"]:
        df[column] = df[column].where(df[column].notna(), None)
        df[column] = df[column].map(
            lambda value: value.strip().lower()
            if isinstance(value, str)
            else value
        )

    # 9. Terapkan filter sumber dan label sentimen.
    if label and label != "Semua":
        active_label = (
            "model_label"
            if label_source == "Prediksi model"
            else "verified_label"
        )
        df = df[df[active_label] == label.lower()]

    # 10. Filter Rentang Tanggal
    if "commented_at" in df.columns and not df.empty:
        if active_start:
            df = df[pd.to_datetime(df["commented_at"], errors='coerce').dt.date >= pd.to_datetime(active_start).date()]
        if active_end:
            df = df[pd.to_datetime(df["commented_at"], errors='coerce').dt.date <= pd.to_datetime(active_end).date()]

    # 11. Pilih kolom akhir yang dibutuhkan halaman Data dan Dashboard.
    desired_cols = [
        "comment_id", "platform", "content_category", "is_eligible",
        "commented_at", "text_original", "model_label", "verified_label"
    ]
    if "context_text" in df.columns:
        desired_cols.insert(3, "context_text")

    final_cols = [c for c in desired_cols if c in df.columns]
    return df[final_cols]


def latest_predictions(conn, model_version=None):
    """
    Mengambil prediksi terbaru per comment_id menggunakan pola ROW_NUMBER() window function di SQLite.
    """
    query = """
    WITH ranked_preds AS (
        SELECT
            p.prediction_id,
            p.comment_id,
            p.model_name,
            p.model_version,
            p.predicted_label,
            p.score,
            p.score_type,
            p.predicted_at,
            p.run_id,
            ROW_NUMBER() OVER (PARTITION BY p.comment_id ORDER BY p.predicted_at DESC) as rn
        FROM predictions p
        WHERE (:model_version IS NULL OR p.model_version = :model_version)
    )
    SELECT
        rp.prediction_id AS id,
        rp.comment_id,
        c.text_original,
        rp.predicted_label,
        rp.score,
        rp.score_type,
        rp.model_version,
        rp.predicted_at,
        rp.run_id
    FROM ranked_preds rp
    LEFT JOIN comments c ON rp.comment_id = c.comment_id
    WHERE rp.rn = 1
    """
    df = pd.read_sql(query, conn, params={"model_version": model_version})
    if "text_original" not in df.columns:
        df["text_original"] = pd.NA
    df["text_original"] = df["text_original"].fillna("Teks tidak tersedia")
    return df
