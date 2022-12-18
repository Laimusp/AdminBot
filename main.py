import sqlite3
import asyncio
import logging

from aiogram import Bot, Dispatcher

from handlers import ban, kick, ro_warn, message_statistick


async def main():
    logging.basicConfig(level=logging.INFO)
    ro_connect = sqlite3.connect('database/ro_info.sqlite')
    stat_connect = sqlite3.connect('database/stat.sqlite')

    bot = Bot(token='1799127573:AAEGlmHuLjreW5rgRWE_eC9dGCQ1V5ubX7Y', parse_mode='HTML')
    dp = Dispatcher()

    dp.include_router(ban.router)
    dp.include_router(kick.router)
    dp.include_router(ro_warn.router)
    dp.include_router(message_statistick.router)

    # пропускаем все накопленные входящие
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, ro_connect=ro_connect, stat_connect=stat_connect)


if __name__ == '__main__':
    asyncio.run(main())
