import hashlib
import re

def normalize(t: str) -> str:
    t = re.sub(r"\s+", " ", str(t).lower()).strip()
    return t.strip(".,!?;:")

def text_hash(t: str) -> str:
    return hashlib.sha256(normalize(t).encode("utf-8")).hexdigest()
