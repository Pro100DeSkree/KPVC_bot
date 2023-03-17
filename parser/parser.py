from parser.BeautifulSoup import get_soup
import requests
from parser import schedule_changes
from parser import first_course_schedule
from parser import second_course_schedule
from parser import third_course_schedule
from parser import fourth_course_schedule
from data import working_with_db, sqlite_db

url = "https://college.ks.ua/#"


async def main(debug: bool = False):

    if debug:
        with open("./parser/KPVC_site.html") as f:
            soup_raw = f.read()
    else:
        r = requests.get(url)
        soup_raw = r.text
        with open("./parser/KPVC_site.html", "w") as f:
            f.write(soup_raw)

    soup = get_soup(soup_raw)
    schedule_soup = soup.find('div', id="content")

    # Отримуємо та записуємо зміни в розкладі
    list_schedule_changes = await schedule_changes.get_schedule_changes(schedule_soup)
    await working_with_db.write_schedule_changes(list_schedule_changes)

    # Отримуємо та записуємо розклад першого курсу
    # list_first_course_schedule = await first_course_schedule.get_first_course_schedule(schedule_soup)
    # await working_with_db.write_first_course_schedule(list_first_course_schedule)

    # Отримуємо та записуємо розклад другого курсу
    # list_second_course_schedule = await second_course_schedule.get_second_course_schedule(schedule_soup)
    # await working_with_db.write_second_course_schedule(list_second_course_schedule)

    # Отримуємо та записуємо розклад третього курсу
    list_third_course_schedule = await third_course_schedule.get_third_course_schedule(schedule_soup)
    await working_with_db.write_third_course_schedule(list_third_course_schedule)

    # Отримуємо та записуємо розклад четвертого курсу
    # list_fourth_course_schedule = await fourth_course_schedule.get_fourth_course_schedule(soup)
    # await working_with_db.write_fourth_course_schedule(list_fourth_course_schedule)


if __name__ == '__main__':
    sqlite_db.sql_star("../data/database.db")
    main(debug=True)
