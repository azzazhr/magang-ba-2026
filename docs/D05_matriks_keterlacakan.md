# Matriks Keterlacakan Kebutuhan Fungsional & Pengujian (Bab 3.6)
**Diperbarui:** Hari 31 · Rabu, 18 November 2026  
**Penyusun:** Azzahra Attaqina  
**Referensi Test Case:** `tests/test_cases.xlsx`  

---

## Pemetaan Kebutuhan Fungsional (KF) ↔ Fitur ↔ Tabel DB ↔ Test Case

| Kode KF | Fitur Aplikasi | Deskripsi Kebutuhan Fungsional | Tabel Basis Data Terkait | Test Case Terkait | Jenis Pengujian |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **KF-01** | **A. Impor** | Sistem mampu menerima unggahan file CSV *posts* dan *comments* sesuai skema kolom wajib dan format encoding UTF-8 yang valid. | `posts`, `comments` | `TC-01`, `TC-02`, `TC-03` | Positif & Negatif |
| **KF-02** | **B. Pemeriksaan Kualitas** | Sistem mampu memvalidasi integritas relasi (`post_id`), validitas tanggal, kelayakan teks, serta mencegah duplikasi data saat impor ulang. | `posts`, `comments` | `TC-02`, `TC-04`, `TC-05`, `TC-06` | Positif & Negatif |
| **KF-03** | **C. Pencarian & Filter** | Sistem mampu menyaring data komentar berdasarkan kombinasi platform, rentang tanggal, kategori, serta kata kunci teks secara akurat. | `posts`, `comments` | `TC-07`, `TC-08` | Positif |
| **KF-04** | **D. Analisis Sentimen** | Sistem mampu menjalankan inferensi sentimen model IndoBERT (`T3_indobert_len64`) pada subset komentar layak dan menyimpan riwayat *run* tanpa menimpa hasil lama. | `comments`, `predictions` | `TC-09`, `TC-10` | Positif |
| **KF-05** | **E. Verifikasi Manusia** | Sistem mampu mencatat koreksi label manual beserta identitas pemeriksa dan alasan wajib ke riwayat audit tanpa mengubah prediksi asli AI. | `predictions`, `verification_history` | `TC-11`, `TC-12` | Positif & Negatif |
| **KF-06** | **F. Dashboard** | Sistem mampu menampilkan ringkasan metrik dan grafik visual pada mode prediksi maupun verifikasi secara konsisten dengan basis data. | `posts`, `comments`, `predictions`, `verification_history` | `TC-13` | Positif |
| **KF-07** | **G. Ekspor** | Sistem mampu mengekspor dataset komentar terfilter sesuai kontrak kolom bebas identitas pribadi beserta file manifest metadata versi data dan model. | `posts`, `comments`, `predictions`, `verification_history` | `TC-14`, `TC-15` | Positif |

---

## Ringkasan Cakupan Keterlacakan
* **Total Kebutuhan Fungsional (KF):** 7 Modul Utama (`KF-01` s.d. `KF-07`, mencakup seluruh fitur **A–G**).
* **Total Skenario Uji (`Test Case`):** 15 Skenario (`TC-01` s.d. `TC-15`), terdiri dari **9 kasus positif** dan **6 kasus negatif** (`TC-02`, `TC-03`, `TC-04`, `TC-05`, `TC-08` variasi nol hasil, dan `TC-12`).
* **Status Keterlacakan:** 100% seluruh `KF` memiliki minimal satu *test case* terhubung.
