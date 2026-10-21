# Data Dictionary v0 (Hari 09)
**Tanggal Penyusunan:** 19 Oktober 2026

Dokumen ini mendefinisikan struktur kolom untuk tabel master `posts_v0` dan `comments_v0` yang digunakan dalam sistem analisis bantuan sosial dan pemrosesan komentar.

---

## 1. Tabel `posts_v0` (Unggahan)
Tabel ini menyimpan metadata dari setiap unggahan (*post*) yang menjadi induk dari komentar-komentar terkumpul.

| Nama Kolom | Tipe Data | Wajib (Required) | Arti / Deskripsi | Nilai yang Diizinkan | Contoh Format |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `post_id` | String / Int | Ya | Identifikasi unik untuk setiap unggahan | Unique Identifier | `p_001`, `109283` |
| `platform` | String | Ya | Platform asal unggahan media sosial | `Instagram`, `TikTok`, dll. | `Instagram` |
| `published_at` | Datetime | Ya | Waktu unggahan dipublikasikan | Format ISO 8601 | `2026-10-19 08:30:00` |
| `text_content` | Text | Tidak | Teks deskripsi atau *caption* dari unggahan | Bebas / Teks | "Bantuan sosial tahap 2..." |

---

## 2. Tabel `comments_v0` (Komentar)
Tabel ini menyimpan data interaksi komentar dari para pengguna pada unggahan terkait.

| Nama Kolom | Tipe Data | Wajib (Required) | Arti / Deskripsi | Nilai yang Diizinkan | Contoh Format |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `comment_id` | String / Int | Ya | Identifikasi unik untuk setiap komentar | Unique Identifier | `c_001`, `987654` |
| `post_id` | String / Int | Ya | ID unggahan induk tempat komentar berada | Harus ada di `posts_v0` | `p_001`, `109283` |
| `text_content` | Text | Ya | Isi teks asli dari komentar pengguna | Bebas / Teks | "Bagaimana cara daftar bansos?" |
| `text_original` | Text | Ya | Salinan teks asli sebelum normalisasi | Bebas / Teks | "Bagaimana cara daftar bansos?" |
| `text_hash` | String | Ya | Nilai hash SHA-256 dari teks ternormalisasi | Kode Hash 64 karakter | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `published_at` | Datetime | Ya | Waktu komentar dipublikasikan | Format ISO 8601 | `2026-10-19 09:15:00` |
| `status_eksklusi` | String | Ya | Status kelayakan data komentar | `Aktif`, `E1`, `E3`, `E4`, `E5` | `Aktif` |
| `alasan_eksklusi` | String | Ya | Keterangan alasan jika data dikeluarkan | `Lolos`, nama kode eksklusi | `Lolos` |
