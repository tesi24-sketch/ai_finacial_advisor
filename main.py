from fastapi import FastAPI
from pydantic import BaseModel
from claude_client import chat

app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    session_id: str
    message: str

@app.post("/chat")
def chat_endpoint(req: ChatRequest):
    reply = chat(req.session_id, req.message)
    return {"reply": reply}
