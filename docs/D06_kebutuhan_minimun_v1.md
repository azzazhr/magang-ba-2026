## Kebutuhan Minimum v1 (Minimum Viable Product)

### A. Tujuh Fitur Wajib dengan Perilaku Minimum
1. **KF-01 (Ekstraksi Data):** Sistem mampu menerima input tautan unggahan media sosial dan mengambil data teks komentar mentah.
2. **KF-02 (Penyaringan Otomatis):** Sistem mendeteksi serta menyaring data duplikat atau spam dengan menandainya ke status eksklusi.
3. **KF-03 (Pratinjau Prediksi):** Pengguna dapat melihat teks komentar beserta hasil prediksi awal model AI dan skor keyakinannya.
4. **KF-04 (Koreksi & Audit Trail):** Admin dapat mengubah label sentimen secara manual dan sistem merekamnya sebagai entri baru.
5. **KF-05 (Ringkasan Dashboard):** Sistem menampilkan rekapitulasi jumlah akhir sebaran sentimen (Positif, Negatif, Netral) dalam bentuk angka dan grafik.
6. **KF-06 (Ekspor Rekapitulasi):** Sistem menyediakan tombol untuk mengunduh rekapitulasi data hasil verifikasi ke dalam bentuk format laporan.
7. **KF-07 (Autentikasi Dasar):** Sistem membatasi akses halaman verifikasi dan pengelolaan data hanya untuk pengguna yang memiliki hak akses admin.

### B. Hal yang Tidak Dikerjakan pada v1
* Integrasi *real-time streaming* komentar secara otomatis tanpa tautan manual.
* Analisis tingkat lanjut menggunakan model *Deep Learning* yang kompleks (cukup menggunakan model klasifikasi dasar pada tahap ini).
* Fitur multi-bahasa otomatis untuk deteksi slang daerah yang sangat spesifik di luar kamus dasar.

### C. Persetujuan Pembimbing
*Status:* Menunggu konfirmasi dan persetujuan dari dosen pembimbing lapangan / akademik sebelum dilanjutkan ke tahap implementasi kode.