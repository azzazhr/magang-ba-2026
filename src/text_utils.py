import hashlib
import re

def normalize(t: str) -> str:
    """Membersihkan dan menormalisasi teks komentar sebelum proses pencocokan atau hashing."""
    t = re.sub(r"\s+", " ", str(t).lower()).strip()
    return t.strip(".,!?;:")

def text_hash(t: str) -> str:
    """Menghasilkan nilai hash SHA-256 yang unik untuk teks yang telah dinormalisasi."""
    return hashlib.sha256(normalize(t).encode("utf-8")).hexdigest()
