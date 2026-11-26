# Pedoman Pelabelan Sentimen (Versi Final — v1.0)

- **Versi Dokumen:** Final (`v1.0`)
- **Tanggal Penetapan:** 27 November 2026
- **Penyusun:** Azzahra Attaqina (Laboratorium Business Analytics, Polinema)
- **Dataset Acuan:** Komentar media sosial resmi Pemerintah Provinsi Jawa Timur (`comments_v1.csv`, 1.000 baris)

---

## 1. Definisi Kelas Sentimen Utama

Setiap komentar masyarakat yang lolos penyaringan kelayakan diklasifikasikan ke dalam **3 kelas sentimen utama**:

| Kelas Label | Kode Sistem | Definisi Operasional | Contoh Ilustrasi Aktual |
| :--- | :---: | :--- | :--- |
| **Positif** | `positif` | Komentar yang menyampaikan apresiasi, dukungan, rasa syukur, pujian, kepuasan, atau kebanggaan terhadap program, kebijakan, maupun kinerja Pemprov Jawa Timur. | *"Mantap🔥"*, *"Terbaik pak langkah yang sangat tepat"*, *"Alhamdulillah masuk 10 besar"*, *"Bojonegoro..... Lanjutkan!"* |
| **Negatif** | `negatif` | Komentar yang mengandung keluhan, kemarahan, kritik keras, kekecewaan, protes, penolakan, atau sindiran tajam terhadap layanan/kebijakan. | *"Gubernur Gak pecus blasss"*, *"Roda 4 udah bertahun2 kagak ada pemutihan"*, *"Nganjuk opo2 kok Gleput 😜"* |
| **Netral** | `netral` | Komentar yang bersifat informatif, berupa pertanyaan prosedural tanpa emosi, sekadar menandai akun lain, atau meluruskan fakta secara objektif. | *"Samsat Ngawi igne nopo nggeh?"*, *"Roda 4 kapan ibu?"*, *"ini videonya bukan tembakau campalok"* |

---

## 2. Aturan Khusus Kasus Sulit & Eksklusi

Untuk menjaga konsistensi antar-anotator, ditetapkan **6 aturan operasional** berikut:

1. **Spam, Iklan & Bot (`SPAM` $\rightarrow$ Eksklusi):** Komentar berisi promosi produk, tautan penipuan/judi, atau komentar otomatis tidak relevan tidak dilabeli sentimen dan diberi status **Eksklusi** (`is_eligible = 0`).
2. **Pertanyaan Layanan (`SULIT-TANYA` $\rightarrow$ `netral`):** Pertanyaan murni mengenai jadwal, syarat, atau prosedur layanan publik tanpa nada marah/mengeluh wajib dilabeli **Netral**.
3. **Sarkasme & Sindiran (`SULIT-SARKASME` $\rightarrow$ `negatif`):** Komentar yang memakai kata pujian atau emoji tertawa namun konteks kalimatnya menyindir/mengejek kebijakan (contoh: *"Syarat dan ketentuan Berlaku😂 yang desil 6-10 sini kumpul"*) wajib dilabeli **Negatif**.
4. **Koreksi Fakta (`SULIT-KOREKSI` $\rightarrow$ `netral`):** Komentar yang meluruskan data atau visual unggahan tanpa ekspresi kemarahan/pujian dilabeli **Netral**.
5. **Bahasa Daerah (`SULIT-BAHASA` $\rightarrow$ Tetap Layak):** Komentar berbahasa Jawa atau Madura tetap dinilai layak (`is_eligible = 1`); makna sentimen ditentukan berdasarkan arti kontekstualnya dan diberi catatan `RAGU` bila ambigu.
6. **Emotikon Tunggal & Tag Akun:** Komentar yang hanya berisi emotikon dukungan (mis. `👏👏👏`, `🔥`) dilabeli **Positif**, sedangkan komentar yang sekadar menyebut/menandai akun lain tanpa opini dilabeli **Netral** dengan catatan `RAGU - sekadar tag akun`.

---

## 3. Riwayat Perubahan Pedoman

| Versi | Tahap / Hari | Ringkasan Perubahan |
| :---: | :--- | :--- |
| `v0.1` | Hari 4–5 (Uji Pilot) | Penetapan 3 kelas sentimen dasar (`Positif`, `Negatif`, `Netral`) beserta 5 aturan penanganan kasus khusus (`SPAM`, `SULIT-TANYA`, `SULIT-SARKASME`, `SULIT-KOREKSI`, `SULIT-BAHASA`). |
| `v0.2` | Hari 11–15 (Pelabelan Batch 1–5) | Penambahan standarisasi kode catatan keraguan (`RAGU - sekadar tag akun`, `RAGU - sentimen ganda`, `teks asli cuma emoticon`) serta sesi pemeriksaan mandiri (*re-check*) yang mengoreksi **10 label** dari 1.000 komentar. |
| `v1.0` | Hari 16 & Hari 38 (Final) | Penguncian aturan *adjudication* bersama peninjau kedua (R2), pemetaan kode label huruf kecil (`positif`, `netral`, `negatif`) untuk integrasi model IndoBERT, serta dokumentasi statistik kesepakatan aktual. |

---

## 4. Statistik Kesepakatan & Sebaran Label Aktual

### A. Hasil Uji Kesepakatan Antar-Anotator (Mahasiswa R1 vs Penilai Kedua R2)
Berdasarkan pemeriksaan silang buta (*blind review*) pada himpunan uji kesepakatan (dokumentasi Hari 16):
- **Jumlah Pasangan Sampel Uji Kesepakatan ($n$):** **230 komentar**
- **Tingkat Kesepakatan Mentah (*Raw Agreement*):** **85,65%** (197 komentar sepakat langsung)
- **Koefisien *Cohen's Kappa* ($\kappa$):** **0,5390** (kategori *Moderate Agreement*)
- **Jumlah Kasus Perbedaan yang Diadjudikasi:** **33 baris** (`data/processed/adjudication.csv`), sehingga diperoleh **967 baris valid** untuk pelatihan setelah penyisihan kasus yang tetap ambigu.

| Penilai R1 \ Penilai R2 | Negatif | Netral | Positif | Total R1 |
| :--- | :---: | :---: | :---: | :---: |
| **Negatif** | 1 | 0 | 0 | **1** |
| **Netral** | 10 | 173 | 15 | **198** |
| **Positif** | 3 | 5 | 23 | **31** |
| **Total R2** | **14** | **178** | **38** | **230** |

### B. Rekapitulasi Sebaran Label Dataset `v1` (Batch 1–5)
- **Rekapitulasi Pemeriksaan Ulang (*Re-check* Mandiri):** **10 data** mengalami penyesuaian label selama proses kendali mutu batch 1–5.
- **Sebaran Label Sentimen Pelabelan Batch 1–5 (1.000 komentar):**
  - **Netral:** 802 komentar (80,2%)
  - **Positif:** 146 komentar (14,6%)
  - **Negatif:** 52 komentar (5,2%)
