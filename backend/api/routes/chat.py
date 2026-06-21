# Chat endpoint - wires retrieval + LLM together

from fastapi import APIRouter, HTTPException
from api.models.schemas import ChatRequest, ChatResponse, SourceDocument
from services.retrieval import hybrid_search
from services.llm import generate_answer

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    try:
        filters = {
            "filter_machine_type": request.filter_machine_type,
            "filter_source_table": request.filter_source_table,
            "filter_date_from": request.filter_date_from,
            "filter_date_to": request.filter_date_to,
        }

        # Step 1 - Hybrid search for relevant context
        search_results = hybrid_search(request.question, filters)

        # Step 2 - Generate AI answer grounded in context
        answer = generate_answer(request.question, search_results)

        # Step 3 - Format sources for response
        sources = [
            SourceDocument(
                content=result["content"],
                source_table=result["metadata"].get("source_table", "unknown"),
                machine_type=result["metadata"].get("machine_type", "unknown"),
                event_date=result["metadata"].get("event_date", "unknown"),
                score=result["score"]
            )
            for result in search_results
        ]

        return ChatResponse(
            answer=answer,
            sources=sources,
            question=request.question,
            session_id=request.session_id
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))