# Laporan Pemeriksaan Tiga Ekspor (D27)
*Tanggal: 12 November 2026*
*Nama: Azzahra Attaqina*

## 1. Ringkasan Pengujian Arsip Ekspor (E1, E2, E3)
* **E1.zip (Semua Data):** Berhasil menghasilkan arsip ZIP berisi `data.csv` dan `export_manifest.json` dengan total seluruh baris data secara lengkap.
* **E2.zip (Filter Platform - Instagram):** Berhasil menyaring data khusus platform Instagram, dengan jumlah baris dan metadata filter yang tercatat akurat di dalam file manifest.
* **E3.zip (Filter Kategori - Pelayanan Publik):** Berhasil menyaring data khusus kategori "Pelayanan Publik" sesuai dengan struktur data di basis SQLite.

## 2. Hasil Verifikasi Checklist
* **Setiap ekspor memiliki manifest:** Terverifikasi, setiap file ZIP menyertakan `export_manifest.json` yang memuat metadata waktu ekspor, filter, versi model (`v1.0`), dan daftar kolom.
* **Tiga ekspor diperiksa dan konsisten:** Struktur 21 kolom kontrak (`EXPORT_COLUMNS`) konsisten di semua arsip ZIP tanpa ada pergeseran urutan.
* **Versi data dan model tercantum:** Tercatat jelas di dalam manifest (`data_version: "v1"`, `model_version: "v1.0"`).
* **Tidak ada identitas pengguna:** Seluruh arsip bersih dari atribut PII (`username`, `author`, dll.) sesuai kebijakan privasi.
