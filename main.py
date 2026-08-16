import os
import json
import httpx
from uuid import uuid4
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from Database.crud import get_or_create_users
from tools.definitions import TOOL_DEFINITION
from tools.registry import TOOL_REGISTRY

load_dotenv()
app = FastAPI()

FILE_NAME = 'Data.json'
conversations = {}


class ChatRequest(BaseModel):
    message: str
    conversation_id: str
    platform: str
    platform_user_id: str
    display_name: str | None = None


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
    user = await get_or_create_users(
        platform= request.platform,
        platform_user_id=request.platform_user_id,
        display_name=request.display_name,
    )
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
                "messages": conversations[request.conversation_id],
                "tools": TOOL_DEFINITION,
            }
        )

    data = response.json()
    if "error" in data:
        return {"error": data["error"]["message"]}

    message = data["choices"][0]["message"]
    tool_calls = message.get("tool_calls") or message.get("tool_call") or []

    if tool_calls:
        conversations[request.conversation_id].append(message)

        for call in tool_calls:
            function_data = call.get("function", {})
            tool_name = function_data.get("name")
            raw_arguments = function_data.get("arguments", "{}")

            if isinstance(raw_arguments, str):
                try:
                    arguments = json.loads(raw_arguments)
                except json.JSONDecodeError:
                    arguments = {}
            else:
                arguments = raw_arguments or {}

            print(f"[TOOL CALL]{tool_name}({arguments})")

            tool_function = TOOL_REGISTRY.get(tool_name)
            if tool_function is None:
                result = {"error": f"Tool not found: {tool_name}"}
            else:
                result = tool_function(**arguments)

            print(f"[TOOL RESULT]{result}")

            conversations[request.conversation_id].append({
                "role": "tool",
                "tool_call_id": call.get("id"),
                "name": tool_name,
                "content": json.dumps(result),
            })

    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={"Authorization": f"Bearer {api_key}"},
            json={
                "model": 'meta-llama/llama-3.3-70b-instruct',
                "messages": conversations[request.conversation_id],
                "tools": TOOL_DEFINITION,
            }
        )
        data = response.json()
        print("RAW RESPONSE", json.dumps(data, indent=2))
        message = data["choices"][0]["message"]

    reply = message['content']
    conversations[request.conversation_id].append({"role":"assistant", "content":reply})


       
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