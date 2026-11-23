# Laporan Pemeriksaan Kredensial, Privasi Data, & Penyimpanan Aset — Hari 36

- **Hari / Tanggal:** Rabu, 25 November 2026
- **Pelaksana:** Azzahra Attaqina
- **Pembimbing Lapangan:** Pak Rakhmat
- **Direktori Proyek:** `magang-ba-2026`

---

## 1. Hasil Pencarian Rahasia / Kredensial (`token`, `api_key`, `password`, `secret`, `api`)

- **Cakupan Pemindaian:** Seluruh berkas kode dan konfigurasi pada `src/`, `app/`, `docs/`, `tests/`, dan root proyek (`.py`, `.md`, `.json`, `.yaml`, `.yml`, `.toml`, `.cfg`, `.ini`).
- **Perintah / Metode Pemindaian:** Pencarian pola regex *case-insensitive* `\b(token|api_key|apikey|password|passwd|secret|api)\b`.
- **Jumlah Temuan Kredensial Tertanam (*Hardcoded*):** **0 temuan** (bersih).
- **Tindakan Pengamanan Konfigurasi:**
  1. Menyediakan templat konfigurasi aman pada berkas **`.env.example`** (`APP_ENV`, `DB_PATH`, `MODEL_NAME_OR_PATH`, `HF_TOKEN`, `API_KEY`, `SECRET_KEY` dengan nilai kosong).
  2. Mendaftarkan `.env` dan `.env.*` (kecuali `!.env.example`) ke dalam **`.gitignore`** agar berkas rahasia lokal tidak ikut terunggah atau terbawa saat serah terima paket kode.

---

## 2. Pemeriksaan Privasi Nama Pengguna Media Sosial pada Data & Ekspor

- **Cakupan Pemeriksaan:** Basis data aktif (`data/app_test.db` pada tabel `posts` dan `comments`) serta seluruh berkas hasil ekspor di folder `exports/` (`CSV` dan `manifest JSON`).
- **Hasil Pemeriksaan:**
  - Tidak terdapat kolom identitas akun pribadi/nama pengguna media sosial (`username`, `author_name`, `handle`) yang diekspos pada berkas ekspor.
  - Seluruh catatan komentar diidentifikasi menggunakan ID anonim berbasis hash (`comment_id` / `text_hash`), sehingga aman untuk diserahkan bersama paket aplikasi.

---

## 3. Keputusan Penyimpanan Data dan Model Besar (Diskusi Bersama Pembimbing)

- **Hasil Keputusan:**
  - **Basis Data Teruji (`data/app_test.db`) & Sampel Data Uji (`tests/data/`):** Disertakan langsung di dalam paket serah terima proyek karena ukurannya ringan dan diperlukan agar aplikasi langsung dapat dijalankan ulang (*ready-to-run*) saat demonstrasi dan evaluasi.
  - **Cadangan Basis Data Lama (`data/backup/`) & Artefak Sementara:** Tidak disertakan ke dalam paket utama (`diabaikan melalui .gitignore`) agar paket serah terima tetap ringkas dan bersih.
  - **Bobot Model Bahasa Besar (*Pretrained Transformer Weights*):** Tidak disalin secara fisik ke dalam repositori kode (`models/` diabaikan di `.gitignore`); model dimuat otomatis melalui identifier Hugging Face (`MODEL_NAME_OR_PATH` pada `.env.example`) atau menggunakan penyimpanan cache terpisah di lingkungan lab.

---

**Pengesahan:**
- **Mahasiswa / Pengembang:** Azzahra Attaqina — Tanggal: `25 November 2026`
- **Pembimbing Lapangan:** Pak Rakhmat — Tanggal: `25 November 2026`
