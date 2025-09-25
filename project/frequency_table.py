import pandas as pd
import numpy as np
import math

def build_frequency_table(values: pd.Series):
    """
    Bangun tabel distribusi frekuensi dari data numerik.
    """
    n = len(values)
    min_val = values.min()
    max_val = values.max()

    # Tentukan jumlah kelas (Sturges)
    k = math.ceil(1 + 3.3 * math.log10(n))

    # Lebar interval
    interval = math.ceil((max_val - min_val) / k)
    if interval == 0:
        interval = 1

    start = math.floor(min_val)
    bins = [start + i * interval for i in range(k + 1)]

    # Hitung frekuensi
    freq, edges = np.histogram(values, bins=bins)

    # Frekuensi kumulatif dan relatif
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
