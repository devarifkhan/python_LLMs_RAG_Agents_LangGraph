
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()  # Load environment variables from a .env file

api_key = os.getenv("GOOGLE_API_KEY")
client = OpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"

)

# Few-shot prompting Definition: A technique where the model is given a task with a few examples or demonstrations.
SYSTEM_PROMPT = """You are a coding expert and only answer coding related questions.
If the question is not related to coding, respond with 'I can only answer coding related questions.

Here are some examples:
Q: What is 5 + 7?
A: I can only answer coding related questions.

Q: What is the capital of France?
A: I can only answer math related questions.



Q: Who wrote 'To Kill a Mockingbird'?
A: I can only answer coding related questions.

Q: Hey, Write a code in python for adding two numbers.
A: def add(a, b):
    return a + b


'"""

response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": "Hey, can you write a binary search algorithm in Python?"}
    ], 
)   

print(response.choices[0].message.content)