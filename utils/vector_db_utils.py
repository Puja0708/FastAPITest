from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')
index = faiss.IndexFlatL2(384)  # 384 is the embedding size for MiniLM
documents = []

def store_to_vector_db(texts: list[str], metadata: dict = {}):
    global documents
    embeddings = model.encode(texts)
    index.add(np.array(embeddings))
    documents.extend(texts)

def retrieve_from_vector_db(query: str, top_k: int = 5) -> list[str]:
    query_embedding = model.encode([query])
    distances, indices = index.search(np.array(query_embedding), top_k)
    return [documents[i] for i in indices[0]]
