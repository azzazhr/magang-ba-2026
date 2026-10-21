# Laporan Kualitas Data v0 (Hari 09)
**Tanggal Penyusunan:** 19 Oktober 2026

## 1. Ringkasan Eksekutif Pemrosesan Data
Penggabungan data dari seluruh batch (Pilot, Batch 1, Batch 2, dan Batch 3) menghasilkan basis data awal (*v0*) dengan rincian sebagai berikut:
* **Total Baris Mentah (Raw):** 2,152 komentar dan 124 postingan (*posts*)
* **Total Komentar Lolos (Layak Aktif):** 1,777 komentar
* **Total Komentar Dieksklusi:** 375 komentar

## 2. Rincian Eksklusi Berdasarkan Alasan
Berikut adalah rincian data yang dikeluarkan beserta alasannya:
* **E1_Duplicate_Comment_ID:** 214 baris (dikeluarkan karena duplikasi ID komentar yang identik).
* **E4_Orphan_Comment:** 150 baris (dikeluarkan karena `post_id` komentar tidak ditemukan pada master tabel `posts_v0`).
* **E3_Empty_Text:** 11 baris (dikeluarkan karena teks komentar kosong atau hanya berisi spasi).
* **E2_Duplicate_Text:** Ditangani pada tahap batch sebelumnya menggunakan *hash* SHA-256.

## 3. Evaluasi Target Kuantitatif
* Target minimal kumulatif data layak: **1,000 komentar**.
* Hasil aktual data layak: **1,777 komentar**.
* **Status:** Target tercapai dan terlampaui dengan aman (memenuhi syarat untuk dilanjutkan ke tahap pelabelan dan pemodelan).

## 4. Penanganan & Tindak Lanjut
* Data yang lolos disimpan ke `data/processed/comments_v0_audited.csv` dan `comments_v0.csv`.
* File data mentah (`data/raw/`) tetap dijaga keasliannya tanpa ada modifikasi (*frozen*).
