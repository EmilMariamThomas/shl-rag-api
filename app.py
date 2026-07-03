from fastapi import FastAPI
from pydantic import BaseModel

from agent import chat  # your existing function

app = FastAPI(title="SHL AI Agent")


# ---------- Request Schema ----------
class ChatRequest(BaseModel):
    messages: list


# ---------- Response Schema ----------
class ChatResponse(BaseModel):
    reply: str
    recommendations: list
    end_of_conversation: bool


# ---------- Health Check ----------
@app.get("/")
def home():
    return {"status": "running"}


# ---------- Chat Endpoint ----------
@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):

    result = chat(request.messages)

    return ChatResponse(
        reply=result["reply"],
        recommendations=result["recommendations"],
        end_of_conversation=result["end_of_conversation"]
    )