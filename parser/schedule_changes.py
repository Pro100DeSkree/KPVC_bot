

async def get_schedule_changes(soup):
    # TODO: Розібратися з парсингом "Групи 211, 272, 351 йдуть на практику"
    list_schedule_changes = []
    # HTML змін в розкладі
    schedule_changes = soup.find('div', class_="form-184").findNext("div", class_="shedule_content")

    # Перша таблиця зі змінами
    first_table_date = schedule_changes.find('p', class_="shedule_content__title")
    first_table_raw = schedule_changes.find('tbody')
    first_table_r = first_table_raw.findAll('tr')
    # print(first_table_date)
    # print(first_table_raw)

    # Друга таблиця зі змінами
    second_table_date = first_table_date.findNext('p', class_="shedule_content__title")
    second_table_raw = first_table_raw.findNext('tbody')
    second_table_r = second_table_raw.findAll('tr')
    # print(second_table_date)
    # print(second_table_raw)

    list_schedule_changes.append({first_table_date.text.strip(): await pars_table(first_table_r)})
    list_schedule_changes.append({second_table_date.text.strip(): await pars_table(second_table_r)})

    return list_schedule_changes
# End def


async def pars_table(table_row):
    list_of_changes_for_day = []
    practice_study_list = []
    for item in table_row:
        practice_study = item.find("td", colspan="5")
        group_num_row_raw = item.find('td')
        lesson_num_row_raw = group_num_row_raw.findNext('td')
        lesson_before_row_raw = lesson_num_row_raw.findNext('td')
        lesson_after_row_raw = lesson_before_row_raw.findNext('td')
        classroom_num_row_raw = lesson_after_row_raw.findNext('td')
        if practice_study is not None:
            practice_study_list.append(practice_study.text.strip())
        else:
            if group_num_row_raw.text.strip() != "" and group_num_row_raw.text.strip() != "Гр.":
                list_of_changes_for_day.append([group_num_row_raw.text.strip(),
                                                lesson_num_row_raw.text.strip(),
                                                ' '.join(lesson_before_row_raw.text.strip().split()),
                                                ' '.join(lesson_after_row_raw.text.strip().split()),
                                                classroom_num_row_raw.text.strip()])
            elif group_num_row_raw.text.strip() == "" and lesson_before_row_raw.text.strip() != "":
                list_of_changes_for_day.append(' '.join(lesson_before_row_raw.text.strip().split()))
        # End if-else
    # End for
    list_of_changes_for_day.append({"practice": practice_study_list})
    return list_of_changes_for_day
# End def
