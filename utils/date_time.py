import icu  # PyICU
from datetime import date, timedelta, datetime

months = [('січня', 'Січень'), ('лютого', 'Лютий'), ('березня', 'Березень'),
          ('квітня', 'Квітень'), ('травня', 'Травень'), ('червня', 'Червень'),
          ('липня', 'Липень'), ('серпня', 'Серпень'), ('вересня', 'Вересень'),
          ('жовтня', 'Жовтень'), ('листопада', 'Листопад'), ('грудня', 'Грудень')]


def convert(date_str: str):
    df = icu.SimpleDateFormat('', icu.Locale('ua'))
    output_df = icu.SimpleDateFormat('dd.MM.yyyy')

    for month in months:
        date_str = date_str.replace(month[0], month[1])  # Якщо місяць написано не по формату, то змінюємо слово
    # End for
    df.applyPattern('dd LLLL yyyy')
    try:
        data = output_df.format(df.parse(date_str))
        return data
    except icu.ICUError:
        return None
    # End try-except
# End def


def time_converter(date_str: str):
    date_str = date_str
    first_text = date_str.partition(' р')[-3]
    row_string = date_str.partition('., ')[2].partition(', ')

    date_str = first_text.replace('»', '').replace('на «', '')
    weekday = row_string[0].replace('(', '')
    num_or_denom = row_string[-1].replace(')', '')

    return [convert(date_str), weekday, num_or_denom]
# End def


async def get_date(date_format='%d.%m.%Y', add_day=None):
    date_list = []
    if add_day is None:
        return date.today().strftime(date_format)
    else:
        to_day = date.today()
        return [(to_day + timedelta(days=i)).strftime(date_format) for i in range(1, add_day)]


async def get_current_weekday():
    days = ["неділя", "понеділок", "вівторок", "середа", "четвер", "п'ятниця", "субота"]
    weekday_num = datetime.now() + timedelta(days=1)
    return days[weekday_num.weekday()]
# End def


async def get_current_weekday_test():
    # Словник назв днів тижня
    days_in_ukr = {
        0: "Понеділок",
        1: "Вівторок",
        2: "Середа",
        3: "Четвер",
        4: "П'ятниця",
        5: "Субота",
        6: "Неділя"
    }

    today = date.today()  # Отримуємо поточну дату
    current_day_of_week = today.weekday()  # Визначаємо номер поточного дня тижня (0 - понеділок, 6 - неділя)
    return days_in_ukr[(current_day_of_week + 1) % 7]  # Визначаємо номер наступного дня тижня
# End def


async def get_current_time():
    curr_time = datetime.now()
    return curr_time.strftime("%H:%M")
# End def


if __name__ == "__main__":
    print(time_converter("на «28» лютого 2023 р., (вівторок, чисельник)"))
    # print(convert("01 березня 2023"))
# End if
