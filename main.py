import asyncio

from aiogram import Dispatcher, Bot
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from config import settings
from handlers.routers import routers_list
from middlewares.db import DbSessionMiddleware


async def main():
    engine = create_async_engine(url=settings.database_url, echo=True)
    sessionmaker = async_sessionmaker(engine, expire_on_commit=False)

    bot = Bot(settings.bot_token)
    dp = Dispatcher()

    dp.update.middleware(DbSessionMiddleware(session_pool=sessionmaker))

    dp.include_routers(*routers_list)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())