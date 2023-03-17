

async def get_third_course_schedule(soup):
    schedule = {}
    first_column_group_num = -1
    second_column_group_num = -1
    weekday_str = ""

    third_course_schedule = soup.find('div', class_="form-189")

    title = third_course_schedule.find('p', class_="shedule_content__title")
    full_tabel_raw = third_course_schedule.find('tbody')
    all_table_row_raw = full_tabel_raw.findAll('tr')

    # TODO: Треба оптимізувати наступний for
    for row in all_table_row_raw:
        # --------------------------------------------------------------------------------------------------------------
        # Парсинг даних
        # Перша половина колон
        if len(row.findAll('td')) == 8:
            weekday_raw = row.find('td')
            weekday_str = weekday_raw.text.strip()
            fir_les_num_raw = weekday_raw.findNext('td')
        else:
            fir_les_num_raw = row.find('td')
        fir_gro_or_les_and_teach_raw = fir_les_num_raw.findNext('td')
        fir_classroom_num_raw = fir_gro_or_les_and_teach_raw.findNext('td')

        # Друга половина колон
        sec_les_num_raw = fir_classroom_num_raw.findNext('td')
        sec_gro_or_les_and_teach_raw = sec_les_num_raw.findNext('td')
        sec_classroom_num_raw = sec_gro_or_les_and_teach_raw.findNext('td')

        if fir_les_num_raw.text.strip() != "" or fir_gro_or_les_and_teach_raw.text.strip() != "":

            if await string_validation(fir_gro_or_les_and_teach_raw.text.strip()) is not None:
                first_column_group_num = await string_validation(fir_gro_or_les_and_teach_raw.text.strip())
            if await string_validation(sec_gro_or_les_and_teach_raw.text.strip()) is not None:
                second_column_group_num = await string_validation(sec_gro_or_les_and_teach_raw.text.strip())
            # ----------------------------------------------------------------------------------------------------------
            # Пакування в словар першої половини таблиці
            if fir_les_num_raw.text.strip() != "":
                schedule_keys = schedule.keys()
                if first_column_group_num in schedule_keys:
                    first_dict_schedule = schedule[first_column_group_num]
                    first_dict_schedule_keys = first_dict_schedule.keys()
                    if weekday_str in first_dict_schedule_keys:
                        dict_copy = first_dict_schedule.copy()
                        first_list_schedule = dict_copy[weekday_str]
                        first_list_schedule.append([fir_les_num_raw.text.strip(),
                                                    ' '.join(fir_gro_or_les_and_teach_raw.text.strip().replace('\n', ' -').split()),
                                                    fir_classroom_num_raw.text.strip()])
                        dict_copy.update({weekday_str: first_list_schedule})
                        schedule.update({first_column_group_num: dict_copy})
                    else:
                        dict_copy = first_dict_schedule.copy()
                        dict_copy.update({weekday_str: [[fir_les_num_raw.text.strip(),
                                                        ' '.join(fir_gro_or_les_and_teach_raw.text.strip().replace('\n', ' -').split()),
                                                         fir_classroom_num_raw.text.strip()]]})
                        schedule.update({first_column_group_num: dict_copy})
                    # End if-else
                else:
                    schedule.update({first_column_group_num: {weekday_str: [[fir_les_num_raw.text.strip(),
                                                              ' '.join(fir_gro_or_les_and_teach_raw.text.strip().replace('\n', ' -').split()),
                                                              fir_classroom_num_raw.text.strip()]]}})
                # End if-else
                # ----------------------------------------------------------------------------------------------------------
                # Пакування в словар другої половини таблиці
                schedule_keys = schedule.keys()
                if second_column_group_num in schedule_keys:
                    second_dict_schedule = schedule[second_column_group_num]
                    second_dict_schedule_keys = second_dict_schedule.keys()
                    if weekday_str in second_dict_schedule_keys:
                        dict_copy = second_dict_schedule.copy()
                        second_list_schedule = dict_copy[weekday_str]
                        second_list_schedule.append([sec_les_num_raw.text.strip(),
                                                     ' '.join(sec_gro_or_les_and_teach_raw.text.strip().replace('\n', ' -').split()),
                                                     sec_classroom_num_raw.text.strip()])
                        dict_copy.update({weekday_str: second_list_schedule})
                        schedule.update({second_column_group_num: dict_copy})
                    else:
                        dict_copy = second_dict_schedule.copy()
                        dict_copy.update({weekday_str: [[sec_les_num_raw.text.strip(),
                                                        ' '.join(sec_gro_or_les_and_teach_raw.text.strip().replace('\n', ' -').split()),
                                                         sec_classroom_num_raw.text.strip()]]})
                        schedule.update({second_column_group_num: dict_copy})
                    # End if-else
                else:
                    schedule.update({second_column_group_num: {weekday_str: [[sec_les_num_raw.text.strip(),
                                                               ' '.join(sec_gro_or_les_and_teach_raw.text.strip().replace('\n', ' -').split()),
                                                               sec_classroom_num_raw.text.strip()]]}})
                # End if-else
            # End if
        # End if
    # End for
    return {title.text.strip(): schedule}
# End def


async def string_validation(string: str):
    if 3 <= len(string) <= 8 and \
            string != "ДЕНЬ" and \
            string != "РОБОТИ" and \
            string != "СТУДЕНТА":
        return int(string)
    # End if
# End def
