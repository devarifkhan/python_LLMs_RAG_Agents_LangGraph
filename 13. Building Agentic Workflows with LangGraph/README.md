# Building Agentic Workflows with LangGraph

Three small LangGraph examples.

| File | What it shows |
|---|---|
| `chat.py` | A minimal two-node graph (`chatbot` → `samplenode`) with a `messages` state |
| `chat_checkpoint.py` | The same graph with a **MongoDB checkpointer**: state is saved per `thread_id` and survives restarts |
| `chat_2.py` | **LLM-as-judge with fallback**: an OpenAI model answers, a judge node scores the answer, and if it is not good a Gemini node answers instead |

```
chat_2.py:  START → chatbot (OpenAI) → evaluate ──good──▶ endnode → END
                                          └──bad──▶ chatbot_gemini → endnode
```

## Setup

```bash
pip install langgraph langgraph-checkpoint-mongodb langchain-openai openai python-dotenv pydantic
cp .env.example .env    # then fill in your keys and a MongoDB password
```

The MongoDB username and password live only in `.env`. Both `docker-compose.yml` and `chat_checkpoint.py` read them from there.

## Run

```bash
python chat.py

# MongoDB checkpointer
docker compose up -d          # starts MongoDB with the credentials from .env
python chat_checkpoint.py     # run it twice: the stored message count grows (3 → 6)

# LLM-as-judge with Gemini fallback (needs OPENAI_API_KEY and GOOGLE_API_KEY)
python chat_2.py
```

Stop MongoDB with `docker compose down` (add `-v` to delete the stored data).
