# Laporan Evaluasi Akhir - Hari 19
**Tanggal:** 2 November 2026  
**Nama Praktikan:** Azzahra Attaqina  

## 1. Ringkasan Performa Test Final
- **Model Terpilih:** IndoBERT (`T3`, `max_length=64`)
- **Akurasi Test Final:** 0.4384
- **Macro-F1 Test Final:** 0.3783
- **Durasi Inferensi:** 16.49 detik (146 sampel)

## 2. Tabel Kategori Kesalahan (Error Analysis)
| Kategori Kesalahan | Jumlah | Contoh Catatan |
| :--- | :---: | :--- |
| Sarkasme | - | Perlu penyesuaian konteks kiasan |
| Campuran Pujian-Kritik | - | Ulasan mengandung unsur pro dan kontra |
| Target Lain | - | Menyebut objek selain topik utama |
| Bahasa Daerah / Slang | - | Penggunaan bahasa informal/lokal |
| Butuh Konteks Unggahan | - | Memerlukan informasi teks pendukung |
| Label Acuan Meragukan | - | Variasi subjektivitas anotasi manusia |
| Lainnya / Ambigu | 30 | Model zero-shot kurang adaptif terhadap domain spesifik |
