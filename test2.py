from aiogram import Bot, Dispatcher
import asyncio
from hendlers import router
from models import async_main


async def main():
    await async_main()
    bot = Bot(token='Ваш токен')
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен')
