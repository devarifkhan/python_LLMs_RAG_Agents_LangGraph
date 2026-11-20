# GenAI Learning Repository

Learning repository for my GenAI studies.

It starts with Python concurrency and Pydantic, then covers prompt engineering, local and hosted LLMs, tool-using agents, RAG pipelines (including a queue-based, horizontally scalable one) and agentic workflows with LangGraph. Each folder is a small, self-contained project.

## Contents

| # | Folder | Description | Status |
|---|---|---|---|
| 01 | [MultiThreading, Multiprocessing, GIL in python](<01. MultiThreading, Multiprocessing, GIL in python/>) | Threads vs processes, the GIL, sharing data with `Queue` and `Value` | ✅ Working |
| 02 | [Asyncio in python](<02. Asyncio in python/>) | Event loop, coroutines, mixing asyncio with threads/processes, race conditions and deadlocks | ✅ Working |
| 03 | [pydantic](<03. pydantic/>) | Field and model validators, nested and self-referencing models, computed fields, serialization | ✅ Working |
| 04 | [Core Foundations of Generative AI](<04. Core Foundations of Generative AI/>) | Tokenization with `tiktoken` (encode / decode) | ✅ Working |
| 05 | [Advanced Prompt Engineering Techniques](<05. Advanced Prompt Engineering Techniques/>) | Zero-shot, few-shot, persona and chain-of-thought prompting with Gemini | ✅ Working |
| 06 | [Prompt Serialization & Instruction Formats](<06. Prompt Serialization & Instruction Formats/>) | Notes on Alpaca, ChatML and other prompt formats | ✅ Working |
| 07 | [Local LLM Deployment & API Integration](<07.  Local LLM Deployment & API Integration/>) | FastAPI server in front of a local Ollama model | ✅ Working |
| 08 | [Running LLMs via Hugging Face Hub](<08. Running LLMs via Hugging Face Hub/>) | Running Gemma 3 (image + text) locally with `transformers` (needs a CUDA GPU) | ✅ Working |
| 09 | [Weather Agent](<09. Weather Agent/>) | Agent that detects weather intent, calls the Meteosource API and streams an answer based on real data | ✅ Working |
| 10 | [RAG Architectures and LangChain](<10. Retrieval-Augmented Generation (RAG) Architectures and LangChain/>) | PDF → chunks → Gemini embeddings → Qdrant → retrieval-augmented answers | ✅ Working |
| 11 | [Scalable RAG with Async Queues & Distributed Workers](<11. Scalable RAG with Async Queues & Distributed Workers/>) | FastAPI + Redis/RQ workers that run the RAG pipeline asynchronously | ✅ Working |
| 12 | [Multi Modal Agents](<12. Multi Modal Agents/>) | Text + image prompts to a multimodal model | 🚧 Work in progress |
| 13 | [Building Agentic Workflows with LangGraph](<13. Building Agentic Workflows with LangGraph/>) | LangGraph state graphs, MongoDB checkpointing, LLM-as-judge with a Gemini fallback | ✅ Working |
| 14 | [The Memory Layer](<14. The Memory Layer – Building Short, Long, and Semantic Memory in AI Agents/>) | Long-term / semantic memory for agents with mem0 and Qdrant | 🚧 Work in progress |

## Tech stack

Python · Pydantic · OpenAI SDK · Google Gemini · Ollama · Hugging Face `transformers` · LangChain · LangGraph · Qdrant · MongoDB · Redis / RQ · FastAPI · Docker Compose

## Running a project

Each folder is independent. In general:

1. Create a virtual environment: `python -m venv .venv && source .venv/bin/activate`
2. Install the packages listed in that folder's README (or imported at the top of its scripts).
3. Copy `.env.example` to `.env` in that folder and add your own API keys. `.env` files are git-ignored and no keys are stored in this repository.
4. If the folder has a `docker-compose.yml`, start it with `docker compose up -d`.

Folders 07, 09, 10, 11 and 13 each have their own README with detailed setup steps.
