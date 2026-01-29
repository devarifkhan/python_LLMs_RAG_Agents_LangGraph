from mem0 import Memory

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

mem_client = Memory.from_client(config)