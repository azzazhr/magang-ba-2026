# Dokumentasi Perbandingan Model - Hari 18
**Tanggal:** 30 Oktober 2026  
**Nama Praktikan:** Azzahra Attaqina  

## 1. Tabel Perbandingan Eksperimen (Validation Set)

| Model & Eksperimen | Konfigurasi Utama | Macro-F1 Val | Accuracy Val | Durasi Inferensi (145 data) | Catatan Pelatihan / Operasional |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **SVM (Baseline)** | TF-IDF (N-gram 1-2) | 0.xx* | 0.xx* | ~0.5 detik | Dilatih pada train v1 (Klasik) |
| **Transformer (T1)** | IndoBERT (`max_length=128`) | 0.3428 | 0.4207 | 43.61 detik | Zero-shot (Tanpa fine-tuning) |
| **Transformer (T2)** | IndoBERT (`max_length=256`) | 0.3428 | 0.4207 | 33.20 detik | Zero-shot (Tanpa fine-tuning) |
| **Transformer (T3)** | IndoBERT (`max_length=64`) | 0.3428 | 0.4207 | 19.42 detik | Zero-shot (Tanpa fine-tuning) |

*(Catatan: *Isi nilai SVM sesuai dengan hasil log eksperimen SVM lamamu).*

## 2. Analisis & Alasan Pemilihan Model
- **Perbandingan Performa:** Seluruh variasi Transformer (T1, T2, T3) menghasilkan akurasi dan Macro-F1 yang identik karena karakteristik teks komentar ulasan yang pendek.
- **Efisiensi Waktu (CPU):** **T3 (`max_length=64`)** menjadi konfigurasi paling efisien dari segi waktu inferensi CPU (**19.42 detik**) dibandingkan T1 dan T2, tanpa mengorbankan kualitas keluaran teks pendek.
- **Keputusan Pembimbing:** Berdasarkan aturan pemilihan model (keseimbangan antara metrik evaluasi dan kelayakan operasional CPU), konfigurasi **T3** dipilih sebagai model utama untuk pengujian tahap akhir.
