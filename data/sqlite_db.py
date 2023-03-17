import sqlite3 as sq


def sql_star(db_path=r"./data/database.db"):
    global db, cur
    with sq.connect(db_path) as db:
        cur = db.cursor()
        if db:
            print("Data base connected!")
        # End if
    # End with
# End def


# ----------------------------------------------------------------------------------------------------------------------
# Запис\Зчитування таблиці адмінів

async def write_new_admin(new_admin_id):
    cur.execute(f"""SELECT user_id FROM admins_t WHERE user_id = ?""", new_admin_id)
    if cur.fetchone() is None:
        cur.execute("""INSERT INTO admins_t VALUES (?, ?)""", (new_admin_id, True))
        db.commit()
        return 0
    else:
        return 1
    # End if-else
# End def


async def read_admin():
    cur.execute(f"SELECT user_id FROM admins_t")
    list_a = []
    for row in cur.fetchall():
        list_a.append(row[0])
    # End for
    return list_a
# End def


# ----------------------------------------------------------------------------------------------------------------------
# Запис\Зчитування таблиці змін в розкладі

async def write_update_schedule_changes(date, weekday, num_or_denom, group_num, lesson_num,
                                        lesson_before, practice_study, lesson_after, classroom_num):
    cur.execute(f"""SELECT * FROM schedule_changes_t WHERE change_date = ? AND group_num = ? AND 
                                                           lesson_num = ? OR practice_study = ?""", (date, group_num,
                                                                                                 lesson_num, practice_study,))
    if cur.fetchone() is None:  # Якщо в БД немає такого елементу, то додаємо його
        cur.execute("""INSERT INTO schedule_changes_t VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", (None, date, weekday,
                                                                                                 num_or_denom,
                                                                                                 group_num, lesson_num,
                                                                                                 lesson_before,
                                                                                                 practice_study,
                                                                                                 lesson_after,
                                                                                                 classroom_num,))
        db.commit()
        return 0
    else:  # Якщо в БД вже записано такий елемент, то вносимо зміни
        cur.execute(f"""UPDATE schedule_changes_t SET change_date = ?, weekday = ?, num_or_denom = ?, group_num = ?,
                                                      lesson_num = ?, lesson_before = ?, lesson_after = ?, 
                                                      classroom_num = ? WHERE change_date = ? AND group_num = ? 
                                                      AND lesson_num = ?""", (date, weekday, num_or_denom, group_num,
                                                                              lesson_num, lesson_before, lesson_after,
                                                                              classroom_num, date, group_num, lesson_num,))
        db.commit()
        return 1
    # End if-else
# End def


async def read_schedule_changes():
    cur.execute("""SELECT * FROM schedule_changes_t""")
    return cur.fetchall()
# End def


# ----------------------------------------------------------------------------------------------------------------------
# Запис\Зчитування таблиці розкладу першого курсу

async def write_first_course_schedule():
    pass
# End def


async def read_first_course_schedule():
    return None
# End def


# ----------------------------------------------------------------------------------------------------------------------
# Запис\Зчитування таблиці розкладу другого курсу

async def write_second_course_schedule():
    pass
# End def


async def read_second_course_schedule():
    return None
# End def


# ----------------------------------------------------------------------------------------------------------------------
# Запис\Зчитування таблиці розкладу третього курсу

async def write_update_third_course_schedule(group_num, weekday, lesson_num, lesson_and_teacher, classroom_num, semester, years):
    cur.execute(f"""SELECT * FROM third_course_schedule_t WHERE group_num = ? AND weekday = ? AND lesson_num = ? AND years = ?""",
                (group_num, weekday, lesson_num, years,))
    if cur.fetchone() is None:  # Якщо в БД немає такого елементу, то додаємо його
        cur.execute("""INSERT INTO third_course_schedule_t VALUES (?, ?, ?, ?, ?, ?, ?, ?)""", (None, group_num, weekday,
                                                                                                lesson_num, lesson_and_teacher,
                                                                                                classroom_num, semester,
                                                                                                years,))
        db.commit()
        return 0
    else:  # Якщо в БД вже записано такий елемент, то вносимо зміни
        cur.execute(f"""UPDATE third_course_schedule_t SET group_num = ?, weekday = ?, lesson_num = ?, 
                                                            lesson_and_teacher = ?, classroom_num = ?, semester = ?,
                                                            years = ? WHERE group_num = ? AND weekday = ? AND
                                                            lesson_num = ?""", (group_num, weekday, lesson_num,
                                                                                lesson_and_teacher, classroom_num,
                                                                                semester, years, group_num,
                                                                                weekday, lesson_num,))
        db.commit()
        return 1
    # End if-else
# End def


async def read_third_course_schedule():
    cur.execute("""SELECT * FROM third_course_schedule_t""")
    return cur.fetchall()
# End def


async def get_third_course_schedule_by_weekday(weekday):
    cur.execute("""SELECT * FROM third_course_schedule_t WHERE weekday = ?""", (weekday,))
    return cur.fetchall()
# End def


# ----------------------------------------------------------------------------------------------------------------------
# Запис\Зчитування таблиці розкладу четвертого курсу

async def write_fourth_course_schedule():
    pass
# End def


async def read_fourth_course_schedule():
    return None
# End def


# ----------------------------------------------------------------------------------------------------------------------
# Запис\Зчитування таблиці підписок користувачів

async def update_subscribe(chat_id, schedule_sub, schedule_ch_sub):
    cur.execute(f"""SELECT * FROM subscriptions_t WHERE chat_id = ?""", (chat_id,))
    if cur.fetchone() is not None:
        cur.execute(f"""UPDATE subscriptions_t SET schedule_sub = ?, schedule_ch_sub = ?
                                                   WHERE chat_id = ?""", (schedule_sub, schedule_ch_sub, chat_id,))
        db.commit()
    # End if-else
# End def------------------------------------------------------
# Запис\Зчитування таблиці підписок користувачів


async def write_subscribe(user_id, chat_id):
    cur.execute(f"""SELECT * FROM subscriptions_t WHERE chat_id = ?""", (chat_id,))
    if cur.fetchone() is None:
        cur.execute(f"""INSERT INTO subscriptions_t VALUES (?, ?, ?, ?, ?)""", (None, user_id, chat_id, 0, 0,))
        db.commit()
    # End if
# End def


async def read_subscribe_by_chat_id(chat_id):
    cur.execute(f"""SELECT schedule_sub, schedule_ch_sub FROM subscriptions_t WHERE chat_id = ?""", (chat_id,))
    return cur.fetchone()
    # End if-else
# End def


async def get_chat_ids_subscribe_schedule():
    cur.execute("""SELECT user_id, chat_id FROM subscriptions_t WHERE schedule_sub = '1'""")
    return cur.fetchall()
# End def


async def get_chat_ids_subscribe_schedule_ch():
    cur.execute("""SELECT chat_id FROM subscriptions_t WHERE schedule_ch_sub = '1'""")
    return cur.fetchall()
# End def


# ----------------------------------------------------------------------------------------------------------------------
# Перевірка\реєстрація\читання користувачів

async def register_user(user_id, user_name, first_name, last_name, user_group):
    if await read_users_by_id(user_id) is None:
        cur.execute("""INSERT INTO users_t VALUES (?, ?, ?, ?, ?)""", (user_id, user_name,
                                                                       first_name, last_name, None,))
        db.commit()
    else:
        cur.execute(f"""UPDATE users_t SET user_name = ?, first_name = ?, last_name = ?,  user_group = ?
                                           WHERE user_id = ?""", (user_name, first_name,
                                                                  last_name, user_group, user_id,))
        db.commit()
# End def


async def read_users_by_id(user_id):
    cur.execute(f"""SELECT * FROM users_t WHERE user_id = ?""", (user_id,))
    return cur.fetchone()
# End def


async def get_users_groups():
    cur.execute(f"""SELECT user_id, user_group FROM users_t""")
    return cur.fetchall()
# End def


# ----------------------------------------------------------------------------------------------------------------------
# Зберігання репорту

async def write_rep(user_id, message_text, date):
    cur.execute("""INSERT INTO reports_t VALUES (?, ?, ?, ?)""", (None, user_id, message_text, date,))
    db.commit()
# End def


# ----------------------------------------------------------------------------------------------------------------------
# Запис/зчитування груп

async def write_group(course_num, group_num, specialty):
    cur.execute(f"""SELECT * FROM all_groups_t WHERE group_num = ?""", (group_num,))
    if cur.fetchone() is None:
        cur.execute("""INSERT INTO all_groups_t VALUES (?, ?, ?, ?)""", (None, course_num, group_num, specialty,))
        db.commit()
    # End if
# End def


async def read_groups_by_course(course):
    cur.execute(f"""SELECT group_num FROM all_groups_t WHERE course_num = ?""", (course,))
    return cur.fetchall()
# End def


async def read_groups():
    cur.execute(f"""SELECT group_num FROM all_groups_t""")
    return cur.fetchall()
# End def
