# Zepto Support Assistant

A simple RAG-based customer support assistant for answering Zepto policy questions.

## Features

- 8 Zepto policy documents
- Local embeddings using `all-MiniLM-L6-v2`
- ChromaDB for document retrieval
- LangGraph for query routing
- FastAPI REST API
- Docker support
- Offline mock mode for deterministic answers

## RAG Pipeline

```text
Documents
   ↓
Ingestion & Chunking
   ↓
Embeddings
(all-MiniLM-L6-v2)
   ↓
ChromaDB
   ↓
Query Retrieval
   ↓
LangGraph
   ↓
Answer Generation
```

### Pipeline Flow

Ingestion – app/ingestion.py loads the 8 policy documents and stores their embeddings in ChromaDB.
Embedding – all-MiniLM-L6-v2 converts documents and user queries into vectors.
Retrieval – retrieve_and_answer retrieves the top 3 relevant documents from ChromaDB.
Generation – LangGraph generates the final answer using the retrieved context.
Routing – classify_intent sends policy questions to retrieval and other questions to direct_answer.

By default, MOCK_LLM=1 is used. In this mode, no external LLM API is required.

## API

POST /ask

Request:

```json
{
  "query": "How much is the delivery fee?"
}
```

Response:

```json
{
  "answer": "Based on the retrieved context: Delivery Policy...",
  "sources": ["doc_01", "doc_05", "doc_02"],
  "confidence": 1.0
}
```

General Question

Request:

```json
{
  "query": "What is Python?"
}
```

Response:

```json
{
  "answer": "I can only answer questions about Zepto policies right now.",
  "sources": [],
  "confidence": 1.0
}
```

## Run Locally

Activate the virtual environment:

```powershell
.\.venv\Scripts\Activate
```

Run the FastAPI application:

```bash
uvicorn main:app --reload
```

Open the Swagger UI:

http://127.0.0.1:8000/docs

## Docker

Build the Docker image:

```bash
docker build -t zepto-support-assistant .
```

Run the container:

```bash
docker run -d -p 8000:8000 --name zepto-support zepto-support-assistant
```

Open the API documentation:

http://127.0.0.1:8000/docs

Check the running container:

```bash
docker ps
```

## Project Structure

```text
support_assistant/
├── app/
│   ├── ingestion.py
│   ├── graph.py
│   ├── models.py
│   └── prompts.py
├── docs/
│   ├── doc_01.txt
│   ├── doc_02.txt
│   ├── doc_03.txt
│   ├── doc_04.txt
│   ├── doc_05.txt
│   ├── doc_06.txt
│   ├── doc_07.txt
│   └── doc_08.txt
├── chroma_db/
├── main.py
├── Dockerfile
├── requirements.txt
└── README.md
```

## Technologies Used

Python
FastAPI
LangGraph
ChromaDB
Sentence Transformers
Pydantic
Docker