from fastapi import FastAPI
from pydantic import BaseModel

from agent import chat

app = FastAPI(title="SHL AI Agent")


class ChatRequest(BaseModel):
    messages: list


class ChatResponse(BaseModel):
    reply: str
    recommendations: list
    end_of_conversation: bool


@app.get("/")
def home():
    return {"message": "SHL AI Agent is running"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):

    result = chat(request.messages)

    return ChatResponse(
        reply=result["reply"],
        recommendations=result["recommendations"],
        end_of_conversation=result["end_of_conversation"]
    )