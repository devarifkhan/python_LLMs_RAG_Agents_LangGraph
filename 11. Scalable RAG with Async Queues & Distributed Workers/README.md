# Scalable RAG with Async Queues & Distributed Workers

A question-answering API over your own PDF. Questions are not answered inside the HTTP request. Instead, the API puts each one on a **Redis queue** and returns a `job_id` straight away. A separate **RQ worker** runs the RAG pipeline: it searches **Qdrant** for the most relevant chunks and asks **Gemini 2.5 Flash** to answer from them. You can add more workers to handle more load.

```
client ──POST /chat──▶ FastAPI ──enqueue──▶ Redis ──▶ RQ worker(s)
   ▲                                                    │
   │                                     Qdrant search (top 3 chunks)
   │                                                    │
   └──GET /job-status?job_id=…── FastAPI ◀── result ── Gemini 2.5 Flash
```

## Project structure

| Path | Purpose |
|---|---|
| `server.py` | FastAPI app: `POST /chat` queues a job, `GET /job-status` returns its status and result |
| `queues/worker.py` | The job the worker runs: Qdrant similarity search, then the Gemini call |
| `client/rq_client.py` | Redis connection and RQ queue |
| `main.py` | Starts the API with uvicorn on port 8000 |
| `docker-compose.yml` | Qdrant (port 6333) and Redis (port 6379) |

## Requirements

- Python 3.10+
- Docker
- A Google Gemini API key

```bash
pip install fastapi uvicorn rq redis python-dotenv langchain-qdrant langchain-google-genai google-genai
```

Create a `.env` file in this folder:

```
GOOGLE_API_KEY=your_key_here
```

## How to run

**1. Start Qdrant and Redis**

```bash
docker compose up -d
```

**2. Index the PDF (one time only)**

The `learning_rag` collection is built by the indexing script in folder 10, which uses the same embedding model as the worker (`gemini-embedding-001`). Place any PDF in folder 10, then run:

```bash
cd "../10. Retrieval-Augmented Generation (RAG) Architectures and LangChain"
python index.py
```

**3. Start a worker** (from this folder; open more terminals to add more workers)

```bash
rq worker --url redis://localhost:6379
```

> On macOS, run `export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES` first.

**4. Start the API**

```bash
python main.py
```

## Usage

```bash
# Queue a question
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What is this document about?"}'
# → {"status": "queued", "job_id": "abc123..."}

# Check the result
curl "http://localhost:8000/job-status?job_id=abc123..."
# → {"status": "finished", "result": "The document is about ..."}
```

The `status` field can be `queued`, `started`, `finished` or `failed`. `result` is `null` until the job finishes. If the `job_id` is unknown, the API returns **404**.

Interactive API docs: http://localhost:8000/docs
