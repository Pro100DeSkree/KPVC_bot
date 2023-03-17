from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

import config
import handlers.client
from data.sqlite_db import write_new_admin
from aiogram import types, Dispatcher
from aiogram.types import InputFile
from data import working_with_db
from create_bot import bot
from parser import parser
import strings
from utils import date_time, create_tabe

msg_cancel = ["скасувати", "cencel", '/cencel']


# ----------------------------------------------------------------------------------------------------------------------
# Додавання нових адміністраторів

class FsmAddAdmin(StatesGroup):
    message_repl = State()


async def add_new_admin(message: types.Message):
    user_id = message.from_user.id
    if await working_with_db.check_is_admin(user_id):
        await message.answer(strings.MSG_ADD_ADMIN[0])  # Перешліть повідомлення користувача котрого хочете додати
        await FsmAddAdmin.message_repl.set()
    else:
        await message.answer(strings.INVALID_MESSAGE)  # Не відома команда


async def accept_message(message: types.Message, state: FSMContext):
    await state.finish()
    if message.text.lower() in msg_cancel:
        await state.finish()
        await message.answer(strings.MSG_CANCEL_COMMAND)  # Скасовано
    else:
        # noinspection PyBroadException
        try:
            new_admin_id = message.forward_from.id
            check_db = await write_new_admin(new_admin_id)
        except Exception:
            new_admin_id = message.from_user.id
            check_db = await write_new_admin(new_admin_id)
        # End try-except
        if check_db == 0:
            await message.answer(strings.MSG_ADD_ADMIN[1])  # Додав!
        else:
            await message.answer(strings.MSG_ADD_ADMIN[2])  # Цей користувач вже адмін!
        # End if-else
    # End if-else
# End def


# ----------------------------------------------------------------------------------------------------------------------
# Надсилання БД в ПП

async def update_db(message: types.Message):
    user_id = message.from_user.id
    if await working_with_db.check_is_admin(user_id):
        try:
            await parser.main(debug=config.DEBUG)
            # await parser.main(debug=False)
            await bot.send_message(message.chat.id, "Базу даних успішно оновлено!")
        except Exception as e:
            await bot.send_message(message.chat.id, f"Помилка!! БД не оновлено!\n{e}")
    else:
        await message.answer(strings.INVALID_MESSAGE)  # "Не відома команда"
    # End if-else
# End def


# ----------------------------------------------------------------------------------------------------------------------
# Надсилання БД в ПП

async def unloading_db(message: types.Message):
    user_id = message.from_user.id
    if await working_with_db.check_is_admin(user_id):
        db = InputFile(r'./data/database.db')
        await message.answer_document(db)
    else:
        await message.answer(strings.INVALID_MESSAGE)  # "Не відома команда"
    # End if-else
# End def


# ----------------------------------------------------------------------------------------------------------------------
# Надсилання БД в ПП

async def unloading_log_file(message: types.Message):
    user_id = message.from_user.id
    if await working_with_db.check_is_admin(user_id):
        log_file = InputFile(r'./log_file.log')
        await bot.send_document(user_id, log_file)
    else:
        await message.answer(strings.INVALID_MESSAGE)  # "Не відома команда"
    # End if-else
# End def


async def test(message: types.Message):  # TODO ДЛЯ ТЕСТІВ
    await handlers.client.mailing()
# En def


# ----------------------------------------------------------------------------------------------------------------------
# Реєстрація хендлерів
def register_handlers_admin(dp: Dispatcher):
    # Додавання адміна
    dp.register_message_handler(add_new_admin, commands=['new_admin', 'add_admin'])
    dp.register_message_handler(accept_message, content_types=['text'], state=FsmAddAdmin.message_repl)
    # Робота з DB:
    # Оновити базу даних
    dp.register_message_handler(update_db, commands=['update_db'])
    # Очистити базу даних (Або не очистити...) В кінці року автоматично перевести всіх на рівень вище
    # dp.register_message_handler(update_db, commands=['update_db'])
    # Отримати базу даних
    dp.register_message_handler(unloading_db, commands=['unload_db', 'ud'])
    # Отримати лог-файл
    dp.register_message_handler(unloading_log_file, commands=['unload_log', 'ul'])

    dp.register_message_handler(test, commands=['test', 't'])
