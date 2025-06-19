# preprocess_csv_kg.py

import pandas as pd
import re

# Path ke file mentah dari BPS
csv_path = "data/penduduk-15-tahunCURANG.csv"
output_path = "data/penduduk.csv"

# Baca data, skip baris judul pertama
df = pd.read_csv(csv_path, skiprows=2)

# Ganti nama kolom pertama agar mudah
df.columns.values[1] = "sektor"

# Ambil hanya kolom yang valid (bukan NaN)
df = df.loc[:, ~df.columns.isna()]

# Hapus kolom 'No.' kalau ada
if 'No.' in df.columns:
    df = df.drop(columns=['No.'])

# Ubah ke format baris per sektor per waktu
rows = []
for _, row in df.iterrows():
    sektor = str(row['sektor']).strip()
    for kolom in df.columns[1:]:
        try:
            tahun, bulan = kolom.split("_")
            val = row[kolom]
            if pd.isna(val):
                continue
            val = str(val).replace(",", "").replace(".", "")
            if not re.match(r'^\d+$', val):
                continue
            jumlah = int(val)
            rows.append({
                "sektor": sektor,
                "tahun": tahun,
                "bulan": bulan,
                "jumlah": jumlah
            })
        except Exception as e:
            continue

# Simpan ke file CSV baru
df_out = pd.DataFrame(rows)
df_out.to_csv(output_path, index=False, encoding='utf-8')
print("Data tersimpan di:", output_path)
print(df_out.head())
