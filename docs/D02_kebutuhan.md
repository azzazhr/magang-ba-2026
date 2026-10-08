# Dokumen Kebutuhan Aplikasi

### Keterbatasan

Kebutuhan fungsional dan nonfungsional pada dokumen ini dirumuskan berdasarkan wawancara dari satu pengguna saja (Dosen Pembimbing Lapangan).

### 1. Kebutuhan Fungsional (KF)

| ID        | Kebutuhan Fungsional ("Sistem harus ...")                                                                                      | Fitur | Sumber   | Prioritas           | Cara Menguji                                                                                                 |
| --------- | ------------------------------------------------------------------------------------------------------------------------------ | ----- | -------- | ------------------- | ------------------------------------------------------------------------------------------------------------ |
| **KF-01** | Sistem harus menampilkan jumlah baris data yang diterima dan ditolak beserta alasannya setelah proses impor file.              | A     | Bab 1/W1 | Wajib               | Impor file berisi 3 baris rusak; ringkasan menyebut 3 ditolak dengan alasan yang jelas.                      |
| **KF-02** | Sistem harus menolak data komentar yang terduplikasi atau tidak memiliki ID unggahan.                                          | B     | Bab 1/W1 | Wajib               | Masukkan data ber-ID sama; sistem hanya menyimpan satu dan membuang duplikatnya.                             |
| **KF-03** | Sistem harus menyediakan filter penyaringan data berdasarkan platform, yaitu Instagram, TikTok, dan Threads.                   | C     | W1       | Wajib               | Pilih filter platform "TikTok"; antarmuka hanya menampilkan daftar data dari TikTok.                         |
| **KF-04** | Sistem harus menyediakan minimal 2 atau 3 opsi metode analisis sentimen yang dapat dipilih oleh pengguna.                      | D     | W1       | Wajib               | Buka opsi "Metode Sentimen", pilih salah satu metode; sistem memproses sentimen berdasarkan metode tersebut. |
| **KF-05** | Sistem harus memfasilitasi pengguna untuk mengoreksi label sentimen prediksi secara manual dan menyimpan riwayat perubahannya. | E     | Bab 1/W1 | Wajib               | Ubah label dari Negatif ke Positif; sistem menyimpan perubahan tersebut ke dalam log histori.                |
| **KF-06** | Sistem harus menampilkan _dashboard_ utama hasil analisis secara visual menggunakan antarmuka dari _library_ Streamlit.        | F     | W1       | Wajib               | Buka halaman _dashboard_; grafik sebaran sentimen termuat menggunakan komponen visual Streamlit.             |
| **KF-07** | Sistem harus dapat mengekspor dan mengunduh data bersih yang telah dianalisis.                                                 | G     | Bab 1/W1 | Wajib               | Klik tombol unduh CSV; file berisi hasil sentimen berhasil terunduh ke komputer lokal.                       |
| **KF-08** | Sistem harus menyediakan fitur pencarian data lintas platform berdasarkan _hashtag_ (misal: #PemprovJatim).                    | -     | W1       | Tambahan (Opsional) | Ketik _hashtag_ di kolom pencarian; sistem memunculkan unggahan terkait _hashtag_ tersebut.                  |

### 2. Kebutuhan Nonfungsional (KNF)

- **KNF-01:** Aplikasi dikembangkan menggunakan bahasa pemrograman Python.
- **KNF-02:** Seluruh source code aplikasi dikelola menggunakan GitHub dan diperbarui secara berkala selama proses pengembangan. Tautan repository dicantumkan sebagai bagian dari dokumentasi laporan.
- **KNF-03:** Aplikasi diharapkan dapat dijalankan secara lokal melalui localhost dan tetap dapat digunakan pada perangkat dengan spesifikasi standar tanpa bergantung pada GPU dengan kemampuan tinggi.
- **KNF-04:** Pengembangan fitur tambahan, termasuk pencarian berdasarkan hashtag, dilakukan setelah seluruh 7 fitur wajib selesai dan dapat digunakan sesuai kebutuhan yang telah ditentukan.

### 3. Skenario Penggunaan

**Skenario S1 – Analisis berdasarkan Platform dan Metode**

- **Aktor:** Peneliti Lab
- **Tujuan:** Melakukan analisis sentimen terhadap data dari platform tertentu menggunakan metode analisis yang dipilih.
- **Langkah:** Buka aplikasi utama → pada panel _filter_, pilih platform "TikTok" → buka menu metode, pilih "Metode Analisis B" → klik tombol "Analisis".
- **Hasil yang Diharapkan:** Sistem hanya menampilkan data dari platform yang dipilih dan memberikan label sentimen berdasarkan metode analisis yang digunakan.

**Skenario S2 – Verifikasi Prediksi Model**

- **Aktor:** Peneliti Lab
- **Tujuan:** Memeriksa dan memperbaiki hasil prediksi sentimen yang dianggap kurang sesuai, misalnya pada komentar yang mengandung sarkasme atau konteks tertentu.
- **Langkah:** Buka halaman Verifikasi → cari _ID komentar_ yang salah klasifikasi → ubah label prediksi (misal: dari Positif ke Negatif) → tulis alasan koreksi → klik "Simpan".
- **Hasil yang Diharapkan:** Label hasil koreksi tersimpan sebagai label akhir dan perubahan tersebut tercatat dalam riwayat koreksi.

**Skenario S3 – Pencarian Topik Spesifik (Skenario Fitur Opsional)**

- **Aktor:** Peneliti Lab
- **Tujuan:** Mencari dan mengeksplorasi data yang berkaitan dengan topik tertentu menggunakan hashtag.
- **Langkah:** Buka kolom pencarian → ketik _hashtag_ `#PemprovJatim` → klik tombol "Cari".
- **Hasil yang Diharapkan:** Sistem menampilkan data atau unggahan yang relevan dengan hashtag tersebut dari platform yang tersedia. Fitur ini bersifat opsional dan hanya dikembangkan apabila 7 fitur wajib telah selesai.
