# Laporan Rekapitulasi User Acceptance Testing (UAT) — Hari 33

- **Hari / Tanggal:** Jumat, 20 November 2026
- **Jumlah Pengguna Aktual:** **1 pengguna** (`U1`)
- **Total Skenario Diuji:** 3 skenario (`S1`, `S2`, `S3`)
- **Keterbatasan Pengujian:** Pengujian melibatkan **1 pengguna (`U1`)** karena keterbatasan ketersediaan partisipan pada jadwal evaluasi. Dengan jumlah partisipan tunggal, temuan usabilitas merepresentasikan alur berpikir dan kebiasaan navigasi satu profil pengguna saja, sehingga belum mencakup variasi tingkat literasi digital maupun perspektif dari peran pengguna lain.

---

## 1. Lembar Rekapitulasi UAT

| Pengguna | Skenario | Status | Waktu | Kendala dan Umpan Balik |
| :--- | :---: | :--- | :---: | :--- |
| U1 | S1 | Selesai mandiri | 23 detik | Sempat ragu 3–4 detik mengira pencarian berada di Dashboard sebelum pindah ke menu Data; setelah itu filter platform, kata kunci `"pendaftaran"`, dan bulan September berjalan lancar tanpa bantuan. |
| U1 | S2 | Selesai mandiri | 17 detik | Langsung membuka menu Verifikasi dan mengubah label sentimen yang tidak sesuai; tidak ada galat sistem, hanya perlu menambahkan filter label sentimen pada daftar verifikasi. |
| U1 | S3 | Selesai mandiri | 34 detik | Sempat mencari tombol ekspor di halaman Dashboard sebelum pindah ke menu Ekspor; unduhan CSV dan manifest JSON berhasil, namun istilah teknis di JSON dinilai kurang ramah pengguna awam dan filter ekspor belum mencakup rentang tanggal. |

---

## 2. Ringkasan Temuan & Umpan Balik

- **Tingkat Keberhasilan Tugas:** 3 dari 3 skenario (**100% Selesai mandiri**) dengan total waktu penyelesaian keseluruhan **74 detik (1 menit 14 detik)**.
- **Aspek Positif (Paling Membantu):** Fitur penyaringan cepat pada halaman **Data** serta ringkasan metrik persentase verifikasi otomatis pada halaman **Dashboard** dinilai sangat memangkas waktu rekapitulasi manual.
- **Titik Friksi & Kebingungan Antarmuka:**
  1. Pemisahan fungsi antara **Dashboard** (ringkasan), **Data** (pencarian detail), dan **Ekspor** (unduhan) sempat menimbulkan jeda navigasi singkat di awal skenario.
  2. Metadata teknis pada berkas manifest JSON (`T3_indobert_len64`) terasa kurang familiar bagi pengguna non-teknis.
- **Kebutuhan Peningkatan (Enhancement):**
  1. Penambahan filter rentang tanggal dan sumber label pada halaman **Ekspor** (`BUG-04` / peningkatan minor).
  2. Penambahan filter berdasarkan jenis label sentimen pada halaman **Verifikasi**.
- **Penerimaan Pengguna:** Pengguna menyatakan **bersedia** menggunakan aplikasi untuk pemantauan rutin karena alur audit riwayat prediksi dan koreksi manual jauh lebih terstruktur dibandingkan pengelolaan spreadsheet manual.

---

## 3. Pembaruan Daftar Bug (`docs/bug_list.csv`)
- Tidak ditemukan galat teknis (*crash* / *error*) baru selama sesi UAT `U1`.
- Satu temuan keterbatasan fungsionalitas minor dicatat sebagai **`BUG-04`** (penambahan filter rentang tanggal pada halaman Ekspor) ke dalam `docs/bug_list.csv`.
