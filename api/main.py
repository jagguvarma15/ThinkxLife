from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import traceback
import os

from chatbot.chatbot_core import generate_response

class ChatRequest(BaseModel):
    message: str
    history: list = []  # default to empty if omitted

class ChatResponse(BaseModel):
    response: str

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    try:
        # DEBUG: print the API key to verify .env loaded
        print("OPENAI_API_KEY =", os.getenv("OPENAI_API_KEY")[:8] + "…")
        # Generate response with only message and history
        reply = generate_response(req.message, req.history)
        return ChatResponse(response=reply)

    except Exception as e:
        # print full traceback to your Uvicorn console
        print("Exception in /chat:")
        traceback.print_exc()
        # return a clean HTTP 500 with the error message
        raise HTTPException(status_code=500, detail=str(e))
