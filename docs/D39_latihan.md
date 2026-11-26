# Catatan Latihan Presentasi Akhir Magang (Hari 39)

- **Hari / Tanggal:** Senin, 30 November 2026
- **Penyaji:** Azzahra Attaqina (NIM: `2341720224`)
- **Berkas Slide:** `reports/Slide_2341720224.pptx` (10 Slide)
- **Target Durasi Total:** **10 menit 00 detik** (600 detik)

---

## 1. Perbandingan Waktu Latihan 1 vs Latihan 2

| Segmen Waktu Target | Slide | Topik Bahasan | Target | Latihan 1 | Selisih L1 | Latihan 2 | Selisih L2 |
| :--- | :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| **00:00 – 01:00** | 1–2 | Identitas, masalah pengguna lab, & tujuan aplikasi | 60 dtk | 75 dtk | +15 dtk | 58 dtk | -2 dtk |
| **01:00 – 03:00** | 3–4 | Analisis kebutuhan (`W1`), arsitektur 3 lapis, & ERD 4 tabel | 120 dtk | 140 dtk | +20 dtk | 116 dtk | -4 dtk |
| **03:00 – 05:00** | 5–6 | Data aktual (`v0` & `v1`), split, pedoman label, & kesepakatan anotator | 120 dtk | 132 dtk | +12 dtk | 118 dtk | -2 dtk |
| **05:00 – 07:00** | 7 | Model sentimen: perbandingan validation, test final, & skor `softmax` | 120 dtk | 128 dtk | +8 dtk | 115 dtk | -5 dtk |
| **07:00 – 09:00** | 8–9 | Demo alur 7 fitur, pengujian `15 TC`, UAT (`U1`), & keterbatasan | 120 dtk | 115 dtk | -5 dtk | 114 dtk | -6 dtk |
| **09:00 – 10:00** | 10 | Rencana lanjutan, 3 lembar peluang penelitian, & serah terima | 60 dtk | 62 dtk | +2 dtk | 56 dtk | -4 dtk |
| **TOTAL DURASI** | **1–10** | **Keseluruhan Presentasi** | **10:00** | **10:52** | **+52 dtk** | **09:37** | **-23 dtk** |

---

## 2. Evaluasi & Perbaikan dari Latihan 1 ke Latihan 2

1. **Pemadatan Latar Belakang & Kebutuhan (Slide 1–3):** Pada Latihan 1, penjelasan hambatan spreadsheet dan rincian 8 kebutuhan fungsional memakan waktu berlebih (+35 detik). Pada Latihan 2, penyampaian difokuskan pada 3 hambatan utama dan ringkasan 7 fitur wajib + 3 skenario sehingga hemat 39 detik.
2. **Fokus Angka Kunci pada Data & Model (Slide 5–7):** Pada Latihan 1, pembacaan setiap aturan eksklusi satu per satu membuat durasi melewati batas (+20 detik). Pada Latihan 2, penyajian diringkas ke angka kunci (`2.152` mentah $ightarrow$ `1.777` `v0` $ightarrow$ `1.000` `v1`; *Kappa* `0,5390`; `T3_indobert_len64` dipilih karena inferensi CPU `19,42` detik; *test final* `Accuracy 0,4384`, `Macro-F1 0,3783`) sehingga selesai 23 detik lebih cepat dari batas 10 menit.
3. **Kesiapan Cadangan Demo (Slide 8):** Untuk mengantisipasi kendala teknis saat demo langsung, disiapkan 7 tangkapan layar berurutan pada `reports/demo_cadangan/` (`01_Home.png` s.d. `07_Ekspor_CSV_Manifest.png`).
