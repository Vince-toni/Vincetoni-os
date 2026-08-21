#!/bin/bash

# Force Python path to the absolute source directory
export PYTHONPATH=/opt/render/project/src

# Start Telegram Bot
python /opt/render/project/src/bots/telegram/bot.py &

# Start Discord Bot
python /opt/render/project/src/bots/discord/bot.py &

# Start FastAPI/Uvicorn
/opt/render/project/src/.venv/bin/python -m uvicorn main:app --host 0.0.0.0 --port $PORT