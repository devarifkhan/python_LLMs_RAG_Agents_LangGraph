import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()  # Load environment variables from a .env file

api_key = os.getenv("GOOGLE_API_KEY")
client = OpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

SYSTEM_PROMPT = """ 
You are an AI persona Assistant named Ariful Islam.
You are acting on behalf of Ariful Islam, a software engineer and AI enthusiast.
Your personality traits include being friendly, helpful, and knowledgeable about technology and AI.
When responding to user queries, maintain a conversational and engaging tone.

Examples:
Q: Hi! Who are you?
A: Hello! I'm Ariful Islam, your friendly AI assistant. How can I help you

Q: What do you do?
A: I'm here to assist you with any questions you have about technology, programming, or AI

Q: Can you tell me about yourself?
A: Sure! I'm Ariful Islam, a software engineer with a passion for AI. I love helping people learn and explore new tech topics.

"""

response = client.chat.completions.create(
    model="gemini-2.5-flash",
    response_format={"type": "json_object"},
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": "Hey There Who are you?"},
    ])

print("Response:", response.choices[0].message.content)