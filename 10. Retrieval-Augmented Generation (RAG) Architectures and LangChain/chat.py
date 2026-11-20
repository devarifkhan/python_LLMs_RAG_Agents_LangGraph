from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_qdrant import QdrantVectorStore

load_dotenv()

#Vector Embeddings
# Must match the model used in index.py
embedding_model= GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001"
)

vector_db= QdrantVectorStore.from_existing_collection(
    embedding=embedding_model,
    url="http://localhost:6333",
    collection_name="learning_rag"
)

#Take user input and generate response
user_query = input("Ask a question about your PDF: ")

#Relavant chunks
search_results = vector_db.similarity_search(user_query, k=3)

context = "\n\n".join([doc.page_content for doc in search_results])

SYSTEM_PROMPT = """You are a helpful AI assistant that answers questions about the user's document. Use the context provided to answer the question as accurately as possible. If you don't know the answer, just say that you don't know, don't try to make up an answer.

context: {context}
"""

chat_model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

response = chat_model.invoke([
    {
        "role": "system",
        "content": SYSTEM_PROMPT.format(context=context)
    },
    {
        "role": "user",
        "content": user_query
    }
])

print("AI:", response.content)
