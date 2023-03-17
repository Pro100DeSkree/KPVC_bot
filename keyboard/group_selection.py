from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import types
from data import working_with_db
from create_bot import bot

select_course_callback_list = ["first_course", "second_course", "third_course", "fourth_course"]

SELECT_COURSE_IKB = InlineKeyboardMarkup(row_width=2) \
    .insert(InlineKeyboardButton(text=f"1-й курс", callback_data=select_course_callback_list[0])) \
    .insert(InlineKeyboardButton(text=f"2-й курс", callback_data=select_course_callback_list[1])) \
    .insert(InlineKeyboardButton(text=f"3-й курс", callback_data=select_course_callback_list[2])) \
    .insert(InlineKeyboardButton(text=f"4-й курс", callback_data=select_course_callback_list[3]))


async def get_keyboard(btn_clicked):     # TODO: Треба отримати всі номери груп та додати їх кнопки
    select_group_ikb = InlineKeyboardMarkup(row_width=4)
    match btn_clicked:
        case "first_course":
            pass
        case "second_course":
            pass
        case "third_course":
            list_groups = await working_with_db.read_groups_by_course(3)
            for group in list_groups:
                select_group_ikb.insert(InlineKeyboardButton(text=group[0], callback_data=group[0]))
        case "fourth_course":
            pass
    # End match-case
    return select_group_ikb
# End def


async def send_message(message: types.Message):
    user = await working_with_db.read_user_by_user_id(message)
    if user[-1] is None:
        await bot.send_message(message.from_user.id, "Оберіть курс на якому ви зараз:", reply_markup=SELECT_COURSE_IKB)
        return False  # Якщо юзер ще не вибрав групу
    else:
        return True  # Якщо юзер вже вибрав групу
    # End if-else
# End def


async def edit_keyboard(chat_id, message_id, btn_clicked):
    select_group_ikb = await get_keyboard(btn_clicked)
    await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text="Оберіть номер вашої групи:")
    await bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id, reply_markup=select_group_ikb)
# End def
