import pandas as pd
import numpy as np
import math

def build_frequency_table(values: pd.Series) -> pd.DataFrame:
    """
    Membangun tabel distribusi frekuensi dari data numerik menggunakan algoritma Sturges.
    """
    if len(values) == 0:
        return pd.DataFrame()

    n = len(values)
    min_val = values.min()
    max_val = values.max()

    # Algoritma Sturges untuk menentukan jumlah kelas
    k = math.ceil(1 + 3.3 * math.log10(n))

    # Pastikan k tidak terlalu kecil atau besar
    k = max(3, min(k, 20))

    # Hitung lebar interval
    range_val = max_val - min_val
    interval = math.ceil(range_val / k) if range_val > 0 else 1

    # Buat bins
    start = math.floor(min_val)
    bins = [start + i * interval for i in range(k + 1)]

    # Hitung frekuensi
    freq, edges = np.histogram(values.dropna(), bins=bins)

    # Hitung statistik tambahan
    cum_freq = np.cumsum(freq)
    rel_freq = freq / n * 100

    # Buat DataFrame hasil
    dist_table = pd.DataFrame({
        "Interval": [f"{int(edges[i])} - {int(edges[i+1])}" for i in range(len(edges) - 1)],
        "Frekuensi": freq,
        "Frekuensi Kumulatif": cum_freq,
        "Frekuensi Relatif (%)": rel_freq.round(2)
    })

    return dist_table

def get_manual_weight_data() -> pd.DataFrame:
    """
    Menggunakan data berat badan yang diberikan pengguna secara manual
    """
    # Data berat badan yang diberikan (30 data)
    weight_data = [
        128, 63, 97, 134, 133, 136, 125, 110, 118, 94,  # Baris pertama
        76, 84, 132, 105, 80, 87, 100, 77, 120, 109,    # Baris kedua
        90, 72, 103, 78, 94, 118, 117, 80, 140, 94      # Baris ketiga
    ]

    # Membuat DataFrame dengan informasi tambahan
    df = pd.DataFrame({
        'No': range(1, len(weight_data) + 1),
        'Berat_Badan_kg': weight_data,
        'Kategori': ['Dewasa'] * len(weight_data)
    })

    return df

def analyze_weight_data():
    """
    Menganalisis data berat badan orang dewasa
    """
    print("🏋️ Analisis Data Berat Badan Orang Dewasa")
    print("=" * 50)

    # Load data manual
    df = get_manual_weight_data()

    print(f"📊 Total data: {len(df)} orang dewasa")
    print(f"📏 Rentang berat badan: {df['Berat_Badan_kg'].min()} - {df['Berat_Badan_kg'].max()} kg")
    print(f"⚖️ Rata-rata berat badan: {df['Berat_Badan_kg'].mean():.1f} kg")
    print(f"📊 Median berat badan: {df['Berat_Badan_kg'].median():.1f} kg")
    print(f"📈 Standar deviasi: {df['Berat_Badan_kg'].std():.1f} kg")
    print()

    # Bangun tabel distribusi frekuensi
    weight_values = df['Berat_Badan_kg']
    freq_table = build_frequency_table(weight_values)

    print("📋 TABEL DISTRIBUSI FREKUENSI BERAT BADAN")
    print("=" * 50)
    print(freq_table.to_string(index=False))

    # Simpan hasil ke file CSV
    freq_table.to_csv("tabel_frekuensi_berat_badan_dewasa.csv", index=False)
    df.to_csv("dataset_berat_badan_dewasa.csv", index=False)

    print("\n💾 Hasil telah disimpan ke:")
    print("   - tabel_frekuensi_berat_badan_dewasa.csv")
    print("   - dataset_berat_badan_dewasa.csv")

    return df, freq_table

def additional_analysis(df: pd.DataFrame):
    """
    Analisis tambahan untuk data berat badan
    """
    print("\n🔍 ANALISIS TAMBAHAN")
    print("=" * 30)

    # Klasifikasi berat badan berdasarkan kategori WHO
    def classify_weight(weight):
        if weight < 18.5:
            return "Underweight"
        elif 18.5 <= weight < 25:
            return "Normal"
        elif 25 <= weight < 30:
            return "Overweight"
        else:
            return "Obese"

    df['Kategori_Berat'] = df['Berat_Badan_kg'].apply(classify_weight)

    # Distribusi kategori berat badan
    kategori_dist = df['Kategori_Berat'].value_counts()
    kategori_pct = (kategori_dist / len(df) * 100).round(2)

    print("📊 Distribusi Kategori Berat Badan:")
    for kategori, jumlah in kategori_dist.items():
        persentase = kategori_pct[kategori]
        print(f"   {kategori}: {jumlah} orang ({persentase}%)")

    # Statistik tambahan
    print("\n📈 Statistik Deskriptif:")
    print(f"   Berat minimum: {df['Berat_Badan_kg'].min()} kg")
    print(f"   Berat maximum: {df['Berat_Badan_kg'].max()} kg")
    print(f"   Q1 (Kuartil 1): {df['Berat_Badan_kg'].quantile(0.25):.1f} kg")
    print(f"   Q3 (Kuartil 3): {df['Berat_Badan_kg'].quantile(0.75):.1f} kg")
    print(f"   IQR: {df['Berat_Badan_kg'].quantile(0.75) - df['Berat_Badan_kg'].quantile(0.25):.1f} kg")

    # Outlier detection menggunakan IQR method
    Q1 = df['Berat_Badan_kg'].quantile(0.25)
    Q3 = df['Berat_Badan_kg'].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    outliers = df[(df['Berat_Badan_kg'] < lower_bound) | (df['Berat_Badan_kg'] > upper_bound)]
    print(f"\n⚠️ Outliers terdeteksi: {len(outliers)} data")
    if len(outliers) > 0:
        print(f"   Batas bawah: {lower_bound:.1f} kg")
        print(f"   Batas atas: {upper_bound:.1f} kg")
        print("   Data outlier:")
        for _, row in outliers.iterrows():
            print(f"     No.{row['No']}: {row['Berat_Badan_kg']} kg")

def main():
    """
    Main function untuk menjalankan analisis
    """
    print("🚀 Program Analisis Berat Badan Orang Dewasa")
    print("Menggunakan algoritma tabel distribusi frekuensi Sturges")
    print()

    # Analisis utama
    df, freq_table = analyze_weight_data()

    # Analisis tambahan
    additional_analysis(df)

    print("\n✅ Analisis selesai!")

if __name__ == "__main__":
    main()
