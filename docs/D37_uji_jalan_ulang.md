# Laporan Uji Jalan Ulang (Clean Run) & Perbaikan README — Hari 37

- **Hari / Tanggal:** Kamis, 26 November 2026
- **Pelaksana:** Azzahra Attaqina
- **Pembimbing Lapangan:** Pak Rakhmat
- **Lingkungan Uji Bersih:** Salinan proyek tanpa `.venv` dan tanpa berkas basis data `.db` (`localhost:8501`)

---

## 1. Ringkasan Langkah Uji Jalan Ulang & Waktu Eksekusi

| Tahap Uji | Perintah / Aksi yang Dilakukan | Durasi | Status |
| :--- | :--- | :---: | :---: |
| 1. Persiapan Lingkungan Bersih | Menyalin paket kode tanpa `.venv` & `*.db`, membuat virtual environment baru (`python -m venv .venv`) | ~15 detik | Berhasil |
| 2. Instalasi Dependensi | Menjalankan `pip install -r requirements.txt` (7 paket terpasang) | ~2 menit 10 detik | Berhasil |
| 3. Inisialisasi Basis Data | Menjalankan `python -m src.db` untuk membentuk `data/app.db` (4 tabel) | < 1 detik | Berhasil |
| 4. Menjalankan Web App | Menjalankan `streamlit run app/Home.py` (`http://localhost:8501`) | ~3 detik | Berhasil |
| 5. Impor Data `v1` | Mengimpor `posts_b1.csv`, `posts_b2.csv`, `posts_b3.csv` lalu `comments_v1.csv` pada menu **Impor** | ~4 detik | Berhasil |
| 6. Analisis Sentimen | Menjalankan inferensi model `crypter70/IndoBERT-Sentiment-Analysis` (`T3_indobert_len64`) pada menu **Analisis** | ~12 detik | Berhasil |
| 7. Verifikasi & Dashboard | Memeriksa tabel prediksi pada **Verifikasi** dan seluruh grafik pada **Dashboard** | ~2 detik | Berhasil |

---

## 2. Kendala & Kekurangan `README.md` yang Ditemukan

1. **Instruksi instalasi dan menjalankan aplikasi belum tertulis:** `README.md` awal hanya berisi 1 paragraf deskripsi proyek tanpa langkah pembuatan `.venv`, instalasi `requirements.txt`, maupun perintah `streamlit run app/Home.py`.
2. **Perbedaan perintah inisialisasi basis data:** Contoh umum menggunakan `python -m src.db --init`, sedangkan skrip aktual `src/db.py` dijalankan langsung dengan perintah `python -m src.db`.
3. **Urutan wajib impor data belum dijelaskan:** Pengguna baru berisiko mengunggah `comments_v1.csv` sebelum `posts_*.csv`, yang akan ditolak oleh validasi *foreign key* `post_id`.

---

## 3. Hasil Perbandingan Data & Prediksi (Rujukan vs Clean Run)

### A. Perbandingan Jumlah Data & Validasi Kualitas Impor
- **Tabel `posts`:** Seluruh unggahan induk dari `posts_b1.csv`, `posts_b2.csv`, dan `posts_b3.csv` masuk utuh; percobaan unggah ulang mengonfirmasi perilaku *idempotent* (`0` diterima, `27` dan `74` baris duplikat dilewati).
- **Tabel `comments` (`comments_v1.csv`):** Validasi kualitas data berjalan konsisten dengan basis data rujukan: **1.000 komentar unik** diterima masuk ke database dan **1.185 baris duplikat** (`Q03` ID duplikat & `Q08` teks duplikat per pos) ditolak bersih.

### B. Perbandingan Sebaran Prediksi (50 Komentar Uji)
| Kelas Sentimen | Hasil Sebelumnya (Rujukan) | Hasil Clean Run (`localhost:8501`) | Selisih |
| :--- | :---: | :---: | :---: |
| **Positif** | 25 | 25 | 0 |
| **Netral** | 18 | 18 | 0 |
| **Negatif** | 7 | 7 | 0 |
| **Total** | **50** | **50** | **0 (Identik 100%)** |

### C. Pemeriksaan 20 Sampel Prediksi Acak
- Pemeriksaan pada 20 sampel prediksi acak (termasuk 10 baris teratas pada menu **Verifikasi**: `IG-P004-C001` s.d. `IG-P004-C010`) menunjukkan **100% label prediksi dan skor keyakinan identik** (contoh: `IG-P004-C001` = `positif` dengan skor `0.9015`, `IG-P004-C004` = `negatif` dengan skor `0.9999`, `IG-P004-C007` = `netral` dengan skor `0.9990`), karena model menggunakan revisi tetap (`T3_indobert_len64`) dan inferensi deterministik pada CPU.

---

## 4. Tindakan Perbaikan yang Dilakukan
- Memperbarui **`README.md`** dengan panduan lengkap langkah demi langkah (prasyarat sistem, pembuatan `.venv`, `pip install -r requirements.txt`, `python -m src.db`, `streamlit run app/Home.py`, peringatan urutan impor `posts` sebelum `comments`, serta struktur direktori proyek).
- Menguji ulang seluruh alur dari awal mengikuti `README.md` versi baru dan memastikan semua halaman (`Home`, `Impor`, `Data`, `Analisis`, `Verifikasi`, `Dashboard`, `Ekspor`) berjalan normal tanpa error.
