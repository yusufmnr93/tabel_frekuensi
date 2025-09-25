import pandas as pd
from parser import parse_years
from frequency_table import build_frequency_table

# Baca dataset CSV
df = pd.read_csv(r"D:/tugas matkul/Semester 3/Statistics/tabel frekuensi/project/job_dataset.csv")

# Ambil kolom YearsOfExperience dan parsing ke angka
values = df["YearsOfExperience"].apply(parse_years).dropna()

# Bangun tabel distribusi frekuensi
dist_table = build_frequency_table(values)

# Tampilkan hasil ke terminal
print("\n=== Tabel Distribusi Frekuensi ===\n")
print(dist_table.to_string(index=False))

# Simpan ke CSV baru
dist_table.to_csv("tabel_frekuensi.csv", index=False)
print("\nTabel frekuensi sudah disimpan ke 'tabel_frekuensi.csv'")
