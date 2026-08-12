import asyncio
from sqlalchemy import text
from Database import engine

async def test_connection():
    async with engine.connect() as conn:
        result = await conn.execute(text("SELECT 1"))
        print("Connection successful:", result.scalar())

asyncio.run(test_connection())