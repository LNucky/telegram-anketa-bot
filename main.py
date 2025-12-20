from config import BOT_TOKEN, DATABASE_URL
from aiogram import Dispatcher, Bot
from handlers.start_handler import router as start_router
from handlers.message_handler import router as message_router
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from middlewares.db import DbSessionMiddleware



async def main():
    engine = create_async_engine(url=DATABASE_URL, echo=True)
    sessionmaker = async_sessionmaker(engine, expire_on_commit=False)

    bot = Bot(BOT_TOKEN)
    dp = Dispatcher()

    dp.update.middleware(DbSessionMiddleware(session_pool=sessionmaker))

    dp.include_router(start_router)
    dp.include_router(message_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())