from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.llm import LLMService
from app.services.retriever import Retriever
from fastapi.responses import StreamingResponse
from app.services.cache import get_cache, set_cache
from typing import List,Optional
from pydantic import BaseModel

router =APIRouter()
retriever = Retriever()
llm = LLMService()

class Message(BaseModel):
    role: str
    content: str

class QueryRequest(BaseModel):
    question: str
    history: Optional[List[Message]] = []

#Standard endpoint for testing 
@router.post("/query")
async def query_rag(request: QueryRequest):
    # Step 1: Retrieve relevant context
    context = retriever.retrieve(request.question)
    # Step 2: Generate answer using LLM with streaming response
    answer = llm.stream(context, request.question)
    return{
        "answer":answer
    }


#Streaming endpoint (for UI)
@router.post("/query-stream")
async def query_rag_stream(request: QueryRequest):
    cached = get_cache(request.question)
    if cached:
        def stream_cache():
            for char in cached:
                yield char
        return StreamingResponse(stream_cache(), media_type="text/plain")
    try:
        context = retriever.retrieve(request.question)
        def generate():
            full_response = ""
            for token in llm.stream(context, request.question, request.history or []):
                yield token
            set_cache(request.question, full_response)
        return StreamingResponse(generate(), media_type="text/plain")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
