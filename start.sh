#!/bin/bash
python bot/telegram/bot.py &
python bot/discord/bot.py &
uvicorn main:app --host 0.0.0.0 --port $PORT