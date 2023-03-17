from aiogram import types, Dispatcher
from data import working_with_db

import strings
from create_bot import bot


async def echo_message(message: types.Message):
    await message.answer(strings.INVALID_MESSAGE)


def register_handlers_other(dp: Dispatcher):
    dp.register_message_handler(echo_message)
