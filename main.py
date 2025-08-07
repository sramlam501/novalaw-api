from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import os

app = FastAPI()

# CORS – allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to Framer domain later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request body model
class AskRequest(BaseModel):
    question: str

# POST /ask – AI answer via Ollama Qwen
@app.post("/ask")
def ask_legal_ai(request: AskRequest):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "qwen:7b",
            "prompt": request.question,
            "stream": False
        }
    )
    result = response.json()
    return {"answer": result.get("response", "No answer returned")}

# GET /template/{name} – Return static legal template from file
@app.get("/template/{name}")
def get_template(name: str):
    try:
        with open(f"templates/{name}.txt", "r", encoding="utf-8") as file:
            content = file.read()
            return {"template": content}
    except FileNotFoundError:
        return {"error": "Template not found"}
