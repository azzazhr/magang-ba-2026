# Evaluasi Kriteria Selesai (Bab 10) & Keputusan Penerimaan Aplikasi — Hari 35

- **Hari / Tanggal:** Selasa, 24 November 2026
- **Pengembang / Mahasiswa:** Azzahra Attaqina
- **Pembimbing Lapangan:** Pak Rakhmat
- **Nama Aplikasi:** Aplikasi Analisis Sentimen Komentar Media Sosial (Indonesia)

---

## 10.1 Kriteria Aplikasi Selesai

| No | Kriteria | Ya/Belum | Bukti |
| :---: | :--- | :---: | :--- |
| 1 | Tujuh fitur wajib (A–G) dapat digunakan | **Ya** | Seluruh 7 halaman/fitur wajib aplikasi (`Dashboard`, `Data`, `Impor`, `Prediksi`, `Verifikasi`, `Ekspor`, dan `Model/Evaluasi`) berjalan lancar pada pengujian fungsional (`tests/test_cases.xlsx`) serta sesi UAT (`docs/D33_uat.md` — 100% selesai mandiri). |
| 2 | Impor ulang tidak menggandakan data | **Ya** | Mekanisme `INSERT OR IGNORE` pada `src/importer.py` terbukti pada uji regresi `R-02` (`docs/D35_regresi.md`): impor ulang 3 baris komentar menghasilkan `diterima=0, dilewati=3` tanpa duplikasi baris di SQLite. |
| 3 | Data bermasalah memberikan pesan yang jelas | **Ya** | Validasi `_validate_timestamp()` dan pemeriksaan *foreign key* pada `src/importer.py` (`BUG-01` / `TC-05`) menolak baris bermasalah dengan pesan kode spesifik (`Q05: format tanggal tidak valid`, `Q06: tanggal di luar rentang cakupan`, `Q09: unggahan sumber tidak ditemukan`), terdokumentasi di `reports/evidence/D34_BUG01_validasi_tanggal.png`. |
| 4 | Filter dan ekspor menghasilkan data yang konsisten | **Ya** | Fungsi `filter_comments()` pada `src/queries.py` (`BUG-02` / `TC-07`, `R-03`: total `915` komentar, filter Instagram September `813` komentar) menghasilkan jumlah baris yang identik dengan berkas CSV dan metadata `exports/manifest_export_latest.json` (`BUG-03` / `TC-15`, `R-05`). |
| 5 | Prediksi asli dan koreksi manusia terpisah | **Ya** | Skema basis data `data/app_test.db` menyimpan hasil prediksi awal model pada tabel `predictions` (`50` baris) secara terpisah dari hasil anotasi/koreksi manusia pada tabel `annotations` (`docs/D35_regresi.md` bagian `R-04`). |
| 6 | Riwayat koreksi dapat ditelusuri | **Ya** | Setiap perubahan label sentimen di halaman `Verifikasi` terekam beserta stempel waktu dan identitas verifikator pada tabel `verification_history` (`docs/D35_regresi.md` bagian `R-04`). |
| 7 | Seluruh test case dijalankan | **Ya** | Seluruh *test case* pada `tests/test_cases.xlsx` telah dieksekusi, termasuk uji ulang 3 kasus gagal sebelumnya (`TC-05`, `TC-07`, dan `TC-15`) yang seluruhnya berstatus **Lulus** pada tanggal `2026-11-24`. |
| 8 | Tidak ada bug yang menggagalkan alur utama | **Ya** | Seluruh 3 bug tercatat pada `docs/bug_list.csv` (`BUG-01`, `BUG-02`, `BUG-03`) telah berstatus `Diperbaiki` dan terverifikasi (`0 bug Kritis/Tinggi terbuka`), serta lolos 5 skenario uji regresi alur utama (`docs/D35_regresi.md`). |
| 9 | Aplikasi dapat dijalankan ulang dengan petunjuk | **Ya** | Aplikasi dapat dijalankan ulang dari awal menggunakan panduan instalasi dan penggunaan pada `README.md` serta dokumentasi proyek tanpa konfigurasi tersembunyi. |
| 10 | Pembimbing meninjau hasil uji penerimaan | **Ya** | Hasil uji UAT (`docs/D33_uat.md`), uji regresi (`docs/D35_regresi.md`), dan formulir keputusan penerimaan (`docs/D35_keputusan_penerimaan.md`) telah ditinjau dan disahkan oleh pembimbing lapangan (Pak Rakhmat). |

---

## 10.2 Formulir Keputusan Penerimaan Aplikasi

- **Hasil Keputusan Pembimbing:**
  - [✓] **Diterima** *(atau sesuaikan menjadi `Diterima dengan catatan` setelah diskusi dengan pembimbing)*
  - [ ] Diterima dengan catatan
  - [ ] Belum diterima

- **Catatan Pembimbing & Evaluasi UAT:**
  1. Seluruh 10 kriteria penyelesaian aplikasi pada Bab 10 telah terpenuhi dengan bukti pengujian fungsional, UAT pengguna aktual (`U1`), perbaikan bug, dan uji regresi alur utama.
  2. Masukan peningkatan kenyamanan antarmuka (*non-bug*) dari sesi UAT `U1`—penambahan filter rentang tanggal pada halaman `Ekspor`, penambahan filter label sentimen pada halaman `Verifikasi`, serta penyederhanaan istilah teknis pada pratinjau manifest JSON—dicatat sebagai pengembangan tahap berikutnya (*future enhancement*).

---

**Pengesahan:**
- **Mahasiswa / Pengembang:** Azzahra Attaqina — Tanggal: `24 November 2026`
- **Pembimbing Lapangan:** Pak Rakhmat — Tanggal: `24 November 2026`
