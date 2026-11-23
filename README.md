# Aplikasi Analisis Konten dan Sentimen Media Sosial

Aplikasi web berbasis **Streamlit** dan **IndoBERT** untuk membantu dosen dan peneliti Laboratorium Business Analytics mengimpor, memeriksa kualitas data, mencari, menganalisis sentimen, memverifikasi, serta mengekspor data unggahan dan komentar media sosial resmi Pemprov Jawa Timur.

---

## 1. Prasyarat Sistem
- **Python:** versi `3.10` – `3.13`
- **Sistem Operasi:** Windows 10/11, macOS, atau Linux
- **Koneksi Internet:** Diperlukan saat pertama kali mengunduh bobot model dari Hugging Face (`crypter70/IndoBERT-Sentiment-Analysis`) jika belum tersimpan di cache lokal.

---

## 2. Instalasi & Konfigurasi Awal

1. **Buka terminal di direktori utama proyek**, lalu buat dan aktifkan lingkungan virtual (*virtual environment*):
   - **Windows (Command Prompt / PowerShell):**
     ```bash
     python -m venv .venv
     .venv\Scripts\activate
     ```
   - **macOS / Linux:**
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```

2. **Instal seluruh dependensi paket:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Siapkan berkas konfigurasi lingkungan (`.env`):**
   Salin `.env.example` menjadi `.env` (opsional jika menggunakan pengaturan baku):
   ```bash
   copy .env.example .env      # Windows
   cp .env.example .env        # macOS / Linux
   ```

---

## 3. Inisialisasi Basis Data

Sebelum menjalankan aplikasi untuk pertama kali, buat struktur tabel SQLite (`posts`, `comments`, `predictions`, `verification_history`) dengan perintah:

```bash
python -m src.db
```

Perintah di atas akan membuat berkas basis data kosong di `data/app.db` dan menampilkan pesan:
`Database SQLite dan 4 tabel berhasil diinisialisasi.`

---

## 4. Menjalankan Aplikasi & Alur Penggunaan

1. **Jalankan server aplikasi Streamlit:**
   ```bash
   streamlit run app/Home.py
   ```
   Aplikasi akan terbuka otomatis di peramban pada alamat `http://localhost:8501`.

2. **Urutan Penggunaan Menu di Aplikasi:**
   1. **Impor (`1_Impor`):**
      - *Penting:* Unggah dan impor berkas **Posts** (`posts_*.csv`) terlebih dahulu sebelum berkas **Comments** (`comments_v1.csv`), karena tabel `comments` memiliki relasi *foreign key* terhadap `post_id`.
   2. **Data (`2_Data`):** Telusuri komentar, lakukan pencarian kata kunci, dan saring berdasarkan platform, rentang tanggal, maupun kategori konten.
   3. **Analisis (`3_Analisis`):** Jalankan inferensi sentimen (positif, netral, negatif) menggunakan model `crypter70/IndoBERT-Sentiment-Analysis` (`T3_indobert_len64`).
   4. **Verifikasi (`4_Verifikasi`):** Tinjau skor keyakinan prediksi dan lakukan koreksi label manual dengan pencatatan riwayat audit.
   5. **Dashboard (`5_Dashboard`):** Pantau ringkasan KPI, distribusi sentimen, kategori konten, dan tren mingguan komentar.
   6. **Ekspor (`6_Ekspor`):** Unduh data hasil penyaringan dalam format CSV beserta berkas metadata manifest JSON.

---

## 5. Struktur Direktori Proyek

```text
magang-ba-2026/
├── app/
│   ├── Home.py                 # Halaman utama aplikasi Streamlit
│   └── pages/                  # Halaman fitur (1_Impor s.d. 6_Ekspor)
├── data/
│   ├── raw/                    # Dataset mentah per batch
│   ├── processed/              # Dataset bersih siap impor (posts & comments_v1)
│   └── splits/                 # Manifest pembagian data latih/validasi/uji
├── docs/                       # Dokumentasi teknis, audit, dan laporan uji
├── exports/                    # Hasil ekspor CSV dan manifest JSON
├── models/                     # Konfigurasi & model_card.json model terpilih
├── src/                        # Modul inti (db, importer, quality, predict, verify, dashboard, export)
├── tests/                      # Pengujian otomatis (unit & integrasi)
├── .env.example                # Template variabel lingkungan
├── .gitignore                  # Daftar pengecualian berkas lokal & rahasia
├── requirements.txt            # Daftar dependensi Python beserta versinya
└── README.md                   # Panduan instalasi dan penggunaan aplikasi
```
