# VINCETONI OS

> **An AI-powered personal agent, API gateway, automation platform, and coding agent.**

VINCETONI is designed to become a central AI system that can connect to multiple applications, bots, APIs, developer tools, social platforms, media tools, and eventually operate as an autonomous coding agent.

The core idea is simple:

```text
             ┌──────────────────────┐
             │      VINCETONI           │
             │      AI AGENT            │
             └──────────┬───────────┘
                        │
                 ┌──────▼──────┐
                 │ AI ROUTER   │
                 └──────┬──────┘
                        │
       ┌────────────────┼────────────────┐
       ▼                ▼                ▼
   AI Models         Tools            Memory
       │                │                │
 OpenRouter       GitHub/Search      PostgreSQL
 Gemini/OpenAI    Browser/Terminal   Redis/Vector DB
 Local Models     Media/Social
```

The first goal is **not** to build the complete autonomous agent.

The first goal is to build a reliable **VINCETONI Assistant API** that every bot and application can use.

---

# 1. Vision

VINCETONI should eventually be capable of:

* AI conversations
* Persistent memory
* Web research
* Search
* GitHub management
* Reading repositories
* Reading commits
* Creating issues
* Creating branches
* Creating pull requests
* Running code
* Running tests
* Editing files
* Image processing
* Image hosting
* GIF conversion
* Video processing
* Sticker creation
* WhatsApp integration
* Telegram integration
* Discord integration
* YouTube integrations
* Scheduled automation
* Multi-agent workflows
* Coding-agent capabilities
* API creation
* Custom plugins/tools

The important design principle is:

> **VINCETONI owns the interface and orchestration. External providers are replaceable.**

For example, VINCETONI should not depend permanently on one AI provider.

```text
VINCETONI
    │
    ├── OpenRouter
    ├── OpenAI
    ├── Gemini
    ├── Local Models
    └── Future Providers
```

---

# 2. Development Strategy

Build VINCETONI in stages.

## Phase 1 — Assistant API

Build:

```text
FastAPI
   ↓
AI Provider
   ↓
OpenRouter
   ↓
Model
```

Features:

* API authentication
* Chat endpoint
* Conversation IDs
* Message history
* Model selection
* Streaming responses
* Error handling
* Logging
* Basic rate limiting

Example:

```http
POST /v1/chat
```

Request:

```json
{
  "message": "Explain recursion simply.",
  "conversation_id": "abc123"
}
```

Response:

```json
{
  "reply": "Recursion is when a function...",
  "conversation_id": "abc123"
}
```

---

# 3. Phase 2 — Memory

Add persistent conversations.

```text
User
 │
 ▼
VINCETONI API
 │
 ├── Conversation history
 ├── User preferences
 ├── Long-term memory
 └── Context retrieval
```

Recommended starting database:

```text
PostgreSQL
```

Later:

```text
PostgreSQL
     +
Vector Database
```

Potential vector options:

* pgvector
* Qdrant
* Weaviate

Do not over-engineer memory initially.

Start with normal PostgreSQL conversation history.

---

# 4. Phase 3 — Tools

This is where VINCETONI starts becoming an actual agent.

Instead of only generating text, the AI can request tools.

Example:

```json
{
  "tool": "github.get_commits",
  "arguments": {
    "repository": "owner/project"
  }
}
```

The VINCETONI tool system executes the operation and returns the result to the agent.

Basic tool structure:

```text
tools/
├── filesystem/
├── terminal/
├── search/
├── browser/
├── github/
├── git/
├── media/
├── social/
└── custom/
```

---

# 5. Phase 4 — Agent Loop

The assistant becomes an agent.

Instead of:

```text
User → AI → Answer
```

VINCETONI becomes:

```text
User
 ↓
Understand
 ↓
Plan
 ↓
Select Tool
 ↓
Execute
 ↓
Observe Result
 ↓
Decide Next Action
 ↓
Verify
 ↓
Answer
```

Example:

> "Fix the login bug in my GitHub project."

VINCETONI could eventually:

```text
1. Find repository
2. Inspect repository
3. Read relevant files
4. Identify bug
5. Create plan
6. Modify files
7. Run tests
8. Inspect failures
9. Fix failures
10. Run tests again
11. Create Git branch
12. Commit changes
13. Push branch
14. Create pull request
15. Report result
```

---

# 6. Phase 5 — Coding Agent

The coding agent should have controlled access to:

```text
Filesystem
Terminal
Git
GitHub
Package managers
Testing
Build systems
Browser
Documentation
Search
```

### IMPORTANT

Do not allow the AI to execute arbitrary commands directly on your main machine.

Use:

```text
Docker
```

or another isolated sandbox.

Architecture:

```text
VINCETONI Agent
       │
       ▼
Execution Manager
       │
       ▼
Sandbox / Container
       │
       ├── Project files
       ├── Terminal
       ├── Tests
       └── Build tools
```

The agent should have explicit permissions.

For example:

```text
filesystem.read
filesystem.write
terminal.execute
git.diff
git.commit
github.create_pr
```

Some dangerous operations should require confirmation.

---

# 7. Full Project Structure

Recommended starting structure:

```text
vincetoni-os/
│
├── apps/
│   ├── dashboard/
│   ├── web/
│   └── mobile/
│
├── gateway/
│   └── express/
│       ├── src/
│       │   ├── routes/
│       │   ├── controllers/
│       │   ├── middleware/
│       │   └── server.js
│       └── package.json
│
├── agent/
│   ├── agent.py
│   ├── planner.py
│   ├── executor.py
│   ├── observer.py
│   ├── verifier.py
│   ├── context.py
│   ├── memory.py
│   └── loop.py
│
├── api/
│   └── v1/
│       ├── chat.py
│       ├── users.py
│       ├── conversations.py
│       └── tools.py
│
├── providers/
│   ├── openrouter/
│   ├── openai/
│   ├── gemini/
│   └── local/
│
├── tools/
│   ├── filesystem/
│   ├── terminal/
│   ├── browser/
│   ├── search/
│   ├── github/
│   ├── git/
│   ├── media/
│   ├── social/
│   └── custom/
│
├── services/
│   ├── ai/
│   ├── search/
│   ├── github/
│   ├── media/
│   ├── social/
│   └── automation/
│
├── workers/
│   ├── ai_worker.py
│   ├── media_worker.py
│   └── automation_worker.py
│
├── database/
│   ├── models/
│   ├── migrations/
│   └── seed/
│
├── plugins/
│   ├── github/
│   ├── search/
│   ├── media/
│   ├── youtube/
│   └── custom/
│
├── sandbox/
│   ├── docker/
│   └── workspaces/
│
├── shared/
│   ├── schemas/
│   ├── utils/
│   ├── constants/
│   └── types/
│
├── tests/
│
├── .env.example
├── .gitignore
├── docker-compose.yml
├── requirements.txt
├── package.json
└── README.md
```

---

# 8. Python + Express Architecture

The recommended architecture is:

```text
                 Clients
                    │
       ┌────────────┼────────────┐
       │            │            │
    WhatsApp     Discord      Website
       │            │            │
       └────────────┼────────────┘
                    ▼
             Express Gateway
                    │
                    ▼
              Python Backend
                    │
       ┌────────────┼────────────┐
       ▼            ▼            ▼
      AI          Tools        Memory
       │            │            │
       ▼            ▼            ▼
  OpenRouter    GitHub/etc.  PostgreSQL
```

Express can handle:

* Authentication
* API gateway
* WebSocket connections
* Public API
* Request routing
* Bot integrations

Python can handle:

* AI agents
* Tool execution
* Automation
* Media processing
* AI workflows
* Background workers

---

# 9. OpenRouter

OpenRouter can be the initial model gateway.

The VINCETONI application should communicate with **your own provider abstraction**, not directly depend on OpenRouter everywhere.

Bad:

```text
100 files → OpenRouter API
```

Better:

```text
VINCETONI
    ↓
AI Provider Interface
    ↓
OpenRouter
```

Example:

```python
class AIProvider:
    async def chat(self, messages, model=None):
        raise NotImplementedError
```

Then:

```text
AIProvider
    │
    ├── OpenRouterProvider
    ├── OpenAIProvider
    ├── GeminiProvider
    └── LocalProvider
```

This means you can change providers later without rewriting VINCETONI.

---

# 10. Model Routing

Eventually VINCETONI should decide which model is appropriate.

Example:

```text
Simple question
      ↓
Cheap / fast model

Complex reasoning
      ↓
Reasoning model

Coding
      ↓
Coding-capable model

Large document
      ↓
Long-context model

Image generation
      ↓
Image model

Vision
      ↓
Vision-capable model
```

The router might eventually look like:

```python
if task.type == "coding":
    model = coding_model

elif task.type == "research":
    model = research_model

elif task.type == "simple_chat":
    model = cheap_model

elif task.type == "vision":
    model = vision_model
```

Do not build complicated automatic routing on day one.

Start with manual model selection.

---

# 11. Web Research

VINCETONI should eventually have a web-search tool.

Conceptually:

```text
Agent
  ↓
web.search()
  ↓
Search provider
  ↓
Results
  ↓
Agent
  ↓
Read relevant pages
  ↓
Answer with sources
```

Possible providers can include search APIs rather than relying on fragile scraping.

IMPORTANT:

Use official APIs where available and respect the terms and robots/access rules of websites you interact with.

---

# 12. GitHub Tools

GitHub should become one of VINCETONI's most important integrations.

Possible tools:

```text
github.list_repositories
github.get_repository
github.get_file
github.search_code
github.get_commits
github.get_issue
github.create_issue
github.update_issue
github.create_branch
github.create_commit
github.create_pull_request
github.get_pull_request
github.comment_pull_request
```

Eventually:

```text
User:
"Check my latest PR."

VINCETONI:
→ GitHub
→ Read PR
→ Read changed files
→ Inspect checks
→ Analyze
→ Report
```

Later the coding agent can automatically address review feedback.

---

# 13. Media Tools

Many media features do not need an external API.

Use local tools when practical.

Potential stack:

```text
Images
  → Pillow

Video
  → FFmpeg

GIF
  → FFmpeg / Pillow

Computer vision
  → OpenCV

Image manipulation
  → Pillow / OpenCV

Storage
  → S3-compatible storage / Cloud storage
```

Example tool API:

```text
media.image.resize
media.image.convert
media.image.compress
media.image.upload

media.video.convert
media.video.extract_audio

media.gif.create
media.gif.optimize

media.sticker.create
```

---

# 14. Social Integrations

Create adapters rather than mixing social APIs into the agent.

```text
social/
├── whatsapp/
├── telegram/
├── discord/
├── youtube/
└── other/
```

Then VINCETONI can expose a unified interface:

```text
send_message()
```

while the adapter handles the platform-specific API.

Example:

```text
VINCETONI
     │
     ▼
send_message()
     │
 ┌───┼─────────────┐
 ▼   ▼             ▼
WA Telegram     Discord
```

---

# 15. Plugin System

Every capability should eventually become a plugin/tool.

Example:

```text
Plugin
├── name
├── description
├── permissions
├── input schema
├── output schema
└── execute()
```

Example:

```python
class GitHubCreateIssueTool:

    name = "github.create_issue"

    description = "Create an issue in a GitHub repository."

    async def execute(self, repo, title, body):
        ...
```

The AI does not need to know how the implementation works.

It only needs to know:

```text
github.create_issue
```

and the required arguments.

---

# 16. Tool Permissions

VINCETONI should eventually have permission levels.

```text
READ
WRITE
EXECUTE
NETWORK
ADMIN
```

Example:

```text
github.read_repository
    → READ

github.create_issue
    → WRITE

terminal.execute
    → EXECUTE

browser.open
    → NETWORK
```

High-risk actions should request confirmation.

For example:

```text
VINCETONI wants to execute:

rm -rf ...

Allow? [Yes] [No]
```

Never give every tool unrestricted access.

---

# 17. Database

Start simple.

### PostgreSQL

Use PostgreSQL for:

```text
Users
Conversations
Messages
API keys
Tool executions
Tasks
Agent runs
Plugins
Permissions
```

Possible tables:

```text
users
conversations
messages
api_keys
agent_runs
tool_calls
tasks
plugins
permissions
```

Later add:

```text
pgvector
```

for semantic memory.

---

# 18. Redis

Redis can eventually handle:

```text
Caching
Sessions
Rate limiting
Queues
Temporary agent state
Background jobs
```

Don't make Redis mandatory for version 0.1 unless you actually need it.

---

# 19. Background Workers

Long-running jobs should not block the API.

Example:

```text
API
 │
 ├── Immediate response
 │
 └── Queue
       │
       ▼
    Worker
       │
       ├── AI task
       ├── Media task
       ├── GitHub task
       └── Automation
```

Potential Python options:

```text
Celery
RQ
Dramatiq
Arq
```

Pick one later based on your workload.

---

# 20. Initial Dependencies

Do NOT install everything immediately.

Start small.

## Python

Suggested initial stack:

```text
fastapi
uvicorn
httpx
pydantic
pydantic-settings
python-dotenv
```

For database:

```text
sqlalchemy
asyncpg
alembic
```

For authentication/security:

```text
pyjwt
passlib
```

For later AI functionality:

```text
openai
```

The OpenAI-compatible client can also be useful for providers that expose compatible APIs.

For media:

```text
Pillow
opencv-python
```

And install FFmpeg separately on the system/container.

---

# 21. Node / Express

Initial dependencies:

```text
express
cors
dotenv
helmet
zod
```

For HTTP/API communication:

```text
axios
```

For GitHub later:

```text
octokit
```

---

# 22. Development Environment

Recommended:

```text
Python
Node.js
PostgreSQL
Git
Docker
FFmpeg
```

Later:

```text
Redis
Vector DB
Object Storage
```

---

# 23. Environment Variables

Never hard-code API keys.

Create:

```text
.env.example
```

Example:

```env
APP_ENV=development

VINCETONI_API_KEY=

OPENROUTER_API_KEY=

OPENAI_API_KEY=
GEMINI_API_KEY=

DATABASE_URL=

REDIS_URL=

GITHUB_TOKEN=

WHATSAPP_TOKEN=
TELEGRAM_BOT_TOKEN=
DISCORD_TOKEN=

STORAGE_ENDPOINT=
STORAGE_ACCESS_KEY=
STORAGE_SECRET_KEY=
```

Your real `.env` should never be committed.

---

# 24. First API

The first milestone should be extremely small.

```text
POST /v1/chat
```

Flow:

```text
Request
   ↓
Validate
   ↓
Authenticate
   ↓
Load conversation
   ↓
Send messages to provider
   ↓
Receive response
   ↓
Save conversation
   ↓
Return response
```

Example:

```json
{
  "message": "Hello VINCETONI",
  "conversation_id": "conversation-001"
}
```

Response:

```json
{
  "id": "response-001",
  "conversation_id": "conversation-001",
  "message": "Hello! I'm VINCETONI."
}
```

Once this works, **stop and test it thoroughly**.

---

# 25. Then Add Streaming

After normal chat works:

```text
POST /v1/chat/stream
```

Possible architecture:

```text
VINCETONI
   ↓
Model
   ↓
Token stream
   ↓
SSE/WebSocket
   ↓
Bot / Website
```

This will make the assistant feel much more responsive.

---

# 26. Then Add Tools

First tools should be harmless:

```text
calculator
current_time
web_search
read_file
list_directory
```

Then:

```text
GitHub read operations
```

Then eventually:

```text
GitHub write operations
terminal
code editing
```

Build capabilities gradually.

---

# 27. Coding Agent Roadmap

After the Assistant API is stable:

```text
LEVEL 1
Chat
 ↓
LEVEL 2
Memory
 ↓
LEVEL 3
Tool calling
 ↓
LEVEL 4
Web research
 ↓
LEVEL 5
GitHub integration
 ↓
LEVEL 6
Filesystem tools
 ↓
LEVEL 7
Terminal sandbox
 ↓
LEVEL 8
Coding agent
 ↓
LEVEL 9
Multi-agent workflows
```

Don't jump straight to Level 9.

---

# 28. Multi-Agent Future

Eventually VINCETONI could have specialized agents:

```text
                    VINCETONI
                        │
                 MASTER AGENT
                        │
        ┌───────────────┼────────────────┐
        ▼               ▼                ▼
   Coding Agent    Research Agent    Media Agent
        │               │                │
        ▼               ▼                ▼
      GitHub          Web Search        FFmpeg
      Terminal        Browser           Pillow
      Tests           Sources            Images
```

The master agent delegates tasks to specialists.

---

# 29. Bot Architecture

All bots should use the same VINCETONI API.

```text
WhatsApp ─────┐
Telegram ─────┤
Discord ──────┤
Website ──────┤
Dashboard ────┤
Mobile ───────┘
               │
               ▼
        VINCETONI API
               │
               ▼
           AI Agent
```

This is important.

Do NOT build a separate AI system inside every bot.

Build one brain.

---

# 30. API Philosophy

VINCETONI should become the abstraction layer.

Instead of:

```text
Bot → OpenRouter
Bot → GitHub
Bot → Search
Bot → Media API
Bot → Database
```

Use:

```text
Bot
 ↓
VINCETONI
 ├── AI
 ├── Search
 ├── GitHub
 ├── Media
 ├── Memory
 └── Automation
```

That way, every application gets the same capabilities.

---

# 31. Security Rules

These rules should be treated as core architecture, not optional features.

### Never:

* Commit API keys
* Store secrets in source code
* Give the agent unlimited terminal access
* Allow unrestricted filesystem access
* Automatically execute destructive commands
* Trust arbitrary tool arguments
* Allow plugins to silently escalate permissions

### Always:

* Validate inputs
* Authenticate API requests
* Log tool calls
* Rate-limit public endpoints
* Sandbox code execution
* Restrict filesystem access
* Add permission checks
* Require confirmation for dangerous operations

---

# 32. Development Rules

Keep the core small.

Prefer:

```text
Provider
Tool
Agent
Service
Plugin
```

over creating huge files containing everything.

Each integration should be replaceable.

For example:

```text
providers/openrouter/
```

should not contain application-specific business logic.

---

# 33. V0.1 Milestone

The first working VINCETONI should only need:

```text
FastAPI
OpenRouter
PostgreSQL
Authentication
Chat
Conversation history
Logging
```

Architecture:

```text
Client
  ↓
FastAPI
  ↓
Auth
  ↓
Conversation Service
  ↓
AI Provider
  ↓
OpenRouter
  ↓
Model
```

That's it.

If this works reliably, you have the foundation.

---

# 34. V0.2

Add:

```text
Streaming
Model selection
Provider abstraction
API keys
Rate limiting
Web search
Basic tools
```

---

# 35. V0.3

Add:

```text
GitHub
Memory
Plugins
Tool permissions
Background jobs
```

---

# 36. V0.4

Add:

```text
Filesystem
Terminal
Docker sandbox
Code execution
Testing
Git operations
```

---

# 37. V1.0

VINCETONI becomes a proper agent:

```text
Natural language
      ↓
Planning
      ↓
Reasoning
      ↓
Tool selection
      ↓
Execution
      ↓
Observation
      ↓
Verification
      ↓
Final response
```

At this point, VINCETONI is no longer just an AI API.

It's an **agent platform**.

---

# 38. The Golden Rule

Build VINCETONI in this order:

```text
              ┌─────────────┐
              │  AI MODEL   │
              └──────┬──────┘
                     │
                     ▼
              ┌─────────────┐
              │ ASSISTANT   │
              │     API     │
              └──────┬──────┘
                     │
                     ▼
              ┌─────────────┐
              │   MEMORY    │
              └──────┬──────┘
                     │
                     ▼
              ┌─────────────┐
              │    TOOLS    │
              └──────┬──────┘
                     │
                     ▼
              ┌─────────────┐
              │    AGENT    │
              └──────┬──────┘
                     │
                     ▼
              ┌─────────────┐
              │ CODING AGENT│
              └─────────────┘
```

**Don't start by building the autonomous coding agent.**

Start by building the **brain's API**.

Then give the brain memory.

Then give it tools.

Then give it the ability to plan.

Then give it controlled execution.

Then you have a coding agent.

---

# 39. First Build Checklist

## Step 1

Create the repository:

```bash
mkdir vincetoni-os
cd vincetoni-os
git init
```

## Step 2

Create the Python environment:

```bash
python -m venv .venv
```

Activate it and install the initial dependencies:

```bash
pip install fastapi uvicorn httpx pydantic pydantic-settings python-dotenv
```

## Step 3

Create:

```text
api/
agent/
providers/
services/
tools/
database/
tests/
```

## Step 4

Create an OpenRouter provider.

## Step 5

Create:

```text
POST /v1/chat
```

## Step 6

Test the endpoint locally.

## Step 7

Connect one bot to it.

## Step 8

Only after that, add memory and tools.

---

# 40. Long-Term Goal

The final VINCETONI ecosystem should look like:

```text
                         VINCETONI
                            │
                    ┌───────▼───────┐
                    │  MASTER AGENT │
                    └───────┬───────┘
                            │
          ┌─────────────────┼─────────────────┐
          │                 │                 │
       AI CORE           TOOLS            MEMORY
          │                 │                 │
   ┌──────┼──────┐     ┌────┼────┐       PostgreSQL
   │      │      │     │    │    │       Vector DB
OpenAI Gemini OpenRouter GitHub Web       Redis
                     Terminal Media
                     Social  Browser
          │
          ▼
    ┌───────────────┐
    │   API GATEWAY │
    └───────┬───────┘
            │
    ┌───────┼────────┬──────────┐
    ▼       ▼        ▼          ▼
 WhatsApp Telegram Discord    Web
```

### The ultimate principle

> **One brain. Many interfaces. Many tools. Replaceable models. Controlled execution.**

That is the core idea behind VINCETONI.
