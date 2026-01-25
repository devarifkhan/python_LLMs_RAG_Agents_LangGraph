import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GOOGLE_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

MODEL = "gemini-2.5-flash"

def ask_llm(messages):
    response = client.chat.completions.create(
        model=MODEL,
        response_format={"type": "json_object"},
        messages=messages,
    )
    return json.loads(response.choices[0].message.content)

# -------------------------
# STEP 1: START
# -------------------------
user_query = input("👉 ")

start_prompt = f"""
Return ONLY JSON.

Format:
{{"step":"START","CONTENT":"string"}}

User query:
{user_query}
"""

start_res = ask_llm([
    {"role": "system", "content": "You structure user input."},
    {"role": "user", "content": start_prompt}
])

print(f"User Query: {start_res['CONTENT']}")

# -------------------------
# STEP 2: PLAN (Observable CoT)
# -------------------------
plan_prompt = f"""
You are solving the following problem:

{user_query}

Break the solution into clear logical steps.
Do NOT solve it yet.

Return ONLY JSON ARRAY.

Format:
[
  {{"step":"PLAN","CONTENT":"string"}}
]
"""

plan_res = ask_llm([
    {"role": "system", "content": "You plan solutions step by step."},
    {"role": "user", "content": plan_prompt}
])

for p in plan_res:
    print(f"Thinking: {p['CONTENT']}")

# -------------------------
# STEP 3: OUTPUT
# -------------------------
output_prompt = f"""
Solve the problem completely now:

{user_query}

Return ONLY JSON.

Format:
{{"step":"OUTPUT","CONTENT":"string"}}
"""

output_res = ask_llm([
    {"role": "system", "content": "You solve problems accurately."},
    {"role": "user", "content": output_prompt}
])

print(f"Final Output: {output_res['CONTENT']}")
