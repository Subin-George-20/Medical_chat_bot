from app.services.retriever import Retriever

retriever = Retriever()

query = "What is what is causes and symptoms of cancer?"

results = retriever.retrieve(query)

for i, res in enumerate(results):
    print(f"\nResult {i+1}:")
    print(res)