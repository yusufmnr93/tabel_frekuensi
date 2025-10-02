#!/usr/bin/env python3

import pandas as pd
import math
import os

print("TEST FINAL - MEMASTIKAN SEMUA BERFUNGSI")

# Test 1: Cek direktori saat ini
current_dir = os.getcwd()
print(f"Direktori saat ini: {current_dir}")

# Test 2: Cek isi folder project
project_dir = "project"
if os.path.exists(project_dir):
    files = os.listdir(project_dir)
    print(f"File di folder project: {files}")

    # Cari file job_dataset.csv
    csv_file = os.path.join(project_dir, "job_dataset.csv")
    print(f"Path lengkap job_dataset.csv: {csv_file}")
    print(f"File exists: {os.path.exists(csv_file)}")

    if os.path.exists(csv_file):
        try:
            df = pd.read_csv(csv_file)
            print(f"Berhasil baca file: {len(df)} baris")
            print(f"Kolom: {list(df.columns)}")

            if 'YearsOfExperience' in df.columns:
                print("Kolom YearsOfExperience ditemukan")

                # Test parsing sederhana
                sample_data = df['YearsOfExperience'].head(5).tolist()
                print(f"Sample data: {sample_data}")

                # Test algoritma TDistribusiFrekuensi dengan data kecil
                test_data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
                n = len(test_data)
                k = math.ceil(1 + 3.3 * math.log10(n))

                print(f"Test algoritma dengan {n} data, k={k}")

                # Algoritma sederhana
                x_min = min(test_data)
                x_max = max(test_data)
                R = x_max - x_min
                i = math.ceil(R / k)

                interval = [x_min + q * i for q in range(k + 1)]
                print(f"Interval: {interval}")

                # Hitung frekuensi
                f = [0] * k
                for val in test_data:
                    for q in range(k):
                        if q == k - 1:
                            if val >= interval[q] and val <= interval[q+1]:
                                f[q] += 1
                        else:
                            if val >= interval[q] and val < interval[q+1]:
                                f[q] += 1

                print(f"Frekuensi: {f}")

                # Test penyimpanan file
                test_df = pd.DataFrame({'Test': [1, 2, 3]})
                test_file = "test_output.csv"
                test_df.to_csv(test_file, index=False)
                print(f"File test berhasil disimpan: {test_file}")

                # Cek apakah file ada
                if os.path.exists(test_file):
                    print(f"File {test_file} berhasil dibuat")
                    os.remove(test_file)  # Hapus file test
                    print("File test dihapus")
                else:
                    print(f"File {test_file} tidak ditemukan setelah disimpan")

        except Exception as e:
            print(f"Error: {e}")
    else:
        print("File job_dataset.csv tidak ditemukan")
else:
    print("Folder project tidak ditemukan")

print("TEST SELESAI")
