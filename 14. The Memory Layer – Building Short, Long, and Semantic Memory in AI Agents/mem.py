# WORK IN PROGRESS
# This mem0 memory-layer example is not finished and does not run as-is:
# the embedding/LLM model names and the OpenAI vs Gemini client setup still need fixing.
# See the root README for the status of every folder.

from mem0 import Memory
from dotenv import load_dotenv
import os

from openai import OpenAI

load_dotenv()

client= OpenAI()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

config = {
    "version":"v1.1",
    "embedder":{
        "provider":"gemini",
        "config":{
            "model":"text-embedding-3-small",
            "api_key":GEMINI_API_KEY
        }   
    },
    "llm":{
        "provider":"gemini",
        "config":{
            "model":"gemini-1.5-pro-flash",
            "api_key":GEMINI_API_KEY
        }
    },
    "vector_store":{
        "provider":"qdrant",
        "config":{
            "host":"localhost",
            "port":6333
        }
    }

}

mem_client = Memory.from_config(config)
while True:

    user_query = input("Enter your query: ")
    
    search_memory = mem_client.search(
        user_id="arifkhan",
        query=user_query
    )
    
    memories  = [
        f'ID: {mem.get("id")}\nMemory: {mem.get("memory")}'  for mem in search_memory.get("results")
    ]
    
    print("Found memories")
    
    SYSTEM_PROMPT = f"""
    Here is context of the user's conversation history:
    {memories}
    """

    response = client.chat.completions.create(
        model="gemini-1.5-pro-flash",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_query}
        ]
    )
    ai_response =response.choices[0].message.content

    print("AI",ai_response)

    mem_client.add(
        user_id="arifkhan",
        messages=[
            {"role":"user","content":user_query},
            {"role":"assistant","content":ai_response}
        ]
    )


    print("Memory has been saved...")