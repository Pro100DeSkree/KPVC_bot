import io

import loguru
from PIL import Image, ImageDraw, ImageFont
from loguru import logger

from utils import date_time

# Встановлення шрифту та розміру тексту
font_name = 'Noto Serif ExtraCondensed Black Nerd Font Complete.ttf'
font_size = 40

# Ширина лінії таблиці
line_thickness_tabel = 2

# відступ від краю зображення
padding = 5


@logger.catch
async def get_img_tabel_schedule_ch(changes):
    current_date = await date_time.get_date('%d.%m', 3)
    headers = ['Гр.', 'Пара', 'За розкладом', 'За зміною', 'Авд.']
    data = [headers]
    data_practice = []
    title = 'Упс. Якась помилка'
    checking_for_no_changes = False

    for change in changes:
        date = change[1].partition('.2')[0]
        if date in current_date:
            if change[7] is None:
                title = f"На {date}({change[2].lower()}, {change[3]})"
                if data_practice:  # Перевірка чи не порожній список
                    if data_practice[0] != title:
                        data_practice.insert(0, title)
                    # End if
                else:
                    data_practice.insert(0, title)
                # End if-else
                data.append([str(change[-6]), str(change[-5]), change[-4], change[-2], str(change[-1])])
            elif change[7] is not None:
                data_practice.append(str(change[7]))
            # End if-elif-else
            checking_for_no_changes = True
        # End if
    # End for
    if checking_for_no_changes:
        return await __get_tabel(data, headers, data_practice)
    else:
        return None
# End def


async def __get_tabel(data: list, headers, data_practice):

    # Встановлення шрифту та розміру тексту
    font = ImageFont.truetype(font_name, font_size)

    # --------------------------РОЗРАХУНКИ РОЗМІРІВ ТАБЛИЦІ І ВІДПОВІДНО ЗОБРАЖЕННЯ--------------------------

    # Якщо data_practice не пустий то визначаємо найдовший рядок
    max_len_data_practice = 0
    if data_practice:
        max_len_data_practice = (max(int(font.getlength(text)) for text in data_practice)) + 20

    # Визначення максимальної довжини тексту у кожному стовпці
    max_col_widths = []
    for i in range(len(headers)):
        col_texts = [header[i] for header in [headers] + data]
        max_col_widths.append(max([int(font.getlength(text)) for text in col_texts]))
    # End for

    # Визначення ширини та висоти клітинок
    sum_cell_width = sum(list([max_col_widths[i] for i in range(len(headers))]))
    if max_len_data_practice > sum_cell_width:
        len_cell = (max_len_data_practice - sum_cell_width) // int(len(headers))
        cell_widths = list([max_col_widths[i] + len_cell for i in range(len(headers))])
    else:
        cell_widths = list([max_col_widths[i] + 20 for i in range(len(headers))])
    word_height = font.getbbox('A')[-1]
    cell_height = word_height + 20

    # Визначення кількості рядків
    row_count = len(data) + len(data_practice)

    # Визначення ширини та висоти таблиці
    table_width = sum(cell_widths)
    table_height = row_count * cell_height

    # Визначення розміру зображення з урахуванням падінгу та товщини ліній таблиці
    img_width = table_width + (padding * 2) + (line_thickness_tabel * 2)
    img_height = table_height + (padding * 2) + (line_thickness_tabel * 2)
    img = Image.new('RGB', (img_width, img_height), color='white')
    # Створення об'єкта ImageDraw для малювання на зображенні
    d = ImageDraw.Draw(img)
    # -------------------------------------МАЛЮВАННЯ ТАБЛИЦІ І ЗАПОВНЕННЯ ЇЇ--------------------------------------

    # Жовто-блакитний
    for i in range(1, 14):
        if i <= 6:
            d.line(xy=((table_width + padding, line_thickness_tabel + padding + i - 1),
                       (5, line_thickness_tabel + padding + i - 1)), fill='blue')
        else:
            d.line(xy=((table_width + padding, line_thickness_tabel + padding + i - 1),
                       (5, line_thickness_tabel + padding + i - 1)), fill='yellow')
        # End if-else
    # End for

    first_point_x = padding
    first_point_y = padding
    second_point_y = padding

    # Малювання тайтла та "однорядкові" зміни
    for row_index, text in enumerate(data_practice):
        second_point_x = table_width + padding
        second_point_y = second_point_y + cell_height

        d.rectangle((second_point_x, second_point_y, first_point_x, first_point_y), outline='black',
                    width=line_thickness_tabel)

        first_point_y = first_point_y + cell_height

        title_length = font.getlength(text)
        title_point_x = (table_width // 2) - (title_length // 2) + padding
        title_point_y = (second_point_y - cell_height // 2) - (word_height // 2) - padding
        d.text(xy=(title_point_x, title_point_y), text=text, font=font, fill='black')
        # End for

    for row_index, row in enumerate(data):
        second_point_y = second_point_y + cell_height
        second_point_x = padding
        first_point_x = padding
        for index, text in enumerate(row):
            # Визначення координат малювання клітинки
            second_point_x = second_point_x + cell_widths[index]

            d.rectangle((second_point_x, second_point_y, first_point_x, first_point_y), outline='black',
                        width=line_thickness_tabel)

            first_point_x = first_point_x + cell_widths[index]
            word_length = font.getlength(text)

            # Визначення центру клітинки
            cell_center_x = first_point_x - cell_widths[index] // 2
            cell_center_y = second_point_y - cell_height // 2

            # Визначення зміщення тексту відносно центру
            text_point_x = cell_center_x - (word_length // 2)
            text_point_y = cell_center_y - (word_height // 2) - 10

            d.text((text_point_x, text_point_y), text=text, font=font, fill='black')
        # End for
    # End for

    image_bytes = io.BytesIO()
    img.save(image_bytes, format="JPEG")
    image_bytes.seek(0)
    return image_bytes


@logger.catch
async def get_img_tabel_schedule(schedule: list):
    data = []

    return await __get_tabel_schedule(data)
# End def


async def __get_tabel_schedule(data):

    pass
# End def
