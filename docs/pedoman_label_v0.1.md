# Pedoman Pelabelan Data Sentimen (Versi 0.1)

Dokumen ini menjadi acuan utama untuk melabeli sentimen dari komentar masyarakat pada media sosial Pemerintah Provinsi Jawa Timur.

### A. Kelas Sentimen Utama (Berdasarkan Bab 4.10)
1.  **Positif:** Komentar yang mengandung unsur apresiasi, dukungan, kepuasan, rasa syukur, atau kebanggaan terhadap kinerja/program Pemprov. 
    *   *Contoh:* "Mantap🔥", "Terbaik pak langkah yang sangat tepat"
2.  **Negatif:** Komentar yang mengandung unsur keluhan, kemarahan, kritik, kekecewaan, atau penolakan. 
    *   *Contoh:* "Gubernur Gak pecus blasss", "Roda 4 udah bertahun2 kagak ada pemutihan"
3.  **Netral:** Komentar yang bersifat informatif, tidak mengandung emosi yang jelas, atau sekadar memberikan fakta.
    *   *Contoh:* "Samsat Ngawi igne nopo nggeh?"

### B. Aturan Tambahan dari Kasus Pilot
Berdasarkan uji coba data *pilot*, disepakati penambahan 5 aturan khusus untuk menangani komentar yang membingungkan:

1.  **Kasus Spam dan Iklan (Kode: SPAM)** 
    Komentar yang berisi promosi jualan, tautan penipuan, atau *bot* tidak dilabeli sentimen, melainkan langsung diberi status **Eksklusi** di kolom kelayakan.
2.  **Kasus Pertanyaan Layanan (Kode: SULIT-TANYA)** 
    Komentar yang murni berupa pertanyaan terkait layanan tanpa ada nada marah/mengeluh (contoh: *"Roda 4 kapan ibu?"*) wajib dilabeli sebagai **Netral**.
3.  **Kasus Sarkasme/Sindiran (Kode: SULIT-SARKASME)** 
    Komentar yang menggunakan kata-kata baik atau emoji tertawa namun konteksnya mengejek kebijakan (contoh: *"Syarat dan ketentuan Berlaku😂 yang desil 6-10 sini kumpul"*) wajib dilabeli sebagai **Negatif**.
4.  **Kasus Koreksi Fakta (Kode: SULIT-KOREKSI)** 
    Komentar yang meluruskan informasi atau mengoreksi visual unggahan tanpa nada emosi (contoh: *"ini videonya bukan tembakau campalok"*) dilabeli sebagai **Netral**.
5.  **Penggunaan Bahasa Daerah (Kode: SULIT-BAHASA)** 
    Komentar dalam dialek lokal yang kental (Jawa/Madura) tetap berstatus **Layak**. Pelabelan didasarkan pada terjemahannya, dan diberi catatan agar mudah ditinjau ulang jika ragu.