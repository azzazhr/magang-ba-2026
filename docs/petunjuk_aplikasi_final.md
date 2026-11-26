# Petunjuk Penggunaan Aplikasi Final — Analisis Konten dan Sentimen Media Sosial

- **Versi Dokumen:** Final (`v1.0`)
- **Tanggal Rilis:** 27 November 2026
- **Penyusun:** Azzahra Attaqina (Laboratorium Business Analytics, Polinema)

---

## 1. Persiapan Lingkungan & Menjalankan Aplikasi

1. **Buka terminal** pada direktori proyek (`magang-ba-2026`) dan aktifkan lingkungan virtual:
   ```bash
   # Windows
   .venv\Scripts\activate

   # macOS / Linux
   source .venv/bin/activate
   ```

2. **Inisialisasi basis data SQLite** (hanya dilakukan saat pertama kali pemasangan atau saat mereset basis data):
   ```bash
   python -m src.db
   ```

3. **Jalankan antarmuka web Streamlit:**
   ```bash
   streamlit run app/Home.py
   ```

4. **Buka peramban** pada alamat `http://localhost:8501`.

---

## 2. Panduan Fitur per Halaman

### A. Halaman Utama (`Home`)
Menampilkan ringkasan tujuan aplikasi, status koneksi basis data SQLite (`data/app.db`), serta panduan singkat urutan alur kerja mulai dari impor data hingga ekspor laporan.

### B. Halaman Impor Data (`1_Impor`)
1. Pilih jenis data yang akan diunggah (**Posts** atau **Comments**).
2. Unggah **Posts** terlebih dahulu (mis. `posts_b1.csv`, `posts_b2.csv`, `posts_b3.csv`), periksa pratinjau 5 baris pertama, lalu klik **Mulai Impor Posts**.
3. Unggah **Comments** berikutnya (mis. `data/processed/comments_v1.csv`), tinjau laporan validasi kolom dan peringatan duplikasi (`Q03` ID duplikat / `Q08` teks duplikat), lalu klik **Mulai Impor Comments**.
4. Sistem secara idempotent akan menerima baris baru yang valid, melewati baris yang sudah tersimpan, dan mencatat alasan penolakan jika ada pelanggaran *foreign key* atau duplikasi.

### C. Halaman Eksplorasi & Filter Data (`2_Data`)
1. Gunakan panel **Filter Data Lanjutan** di bilah sisi kiri untuk menyaring komentar berdasarkan:
   - **Platform** (Instagram, TikTok, atau semua)
   - **Rentang Tanggal** (Dari Tanggal – Sampai Tanggal)
   - **Kategori Konten** (Infrastruktur, Pendidikan, Kesehatan, Pelayanan Publik, Transportasi, dll.)
   - **Kata Kunci Teks**
2. Tabel utama di sisi kanan menampilkan daftar komentar yang memenuhi kriteria secara *real-time*.

### D. Halaman Analisis Sentimen (`3_Analisis`)
1. Pastikan informasi model aktif menampilkan `crypter70/IndoBERT-Sentiment-Analysis` (`T3_indobert_len64`, `max_length: 64`, `score_type: softmax`).
2. Pilih cakupan sumber data komentar yang hendak dianalisis.
3. Klik tombol **Jalankan Analisis** dan tunggu bilah kemajuan hingga selesai.
4. Hasil prediksi (`positif`, `netral`, `negatif`), skor probabilitas, serta stempel waktu otomatis tersimpan ke tabel `predictions` dan ditampilkan pada pratinjau 10 riwayat prediksi terbaru.

### E. Halaman Verifikasi & Detail Prediksi (`4_Verifikasi`)
1. Tinjau tabel ringkasan hasil prediksi terbaru atau gunakan penyaring versi model di bilah kiri.
2. Pada **Panel Detail Komentar & Koreksi**, pilih `comment_id` untuk melihat teks komentar lengkap beserta konteks unggahan induknya.
3. Jika prediksi model perlu dikoreksi, pilih **Label Baru** (`positif`, `netral`, atau `negatif`), isi **ID Reviewer**, tuliskan **Alasan Koreksi**, lalu klik **Simpan Koreksi**.
4. Setiap koreksi tersimpan permanen sebagai jejak audit di tabel `verification_history`.

### F. Halaman Dashboard Ringkasan (`5_Dashboard`)
1. Gunakan panel **Filter Data Interaktif** di bilah sisi kiri (termasuk pilihan sumber label: *Prediksi model* atau *Label verifikasi*).
2. Amati kartu metrik KPI serta empat grafik utama: distribusi platform, distribusi kategori konten, distribusi sentimen, dan tren mingguan jumlah komentar.

### G. Halaman Ekspor Data (`6_Ekspor`)
1. Atur filter data yang ingin diunduh melalui panel samping.
2. Periksa pratinjau tabel ekspor (21 kolom terstandar tanpa identitas pribadi/PII).
3. Klik tombol unduh untuk memperoleh arsip ZIP yang berisi `data.csv` dan `export_manifest.json`.
