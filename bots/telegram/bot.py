import os
import re
import httpx
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
API_URL = "http://127.0.0.1:8000/v1/chat"

async def send_typing(chat_id: str, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_chat_action(chat_id=chat_id, action="typing" )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    chat_id = str(update.effective_chat.id)
    chat_type = update.effective_chat.type
    bot_username = context.bot.username
    bot_name = 'vince'

    is_mentioned = f"@{bot_username}" in update.message.text
    is_called = is_called = bool(re.search(rf"\b{re.escape(bot_name)}\b", user_message, re.IGNORECASE))
    reply_to = update.message.reply_to_message

    is_reply_to_bot = bool(
        reply_to and reply_to.from_user and reply_to.from_user.id == context.bot.id
    )

    if chat_type != "private" and not (is_mentioned or is_reply_to_bot or is_called):
        return

    print(f"[RECEIVED] chat_id={chat_id} message={user_message!r}")

    await send_typing(chat_id, context)

    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                API_URL,
                json={"message": user_message,
                      "conversation_id": chat_id,
                      "platform": "telegram",
                      "platform_user_id": str(update.effective_user.id),
                      "display_name": update.effective_user.first_name,
                       }
            )
        data = response.json()
        reply = data.get("reply", "Something went wrong on the server side.")

    except httpx.TimeoutException:
        print("[ERROR] Request to our own API timed out")
        reply = "That took too long to think about, try again in a sec."

    except httpx.HTTPError as e:
        print(f"[ERROR] HTTP error talking to our API: {e}")
        reply = "Something went wrong reaching my brain, try again."

    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
        reply = "Something unexpected broke. I've logged it."

    print(f"[REPLY] {reply!r}")

    try:
        await update.message.reply_text(reply)
        print("[SENT] Reply delivered to Telegram")
    except Exception as e:
        print(f"[SEND FAILED] {e}")


app = Application.builder().token(TELEGRAM_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("Starting polling...")
app.run_polling()