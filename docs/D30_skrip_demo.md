# Skrip Demonstrasi Aplikasi Dashboard Analisis Sentimen & Kebijakan Publik
**Hari/Tanggal:** Hari 30 · Selasa, 17 November 2026  
**Penyusun:** Azzahra Attaqina  
**Target Durasi:** 3–5 Menit per Skenario (Total ±12–15 Menit)  

---

## Skenario K1: Alur Masuk Data Baru hingga Inferensi Sentimen (Durasi: ~4 Menit)
* **Tujuan:** Memastikan data unggahan dan komentar publik baru dapat diimpor dengan validasi bersih, lalu diproses oleh model analisis sentimen secara otomatis.
* **Langkah:**
  1. Buka menu **Impor** di sidebar.
  2. Unggah file dataset *posts* dan *comments v1*, lalu klik **"Mulai Impor"**.
  3. Tunjukkan ringkasan jumlah data yang diterima (*accepted*) dan ditolak (*rejected*).
  4. Buka menu **Data** untuk memperlihatkan bahwa data baru sudah masuk tanpa duplikasi ID atau teks kosong.
  5. Buka menu **Analisis**, pilih versi model inferensi (`T3_indobert_len64`), lalu klik **"Jalankan Analisis"** dan tunggu hingga *progress bar* selesai.
* **Hasil yang Diharapkan:** Data baru tersimpan rapi di basis data SQLite, serta kolom prediksi, skor keyakinan, jenis skor, dan versi model terisi otomatis.

---

## Skenario K2: Pemantauan Tren & Distribusi Sentimen pada Dashboard (Durasi: ~4 Menit)
* **Tujuan:** Mengevaluasi gambaran makro opini masyarakat berdasarkan platform dan kategori kebijakan tertentu untuk melihat pola sentimen.
* **Langkah:**
  1. Buka menu **Dashboard** di sidebar.
  2. Jelaskan 5 kartu metrik utama di bagian atas (Total Unggahan, Komentar Layak, Diprediksi, Terverifikasi, dan Persentase Verifikasi).
  3. Terapkan filter interaktif di sidebar: pilih platform tertentu (mis. **YouTube** atau **Instagram**) dan pilih satu **Kategori Konten**.
  4. Tunjukkan perubahan grafik **Distribusi Sentimen** dan **Tren Mingguan**.
  5. Jelaskan cara membaca jenis skor (*confidence score* / margin model bukan probabilitas absolut) serta batasan keterwakilan sampel komentar publik.
* **Hasil yang Diharapkan:** Kartu metrik dan seluruh grafik visual memperbarui tampilan secara *real-time* sesuai filter yang dipilih.

---

## Skenario K3: Investigasi Komentar Negatif, Verifikasi Manual, & Ekspor (Durasi: ~4 Menit)
* **Tujuan:** Menemukan komentar negatif tentang layanan pendaftaran, meninjau konteks aslinya, melakukan koreksi label secara transparan, dan mengekspor bukti laporan.
* **Langkah:**
  1. Buka menu **Data** di sidebar.
  2. Masukkan kata kunci **`daftar`** pada kolom pencarian dan pilih filter label prediksi **`negatif`**.
  3. Buka dan baca **3 komentar** teratas yang muncul untuk memeriksa kesesuaian prediksi model dengan konteks kalimat asli.
  4. Salin satu ID komentar yang dirasa perlu dikoreksi, lalu buka menu **Verifikasi**.
  5. Isi formulir koreksi label (pilih label baru, masukkan ID reviewer, tuliskan alasan minimal 5 karakter), lalu klik **"Simpan Koreksi"**.
  6. Buka menu **Ekspor**, terapkan filter yang sama, dan klik tombol unduh laporan.
* **Hasil yang Diharapkan:** Daftar komentar negatif terkait layanan pendaftaran terfilter akurat, satu koreksi tercatat permanen di tabel `verification_history` (audit trail), dan file hasil ekspor terunduh lengkap dengan manifest.


---

## Catatan Hasil Gladi Bersih Mandiri (Langkah 2)
* **Waktu Pelaksanaan Gladi:** Selasa, 17 November 2026 · Pukul 10.15 – 10.40 WIB
* **Total Durasi Gladi:** ±12 Menit (Masing-masing skenario berada dalam rentang target 3–5 menit)

| Skenario | Durasi Aktual | Status Alur | Catatan Langkah Lambat / Membingungkan |
| :--- | :--- | :--- | :--- |
| **K1 (Impor → Analisis)** | ~4,5 menit | Lancar (1 catatan performa) | **Halaman Analisis terasa agak lama saat pertama kali dibuka** karena sistem memuat aset model inferensi (`T3_indobert_len64`) dan menyiapkan data pratinjau. **Trik saat demo:** buka atau *warm-up* halaman Analisis terlebih dahulu sebelum sesi demo dimulai agar *cache* memori siap. |
| **K2 (Dashboard & Filter)** | ~3,5 menit | Sangat Lancar | Perpindahan filter platform dan kategori konten memperbarui kartu metrik serta grafik dengan cepat tanpa kendala. |
| **K3 (Filter → Verifikasi → Ekspor)** | ~4 menit | Lancar | Pencarian kata kunci `"daftar"`, filter label negatif, verifikasi manual satu komentar, hingga unduh ekspor berjalan sesuai skrip. |

* **Bukti Tangkapan Layar Gladi:** `reports/evidence/D30_gladi_K3.png` *(pastikan 1–2 tangkapan layar gladi sudah disimpan di folder ini)*
