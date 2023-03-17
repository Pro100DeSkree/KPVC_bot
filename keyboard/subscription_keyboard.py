from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import types
from data import working_with_db
from create_bot import bot
import emoji

cross_mark = emoji.emojize(":cross_mark:")
check_mark = emoji.emojize(":check_mark:")

callback_list = ["schedule_sub", "changes_sub"]


async def get_keyboard(subs):
    btn_emoji_sc = cross_mark
    btn_emoji_ch = cross_mark
    # Якщо в БД немає підписки, то ставимо хрестики
    if subs is not None:
        # Якщо підписка на розклад True, то ставимо емоджі галочку
        if subs[0] == 1:
            btn_emoji_sc = check_mark
        # End if
        # Якщо підписка на зміни True, то ставимо емоджі галочку
        if subs[1] == 1:
            btn_emoji_ch = check_mark
        # End if
    # End if
    return InlineKeyboardMarkup(row_width=1) \
        .insert(InlineKeyboardButton(text=f"Розклад - {btn_emoji_sc}", callback_data=callback_list[0])) \
        .insert(InlineKeyboardButton(text=f"Зміни - {btn_emoji_ch}", callback_data=callback_list[1]))
# End def


async def send_message(message: types.Message):
    # Це для того, щоб мати user_id
    await working_with_db.write_subscribe(message)
    subscribes = await working_with_db.read_subscribe_by_chat_id(message.chat.id)
    keyboard = await get_keyboard(subscribes)
    await message.answer("Оберіть на що ви хочете підписатися:", reply_markup=keyboard)
# End def


async def edit_keyboard(chat_id, message_id, callback_data):
    await working_with_db.update_subscribe(chat_id, callback_data)

    subscribes = await working_with_db.read_subscribe_by_chat_id(chat_id)
    keyboard = await get_keyboard(subscribes)
    await bot.edit_message_reply_markup(chat_id, message_id, reply_markup=keyboard)
# End def
