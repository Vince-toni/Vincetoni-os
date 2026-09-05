#!/bin/bash

# Export root folder so Python finds 'database' and other modules
export PYTHONPATH=.

if [ -z "$TELEGRAM_BOT_TOKEN" ]; then
	echo "TELEGRAM_BOT_TOKEN is not set"
	exit 1
fi

if [ -z "$DISCORD_BOT_TOKEN" ]; then
	echo "DISCORD_BOT_TOKEN is not set"
	exit 1
fi

# Start Telegram Bot in the background
python bots/telegram/bot.py &

# Start Discord Bot in the background
python bots/discord/bot.py &

# Start FastAPI server in the foreground
uvicorn main:app --host 0.0.0.0 --port $PORT