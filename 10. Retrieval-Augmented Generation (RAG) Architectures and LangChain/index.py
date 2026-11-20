import sys
from pathlib import Path
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_qdrant import QdrantVectorStore

load_dotenv()

# Must be the same model in index.py, chat.py and folder 11's worker,
# otherwise the query vectors won't match the stored vectors.
EMBEDDING_MODEL = "models/gemini-embedding-001"

# Index every PDF placed in this folder.
pdf_paths = sorted(Path(__file__).parent.glob("*.pdf"))
if not pdf_paths:
    sys.exit("No PDF found. Place any PDF in this folder and run index.py again.")

# load the files in python program
docs = []
for pdf_path in pdf_paths:
    print(f"Loading {pdf_path.name}")
    docs.extend(PyPDFLoader(file_path=pdf_path).load())

# split the documents into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
)
chunks = text_splitter.split_documents(docs)

# Vector Embeddings
embedding_model = GoogleGenerativeAIEmbeddings(
    model=EMBEDDING_MODEL
)

vector_store = QdrantVectorStore.from_documents(
    documents=chunks,
    embedding=embedding_model,
    url="http://localhost:6333",
    collection_name="learning_rag",
    force_recreate=True,  # rebuild the collection on every run
)

print(f"Indexed {len(chunks)} chunks from {len(pdf_paths)} PDF(s).")
