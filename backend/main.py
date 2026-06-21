# FastAPI app entry point

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes.chat import router as chat_router

app = FastAPI(
    title="Production Intelligence Copilot",
    description="AI-powered manufacturing assistant",
    version="1.0.0"
)

# CORS - allows React Native frontend to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(chat_router, prefix="/api/v1", tags=["chat"])

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "Production Intelligence Copilot"}