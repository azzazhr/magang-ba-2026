# Kamus Data (Data Dictionary v1.0)
## Bagian Kolom Ekspor (Export Schema Contract)

Berikut adalah daftar 21 kolom resmi yang menjadi kontrak baku untuk fitur ekspor data (`EXPORT_COLUMNS`):

| No | Nama Kolom (`EXPORT_COLUMNS`) | Deskripsi / Keterangan |
| :---: | :--- | :--- |
| 1 | `comment_id` | ID unik komentar |
| 2 | `post_id` | ID unik unggahan/postingan terkait |
| 3 | `platform` | Platform media sosial (Instagram, YouTube, dll.) |
| 4 | `source_account` | Akun sumber atau channel pemilik unggahan |
| 5 | `post_url` | Tautan/URL menuju unggahan asli |
| 6 | `published_at` | Tanggal dan waktu unggahan dipublikasikan |
| 7 | `context_text` | Teks konteks atau deskripsi unggahan |
| 8 | `content_format` | Format konten (video, carousel, teks, dll.) |
| 9 | `content_category` | Kategori isi konten (Infrastruktur, Layanan Publik, dll.) |
| 10 | `commented_at` | Tanggal dan waktu komentar ditulis |
| 11 | `text_original` | Teks asli komentar dari pengguna |
| 12 | `split` | Pembagian data (train/test/validation) |
| 13 | `data_version` | Versi dataset yang digunakan |
| 14 | `pred_label` | Label hasil prediksi model terbaru |
| 15 | `pred_score` | Skor keyakinan (*confidence score*) prediksi model |
| 16 | `score_type` | Jenis skor (probability, logit, dll.) |
| 17 | `model_version` | Versi model *machine learning* yang mengeksekusi prediksi |
| 18 | `verified_label` | Label hasil validasi/verifikasi manual terbaru |
| 19 | `verify_reason` | Alasan atau catatan koreksi dari validator |
| 20 | `reviewer_id` | ID unik validator/reviewer yang memeriksa |
| 21 | `verified_at` | Waktu saat verifikasi manual dilakukan |

*Kebijakan Keamanan:* Kolom identitas individu seperti `username`, `user_name`, atau `author` **dilarang keras** disertakan dalam ekspor data demi menjaga privasi.
