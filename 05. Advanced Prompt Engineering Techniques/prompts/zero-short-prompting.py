
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()  # Load environment variables from a .env file

api_key = os.getenv("GOOGLE_API_KEY")
client = OpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"

)

# Zero-shot prompting Definition: A technique where the model is given a task without any prior examples or demonstrations.
SYSTEM_PROMPT = """You are a expert in Maths and only and only answer math related questions.
If the question is not related to math, respond with 'I can only answer math related questions.'"""

response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": "Hey, can you tell me a joke?"}
    ], 
)   

print(response.choices[0].message.content)