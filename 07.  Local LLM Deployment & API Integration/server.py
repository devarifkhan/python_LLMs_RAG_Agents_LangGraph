import os

from dotenv import load_dotenv
from fastapi import FastAPI, Body, HTTPException
from ollama import Client, ResponseError

load_dotenv()

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")

app = FastAPI()
client = Client(host=OLLAMA_HOST)


@app.get("/")
def read_root():
    return {"message": "Welcome to the Local LLM Deployment & API Integration Server!"}


@app.get("/contact-us")
def contact_us():
    # Contact details come from .env so that no personal data is stored in the code.
    return {
        "email": os.getenv("CONTACT_EMAIL", ""),
        "phone": os.getenv("CONTACT_PHONE", ""),
        "address": os.getenv("CONTACT_ADDRESS", ""),
    }


@app.post("/chat")
def chat(
    message: str = Body(..., embed=True, description="The message to send to the LLM"),
):
    try:
        response = client.chat(
            model=OLLAMA_MODEL,
            messages=[{"role": "user", "content": message}],
        )
    except ResponseError as e:
        # e.g. the model has not been pulled yet
        raise HTTPException(status_code=502, detail=f"Ollama error: {e.error}")
    except ConnectionError:
        raise HTTPException(status_code=503, detail=f"Cannot reach Ollama at {OLLAMA_HOST}. Is it running?")

    return {"response": response.message.content}
