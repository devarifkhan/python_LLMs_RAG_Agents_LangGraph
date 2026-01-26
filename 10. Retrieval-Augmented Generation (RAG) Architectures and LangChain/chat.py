from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from openai import OpenAI

load_dotenv()

#Vector Embeddings
embedding_model= OpenAIEmbeddings(
    model="text-embedding-3-large"
)

vector_db= QdrantVectorStore.load_from_vectorstore(
    embedding=embedding_model,
    url="http://localhost:6333",
    collection_name="learning_rag"
)

#Take user input and generate response
user_query = input("Ask about go: ")

#Relavant chunks
search_results = vector_db.similarity_search(user_query, k=3)

context = "\n\n".join([doc.page_content for doc in search_results])

SYSTEM_PROMPT = """You are a helpful AI assistant that helps people find information about the Go programming language. Use the context provided to answer the question as accurately as possible. If you don't know the answer, just say that you don't know, don't try to make up an answer.

context: {context}
"""

client = OpenAI()

response= client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "system",
            "content": SYSTEM_PROMPT.format(context=context)
        },
        {
            "role": "user",
            "content": user_query
        }
    ]
)

print("AI:", response.choices[0].message.content)