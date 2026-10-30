# Skrip Evaluasi Akhir pada Test Set
# Catatan: Skrip ini disiapkan sesuai protokol Hari 18 dan BELUM dijalankan hari ini.

import json
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from transformers import pipeline

def main():
    print("Memuat model terpilih dan konfigurasi...")
    with open("models/selected/model_card.json", "r", encoding="utf-8") as f:
        selected_card = json.load(f)

    # Muat dataset & lakukan split konsisten untuk mendapatkan test_df
    df_comments = pd.read_csv("data/processed/comments_v1.csv")
    text_col = 'text_original'
    label_col = 'sentiment_label'
    
    df_clean = df_comments.dropna(subset=[text_col, label_col]).copy()
    df_clean['reference_label'] = df_clean[label_col]

    train_val, test_df = train_test_split(
        df_clean, test_size=0.15, random_state=42, stratify=df_clean['reference_label']
    )

    texts_test = test_df[text_col].tolist()
    true_test_labels = test_df['reference_label'].astype(str).str.lower().str.strip().tolist()

    print(f"Jumlah data test (test_df): {len(test_df)}")

    # Inisialisasi pipeline dengan model terpilih (T3)
    clf = pipeline(
        "text-classification",
        model=selected_card["model_id"],
        revision=selected_card["revision"],
        device=-1,
        truncation=True,
        max_length=selected_card["max_length"]
    )

    print("Menjalankan inferensi pada test set...")
    outputs = clf(texts_test, batch_size=16)

    def map_english_to_indo(model_label):
        lbl = str(model_label).upper().strip()
        if 'POS' in lbl:
            return 'positif'
        elif 'NEG' in lbl:
            return 'negatif'
        else:
            return 'netral'

    preds_test = [map_english_to_indo(o["label"]) for o in outputs]
    
    acc_test = accuracy_score(true_test_labels, preds_test)
    print(f"Akurasi Test Set: {acc_test:.4f}")
    print("
Classification Report Test Set:")
    print(classification_report(true_test_labels, preds_test, zero_division=0))

if __name__ == "__main__":
    # Peringatan: Jangan jalankan fungsi main() ini sebelum tahap final pengujian!
    print("Skrip evaluasi test set siap. Belum dieksekusi sesuai protokol Hari 18.")
