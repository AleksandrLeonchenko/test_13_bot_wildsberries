import asyncio
import logging
from aiogram import Bot, Dispatcher

from config import BOT_TOKEN
from handlers import questions, different_types

logging.basicConfig(level=logging.INFO)


async def main() -> None:
    """
    Асинхронная функция для запуска бота и начала обработки сообщений.

    Raises:
        RuntimeError: Если произойдет ошибка при запуске бота.
    """
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    dp.include_routers(questions.router, different_types.router)

    await bot.delete_webhook(drop_pending_updates=True)

    await dp.start_polling(bot, mylist=[1, 2, 3], mylist2=[11, 22, 33])


if __name__ == "__main__":
    asyncio.run(main())
