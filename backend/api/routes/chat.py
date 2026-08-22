# Chat endpoint - simple question in, AI answer out

from fastapi import APIRouter, HTTPException
from api.models.schemas import ChatRequest, ChatResponse
from services.agent import generate_agent_answer

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    try:
        result = generate_agent_answer(request.question)
        answer = result.get("output", "Sorry, I couldn't generate an answer.")

        return ChatResponse(
            answer=answer,
            question=request.question,
            session_id=request.session_id
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))