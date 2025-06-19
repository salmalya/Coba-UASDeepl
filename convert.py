import pandas as pd
import re

# Path ke file CSV
csv_path = r"E:\KULI\S8\Deepl UAS\data\penduduk-15-tahun.csv"

# Temukan baris header (blok 2011–2024)
with open(csv_path, encoding="utf-8") as f:
    lines = f.readlines()

header_idx = None
for i, line in enumerate(lines):
    if line.strip().startswith("No.,Lapangan Pekerjaan Utama") and "2024" in line:
        header_idx = i
        break

if header_idx is None:
    raise ValueError("Header untuk data 2011-2024 tidak ditemukan.")

# Baca CSV dengan multi-level header
df = pd.read_csv(
    csv_path,
    skiprows=header_idx,
    header=[0, 1],
    encoding="utf-8"
)

# Bersihkan nama kolom
df.columns = pd.MultiIndex.from_tuples([
    (str(a).strip(), str(b).strip()) for a, b in df.columns
])

# Cari kolom sektor
sector_col = None
for col in df.columns:
    if "Lapangan Pekerjaan Utama" in col[0]:
        sector_col = col
        break

if sector_col is None:
    raise ValueError("Kolom sektor tidak ditemukan.")

# Tetapkan kolom 2024 Februari
feb_col = ("2024", "Februari")

# Cari kolom Agustus 2024 meskipun header tidak rapi
agus_col = None
for col in df.columns:
    if col[1] == "Agustus" and "2024" in col[0]:
        agus_col = col
        break

if agus_col is None:
    # fallback: bisa juga diset manual jika parsing masih gagal
    agus_col = ("Unnamed: 29_level_0", "Agustus")

if feb_col not in df.columns or agus_col not in df.columns:
    raise ValueError("Kolom Februari atau Agustus 2024 tidak ditemukan.")

# Bersihkan baris kosong dan "Total"
df = df.dropna(subset=[sector_col])
df = df[~df[sector_col].astype(str).str.lower().str.contains("total")]

# Fungsi membersihkan angka
def clean_number(x):
    if pd.isna(x):
        return None
    x = str(x).replace('"', '').replace(',', '').replace('.', '')
    x = re.sub(r'[^\d]', '', x)
    return int(x) if x else None

# Terapkan fungsi pembersih
df[feb_col] = df[feb_col].apply(clean_number)
df[agus_col] = df[agus_col].apply(clean_number)

# Buat kalimat
sentences = []
for _, row in df.iterrows():
    sektor = str(row[sector_col]).strip()
    jumlah_feb = row[feb_col]
    jumlah_agus = row[agus_col]
    if jumlah_feb is not None:
        juta_feb = jumlah_feb / 1_000_000
        sentences.append(f"In February 2024, as many as {juta_feb:.2f} million people worked in the {sektor} sector.")
    if jumlah_agus is not None:
        juta_agus = jumlah_agus / 1_000_000
        sentences.append(f"In August 2024, as many as {juta_agus:.2f} million people worked in the {sektor} sector.")

# Simpan hasil ke file
output_path = r"data\bps_clean.txt"
with open(output_path, "w", encoding="utf-8") as f:
    for sentence in sentences:
        f.write(sentence + "\n")

print(f"Selesai! File disimpan di: {output_path}")
