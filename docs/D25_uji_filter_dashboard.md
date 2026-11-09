# Dokumentasi Uji Konsistensi Filter Dashboard Hari ke-25 (D25)
*Nama: Azzahra Attaqina*
*Proyek: Analisis Sentimen Kebijakan Publik*
*Tanggal: 10 November 2026*

## 1. Tujuan Pengujian
Pengujian ini dilakukan untuk memastikan bahwa:
1. Fungsi penyaringan data (`filter_comments`) di `src/queries.py` berjalan akurat dengan dukungan parameter label sentimen dan sumber label (*prediksi* vs *verifikasi*).
2. Status filter tersimpan secara konsisten menggunakan `st.session_state` di halaman Dashboard.
3. Hasil agregasi metrik di Dashboard konsisten 100% dengan hasil kueri SQL manual pada database `data/sentiment.db`.

## 2. Tabel Uji Konsistensi 5 Kombinasi Filter

| No | Kombinasi Filter | Halaman Data | Dashboard | SQL manual | Status |
| :---: | :--- | :---: | :---: | :---: | :---: |
| **1** | Tanpa filter | 1,000 | 1,000 | 1,000 | **Konsisten ✅** |
| **2** | Platform: Instagram | 1,000 | 1,000 | 1,000 | **Konsisten ✅** |
| **3** | Kategori: Infrastruktur | 200 | 200 | 200 | **Konsisten ✅** |
| **4** | Label negatif (prediksi) + keyword 'bantuan' | 1 | 1 | 1 | **Konsisten ✅** |
| **5** | Label verifikasi positif + platform (Instagram) | 7 | 7 | 7 | **Konsisten ✅** |

## 3. Catatan Implementasi & Bukti
* **Session State:** Widget filter pada *sidebar* Streamlit berhasil dihubungkan ke `st.session_state` sehingga state filter tetap terjaga.
* **Agregasi Dinamis:** Dashboard berhasil memanggil `filter_comments` dan memperbarui metrik utama secara *real-time*.
* **Bukti Tangkapan Layar:** Berkas tangkapan layar hasil pengujian telah disimpan di folder `reports/evidence/D25_*.png`.
