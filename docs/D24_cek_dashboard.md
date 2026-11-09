# Dokumentasi Pengecekan Dashboard Hari ke-24 (D24)
*Nama: Azzahra Attaqina*
*Proyek: Analisis Sentimen Kebijakan Publik*

## 1. Verifikasi Angka Metrik Utama vs Kueri SQL Manual (Langkah 5)

Berikut adalah pencocokan langsung antara angka yang dirender pada metrik dashboard Streamlit dengan kueri SQL manual pada database `data/sentiment.db`:

| Metrik Dashboard | Hasil Kueri SQL Manual | Kueri SQL SQLite yang Digunakan | Status Pencocokan |
| :--- | :--- | :--- | :--- |
| **Total Unggahan** | 915 | `SELECT COUNT(DISTINCT comment_id) FROM comments` | **COCOK ✅** |
| **Komentar Layak** | 1,000 | `SELECT COUNT(*) FROM comments` | **COCOK ✅** |
| **Komentar Diprediksi** | 50 | `SELECT COUNT(DISTINCT comment_id) FROM predictions` | **COCOK ✅** |
| **Komentar Terverifikasi** | 10 | `SELECT COUNT(DISTINCT comment_id) FROM verification_history` | **COCOK ✅** |
| **Persentase Verifikasi** | 20.0% | Kalkulasi: `(Terverifikasi / Diprediksi) * 100` | **COCOK ✅** |

## 2. Catatan Validitas Implementasi Grafik
* **Grafik 1 (Platform):** Menampilkan sebaran data riil multi-channel (Instagram, YouTube, TikTok, Twitter/X) dari tabel `comments`.
* **Grafik 2 (Kategori Konten):** Menampilkan kategori kebijakan publik (Infrastruktur, Pelayanan Publik, Pendidikan, Kesehatan, Transportasi) secara bersih tanpa nilai `nan`.
* **Grafik 3 (Distribusi Sentimen):** Mendukung pemisahan mode analitik secara transparan antara *Prediksi Model* dan *Label Verifikasi*.
* **Grafik 4 (Tren Komentar per Minggu):** Berbasis atribut waktu `commented_at` yang terdistribusi secara valid pada rentang waktu 1 Juli – 30 September 2026.
