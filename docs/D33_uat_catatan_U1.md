# Catatan Observasi User Acceptance Testing (UAT) — Pengguna U1

- **Hari / Tanggal:** Jumat, 20 November 2026
- **Kode Pengguna:** U1 (identitas dirahasiakan sesuai standar dokumentasi)
- **Pengamat:** Azzahra Attaqina
- **Tujuan Sesi:** Menguji kemudahan alur penggunaan dan kejelasan informasi pada aplikasi (bukan menguji kemampuan pengguna).

---

## 1. Observasi Eksekusi Skenario

### Skenario 1 (S1): Pencarian Komentar Spesifik
- **Tugas:** Menemukan komentar Instagram terkait kata kunci `"pendaftaran"` pada bulan September dan menyebutkan jumlah yang ditemukan.
- **Status:** Selesai mandiri
- **Waktu Pengerjaan:** 23 detik
- **Titik Ragu / Bingung:** Sempat ragu sekitar 3–4 detik di awal karena mengira pencarian detail komentar berada di halaman Dashboard, lalu segera berpindah ke menu **Data** di sidebar.
- **Galat / Error Sistem:** Tidak ada.
- **Bantuan yang Diberikan:** Tidak ada.

### Skenario 2 (S2): Verifikasi & Koreksi Label Sentimen
- **Tugas:** Memeriksa prediksi sentimen otomatis, mengubah label komentar yang kurang tepat, dan menyimpan alasan koreksi.
- **Status:** Selesai mandiri
- **Waktu Pengerjaan:** 17 detik
- **Titik Ragu / Bingung:** Langsung membuka halaman **Verifikasi**; sempat membaca keterangan batas minimal 5 karakter pada kolom alasan sebelum mengetik alasan koreksi.
- **Galat / Error Sistem:** Tidak ada.
- **Bantuan yang Diberikan:** Tidak ada.

### Skenario 3 (S3): Tinjauan Ringkasan & Ekspor Laporan
- **Tugas:** Meninjau ringkasan distribusi sentimen serta persentase data terverifikasi, lalu mengunduh berkas CSV dan manifest JSON.
- **Status:** Selesai mandiri
- **Waktu Pengerjaan:** 34 detik
- **Titik Ragu / Bingung:** Sempat mencari tombol unduh laporan di dalam halaman **Dashboard** selama beberapa detik sebelum menyadari bahwa fitur unduh berada di menu **Ekspor** pada sidebar.
- **Galat / Error Sistem:** Tidak ada.
- **Bantuan yang Diberikan:** Tidak ada.

---

## 2. Jawaban Wawancara Pasca-Uji (4 Pertanyaan)

1. **Bagian paling membantu:**
   > "Halaman **Data** dan **Dashboard** sangat membantu karena penyaringan berdasarkan platform, kata kunci, dan rentang tanggal berjalan cepat, sementara di Dashboard persentase komentar yang sudah diverifikasi langsung terlihat dalam satu layar tanpa perlu hitung manual."

2. **Bagian paling membingungkan:**
   > "Istilah teknis pada manifest ekspor (seperti format JSON dan label versi model `T3_indobert_len64`) agak membingungkan bagi pengguna awam yang hanya butuh laporan biasa. Selain itu, awalnya saya sempat mengira fitur pencarian komentar dan tombol unduh laporan berada langsung di dalam halaman Dashboard."

3. **Informasi yang dirasa masih kurang:**
   > "Di halaman **Ekspor**, pilihan filter baru terbatas pada Platform dan Kategori—akan lebih lengkap jika filter rentang tanggal dan status label (sudah diverifikasi atau prediksi model saja) juga tersedia sebelum mengunduh file. Selain itu, di halaman **Verifikasi** akan sangat membantu jika daftar komentar bisa difilter langsung berdasarkan label sentimennya (misalnya tampilkan yang 'negatif' saja)."

4. **Kesediaan memakai aplikasi secara rutin:**
   > "Ya, saya bersedia memakai aplikasi ini untuk pemantauan rutin karena alurnya jauh lebih rapi dan cepat dibandingkan memeriksa komentar secara manual di spreadsheet, terutama adanya fitur koreksi label yang tetap menyimpan riwayat prediksi awal sehingga mudah diaudit."
