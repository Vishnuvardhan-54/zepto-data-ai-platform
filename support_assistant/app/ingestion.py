from pathlib import Path
import chromadb
from sentence_transformers import SentenceTransformer

# Set project paths
BASE_DIR = Path(__file__).resolve().parent.parent
DOCS_DIR = BASE_DIR / "docs"
CHROMA_DIR = BASE_DIR / "chroma_db"

# Load the local embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Create a persistent ChromaDB client and collection
client = chromadb.PersistentClient(path=str(CHROMA_DIR))

collection = client.get_or_create_collection(
    name="zepto_policies",
    metadata={"hnsw:space": "cosine"}
)

def load_documents():
    """Load all policy documents from the docs folder."""
    documents = []
    ids = []

    # Read each policy document and use its filename as the document ID
    for file_path in sorted(DOCS_DIR.glob("doc_*.txt")):
        text = file_path.read_text(encoding="utf-8").strip()
        if text:
            documents.append(text)
            ids.append(file_path.stem)

    return ids, documents

def build_vector_store():
    """Create embeddings and store the documents in ChromaDB."""
    ids, documents = load_documents()
    if not documents:
        raise ValueError("No policy documents found in the docs folder.")

    # Generate embeddings for all policy documents
    embeddings = embedding_model.encode(
        documents,
        normalize_embeddings=True
    ).tolist()

    # Store documents, IDs, and embeddings in ChromaDB
    collection.upsert(ids=ids, documents=documents,embeddings=embeddings )

    print(f"Loaded {len(documents)} documents into ChromaDB.")

# Run the ingestion process when this file is executed directly
if __name__ == "__main__":
    build_vector_store()