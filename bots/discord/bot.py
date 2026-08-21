import os
import re
import httpx
from dotenv import load_dotenv
import discord
from discord.ext import commands

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
API_URL = "https://vincetoni-os.onrender.com/v1/chat"
BOT_NAME = "vince"

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


async def send_typing(channel):
    return channel.typing()


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("Starting polling...")


@bot.event
async def on_message(message: discord.Message):
    if message.author == bot.user:
        return

    user_message = re.sub(rf"<@!?{bot.user.id}>", "", message.content).strip()
    channel_id = str(message.channel.id)
    is_guild = message.guild is not None
    bot_username = bot.user.name
    bot_name = BOT_NAME

    is_mentioned = bot.user.mentioned_in(message)
    is_called = bool(
        re.search(rf"\b{re.escape(bot_name)}\b", user_message, re.IGNORECASE)
    )

    is_reply_to_bot = False
    if message.reference and message.reference.message_id:
        try:
            referenced = await message.channel.fetch_message(message.reference.message_id)
            if referenced.author.id == bot.user.id:
                is_reply_to_bot = True
        except discord.NotFound:
            pass

    if is_guild and not (is_mentioned or is_reply_to_bot or is_called):
        return

    print(f"[RECEIVED] channel_id={channel_id} message={user_message!r}")

    async with message.channel.typing():
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    API_URL,
                    json={
                        "message": user_message,
                        "conversation_id": channel_id,
                        "platform": "discord",
                        "platform_user_id": str(message.author.id),
                        "display_name": message.author.display_name,
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
        await message.reply(reply)
        print("[SENT] Reply delivered to Discord")
    except Exception as e:
        print(f"[SEND FAILED] {e}")

    await bot.process_commands(message)


bot.run(DISCORD_TOKEN)