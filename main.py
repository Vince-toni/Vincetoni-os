import sys
import os

# Dynamically force project root into Python search path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import json
import httpx
import inspect
from dotenv import load_dotenv
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Internal imports now work safely regardless of working directory
from database.crud import get_or_create_user
from tools.definitions import TOOL_DEFINITIONS
from tools.registry import TOOL_REGISTRY
from system_prompt import VINCETONI_SYSTEM_PROMPT
from models import get_model

load_dotenv()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # your Vite dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

FILE_NAME = 'Data.json'
conversations = {}

class ChatRequest(BaseModel):
    message: str
    conversation_id: str
    platform: str | None = None
    platform_user_id: str | None = None
    display_name: str | None = None
    model: str = "default"


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
    if not request.platform or not request.platform_user_id:
        return {"error": "platform and platform_user_id are required."}

    selected_model = get_model(request.model)

    user = await get_or_create_user(
        platform=request.platform,
        platform_user_id=request.platform_user_id,
        display_name=request.display_name,
    )

    api_key = os.getenv('OPENROUTER_API')

    if request.conversation_id not in conversations:
        conversations[request.conversation_id] = [
            {"role": "system", "content": VINCETONI_SYSTEM_PROMPT}
        ]

    conversations[request.conversation_id].append(
        {"role": "user", "content": request.message}
    )

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={"Authorization": f"Bearer {api_key}"},
            json={
                "model": selected_model,
                "messages": conversations[request.conversation_id],
                "tools": TOOL_DEFINITIONS,
            }
        )

    data = response.json()
    if "error" in data:
        return {"error": data["error"]["message"]}

    message = data["choices"][0]["message"]
    tool_calls = message.get("tool_calls") or []

    if tool_calls:
        conversations[request.conversation_id].append(message)

        for call in tool_calls:
            function_data = call.get("function", {})
            tool_name = function_data.get("name")
            raw_arguments = function_data.get("arguments", "{}")

            try:
                arguments = json.loads(raw_arguments) if isinstance(raw_arguments, str) else (raw_arguments or {})
            except json.JSONDecodeError:
                arguments = {}

            print(f"[TOOL CALL] {tool_name}({arguments})")

            tool_function = TOOL_REGISTRY.get(tool_name)

            if tool_function is None:
                result = {"error": f"Unknown tool: {tool_name}"}
            elif inspect.iscoroutinefunction(tool_function):
                result = await tool_function(**arguments)
            else:
                result = tool_function(**arguments)

            print(f"[TOOL RESULT] {result}")

            conversations[request.conversation_id].append({
                "role": "tool",
                "tool_call_id": call.get("id"),
                "name": tool_name,
                "content": json.dumps(result),
            })

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={"Authorization": f"Bearer {api_key}"},
                json={
                    "model": selected_model,
                    "messages": conversations[request.conversation_id],
                }
            )
        data = response.json()
        message = data["choices"][0]["message"]

    reply = message["content"]
    conversations[request.conversation_id].append({"role": "assistant", "content": reply})

    usage = data.get("usage", {})

    save_data({
        "user_id": str(user.id),
        "platform": request.platform,
        "conversation_id": request.conversation_id,
        "message": request.message,
        "reply": reply,
        "model": data.get("model"),
        "tokens_used": usage.get("total_tokens"),
        "cost": usage.get("cost"),
    })

    return {"reply": reply}