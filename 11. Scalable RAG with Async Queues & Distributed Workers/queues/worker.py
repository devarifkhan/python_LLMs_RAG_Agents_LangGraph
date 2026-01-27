from re import search
from tkinter.filedialog import Open
from urllib import response
from openai import OpenAI

from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
import os

api_key = os.getenv("GOOGLE_API_KEY")


openai_client = OpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)



# vector embeddings
embedding_model = OpenAIEmbeddings(model="text-embedding-3-large")

vector_db = QdrantVectorStore.from_existing_collection(
    embedding=embedding_model,
    collection_name="learning_rag",
    url="http://localhost:6333",
)

def process_query(query:str):
    print("Searching chunks in vector DB...",query)
    search_results = vector_db.similarity_search(query, k=3)
    context = "\n".join([doc.page_content for doc in search_results])
    print("Context retrieved from vector DB:",context)
    
    SYSTEM_PROMPT = """You are a helpful AI assistant that helps people find information about the Go programming language. Use the context provided to answer the question as accurately as possible. If you don't know the answer, just say that you don't know, don't try to make up an answer.
    context: {context}"""
    


    response= openai_client.chat.completions.create(
        model="gemini-2.5-flash",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT.format(context=context)
            },
            {
                "role": "user",
                "content": query
            }
        ]
    )
    
    print("AI Response:",response.choices[0].message.content)