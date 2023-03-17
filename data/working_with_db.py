import config
from aiogram import types
from utils import date_time
from data import sqlite_db
from keyboard import subscription_keyboard


# ----------------------------------------------------------------------------------------------------------------------
# Запис/зчитування змін

async def write_schedule_changes(list_schedule_changes: list):
    for item in list_schedule_changes:
        key = list(item.keys())[0]  # Отримуємо ключ
        list_of_changes: list = item[key]  # Отримуємо список змін у розкладі за один день
        # Отримуємо список з однорядкових змін типу: "Групи 211, 272, 351 йдуть на практику"
        practice_list: list = list_of_changes.pop(-1)['practice']
        # Отримуємо дату, день тижня і чисельник чи знаменник
        date, weekday, num_or_denom = date_time.time_converter(key)
        if len(practice_list) != 0:
            for practice_study in practice_list:
                await sqlite_db.write_update_schedule_changes(date, weekday, num_or_denom, None, None, None, practice_study, None, None)
        for it in list_of_changes:
            await sqlite_db.write_update_schedule_changes(date, weekday, num_or_denom, it[0], it[1], it[2], None, it[3], it[4])
        # End for
    # End for
# End def


async def read_schedule_changes():
    return await sqlite_db.read_schedule_changes()
# End def


# ----------------------------------------------------------------------------------------------------------------------
# Запис/зчитування розкладу першого курсу

async def write_first_course_schedule(dict_course_schedule: dict):
    pass
# End def


async def get_first_course_schedule_by_weekday(weekday):
    return None
# End def


# ----------------------------------------------------------------------------------------------------------------------
# Запис/зчитування розкладу другого курсу

async def write_second_course_schedule(dict_course_schedule: dict):
    pass
# End def


async def get_second_course_schedule_by_weekday(weekday):
    return None
# End def


# ----------------------------------------------------------------------------------------------------------------------
# Запис/зчитування розкладу третього курсу

async def write_third_course_schedule(dict_course_schedule: dict):
    title: str = list(dict_course_schedule.keys())[0]
    semester = title.partition('семестр')[0].partition("на")[-1].strip()
    years = title.partition('н.р.')[0].partition("семестр")[-1].strip()
    for group, schedule in dict_course_schedule[title].items():
        await write_group(str(group))
        for weekday, list_schedule in schedule.items():
            for lesson in list_schedule:
                if lesson[1] != "":
                    await sqlite_db.write_update_third_course_schedule(group, weekday.lower(), lesson[0], lesson[1], lesson[2], semester, years)
                # End if
            # End for
        # End for
    # End for
# End def


async def read_third_course_schedule():
    schedule = await sqlite_db.read_third_course_schedule()
    for less in schedule:
        pass
    return
# End def


async def get_third_course_schedule_by_weekday(weekday):
    data = {305: []}  # TODO: Відформатувати данні
    schedule = await sqlite_db.get_third_course_schedule_by_weekday(weekday.lower())
    for less in schedule:
        print(less)

        break
    return schedule
# End def


# ----------------------------------------------------------------------------------------------------------------------
# Запис/зчитування розкладу четвертого курсу

async def write_fourth_course_schedule(dict_course_schedule: dict):
    pass
# End def


async def get_fourth_course_schedule_by_weekday(weekday):
    return
# End def


# ----------------------------------------------------------------------------------------------------------------------
# Запис/зчитування таблиці підписок користувачів

async def update_subscribe(chat_id, call_data, user_id=None):
    subs = await read_subscribe_by_chat_id(chat_id)
    schedule_sub = False
    schedule_ch_sub = False
    if subs is not None and call_data is not None:
        schedule_sub = subs[-2]
        schedule_ch_sub = subs[-1]
    else:
        subs = [schedule_sub, schedule_ch_sub]

    lambda_converter = lambda x: True if x == 1 else False
    if call_data == subscription_keyboard.callback_list[0]:
        schedule_sub = not lambda_converter(subs[-2])
    if call_data == subscription_keyboard.callback_list[1]:
        schedule_ch_sub = not lambda_converter(subs[-1])

    await sqlite_db.update_subscribe(chat_id, schedule_sub, schedule_ch_sub)
# End def


async def write_subscribe(message: types.Message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    await sqlite_db.write_subscribe(user_id, chat_id)
# End def


async def read_subscribe_by_chat_id(chat_id):
    return await sqlite_db.read_subscribe_by_chat_id(chat_id)
# End def


async def get_chat_ids_subscribe_schedule():
    return [[x[0], x[1]] for x in await sqlite_db.get_chat_ids_subscribe_schedule()]  # Прибираються дужки "тапла"
# End def


async def get_chat_ids_subscribe_schedule_ch():
    return [x[0] for x in await sqlite_db.get_chat_ids_subscribe_schedule_ch()]  # Прибираються дужки "тапла"
# End def


# ----------------------------------------------------------------------------------------------------------------------
# Запис/зчитування таблиці усіх груп/курсів

async def write_group(group_num, specialty: str = None):
    course_num = int(group_num[0])
    await sqlite_db.write_group(course_num, group_num, specialty)
# End def


async def read_groups():
    tuple_list_groups = await sqlite_db.read_groups()
    normal_list_groups = []
    for item in tuple_list_groups:
        normal_list_groups.append(str(item[0]))
    return normal_list_groups
    # End if-else
# End def


async def read_groups_by_course(course):
    return await sqlite_db.read_groups_by_course(course)
# End def


# ----------------------------------------------------------------------------------------------------------------------
# Перевірка чи користувач адміністратор

async def check_is_admin(user_id):
    admins_list = await sqlite_db.read_admin()
    admins_list.append(config.MAIN_ADMIN)
    if user_id in admins_list:
        return True
    else:
        return False
    # End if-else
# End def


# ----------------------------------------------------------------------------------------------------------------------
# Запис репортів

async def write_report(user_id, msg_report):
    data = await date_time.get_date()
    await sqlite_db.write_rep(user_id, msg_report, data)
    pass
# End def


# ----------------------------------------------------------------------------------------------------------------------
# Запис/зчитування зареєстрованих користувачів

async def write_register_user(msg):
    user_id = msg.from_user.id
    user_name = msg.from_user.username
    first_name = msg.from_user.first_name
    last_name = msg.from_user.last_name
    await sqlite_db.register_user(user_id, user_name, first_name, last_name, None)
# End def


async def update_register_user(call: types.CallbackQuery):
    user_id = call.message.chat.id
    user_name = call.message.chat.username
    first_name = call.message.chat.first_name
    last_name = call.message.chat.last_name
    user_group = int(call.data)
    await sqlite_db.register_user(user_id, user_name, first_name, last_name, user_group)
# End def


async def check_user_registration(msg):
    user_id = msg.from_user.id
    if await sqlite_db.read_users_by_id(user_id) is None:
        return True
# End def


async def read_user_by_user_id(msg):
    user_id = msg.from_user.id
    return await sqlite_db.read_users_by_id(user_id)
# End def


async def get_users_groups():
    users_format = {}
    users = await sqlite_db.get_users_groups()
    for user in users:
        users_format.update({user[0]: user[1]})
    # End for
    return users_format
# End def


if __name__ == "__main__":
    sqlite_db.sql_star("./database.db")

    # ТЕСТУВАННЯ write_third_course_schedule
    # first_test_dict = {"Розклад занять на 2 семестр 2022-2023 н.р.": {382: {'Понеділок': [['1', '', ''], ['2', 'Фіз.вихов. - Федін ЮМ.', ''], ['3', 'Правознавство - Мадаєва', ''], ['4', 'Сист.прогр/Комп.сист - Левицький /Бабикін', ''], ['1', '', ''], ['2', '', ''], ['3', '', ''], ['4', '', '']], 'Вівторок': [['1', "Арх.комп'ютера/--- - Максимова/----", ''], ['2', 'Економіка орг.вир - Живець А.М.', ''], ['3', 'Проект.мікропроц.сист. - Уткіна', ''], ['4', 'Системне програмування - Левицький В.М.', ''], ['1', '', ''], ['2', '', ''], ['3', '', ''], ['4', '', '']], 'Середа': [['1', '', ''], ['2', 'Комп.сист.та мережі - Бабикін', ''], ['3', 'Периферійні пристрої - Бездворний', ''], ['4', 'Економіка/Правозн - Живець /Мадаєва', ''], ['1', '', ''], ['2', '', ''], ['3', '', ''], ['4', '', '']], 'Четвер': [['1', '', ''], ['2', 'Іноземна мова за ПС - Аносова, Власенко', ''], ['3', 'Периферійні пристрої - Бездворний', ''], ['4', 'Проект.мікропроц.сист. - Уткіна', ''], ['1', '', ''], ['2', '', ''], ['3', '', ''], ['4', '', '']], "П'ятниця": [['1', 'Проект.мікропроц.сист. - Уткіна', ''], ['2', 'Системне програмування - Левицький В.М.', ''], ['3', "Арх.комп'ютера - Максимова", ''], ['4', 'Комп.сист.та мережі - Бабикін', ''], ['1', '', ''], ['2', '', ''], ['3', '', ''], ['4', '', '']]}}}
    # second_test_dict = {"Розклад занять на 2 семестр 2022-2023 н.р.": {305: {'Понеділок': [['1', 'Фізичне виховання - Рибкін А.В.', ''], ['2', 'Старахув.у туризмі - Литвиненко І.В.', ''], ['3', 'Техн.і орг. тур.обслугов. - Матвієнко Т.В.', ''], ['4', '', '']], 'Вівторок': [['1', 'Старахув.у туризмі - Литвиненко І.В.', ''], ['2', 'Основи менеджменту - Литвиненко І.В.', ''], ['3', 'Інф.системи і технології - Наконечна В.І.', ''], ['4', '', '']], 'Середа': [['1', '', ''], ['2', 'Друга іноземна мова - Вареник А.О.', ''], ['3', 'Основи менеджменту - Литвиненко І.В.', ''], ['4', 'Ін.мова турист.індустрії - Наумкіна, Аносова', '']], 'Четвер': [['1', 'Інф.системи і технології - Наконечна В.І.', ''], ['2', 'Старахув.у туризмі - Литвиненко І.В.', ''], ['3', 'Техн.і орг. тур.обслугов. - Матвієнко Т.В.', ''], ['4', '', '']], "П'ятниця": [['1', 'Друга іноземна мова - Вареник А.О.', ''], ['2', 'Ін.мова турист.індустрії - Наумкіна, Аносова', ''], ['3', 'Основи менеджменту - Литвиненко І.В.', ''], ['4', '', '']]}}}
    # write_third_course_schedule(second_test_dict)

    # ТЕСТУВАННЯ write_schedule_changes:
    # test_list = [{'на «02»  березня 2023 р., (четвер, чисельник)': [['131', '1', 'Коцегубов', 'Литвиненко', ''], ['305', '1', 'Наконечна', 'Матвієнко', ''], ['305', '3', 'Матвієнко', 'Наконечна', '']]},
    #              {'на «01»  березня 2023 р., (середа, чисельник)': [['281', '1', 'Максимова', 'Бабикін', ''], ['361', '1', 'Додатково', 'Комліченко (контроль і ревізія)', ''], ['261', '3', 'Живець', 'Чебукін', ''], ['382', '4', 'Живець', 'Левицький', ''], ['321', '2', 'Шалапко (газ.динам)', 'Чебукін', ''], ['371', '4', 'Сорокін', 'Відсутня', '']]}]
    # write_schedule_changes(test_list)

    # ТЕСТУВАННЯ
# End if
