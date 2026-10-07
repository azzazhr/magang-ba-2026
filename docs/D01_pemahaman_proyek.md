# Pemahaman Proyek Magang: Aplikasi Analisis Konten dan Sentimen Media Sosial

**(a) Masalah Pengguna Lab**
Masalah utama yang dihadapi oleh dosen dan peneliti di Laboratorium Business Analytics adalah kesulitan dan ketidakefisienan dalam mengelola, memverifikasi, serta menganalisis ribuan data komentar media sosial (seperti Instagram, YouTube, dan TikTok) milik Pemerintah Provinsi Jawa Timur secara manual. Selama ini, pengerjaan yang mungkin hanya mengandalkan perangkat lunak _spreadsheet_ tradisional membuat proses analisis menjadi sangat lambat, rentan terhadap redudansi atau duplikasi data, dan menyulitkan kolaborasi antar peneliti. Selain itu, melacak riwayat perubahan label (seperti mengoreksi sentimen prediksi mesin secara manual) hampir mustahil dilakukan tanpa adanya sebuah sistem terintegrasi yang mencatat aktivitas (_history logging_) tersebut. Oleh karena itu, dibutuhkan sebuah aplikasi _web_ internal yang andal untuk mengotomatisasi alur kerja ini.

**(b) Tujuh Fitur Wajib**

1. **Impor Data:** Aplikasi mampu membaca dan memasukkan data mentah dari _file_ CSV ke dalam _database_ SQLite secara terstruktur.
2. **Pemeriksaan Kualitas:** Sistem secara otomatis mendeteksi dan menolak data yang terduplikasi, bernilai kosong, atau tidak memiliki referensi ID unggahan yang jelas.
3. **Pencarian dan Filter:** Pengguna dapat dengan mudah mencari kata kunci spesifik serta memfilter komentar berdasarkan _platform_, rentang waktu, dan label sentimen.
4. **Analisis Sentimen:** Sistem mampu mengklasifikasikan komentar menjadi sentimen positif, negatif, atau netral secara otomatis menggunakan algoritma _Machine Learning_.
5. **Verifikasi Manusia:** Terdapat halaman interaktif khusus bagi peneliti untuk mengevaluasi dan mengoreksi prediksi model yang keliru, serta menyimpan catatan riwayat koreksi tersebut.
6. **Dashboard Utama:** Aplikasi menyediakan antarmuka visual berbasis Streamlit yang menampilkan ringkasan data, grafik distribusi, dan tren sentimen secara interaktif.
7. **Ekspor CSV:** Hasil data yang telah bersih, dianalisis, dan diverifikasi dapat diunduh kembali ke format CSV untuk kebutuhan publikasi ilmiah.

**(c) Hal yang Tidak Wajib**
Dalam pengembangan aplikasi ini, peserta magang tidak diwajibkan untuk membuat fitur pengambilan data otomatis (_scraping_), tidak perlu membangun model kecerdasan buatan dengan akurasi tingkat mutakhir (_state-of-the-art_), dan tidak diwajibkan melakukan _deployment_ ke _server_ awan karena aplikasi cukup dijalankan secara lokal (localhost).

**(d) Perbedaan Keberhasilan Magang dan Penelitian**
Keberhasilan program magang ini dinilai murni dari sisi rekayasa perangkat lunak (_software engineering_), yaitu berfungsinya keseluruhan ketujuh fitur aplikasi di atas secara lancar tanpa _error_. Sebaliknya, keberhasilan sebuah penelitian menuntut akurasi model sentimen yang tinggi, eksperimen algoritma yang mendalam, dan penarikan kesimpulan ilmiah yang kuat dari dataset.

**(e) Batasan Interpretasi Komentar**
Hasil analisis sentimen dari aplikasi ini memiliki batasan interpretasi yang ketat. Sentimen komentar murni hanya merepresentasikan persepsi dari sampel pengguna yang aktif merespons unggahan Pemprov Jatim, sehingga tidak boleh disimpulkan secara statistik sebagai cerminan langsung dari tingkat kepuasan layanan publik seluruh masyarakat Jawa Timur.

**(f) Satu Risiko Terbesar**
Menurut pemahaman saya, risiko terbesar dalam pengerjaan teknis proyek ini adalah terjadinya kebocoran data (_data leakage_). Hal ini bisa terjadi jika kita tidak berhati-hati saat memisahkan dataset, sehingga algoritma secara tidak sengaja "melihat" data uji (_test_) pada saat fase pelatihan (_train_). Akibatnya, hasil evaluasi seolah tampak tinggi, namun model akan gagal total ketika dihadapkan pada data komentar nyata yang baru.
