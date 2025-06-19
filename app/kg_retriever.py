# app/kg_retriever.py
import pickle
import re

# Load KG dari file
with open("data/kg_graph.gpickle", "rb") as f:
    G = pickle.load(f)

# Ambil context dari graph berdasarkan entitas pertanyaan
def query_graph(question):
    question = question.lower()
    sektor = bulan = tahun = None

    # Ambil semua simpul entitas gabungan
    entities = list(G.nodes)

    # Deteksi entitas
    sektor_list = set()
    for n in entities:
        if " - " in n:
            sektor_part = n.split(" - ")[0]
            sektor_list.add(sektor_part)

    for s in sektor_list:
        if s.lower() in question:
            sektor = s
            break

    bulan_match = re.search(r"(februari|agustus)", question)
    if bulan_match:
        bulan = bulan_match.group(1).title()

    tahun_match = re.search(r"\b(20\d{2})\b", question)
    if tahun_match:
        tahun = tahun_match.group(1)

    target_node = f"{sektor} - {bulan} {tahun}" if sektor and bulan and tahun else None

    context = []
    relasi = []

    if target_node and target_node in G:
        for nbr in G[target_node]:
            relation = G[target_node][nbr].get("relation")
            context.append(f"{target_node} {relation} {nbr}")
            relasi.append(f"({target_node}) --[{relation}]--> ({nbr})")

    return context, relasi
