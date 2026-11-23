# Laporan Uji Regresi Alur Utama — Hari 35

- **Hari / Tanggal:** Selasa, 24 November 2026
- **Penguji:** Azzahra Attaqina
- **Tujuan Pengujian:** Memastikan perbaikan bug dari Hari 34 (`BUG-01`, `BUG-02`, dan `BUG-03`) berjalan sesuai spesifikasi dan tidak menimbulkan regresi atau kerusakan pada fitur utama lainnya.

---

## 1. Ringkasan Uji Ulang Test Case Gagal Sebelumnya (`tests/test_cases.xlsx`)

| ID Kasus Uji | Bug Terkait | Area Fitur | Hasil Awal | Hasil Uji Ulang | Tanggal Uji Ulang |
| :---: | :---: | :--- | :---: | :---: | :---: |
| **TC-05** | BUG-01 | Impor Data (`src/importer.py`) — Validasi tanggal invalid (`Q05`) & luar rentang (`Q06`) | Gagal | **Lulus** | 2026-11-24 |
| **TC-07** | BUG-02 | Eksplorasi Data (`src/queries.py`) — Filter kombinasi platform & rentang tanggal | Gagal | **Lulus** | 2026-11-24 |
| **TC-15** | BUG-03 | Ekspor Data (`app/pages/6_Ekspor.py`) — Pembuatan & unduhan manifest JSON | Gagal | **Lulus** | 2026-11-24 |

---

## 2. Pengujian Regresi Alur Utama Aplikasi (End-to-End)

| Kode Regresi | Alur Utama yang Diuji | Metode & Skenario Uji | Hasil Aktual | Status |
| :---: | :--- | :--- | :--- | :---: |
| **R-01** | Koneksi & Integritas Basis Data | Membaca tabel `posts`, `comments`, dan `predictions` pada `data/sentiment.db` | Terbaca normal (`posts=120`, `comments=915`, `predictions=50`) tanpa korupsi skema | **Lulus** |
| **R-02** | Impor Ulang Data (Idempotency) | Mengimpor ulang 3 baris komentar yang sudah ada ke `import_comments()` | `diterima=0`, `dilewati=3` (tidak ada baris ganda) | **Lulus** |
| **R-03** | Pencarian & Penyaringan Data | Memanggil `filter_comments()` tanpa filter, filter platform `Instagram`, dan filter rentang tanggal | Query berjalan lancar (`total=915`, `IG=915`, `IG_Sep=813`) tanpa `TypeError` | **Lulus** |
| **R-04** | Pemisahan Prediksi Asli & Koreksi | Memeriksa struktur tabel prediksi model dan log verifikasi pada SQLite | Prediksi awal model tersimpan terpisah dari koreksi pengguna dan riwayat tercatat | **Lulus** |
| **R-05** | Ekspor CSV & Manifest JSON | Memverifikasi ketersediaan dan struktur JSON `exports/manifest_export_latest.json` | Berkas manifest JSON valid dan memuat metadata parameter ekspor | **Lulus** |

---

## 3. Kesimpulan Uji Regresi
- Seluruh **3 *test case* perbaikan (`TC-05`, `TC-07`, `TC-15`)** lulus pada pengujian ulang tanggal **24 November 2026**.
- Seluruh **5 skenario regresi alur utama (`R-01` s.d. `R-05`)** berjalan stabil tanpa galat baru maupun kerusakan pada fitur yang sudah berjalan sebelumnya.
