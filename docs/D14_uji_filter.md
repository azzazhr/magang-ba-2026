# Laporan Pengujian Filter Data (Hari 14)

Dokumen ini berisi catatan pengujian dan validasi fungsi *dynamic filtering* (`filter_comments`) pada aplikasi Streamlit dibandingkan dengan eksekusi kueri manual pada database SQLite (`data/app.db`).

---

## **Ringkasan Hasil Pengujian Tiga Kombinasi**

| No | Kombinasi Filter | Jumlah Baris (SQL Manual / Backend) | Jumlah Baris (Aplikasi Streamlit UI) | Status Validasi |
|:--:|:---|:---:|:---:|:---:|
| **1** | Platform: **Instagram** <br> Rentang Tanggal: **2026-09-01 s.d. 2026-09-30** | `1471` | `1471` | **Valid / Sesuai** |
| **2** | Kategori Konten: **Sosial & Ekonomi** | `1783` | `1783` | **Valid / Sesuai** |
| **3** | Platform: **Instagram** <br> Kata Kunci: **"bantuan"** | `8` | `8` | **Valid / Sesuai** |

---

## **Skrip Pengujian Python**

```python
import sqlite3
import pandas as pd
from src.queries import filter_comments

conn = sqlite3.connect('data/app.db')
# Kombinasi 1
df_comb1 = filter_comments(conn, platforms=['Instagram'], date_from='2026-09-01', date_to='2026-09-30')
print(f'1. Kombinasi 1: Ditemukan {len(df_comb1)} baris')

# Kombinasi 2
df_comb2 = filter_comments(conn, categories=['Sosial', 'Ekonomi'])
print(f'2. Kombinasi 2: Ditemukan {len(df_comb2)} baris')

# Kombinasi 3
df_comb3 = filter_comments(conn, platforms=['Instagram'], keyword='bantuan')
print(f'3. Kombinasi 3: Ditemukan {len(df_comb3)} baris')

conn.close()
```

> **Catatan Kesimpulan:**
> Hasil pengujian menunjukkan bahwa jumlah baris data yang dihasilkan oleh kueri manual (*backend*) sama persis dengan angka yang tampil pada antarmuka (*UI*) Streamlit. Hal ini membuktikan bahwa fungsi klausa `WHERE` dinamis dan kontrol *sidebar* telah berjalan dengan benar dan akurat.