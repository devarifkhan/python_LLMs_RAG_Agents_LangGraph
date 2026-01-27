from fastapi import FastAPI, Query
from pydantic import BaseModel
from client.rq_client import queue
from queues.worker import worker_queue

app = FastAPI()

class ChatRequest(BaseModel):
    query: str

@app.get("/")
def root():
    return {"message": "Server is running"}

@app.post("/chat")
def chat(request: ChatRequest):
    job = queue.enqueue(worker_queue, request.query)
    return {"status":"queued","job_id":job.id}

@app.get('/job-status')
def get_result(job_id: str= Query(..., description="The job ID to fetch the result for")):
    job = queue.fetch_job(job_id=job_id)
    
    result = job.return_value()
    return {"result": result}