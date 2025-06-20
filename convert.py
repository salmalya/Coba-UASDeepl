import pandas as pd
import re

# Path input dan output
csv_path = "data/penduduk-15-tahun.csv"
output_path = "data/bps_clean.txt"

# Baca file CSV
df = pd.read_csv(csv_path, skiprows=2)

# Bersihkan kolom
df.columns = [col.strip() for col in df.columns]

# Ambil kolom sektor
sector_col = df.columns[1]  # Biasanya "Lapangan Pekerjaan Utama"

# Hapus baris yang kosong atau 'Total'
df = df.dropna(subset=[sector_col])
df = df[~df[sector_col].astype(str).str.lower().str.contains("total")]

# Fungsi membersihkan angka
def clean_number(x):
    if pd.isna(x):
        return None
    x = str(x).replace('"', '').replace(',', '')
    x = re.sub(r'[^\d]', '', x)
    return int(x) if x else None

# Hasil akhir
sentences = []

# Iterasi setiap baris (sektor)
for _, row in df.iterrows():
    sektor = str(row[sector_col]).strip()
    
    # Iterasi setiap kolom tahun_bulan
    for col in df.columns[2:]:  # Lewati kolom No. dan sektor
        if "_" in col:
            year, month = col.split("_")
            jumlah = clean_number(row[col])
            if jumlah:
                juta = jumlah / 1_000_000
                month_en = "February" if month.lower() == "februari" else "August"
                sentences.append(
                    f"In {month_en} {year}, as many as {juta:.2f} million people worked in the {sektor} sector."
                )

# Simpan hasil ke file
with open(output_path, "w", encoding="utf-8") as f:
    f.write("\n".join(sentences))

print(f"Done! Output saved to: {output_path}")
