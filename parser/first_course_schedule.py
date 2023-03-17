
test = 4


def get_first_course_schedule(soup):
    global test
    first_course_schedule = soup.find('div', class_="form-185").findNext("div", class_="shedule_content")

    title = first_course_schedule.find('p', class_="shedule_content__title")
    full_tabel_raw = first_course_schedule.find('tbody')
    all_table_row_raw = full_tabel_raw.findAll('tr')

    # print(all_table_row_raw[4])

    for row in all_table_row_raw:
        # Перша половина колон
        if len(row.findAll('td')) == 7:
            weekday_raw = row.find('td')
            fir_les_num_raw = weekday_raw.findNext('td')
        else:
            fir_les_num_raw = row.find('td')
        fir_gro_or_les_and_teach_raw = fir_les_num_raw.findNext('td')
        fir_classroom_num_raw = fir_gro_or_les_and_teach_raw.findNext('td')

        # Друга половина колон
        sec_les_num_raw = fir_classroom_num_raw.findNext('td')
        sec_gro_or_les_and_teach_raw = sec_les_num_raw.findNext('td')
        sec_classroom_num_raw = sec_gro_or_les_and_teach_raw.findNext('td')

        if fir_les_num_raw.text.strip() != "" or fir_gro_or_les_and_teach_raw != "":
            # print(fir_gro_or_les_and_teach_raw.text.strip())

            # print(weekday_raw.text.strip(),
            #       fir_les_num_raw.text.strip(),
            #       fir_gro_or_les_and_teach_raw.text.strip(),
            #       fir_classroom_num_raw.text.strip(),
            #       "\n\n",
            #       sec_les_num_raw.text.strip(),
            #       sec_gro_or_les_and_teach_raw.text.strip(),
            #       sec_classroom_num_raw.text.strip())
            pass
        if test == 6:
            break
        test = + 1
    # End for
# End def
