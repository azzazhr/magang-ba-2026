import pandas as pd

# Pastikan path ini sesuai dengan lokasi file CSV-mu di VS Code
c = pd.read_csv("data/raw/comments_pilot.csv")

print("--- STATUS KELAYAKAN ---")
print(c.eligibility_status.value_counts())

print("\n--- JUMLAH KOMENTAR PER UNGGAHAN ---")
print(c.groupby("post_id").size())

print("\n--- SEBARAN LABEL SENTIMEN ---")
print(c.reference_label.value_counts(dropna=False))