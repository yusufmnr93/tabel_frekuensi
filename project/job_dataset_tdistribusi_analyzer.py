import pandas as pd
import math
from typing import List, Tuple, Union

# Algoritma TDistribusiFrekuensi yang diberikan pengguna
def TDistribusiFrekuensi(x: List[Union[int, float]], k: int) -> Tuple:
    """
    Menghitung tabel distribusi frekuensi berdasarkan algoritma yang diberikan.

    Input:
    x (List[int/float]): Array data (YearsOfExperience, dll.).
    k (int): Banyak kelas yang diinginkan.

    Output:
    Tuple: (interval, m, f, fr, fk)
           interval: Batas bawah kelas.
           m: Titik tengah kelas.
           f: Frekuensi kelas.
           fr: Frekuensi relatif kelas.
           fk: Frekuensi kumulatif kelas.
    """
    n = len(x)

    # 1. Tentukan Nilai Min, Max, dan Jangkauan (R)
    x_min = min(x)
    x_max = max(x)
    R = x_max - x_min

    # 2. Tentukan Panjang Interval Kelas (i)
    i = math.ceil(R / k)

    # Inisialisasi array untuk output
    interval: List[Union[int, float]] = [0.0] * (k + 1)
    m: List[float] = [0.0] * k     # Titik tengah (k kelas)
    f: List[int] = [0] * k         # Frekuensi (k kelas)
    fr: List[float] = [0.0] * k    # Frekuensi relatif (k kelas)
    fk: List[int] = [0] * k         # Frekuensi kumulatif (k kelas)

    # 3. Hitung Batas Bawah Kelas (interval[q])
    for q in range(k + 1):
        interval[q] = x_min + q * i

    # 4. Hitung Titik Tengah Kelas (m[q])
    for q in range(k):
        m[q] = interval[q] + 0.5 * i

    # 5. Hitung Frekuensi Kelas (f[q])
    for p in range(n):
        for q in range(k):
            if q == k - 1:
                # Kelas terakhir: batas bawah inklusif, batas atas inklusif
                if x[p] >= interval[q] and x[p] <= interval[q+1]:
                    f[q] += 1
            else:
                # Kelas 1 sampai k-1: batas bawah inklusif, batas atas eksklusif
                if x[p] >= interval[q] and x[p] < interval[q+1]:
                    f[q] += 1

    # 6. Hitung Frekuensi Relatif (fr[q])
    for q in range(k):
        fr[q] = f[q] / n

    # 7. Hitung Frekuensi Kumulatif (fk[q])
    if k > 0:
        fk[0] = f[0]

    for q in range(1, k):
        fk[q] = fk[q - 1] + f[q]

    return interval, m, f, fr, fk

def parse_years_of_experience(value: str) -> float:
    """
    Parsing YearsOfExperience dari dataset job
    """
    if not isinstance(value, str):
        return None

    value = value.strip().lower()

    try:
        if '-' in value:  # Range format like "2-5"
            parts = value.split('-')
            if len(parts) == 2:
                start = float(parts[0].strip())
                end = float(parts[1].strip())
                return (start + end) / 2
        elif '+' in value:  # Open-ended format like "10+"
            return float(value.replace('+', ''))
        elif value.replace('.', '').isdigit():  # Single number
            return float(value)
    except (ValueError, IndexError):
        pass

    return None

def analyze_job_dataset():
    """
    Menganalisis dataset job menggunakan algoritma TDistribusiFrekuensi
    """
    print("ANALISIS JOB DATASET DENGAN ALGORITMA TDistribusiFrekuensi")
    print("=" * 70)

    # Load dataset
    try:
        df = pd.read_csv("job_dataset.csv")
        print(f"Dataset berhasil dimuat: {len(df)} baris")
        print(f"Kolom tersedia: {list(df.columns)}")
    except Exception as e:
        print(f"Error loading dataset: {e}")
        return

    # Parse YearsOfExperience
    parsed_years = df["YearsOfExperience"].apply(parse_years_of_experience)
    valid_years = parsed_years.dropna()

    if len(valid_years) == 0:
        print("Tidak ada data YearsOfExperience yang valid")
        return

    print(f"Data YearsOfExperience valid: {len(valid_years)} dari {len(df)} total")
    print(f"Rentang: {valid_years.min()} - {valid_years.max()} tahun")
    print(f"Rata-rata: {valid_years.mean():.1f} tahun")

    # Konversi ke list untuk algoritma
    data_years = valid_years.tolist()

    # Tentukan jumlah kelas menggunakan algoritma Sturges
    n = len(data_years)
    k_sturges = math.ceil(1 + 3.3 * math.log10(n))
    k_sturges = max(3, min(k_sturges, 15))  # Batasan praktis

    print(f"Jumlah kelas (Sturges): {k_sturges}")

    # Jalankan algoritma TDistribusiFrekuensi
    interval, m, f, fr, fk = TDistribusiFrekuensi(data_years, k_sturges)

    # Tampilkan hasil dalam format tabel
    print("\nTABEL DISTRIBUSI FREKUENSI YEARS OF EXPERIENCE")
    print("=" * 90)
    print(f"{'Kelas':<6} {'Interval':<18} {'Titik Tengah':<12} {'Frekuensi':<10} {'F. Relatif':<12} {'F. Kumulatif':<12}")
    print("-" * 90)

    for q in range(k_sturges):
        batas_bawah = interval[q]
        batas_atas = interval[q+1]

        # Format interval untuk display
        if q == k_sturges - 1:
            interval_str = f"{batas_bawah:.0f} - {batas_atas:.0f}"
        else:
            interval_str = f"{batas_bawah:.0f} - {batas_atas-1:.0f}"

        print(f"{q+1:<6} {interval_str:<18} {m[q]:<12.1f} {f[q]:<10} {fr[q]:<12.4f} {fk[q]:<12}")

    # Simpan hasil ke CSV
    results_df = pd.DataFrame({
        'Kelas': range(1, k_sturges + 1),
        'Interval': [f"{interval[q]:.0f} - {interval[q+1]-1 if q < k_sturges-1 else interval[q+1]:.0f}" for q in range(k_sturges)],
        'Titik_Tengah': [round(m[q], 1) for q in range(k_sturges)],
        'Frekuensi': f,
        'Frekuensi_Relatif': [round(fr[q], 4) for q in range(k_sturges)],
        'Frekuensi_Kumulatif': fk
    })

    results_df.to_csv("tabel_tdistribusi_job_dataset.csv", index=False)
    print("\nHasil tabel distribusi telah disimpan ke: tabel_tdistribusi_job_dataset.csv")

    # Analisis tambahan
    print("\nANALISIS TAMBAHAN:")
    print(f"   Total data valid: {n}")
    print(f"   Jumlah kelas: {k_sturges}")
    print(f"   Lebar interval: {interval[1] - interval[0]:.0f}")
    print(f"   Rentang data: {interval[0]:.0f} - {interval[-1]:.0f}")

    # Hitung statistik dasar
    print("\nSTATISTIK DASAR:")
    print(f"   Mean: {valid_years.mean():.2f}")
    print(f"   Median: {valid_years.median():.2f}")
    print(f"   Mode: {valid_years.mode().iloc[0] if len(valid_years.mode()) > 0 else 'N/A'}")
    print(f"   Std Dev: {valid_years.std():.2f}")

    # Distribusi tingkat pengalaman
    print("\nDISTRIBUSI EXPERIENCE LEVEL:")
    exp_levels = df['ExperienceLevel'].value_counts()
    for level, count in exp_levels.items():
        percentage = (count / len(df)) * 100
        print(f"   {level}: {count} ({percentage:.1f}%)")

    return results_df

def main():
    """
    Main function untuk menjalankan analisis
    """
    analyze_job_dataset()

    print("\nAnalisis selesai!")
    print("File output: tabel_tdistribusi_job_dataset.csv")

if __name__ == "__main__":
    main()
