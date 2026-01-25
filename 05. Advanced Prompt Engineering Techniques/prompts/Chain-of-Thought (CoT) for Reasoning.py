
import os
from dotenv import load_dotenv
from openai import OpenAI
import json

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

message_history = [
    {
        'role': 'system', 'content': SYSTEM_PROMPT,
    }
]


user_query = input("👉")
message_history.append({'role': 'user', 'content': user_query})

while True:
    response = client.chat.completions.create(
        model="gemini-2.5-flash",
        response_format={"type": "json_object"},
        messages=message_history,
    )
    raw_content = response.choices[0].message.content
    message_history.append({'role': 'assistant', 'content': raw_content})
    parsed_content = json.loads(raw_content)

    # Always handle as a list for consistency
    steps = parsed_content if isinstance(parsed_content, list) else [parsed_content]
    for item in steps:
        if item['step'] == 'START':
            print(f"User Query: {item['CONTENT']}")
        elif item['step'] == 'PLAN':
            print(f"Thinking: {item['CONTENT']}")
        elif item['step'] == 'OUTPUT':
            print(f"Final Output: {item['CONTENT']}")
            exit(0)
    # After the first response, send a 'continue' message to get the next step
    message_history.append({'role': 'user', 'content': 'continue'})
