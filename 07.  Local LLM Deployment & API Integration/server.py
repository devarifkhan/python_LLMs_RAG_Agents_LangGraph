from fastapi import FastAPI, Body

app = FastAPI()
client= Client(
    host="http://localhost:11434",
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Local LLM Deployment & API Integration Server!"} 

@app.get("/contact-us")
def contact_us():
    return {
        "email": "arifcse209@gmail.com",
        "phone": "+8801764297928",
        "address": "Comilla, Bangladesh"
    }

@app.post("/chat")
def chat(
    message: str = Body(..., description="The message to send to the LLM"),
):
    response = client.chat.completions.create(
        model="local-llm-model",
        messages=[
            {"role": "user", "content": message}
        ]
    )
    return {"response": response.choices[0].message["content"]}
