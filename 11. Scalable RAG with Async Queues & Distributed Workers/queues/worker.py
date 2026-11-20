import os
from dotenv import load_dotenv
from langchain_qdrant import QdrantVectorStore
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from google import genai

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

# vector embeddings
embedding_model = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001",  # must match folder 10 index.py
    google_api_key=api_key,
)

vector_db = QdrantVectorStore.from_existing_collection(
    embedding=embedding_model,
    collection_name="learning_rag",
    url="http://localhost:6333",
)

gemini_client = genai.Client(api_key=api_key)


def worker_queue(query: str):
    print("Searching chunks in vector DB...", query)
    search_results = vector_db.similarity_search(query, k=3)
    context = "\n".join([doc.page_content for doc in search_results])
    print("Context retrieved from vector DB:", context)

    SYSTEM_PROMPT = """You are a helpful AI assistant that answers questions about the user's document. Use the context provided to answer the question as accurately as possible. If you don't know the answer, just say that you don't know, don't try to make up an answer.
    context: {context}"""

    response = gemini_client.models.generate_content(
        model="gemini-2.5-flash",
        contents=query,
        config={
            "system_instruction": SYSTEM_PROMPT.format(context=context),
        },
    )

    print("AI Response:", response.text)
    return response.text
