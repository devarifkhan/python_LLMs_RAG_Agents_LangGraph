# Retrieval-Augmented Generation (RAG) with LangChain

A basic RAG pipeline over your own PDF:

```
PDF ──▶ PyPDFLoader ──▶ 1000-char chunks ──▶ Gemini embeddings ──▶ Qdrant
                                                                     │
question ──▶ similarity search (top 3) ──▶ Gemini 2.5 Flash + context ──▶ answer
```

| File | Purpose |
|---|---|
| `index.py` | Loads every PDF in this folder, splits it into chunks, embeds them with `gemini-embedding-001` and stores them in Qdrant (`learning_rag` collection) |
| `chat.py` | Asks for a question, retrieves the 3 most relevant chunks and answers with Gemini 2.5 Flash |
| `docker-compose.yml` | Qdrant on port 6333 |

## Setup

```bash
pip install langchain-community langchain-text-splitters langchain-google-genai langchain-qdrant pypdf python-dotenv
echo "GOOGLE_API_KEY=your_key_here" > .env
docker compose up -d
```

**Place any PDF in this folder.** PDFs are git-ignored, so none are included in the repo.

## Run

```bash
python index.py   # rebuilds the collection from the PDFs in this folder
python chat.py
```

The collection is also used by folder 11 (Scalable RAG). Both folders use the same embedding model, `gemini-embedding-001`.
