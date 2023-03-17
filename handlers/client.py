import asyncio
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import InputFile

from keyboard import group_selection, subscription_keyboard
from data import working_with_db
from aiogram.dispatcher import FSMContext
from aiogram import types, Dispatcher
from create_bot import bot
from loguru import logger
from os import path
import strings
import os

from parser import parser
from utils import create_tabe, date_time

base_dir = path.dirname(path.abspath(__file__))
if base_dir in "/app/handlers":
    CHAT_ID_REP = os.environ.get('CHAT_ID_REP')
else:
    import config
    CHAT_ID_REP = config.CHAT_ID_REP
# End if-else

update_time_list = ['07:00', '08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '18:00', '19:00', '20:00', '21:00']
update_time_debug = '09:55'


# ----------------------------------------------------------------------------------------------------------------------
# Автоматичне оновлення БД і розсилка

async def auto_update_and_mailing():  # Оновлювати раз в годину 7-13 та 18-21
    update_time_list.append(update_time_debug)  # TODO: ВИДАЛИТИ .append(update_time_debug)
    while True:
        if await date_time.get_current_time() in update_time_list:
            msg_id = (await bot.send_message(config.CHAT_ID_REP, "Час оновлення")).message_id
            logger.debug("Перевірка оновлень на сайті та оновлення БД")
            if await update_db(msg_id):
                await mailing()

                logger.debug("Зміни є. БД оновлено, та розіслано")
                await bot.edit_message_text(chat_id=config.CHAT_ID_REP, message_id=msg_id, text="Успішно оновлено!\nТа розіслано")
            # End if
        # End if
        await asyncio.sleep(60)
    # End while
# End def


async def get_schedule_and_changes():
    next_weekday = await date_time.get_current_weekday_test()
    list_first_schedule = await working_with_db.get_first_course_schedule_by_weekday(next_weekday)
    list_second_schedule = await working_with_db.get_second_course_schedule_by_weekday(next_weekday)
    list_third_schedule = await working_with_db.get_third_course_schedule_by_weekday(next_weekday)
    list_fourth_schedule = await working_with_db.get_fourth_course_schedule_by_weekday(next_weekday)
    list_schedule_ch = await working_with_db.read_schedule_changes()
    return [list_first_schedule, list_second_schedule, list_third_schedule, list_fourth_schedule, list_schedule_ch]
# End def


@logger.catch()
async def update_db(msg_id):
    list_old_data = await get_schedule_and_changes()
    logger.debug("Очікування 15ти хвилинної затримки")
    await asyncio.sleep(15*60)  # Затримка на 15хв, щоб не рівно в **:00
    # await asyncio.sleep(5)
    logger.debug("Перевірка змін на сайті, та оновлення...")
    # noinspection PyBroadException
    try:
        # await parser.main(debug=config.DEBUG)
        await parser.main()
        logger.debug("Перевірка пройшла успішно.")
        await bot.edit_message_text(chat_id=config.CHAT_ID_REP, message_id=msg_id, text="Успішно оновлено!")
        return await is_update_db(list_old_data)
    except Exception as ex:
        return False
    # End try-except
# End def


async def is_update_db(list_old_data):
    list_new_data = await get_schedule_and_changes()
    return False if list_old_data[-1] == list_new_data[-1] else True
# End def


async def mailing():  # Розсилка розкладу і змін в розкладі(якщо юзер підписаний на те і на те)
    # Отримання списків з підписками
    chat_ids_subscribe_schedule = await working_with_db.get_chat_ids_subscribe_schedule()
    chat_ids_subscribe_schedule_ch = await working_with_db.get_chat_ids_subscribe_schedule_ch()

    users_and_user_groups = await working_with_db.get_users_groups()

    schedule_and_changes = await get_schedule_and_changes()
    changes = schedule_and_changes.pop(-1)
    schedule = schedule_and_changes

    if chat_ids_subscribe_schedule:
        pruklad = {382: [-842764909, 1435378166]}
        # for user in chat_ids_subscribe_schedule:
        #     print(user)
        #     users_and_user_groups[user[0]]

        # End for
        await mailing_schedule(chat_ids_subscribe_schedule, schedule)
    # End if
    if chat_ids_subscribe_schedule_ch:
        await mailing_schedule_ch(chat_ids_subscribe_schedule_ch, changes)
    # End if
# End def


# Розсилка розкладу (якщо юзер підписаний тільки на розклад)
async def mailing_schedule(chat_ids_list: list, schedule):
    list_first_schedule = schedule[0]
    list_second_schedule = schedule[1]
    list_third_schedule = schedule[2]
    list_fourth_schedule = schedule[3]

    for chat_id in chat_ids_list:
        # await asyncio.sleep(1/2)  # TODO: sleep - mailing_schedule()
        pass
    # End for
# End def


# Розсилка змін в розкладі (якщо юзер підписаний тільки на зміни)
async def mailing_schedule_ch(chat_ids_list: list, changes: list):
    byte_array = await create_tabe.get_img_tabel_schedule_ch(changes)
    # Відправляємо повідомлення користувачеві, і отримуємо ID картинки
    if byte_array is not None:
        img_id = (await bot.send_photo(chat_ids_list.pop(-1), photo=InputFile(byte_array))).photo[-1].file_id
        for chat_id in chat_ids_list:
            await bot.send_photo(chat_id, photo=img_id)
            # await asyncio.sleep(1/2)  # TODO: sleep - mailing_schedule_ch()
        # End for
    # End if
# End def


# ----------------------------------------------------------------------------------------------------------------------
# Welcome меседж

async def echo_message_start_command(message: types.Message):
    user_id = message.from_user.id
    # Якщо юзер ще не зареєстрований, то зареєструвати його і запропонувати оформити підписку
    if await working_with_db.check_user_registration(message):
        await working_with_db.write_register_user(message)
        await message.answer(f"{strings.MSG_START_CLIENT}\n\n"
                             "Підпишіться на щоденну розсилку розкладу або змін в розкладі: /subscribe")
    else:
        # Якщо пише адміністратор, то відправити йому
        # повідомлення в ПП відмінне від звичайних юзерів
        if await working_with_db.check_is_admin(user_id):
            await bot.send_message(user_id, strings.MSG_START_ADMIN)
        else:
            await message.answer(strings.MSG_START_CLIENT)
    # End if-else
# End def


# ----------------------------------------------------------------------------------------------------------------------
# Список команд /help

async def echo_message_help_command(message: types.Message):
    user_id = message.from_user.id
    if await working_with_db.check_is_admin(user_id):
        await bot.send_message(user_id, strings.MSG_HELP_MENU_ADMIN)
    else:
        await message.answer(strings.MSG_HELP_MENU_CLIENT)
# End def


# ----------------------------------------------------------------------------------------------------------------------
# Підписка/скасування розсилки розкладу/змін в розкладі

async def subscribe_schedule(message: types.Message):
    if await group_selection.send_message(message):
        await subscription_keyboard.send_message(message)
# End def


# ----------------------------------------------------------------------------------------------------------------------
# Репорт

class FsmReport(StatesGroup):
    rep_message = State()
# End class


async def command_report(message: types.Message):
    await working_with_db.check_user_registration(message)
    message_rep_r = message.text

    if len(message_rep_r.split()) > 1:
        msg_rep_len = message_rep_r.partition(' ')[2]
        print(msg_rep_len)
        if len(msg_rep_len) >= 10:
            await send_rep_message(message)
        else:
            await message.answer("Введіть мінімум 10 символів.")
        # End if-else
    else:
        await FsmReport.rep_message.set()
        await message.answer("Опишіть проблему\n*Одним повідомленням*")
    # End if-else
# End def


# Якщо юзер використав просто команду /report, то від нього очікується
# наступне повідомлення з текстом репорту
# TODO: 1. Чомусь не пише що повідомлення коротше за 10 символів
# TODO: 2. Додати /cancel щоб зупинити FSM-state
async def fsm_message_rep(message: types.Message, state: FSMContext):
    if len(message.text) >= 10:
        await send_rep_message(message)
        await state.finish()
    else:
        await message.answer("Введіть мінімум 10 символів.")
    # End if-else
# End def


async def send_rep_message(message):
    user_id = message.from_user.id
    user_name = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    message_text = message.text.partition(' ')[2]

    if len(message_text) == 0:
        message_text = message.text
    # End if

    await working_with_db.write_report(user_id, message_text)  # msg_report
    await message.answer("Репорт було надіслано.\n"
                         "Дякую за співпрацю в покращенні проекту.")
    await bot.send_message(CHAT_ID_REP, f"User name: @{user_name}\n"
                                        f"First name: {first_name}\n"
                                        f"Last name: {last_name}\n"
                                        f"Написав(-ла) репорт:\n\n<b>{message_text}</b>", parse_mode="HTML")
# End def


# ----------------------------------------------------------------------------------------------------------------------
# Реєстрація хендлерів


async def call_back_data(call: types.CallbackQuery):
    data = call.data
    # Якщо натиснуто кнопку підписки на розклад або зміни в розкладі
    if data in subscription_keyboard.callback_list:
        await subscription_keyboard.edit_keyboard(call.message.chat.id, call.message.message_id, data)
    # Якщо натиснуто кнопку з курсом
    elif data in group_selection.select_course_callback_list:
        if data == "third_course":
            await group_selection.edit_keyboard(call.message.chat.id, call.message.message_id, data)
        else:
            await call.answer("Ще не реалізовано. Працює поки що тільки 3 курс")

        # match data:
        #     case "first_course":
        #         await call.answer("Ще не реалізовано. Працює поки що тільки 3 курс")
        #     case "second_course":
        #         await call.answer("Ще не реалізовано. Працює поки що тільки 3 курс")
        #     case "third_course":
        #         await group_selection.edit_keyboard(call.message.chat.id, call.message.message_id, data)
        #     case "fourth_course":
        #         await call.answer("Ще не реалізовано. Працює поки що тільки 3 курс")
        # End match-case
    # Якщо натиснуто кнопку з номером групи:
    elif data in await working_with_db.read_groups():
        await working_with_db.update_register_user(call)
        await bot.delete_message(call.message.chat.id, call.message.message_id)
        await bot.delete_message(call.message.chat.id, call.message.message_id-1)
        await subscription_keyboard.send_message(call.message)
    # End if-elif...
    await call.answer()  # Підтвердження виконання кода(щоб прибрати годинничок на кнопці)
# End def


# ----------------------------------------------------------------------------------------------------------------------
# Реєстрація хендлерів
def register_handlers_client(dp: Dispatcher):
    # Хендлер(-и) відповідає(-ють) за команду /start
    dp.register_message_handler(echo_message_start_command, commands=['start', 's'])
    # Хендлер(-и) відповідає(-ють) за команду /help
    dp.register_message_handler(echo_message_help_command, commands=['help', 'h'])
    # Хендлер(-и) відповідає(-ють) за підписки
    dp.register_message_handler(subscribe_schedule, commands=['my_subscriptions', 'my_sub'])
    # Хендлер(-и) відповідають за репорт
    dp.register_message_handler(command_report, commands=['report', 'rep'])
    dp.register_message_handler(fsm_message_rep, content_types=['callback'], state=FsmReport.rep_message)
    # Обробка кол беків від кнопок
    dp.register_callback_query_handler(call_back_data)
# End def
