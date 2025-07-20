from fastapi import FastAPI,HTTPException, File, UploadFile, BackgroundTasks, Depends, Body, Query, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
import sys
import logging
import tempfile
from contextlib import asynccontextmanager

from models.schema import ConversationSummaryModel

from services.conversation_summarizer.conversation_summarizer import conversation_summarizer_router
from services.data_extraction.extraction import data_extraction_router
from services.rag.rag import rag_router

# Configure logging
logger = logging.getLogger("Helper Server")

# Initialize FastAPI app
app = FastAPI(
    title="Helper Server    API",
    description="API for Helper Server",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/health")
async def health_check():
    try:
        # Simulate a potential error condition (replace with your actual check)
        return JSONResponse(content={"status": "healthy"})
    except Exception as e:
        raise HTTPException(status_code=500, detail={"status": "error", "message": str(e)})


app.include_router(conversation_summarizer_router, tags=["Conversation Summarizer"])
app.include_router(data_extraction_router, tags=["Data Extraction"])
app.include_router(rag_router, tags=["RAG"])
