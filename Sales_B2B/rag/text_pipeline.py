import chromadb
from pathlib import Path

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(name="prospect_context")

async def retrieve_text(prospect_id: str) -> list[str]:
    results = collection.query(
        query_texts=[f"Details for prospect {prospect_id}"],
        n_results=2,
        where={"prospect_id": prospect_id}
    )
    documents = results.get("documents", [[]])[0]
    return documents