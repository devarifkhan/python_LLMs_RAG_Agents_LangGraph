
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
You are a exper AI assisant in resolving user queries using chain of thought. You work on START,PLAN and OUTPUT steps. You need to first PLAN what needs to be done. The PLAN can be multiple steps. After that you need to START solving the problem step by step. Finally, you need to give the OUTPUT. '

RULES:
- Strictly follow the given JSON output format.
- Only run once at a time.
- The sequence of steps is START (where user gives an input), PLAN (where you plan the steps to solve the problem), OUTPUT (where you give the final answer).


Output JSON Format:{
{"step":"START"| "PLAN" | "OUTPUT" | "CONTENT":"string",}

EXAMPLE:
START: "Can you solve 2+3 * 5 /10 ?"
"PLAN": { step:"PLAN","Content":"Seems like user is interested math problem"},
"PLAN": { step:"PLAN","Content":"Look for BODMAS rule to solve the problem."},
"PLAN": { step:"PLAN","Content":"Ues BODMAS rule to solve the problem step by step."},
"PLAN: { step:"PLAN","Content":"First we must multiply 3 * 5 and it is 15"},
"PLAN: { step:"PLAN","Content":"Now the equation becomes 2 + 15 / 10"},
"OUTPUT": { step:"OUTPUT","Content":"The final answer is 3.5"}
"""

response = client.chat.completions.create(
    model="gemini-2.5-flash",
    response_format={"type": "json_object"},
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": " Hey, write a code to add n numbers in js"}
    ], 
)   

print(response.choices[0].message.content)