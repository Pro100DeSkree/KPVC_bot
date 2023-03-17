from handlers import client, admin, other
from data import sqlite_db
from create_bot import dp
from aiogram.utils import executor
from loguru import logger

from handlers.client import auto_update_and_mailing


@logger.catch
async def on_startup(_):  # Пред-налаштування
    sqlite_db.sql_star()  # Підключення БД
    dp.loop.create_task(auto_update_and_mailing())  # Створення потоку автоматичного оновлення БД і розсилка
    logger.info("Bot Started")
    print('bot started')


client.register_handlers_client(dp)
admin.register_handlers_admin(dp)
other.register_handlers_other(dp)


if __name__ == '__main__':
    # TODO: Потрібно розібратись з Логуру і зробити нормальну систему логування
    logger.add("log_file.log", format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}", enqueue=True, level="DEBUG", rotation="50 MB",
               compression="zip")

    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
