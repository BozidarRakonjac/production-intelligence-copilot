# Request and response models for chat endpoint

from pydantic import BaseModel
from typing import Optional


class ChatRequest(BaseModel):
    question: str
    session_id: Optional[str] = None


class ChatResponse(BaseModel):
    answer: str
    question: str
    session_id: Optional[str] = None