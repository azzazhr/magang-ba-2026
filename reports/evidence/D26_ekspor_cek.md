# Laporan Pemeriksaan Ekspor Data (D26)
*Tanggal: 11 November 2026*
*Nama: Azzahra Attaqina*

## 1. Ringkasan Pemeriksaan Kontrak Ekspor
* **Jumlah Kolom:** 21 kolom sesuai dengan kontrak baku `EXPORT_COLUMNS`.
* **Privasi PII:** Terverifikasi aman dan bebas dari atribut identitas pengguna (`username`, `user_name`, `author`).
* **Konsistensi Baris:** Jumlah baris dan pratinjau data di halaman `6_Ekspor.py` berjalan akurat sesuai parameter filter aktif.

## 2. Hasil Pemeriksaan Sampel dan Kesesuaian Database
* **Validasi Kontrak Kolom:** Seluruh 21 kolom terindeks dengan benar; kolom yang tidak memiliki data tetap dipertahankan dalam bentuk kosong (*NaN/Blank*) untuk menjaga struktur kontrak.
* **Kesesuaian 3 Baris Acak:** Berdasarkan pengujian sampel data acak dari fungsi `export_filtered`, label prediksi (`pred_label`) dan struktur metrik 100% konsisten dengan data asli di basis data SQLite (`data/sentiment.db`).
