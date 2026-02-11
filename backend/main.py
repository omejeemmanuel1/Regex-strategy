from fastapi import FastAPI, Request, Response, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import List, Union
from models import ParseRequest, ParseResponse, ErrorResponse
from parser import parse_invoice_text
import time

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Make these attributes of the app instance
app.idempotency_store = {}
app.rate_limit_store = {} # Renamed for clarity

# Middleware for rate limiting and payload size
@app.middleware("http")
async def add_process_middleware(request: Request, call_next):
    # Basic Rate Limiting (e.g., 5 requests per minute per IP)
    # In a real application, use a more robust solution like Redis
    client_ip = request.client.host
    current_time = time.time()
    
    if client_ip not in app.rate_limit_store:
        app.rate_limit_store[client_ip] = []
    
    # Remove requests older than 1 minute
    app.rate_limit_store[client_ip] = [
        t for t in app.rate_limit_store[client_ip] if current_time - t < 60
    ]

    if len(app.rate_limit_store[client_ip]) >= 5:
        return JSONResponse(status_code=429, content={"detail": "Too many requests"})
    
    app.rate_limit_store[client_ip].append(current_time)

    # Payload Size Limit (e.g., 100KB)
    # For simplicity, we'll check content length for text.
    # For actual file uploads, you'd check request.stream()
    if request.headers.get("content-length"):
        content_length = int(request.headers["content-length"])
        if content_length > 1024 * 100:  # 100 KB
            return JSONResponse(status_code=413, content={"detail": "Payload too large"})

    response = await call_next(request)
    return response

@app.post("/parse", response_model=ParseResponse)
async def parse_content(request: ParseRequest, request_id: Union[str, None] = Header(default=None)):
    if request_id:
        if request_id in app.idempotency_store:
            return JSONResponse(content=app.idempotency_store[request_id], status_code=200)

    if isinstance(request.content, str):
        extracted_items = parse_invoice_text(request.content)
    else:
        extracted_items = []
        for text_block in request.content:
            extracted_items.extend(parse_invoice_text(text_block))
    
    response_content = {"extracted_items": extracted_items}

    if request_id:
            app.idempotency_store[request_id] = response_content

    return response_content

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
