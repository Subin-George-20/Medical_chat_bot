from langchain_community.document_loaders import PyPDFLoader
from app.ingestion.chunking import split_documents
from app.services.embedding import EmbeddingModel
from app.db.vector_store import VectorStore

def run_ingestion(file_path):
    # Load the document
    loader = PyPDFLoader(file_path)
    documents = loader.load()

    # Split the document into chunks
    chunks = split_documents(documents)

    #extract text from chunks for embedding
    texts = []
    for chunk in chunks:
        texts.append({
            "text": chunk.page_content,
            "metadata": chunk.metadata
        })

    # Initialize the embedding model 
    embedder = EmbeddingModel()
    embeddings = embedder.embed(texts)
   
   # Store the embeddings in the vector store
    vector_store = VectorStore()
    vector_store.add_embeddings(embeddings, texts)
    vector_store.save()

    print("Ingestion completed successfully.")
   