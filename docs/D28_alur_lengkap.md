# Laporan Uji Alur Lengkap (End-to-End Workflow) - Day 28
**Tanggal:** 13 November 2026  
**Tester:** Azzahra Attaqina  

## Tabel Rekapitulasi Durasi, Jumlah Data, dan Kendala

| Tahap | Durasi | Jumlah Data | Kendala / Catatan |
| :--- | :--- | :--- | :--- |
| **Impor posts + comments** | 34 detik | 1000 komentar | Berjalan lancar pada basis data baru. |
| **Pemeriksaan kualitas** | 10 detik | 1000 komentar | Aman, tidak ada duplikasi ID dan struktur kolom valid. |
| **Pencarian dan filter** | 17 detik | 1615 komentar | Filter platform dan keyword responsif. |
| **Analisis sentimen** | 20 detik | 50 komentar | Model inference sukses mengeksekusi prediksi. |
| **Verifikasi (5)** | 1 menit 32 detik | 5 komentar terverifikasi | Pencatatan riwayat verifikasi sukses. |
| **Dashboard** | 20 detik | 1000 komentar | Metrik dan grafik ter-update real-time. |
| **Ekspor** | 5 detik | Semua platform & kategori | File CSV/Excel berhasil diunduh. |

## Catatan Pengujian
- Seluruh 7 tahap pengujian telah dijalankan secara berurutan di atas basis data kosong baru (`sentiment_d28.db`).
- Navigasi antar halaman aplikasi Streamlit berjalan dengan stabil tanpa error kritis.
