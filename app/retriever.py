# app/retriever.py
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

def get_embedding(text):
    embedding = model.encode([text])[0]
    return embedding

def build_faiss_index(texts):
    dim = 384
    index = faiss.IndexFlatL2(dim)
    vectors = [get_embedding(t) for t in texts]
    index.add(np.array(vectors).astype('float32'))
    return index, texts, vectors
