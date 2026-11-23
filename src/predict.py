import os
import json
import sqlite3
from datetime import datetime
from transformers import pipeline

def load_model():
    """Memuat model dan tokenizer klasifikasi sentimen dari direktori penyimpanan."""
    card_path = "models/selected/model_card.json"
    with open(card_path, "r", encoding="utf-8") as f:
        card = json.load(f)
    clf = pipeline("text-classification", model=card["model_id"], revision=card["revision"], device=-1, truncation=True, max_length=card["max_length"])
    return clf, card

def map_english_to_indo(model_label):
    """Memetakan label prediksi model berbahasa Inggris ke kategori sentimen bahasa Indonesia."""
    lbl = str(model_label).upper().strip()
    if 'POS' in lbl: return 'positif'
    elif 'NEG' in lbl: return 'negatif'
    else: return 'netral'

def predict_and_store(conn, comment_ids):
    """Menjalankan prediksi sentimen pada komentar dan menyimpan hasilnya ke basis data."""
    if not comment_ids: return 0
    clf, card = load_model()
    cursor = conn.cursor()
    placeholders = ','.join(['?'] * len(comment_ids))
    cursor.execute(f"SELECT comment_id, text_original, text_content FROM comments WHERE comment_id IN ({placeholders})", comment_ids)
    rows = cursor.fetchall()
    if not rows: return 0
    ids = [r[0] for r in rows]
    texts = [r[1] if r[1] is not None and str(r[1]).strip() else r[2] for r in rows]
    outputs = clf(texts, batch_size=16)
    labels, scores = [map_english_to_indo(o["label"]) for o in outputs], [o["score"] for o in outputs]
    run_id = f"run-{datetime.now():%Y%m%d-%H%M%S}"
    predicted_at = datetime.now().isoformat(timespec="seconds")
    model_name, model_version, score_type = card.get("model_id"), card.get("experiment_id"), card.get("score_type", "softmax")
    rows_to_insert = [(cid, model_name, model_version, lab, sc, score_type, predicted_at, run_id) for cid, lab, sc in zip(ids, labels, scores)]
    cursor.executemany("INSERT INTO predictions (comment_id, model_name, model_version, predicted_label, score, score_type, predicted_at, run_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", rows_to_insert)
    conn.commit()
    return len(rows_to_insert)
