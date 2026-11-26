# Data Dictionary Final — Aplikasi Analisis Konten dan Sentimen Media Sosial

- **Versi Dokumen:** Final (`v1.0`)
- **Tanggal Pembaruan:** 27 November 2026
- **Basis Data Rujukan:** SQLite (`data/app.db`, skema didefinisikan pada `src/db.py`)
- **Kontrak Ekspor Rujukan:** `src/export.py` (`EXPORT_COLUMNS`, 21 kolom terstandar tanpa PII)

---

## Bagian 1: Skema Empat Tabel Utama Basis Data SQLite (`data/app.db`)

### 1.1 Tabel `posts` (Data Unggahan Induk)
Menyimpan metadata unggahan resmi dari akun media sosial Pemprov Jawa Timur.

| No | Nama Kolom | Tipe Data | Kunci / Batasan | Deskripsi | Contoh Nilai |
| :---: | :--- | :--- | :--- | :--- | :--- |
| 1 | `post_id` | `TEXT` | `PRIMARY KEY` | Pengenal unik unggahan lintas platform | `IG-P004` |
| 2 | `platform` | `TEXT` | Opsional | Nama platform media sosial sumber unggahan | `Instagram`, `TikTok` |
| 3 | `published_at` | `TEXT` | Opsional | Tanggal publikasi unggahan (format ISO / `DD-MM-YYYY`) | `2026-09-29` |
| 4 | `text_content` | `TEXT` | Opsional | Teks takarir (*caption*) atau deskripsi unggahan | `Capaian pembangunan infrastruktur Jatim...` |

---

### 1.2 Tabel `comments` (Data Komentar Pengguna)
Menyimpan teks komentar yang telah dibersihkan, dianonimisasi, dan dipetakan ke unggahan induknya.

| No | Nama Kolom | Tipe Data | Kunci / Batasan | Deskripsi | Contoh Nilai |
| :---: | :--- | :--- | :--- | :--- | :--- |
| 1 | `comment_id` | `TEXT` | `PRIMARY KEY` | Pengenal unik komentar pada dataset | `IG-P004-C001` |
| 2 | `post_id` | `TEXT` | `FOREIGN KEY` $ightarrow$ `posts(post_id)` | Referensi pengenal unggahan induk | `IG-P004` |
| 3 | `text_content` | `TEXT` | Opsional | Teks komentar hasil normalisasi/pembersihan | `Bojonegoro lanjutkan!` |
| 4 | `text_original` | `TEXT` | Opsional | Teks komentar asli setelah anonimisasi `@user` | `Bojonegoro..... Lanjutkan!` |
| 5 | `text_hash` | `TEXT` | Opsional | Nilai *hash* teks untuk deteksi duplikasi cepat | `a94a8fe5ccb19ba6...` |
| 6 | `published_at` | `TEXT` | Opsional | Tanggal publikasi unggahan/komentar rujukan | `2026-09-29` |
| 7 | `commented_at` | `TEXT` | Opsional | Tanggal waktu komentar dikirimkan pengguna | `2026-09-30` |
| 8 | `context_text` | `TEXT` | Opsional | Ringkasan topik atau konteks unggahan induk | `Prestasi dan kebanggaan daerah kabupaten/kota...` |
| 9 | `content_category` | `TEXT` | Opsional | Kategori tematik konten unggahan | `Infrastruktur`, `Pendidikan`, `Pelayanan Publik` |
| 10 | `is_eligible` | `INTEGER` | `1` = Layak, `0` = Tidak | Penanda kelayakan komentar untuk analisis sentimen | `1` |
| 11 | `status_eksklusi` | `TEXT` | Baku: `'Aktif'` | Status keikutsertaan baris dalam dataset analisis | `Aktif`, `Dieksklusi` |
| 12 | `alasan_eksklusi` | `TEXT` | Baku: `'Lolos'` | Keterangan alasan apabila komentar tidak diikutsertakan | `Lolos`, `Q03: ID duplikat` |
| 13 | `split` | `TEXT` | Baku: `'train'` | Pembagian himpunan data eksperimen model | `train`, `validation`, `test` |

---

### 1.3 Tabel `predictions` (Hasil Prediksi Model Sentimen)
Menyimpan keluaran inferensi otomatis dari model klasifikasi sentimen IndoBERT.

| No | Nama Kolom | Tipe Data | Kunci / Batasan | Deskripsi | Contoh Nilai |
| :---: | :--- | :--- | :--- | :--- | :--- |
| 1 | `prediction_id` | `INTEGER` | `PRIMARY KEY AUTOINCREMENT` | Pengenal unik catatan prediksi | `1` |
| 2 | `comment_id` | `TEXT` | `NOT NULL`, `FK` $ightarrow$ `comments(comment_id)` | Pengenal komentar yang diprediksi | `IG-P004-C001` |
| 3 | `model_name` | `TEXT` | Opsional | Nama repositori/arsitektur model yang digunakan | `crypter70/IndoBERT-Sentiment-Analysis` |
| 4 | `model_version` | `TEXT` | Opsional | ID eksperimen atau versi konfigurasi model | `T3_indobert_len64` |
| 5 | `predicted_label` | `TEXT` | Domain: `positif`, `netral`, `negatif` | Kelas sentimen hasil pemetaan prediksi model | `positif` |
| 6 | `score` | `REAL` | Rentang `0.0` – `1.0` | Skor probabilitas keyakinan kelas terpilih | `0.9015` |
| 7 | `score_type` | `TEXT` | Opsional | Jenis fungsi skor probabilitas model | `softmax` |
| 8 | `predicted_at` | `TEXT` | Format ISO-8601 | Stempel waktu saat prediksi dijalankan | `2026-11-23T13:52:22` |
| 9 | `run_id` | `TEXT` | Opsional | Pengenal sesi eksekusi inferensi *batch* | `run-20261123-135222` |

---

### 1.4 Tabel `verification_history` (Riwayat Koreksi & Audit Verifikasi)
Mencatat setiap perubahan label sentimen yang dilakukan secara manual oleh peneliti/verifikator.

| No | Nama Kolom | Tipe Data | Kunci / Batasan | Deskripsi | Contoh Nilai |
| :---: | :--- | :--- | :--- | :--- | :--- |
| 1 | `history_id` | `INTEGER` | `PRIMARY KEY AUTOINCREMENT` | Pengenal unik log riwayat verifikasi | `1` |
| 2 | `comment_id` | `TEXT` | `NOT NULL`, `FK` $ightarrow$ `comments(comment_id)` | Pengenal komentar yang diverifikasi | `IG-P004-C004` |
| 3 | `prediction_id` | `INTEGER` | `FK` $ightarrow$ `predictions(prediction_id)` | Referensi baris prediksi model sebelumnya | `4` |
| 4 | `previous_label` | `TEXT` | Opsional | Label sentimen sebelum dikoreksi | `netral` |
| 5 | `new_label` | `TEXT` | `NOT NULL` | Label sentimen baru hasil keputusan peninjau | `negatif` |
| 6 | `reason` | `TEXT` | Opsional | Alasan atau catatan pembenaran koreksi label | `Keluhan kondisi jalan berdebu jelas bernada negatif` |
| 7 | `reviewer_id` | `TEXT` | Opsional | Kode atau identitas peninjau/peneliti | `R1_Azzahra` |
| 8 | `verified_at` | `TEXT` | `NOT NULL` (ISO-8601) | Stempel waktu saat verifikasi disimpan | `2026-11-23T14:05:10` |

> **Catatan Tabel Pendukung:** Selain 4 tabel operasional di atas, `src/db.py` juga menyediakan tabel `annotators` (`annotator_id`, `name`) dan `annotations` (`annotation_id`, `comment_id`, `annotator_id`, `label`, `created_at`) untuk menyimpan arsip pelabelan manual awal.

---

## Bagian 2: Skema Kolom Ekspor CSV (`data.csv`) & Metadata Manifest

Setiap kali pengguna mengekspor data melalui halaman **6_Ekspor** (`src/export.py`), aplikasi menghasilkan berkas `data.csv` yang menggabungkan atribut unggahan, komentar, prediksi terbaru, dan hasil verifikasi dalam **21 kolom terstandar**. Kolom identitas pengguna (`username`, `user_name`, `author`, `user_id`) **dihapus otomatis** sebelum ekspor demi perlindungan privasi (PII).

| No | Nama Kolom Ekspor | Sumber / Asal Data | Tipe | Deskripsi |
| :---: | :--- | :--- | :--- | :--- |
| 1 | `comment_id` | `comments.comment_id` | `TEXT` | Pengenal unik komentar |
| 2 | `post_id` | `comments.post_id` | `TEXT` | Pengenal unik unggahan induk |
| 3 | `platform` | `posts.platform` | `TEXT` | Platform sumber (`Instagram` / `TikTok`) |
| 4 | `source_account` | Metadata unggahan | `TEXT` | Nama akun resmi instansi sumber (tanpa PII warga) |
| 5 | `post_url` | Metadata unggahan | `TEXT` | Tautan URL publik unggahan induk |
| 6 | `published_at` | `posts.published_at` | `TEXT` | Tanggal publikasi unggahan |
| 7 | `context_text` | `comments.context_text` | `TEXT` | Ringkasan konteks topik unggahan |
| 8 | `content_format` | Metadata unggahan | `TEXT` | Format media unggahan (foto, karosel, video/reels) |
| 9 | `content_category` | `comments.content_category` | `TEXT` | Kategori tematik konten unggahan |
| 10 | `commented_at` | `comments.commented_at` | `TEXT` | Tanggal komentar dikirimkan |
| 11 | `text_original` | `comments.text_original` | `TEXT` | Teks komentar yang sudah dianonimisasi |
| 12 | `split` | `comments.split` | `TEXT` | Pembagian himpunan data (`train` / `validation` / `test`) |
| 13 | `data_version` | Metadata dataset | `TEXT` | Versi paket dataset rujukan (contoh: `v1`) |
| 14 | `pred_label` | `predictions.predicted_label` | `TEXT` | Label sentimen prediksi model (`positif`, `netral`, `negatif`) |
| 15 | `pred_score` | `predictions.score` | `REAL` | Skor keyakinan prediksi model (`0.0` – `1.0`) |
| 16 | `score_type` | `predictions.score_type` | `TEXT` | Jenis skor probabilitas (`softmax`) |
| 17 | `model_version` | `predictions.model_version` | `TEXT` | Versi/ID eksperimen model (`T3_indobert_len64`) |
| 18 | `verified_label` | `verification_history.new_label` | `TEXT` | Label hasil verifikasi manual (kosong jika belum dikoreksi) |
| 19 | `verify_reason` | `verification_history.reason` | `TEXT` | Catatan alasan koreksi oleh verifikator |
| 20 | `reviewer_id` | `verification_history.reviewer_id` | `TEXT` | Identitas peninjau yang melakukan verifikasi |
| 21 | `verified_at` | `verification_history.verified_at` | `TEXT` | Stempel waktu tindakan verifikasi |

### Metadata Pendamping (`export_manifest.json`)
Bersamaan dengan `data.csv`, paket ZIP menyertakan `export_manifest.json` yang mencatat parameter keterlacakan (*reproducibility*): `exported_at`, `filters`, `n_rows`, `data_version`, `split_manifest`, `model_name`, `model_version`, `score_type`, `app_version`, dan daftar `columns`.
