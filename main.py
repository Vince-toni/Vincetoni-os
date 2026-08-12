import os
import json
import httpx
from uuid import uuid4
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel

load_dotenv()
app = FastAPI()

FILE_NAME = 'Data.json'
conversations = {}


class ChatRequest(BaseModel):
    message: str
    conversation_id: str


@app.get('/')
def read_root():
    return {"message": "HELLO VINCETONI"}


def save_data(entry: dict):
    """Append one conversation entry to the JSON log file."""
    history = []

    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, 'r', encoding='UTF-8') as file:
            content = file.read().strip()
            if content:
                try:
                    history = json.loads(content)
                    if not isinstance(history, list):
                        history = []
                except json.JSONDecodeError:
                    history = []

    history.append(entry)

    with open(FILE_NAME, 'w', encoding='UTF-8') as file:
        json.dump(history, file, indent=4)


@app.post('/v1/chat')
async def chat(request: ChatRequest):
    api_key = os.getenv('OPENROUTER_API')

    if request.conversation_id not in conversations:
        conversations[request.conversation_id] = []

    conversations[request.conversation_id].append(
        {"role": "user", "content": request.message}
    )

    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={"Authorization": f"Bearer {api_key}"},
            json={
                "model": 'meta-llama/llama-3.3-70b-instruct',
                "messages": conversations[request.conversation_id]
            }
        )

    data = response.json()

    if "error" in data:
        return {"error": data["error"]["message"]}

    reply = data["choices"][0]["message"]["content"]

    conversations[request.conversation_id].append(
        {"role": "assistant", "content": reply}
    )

    usage = data.get("usage", {})

    save_data({
        "message": request.message,
        "id": conversations[request.conversation_id],
        "reply": reply,
        "model": data.get("model"),
        "tokens_used": usage.get("total_tokens"),
        "cost": usage.get("cost"),
    })

    return {"reply": reply}