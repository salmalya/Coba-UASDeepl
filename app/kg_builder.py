import pandas as pd
import networkx as nx
import pickle

df = pd.read_csv("data/penduduk.csv")
G = nx.DiGraph()

for _, row in df.iterrows():
    sektor = str(row["sektor"]).strip()
    tahun = str(row["tahun"]).strip()
    bulan = str(row["bulan"]).strip()
    jumlah = f"{float(row['jumlah']):.2f} juta"

    if not sektor or not tahun or not bulan or not jumlah:
        continue

    # Buat simpul gabungan unik
    entitas = f"{sektor} - {bulan} {tahun}"

    G.add_node(entitas)
    G.add_node(sektor)
    G.add_node(tahun)
    G.add_node(bulan)
    G.add_node(jumlah)

    # Relasi dari simpul gabungan
    G.add_edge(entitas, sektor, relation="sektor")
    G.add_edge(entitas, tahun, relation="tahun")
    G.add_edge(entitas, bulan, relation="bulan")
    G.add_edge(entitas, jumlah, relation="jumlah")

# Simpan graph
with open("data/kg_graph.gpickle", "wb") as f:
    pickle.dump(G, f)
