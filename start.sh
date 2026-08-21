#!/bin/bash

# Export root folder so Python finds 'database' and other modules
export PYTHONPATH=.

# Start Telegram Bot in the background
python bots/telegram/bot.py &

# Start Discord Bot in the background
python bots/discord/bot.py &

# Start FastAPI server in the foreground
uvicorn main:app --host 0.0.0.0 --port $PORT