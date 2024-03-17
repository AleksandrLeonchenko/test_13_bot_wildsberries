import asyncio
import logging
from aiogram import Bot, Dispatcher
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
# import aiohttp

from config import BOT_TOKEN, DATABASE_URL
from data.database import Base, create_tables, main_2
from handlers import questions, different_types

logging.basicConfig(level=logging.INFO)

async def main() -> None:
    """
    Асинхронная функция для создания таблиц, запуска бота (с доп. аргументами) и начала обработки сообщений.

    Raises:
        RuntimeError: Если произойдет ошибка при запуске бота.
    """
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    dp.include_routers(questions.router, different_types.router)

    await bot.delete_webhook(drop_pending_updates=True)

    # Создаем таблицы перед запуском бота
    await main_2()

    await dp.start_polling(bot, mylist=[1, 2, 3], mylist2=[11, 22, 33])


if __name__ == "__main__":
    asyncio.run(main())

