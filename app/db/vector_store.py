import faiss
import numpy as np
import os
import pickle

class VectorStore:
    def __init__(self,dim = 384, path="vector_store"):
        self.index = faiss.IndexFlatL2(dim)
        self.texts = []
        self.path = path

    def add_embeddings(self, embedding, texts):
        self.index.add(np.array(embedding))
        self.texts.extend(texts)
    
    def save (self):
        if not os.path.exists(self.path):
            os.mkdir(self.path)
        faiss.write_index(self.index, f"{self.path}/index.faiss")
        with open(f"{self.path}/texts.pkl", "wb") as f:
            pickle.dump(self.texts, f)
    
    def load(self):
        self.index = faiss.read_index(f"{self.path}/index.faiss")
        with open(f"{self.path}/texts.pkl", "rb") as f:
            self.texts = pickle.load(f)

    def search(self, query_embedding, top_k=5):
        #convert to numpy array
        query_embedding = np.array(query_embedding)

        #search in faiss index
        distances, indices = self.index.search(query_embedding, top_k)
        results = []
        for idx in indices[0]:
            if idx < len(self.texts):
                results.append(self.texts[idx])
        return results