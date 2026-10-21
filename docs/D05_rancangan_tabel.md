# Rancangan Tabel Database v1.0 (Berdasarkan Bab 4.4 & Temuan Pilot)

## 1. Tabel `posts`

Tabel ini menyimpan data sumber unggahan agar konteks setiap komentar tidak hilang.

- **post_id** (String, Wajib, PK): ID unik unggahan. Contoh: `IG-P001`
- **platform** (String, Wajib): Sumber platform media sosial. Contoh: `Instagram`, `TikTok`
- **url** (String, Wajib): Tautan asli menuju unggahan. Contoh: `https://www.instagram.com/p/xxx/`
- **published_at** (Datetime, Wajib): Waktu unggahan diterbitkan.

## 2. Tabel `comments`

Tabel ini menyimpan teks komentar mentah hasil ekstraksi/scraping.

- **comment_id** (String, Wajib, PK): ID unik untuk setiap komentar. Contoh: `C001`
- **post_id** (String, Wajib, FK): Relasi ke tabel `posts`.
- **text_content** (Text, Wajib): Isi asli komentar dari pengguna.
- **eligibility_status** (String, Wajib): Penanda apakah data layak dipakai atau tidak (contoh: `Layak` atau `Eksklusi`).
  - _Temuan Pilot:_ Perlu status "Eksklusi" untuk menyaring komentar bot/spam ("cek ig kita kak") atau duplikat yang banyak ditemukan saat pendataan manual.

## 3. Tabel `predictions`

Tabel ini menyimpan hasil skor dan label awal yang diberikan oleh sistem/model AI sebelum divalidasi.

- **prediction_id** (String, Wajib, PK): ID unik hasil prediksi. Contoh: `PR-001`
- **comment_id** (String, Wajib, FK): Relasi ke tabel `comments`.
- **predicted_label** (String, Wajib): Keputusan sentimen dari mesin. Contoh: `Positif`, `Negatif`, `Netral`.
- **confidence_score** (Float, Tidak Wajib): Nilai tingkat keyakinan model (dari 0.0 hingga 1.0).

## 4. Tabel `verification_history`

Tabel ini menelusuri jejak perubahan label secara manual agar riwayatnya (audit trail) tetap ada.

- **history_id** (Integer/Auto-increment, Wajib, PK): ID berurutan dari riwayat. Contoh: `1`, `2`
- **comment_id** (String, Wajib, FK): Relasi ke komentar yang divalidasi.
- **final_label** (String, Wajib): Label akhir yang diputuskan oleh manusia (Azza).
- **reasoning_rule** (String, Tidak Wajib): Catatan/alasan khusus mengapa label diubah.
  - _Temuan Pilot:_ Digunakan untuk mencatat kasus khusus seperti sentimen terbalik karena sarkasme (`SULIT-SARKASME`) atau penggunaan istilah khas Malang (`BAHASA-DAERAH`).
- **verified_at** (Timestamp, Wajib): Waktu validasi manual dilakukan.

## Penjelasan Logika Label Terbaru

Setiap koreksi atau validasi label sentimen yang dilakukan secara manual tidak akan menimpa data yang sudah ada, melainkan disimpan sebagai baris data baru di dalam tabel `verification_history`. Untuk menentukan label final saat ini, sistem akan memanggil baris data dengan penanda waktu (`verified_at`) yang paling akhir atau terbaru untuk `comment_id` tersebut. Sementara itu, prediksi awal dari sistem (AI) tetap dipertahankan dengan aman di tabel `predictions` agar perbedaan akurasi antara mesin dan manusia tetap dapat dihitung dan dianalisis.
