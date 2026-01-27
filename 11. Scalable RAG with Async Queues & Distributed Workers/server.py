from fastapi import FastAPI,Query
from client.rq_client import queue
from .queues.worker import worker_queue

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Server is running"}

@app.post("/chat")
def chat(
    query: str = Query(..., description="The input query for the chat model")
):
    job = queue.enqueue(worker_queue, query)
    return {"status":"queued","job_id":job.id}