from app.services.embedding import EmbeddingModel
from app.db.vector_store import VectorStore

class Retriever:
    def __init__(self):
        self.embedder = EmbeddingModel()
        self.vector_store = VectorStore()
        self.vector_store.load() # Load the vector store from disk

    def retrieve(self, query, top_k=5):
        #convert query to embedding
        query_embedding = self.embedder.embed([query])
        #search in vector store
        results = self.vector_store.search(query_embedding, top_k)
        return results