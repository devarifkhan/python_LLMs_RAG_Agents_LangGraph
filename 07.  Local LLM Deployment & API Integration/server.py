from fastapi import FastAPI

app = FastAPI()

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