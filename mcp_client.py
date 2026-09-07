from contextlib import AsyncExitStack
import httpx2
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client
import os
from dotenv import load_dotenv

load_dotenv()

mcp_session: ClientSession | None = None
_exit_stack: AsyncExitStack | None = None

mcp_tool_definitions = []

async def start_mcp():
    global mcp_session, _exit_stack, mcp_tool_definitions
    _exit_stack = AsyncExitStack()

    url = "https://api.githubcopilot.com/mcp/"
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        raise RuntimeError("GITHUB_TOKEN is not set")

    http_client = await _exit_stack.enter_async_context(
        httpx2.AsyncClient(headers={"Authorization": f"Bearer {token}"})
    )

    read, write = await _exit_stack.enter_async_context(
        streamable_http_client(url, http_client=http_client)
    )
    mcp_session = await _exit_stack.enter_async_context(ClientSession(read, write))
    await mcp_session.initialize()
    print("[MCP] Connected to GitHub MCP server")
    tools_result = await mcp_session.list_tools()
    loaded_tools = [
        {
            "type": "function",
            "function": {
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.input_schema,
            },
        }
        for tool in tools_result.tools
    ]
    mcp_tool_definitions.clear()
    mcp_tool_definitions.extend(loaded_tools)
    print(f"[MCP] Loaded {len(mcp_tool_definitions)} tool definitions")

async def call_mcp_tool(tool_name: str, arguments: dict):
    if mcp_session is None:
        return {"error": "MCP session is not connected"}

    available_tools = {
        tool["function"]["name"] for tool in mcp_tool_definitions
    }

    # Keep compatibility with older prompts that used the former local name.
    if tool_name == "list_repositories" and "search_repositories" in available_tools:
        owner = arguments.get("owner")
        arguments = {
            "query": f"user:{owner}" if owner else "",
            "page": arguments.get("page", 1),
            "perPage": arguments.get("perPage", arguments.get("per_page", 100)),
        }
        tool_name = "search_repositories"

    if tool_name not in available_tools:
        return {
            "error": f"Unknown MCP tool: {tool_name}",
            "available_tools": sorted(available_tools),
        }

    result = await mcp_session.call_tool(tool_name, arguments)
    output = ""
    for block in result.content:
        if hasattr(block, "text"):
            output += block.text
    return output

async def stop_mcp():
    if _exit_stack:
        await _exit_stack.aclose()
        print("[MCP] Connection closed")


if __name__ == "__main__":
    import asyncio
    from dotenv import load_dotenv
    load_dotenv()

    async def test():
        await start_mcp()
        print(mcp_tool_definitions[0])  # inspect one converted tool
        print( await call_mcp_tool("get_me", {}))
        await stop_mcp()
       

    asyncio.run(test())
