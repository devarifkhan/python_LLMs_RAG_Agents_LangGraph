# Local LLM Deployment & API Integration

A FastAPI server that puts a REST API in front of a model running locally with [Ollama](https://ollama.com).

| Endpoint | Description |
|---|---|
| `GET /` | Health / welcome message |
| `GET /contact-us` | Contact details, read from `.env` |
| `POST /chat` | Sends `{"message": "..."}` to the local model and returns `{"response": "..."}` |

## Setup

```bash
ollama pull llama3.2            # or any model; set OLLAMA_MODEL to match
pip install fastapi uvicorn ollama python-dotenv
cp .env.example .env
```

## Run

```bash
uvicorn server:app --reload
curl -X POST http://localhost:8000/chat -H "Content-Type: application/json" -d '{"message": "Hello!"}'
```

If Ollama is not running, `/chat` returns **503**. If the model has not been pulled, it returns **502**.
