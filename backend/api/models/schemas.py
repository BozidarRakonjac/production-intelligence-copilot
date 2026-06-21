# Request and response models for chat endpoint

from pydantic import BaseModel
from typing import Optional


class ChatRequest(BaseModel):
    question: str
    session_id: Optional[str] = None              # for conversation history
    filter_machine_type: Optional[str] = None     # "L", "M", "H"
    filter_source_table: Optional[str] = None     # "downtime", "quality", "production"
    filter_date_from: Optional[str] = None        # "2026-06-01"
    filter_date_to: Optional[str] = None          # "2026-06-30"


class SourceDocument(BaseModel):
    content: str
    source_table: str
    machine_type: str
    event_date: str
    score: float


class ChatResponse(BaseModel):
    answer: str
    sources: list[SourceDocument]
    question: str
    session_id: Optional[str] = None