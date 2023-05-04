from database.database_main import base, cursor
from tkinter import messagebox as mes


def result(records):
    list_mechanics = []
    for i in records:
        date = f"{str(i[5]).split('-')[2]}.{str(i[5]).split('-')[1]}.{str(i[5]).split('-')[0]}"
        list_mechanics.append(
            f'ПІБ: {i[1]} {i[2]} {i[3]}   Телефон: {i[4]}   Дата з якої працює: {date}   Статус: {i[6]} ')

    sorted_list_mechanics = sorted(list_mechanics)
    return sorted_list_mechanics


def add_mechanics(surname, name, middle_name, phone, date):
    try:
        cursor.execute('INSERT INTO mechanics (`surname_mechanic`, `name_mechanic`,`middle_name_mechanic`,'
                       '`phone_mechanic`,`date_from_which_works`) '
                       f'VALUES ("{surname}", "{name}", "{middle_name}", "{phone}", "{date}")')
        base.commit()
        return True

    except Exception:
        mes.showerror('Помилка', "Механік з такими даними вже існує.")


def get_mechanics():
    try:
        sqlite_select_mechanics = f'SELECT * FROM mechanics'
        cursor.execute(sqlite_select_mechanics)
        records = cursor.fetchall()
        return result(records)

    except Exception:
        return []


def delete_mechanics(phone):
    try:
        cursor.execute(f'DELETE FROM mechanics WHERE `phone_mechanic` = "{phone}"')
        base.commit()
        return True

    except Exception:
        return False


def sort(pointer, information):
    try:
        sqlite_select_mechanics_by_status = f'SELECT * FROM mechanics WHERE `{pointer}` LIKE "%{information}%" '
        cursor.execute(sqlite_select_mechanics_by_status)
        records = cursor.fetchall()

        return result(records)

    except Exception:
        return []


def sort_by_date_before_or_after(pointer, date_):
    try:
        date = f'{date_.split(".")[2]}.{date_.split(".")[1]}.{date_.split(".")[0]}'

        year, month, number = date.split('.')
        if len(year) != 4 or len(month) != 2 or len(number) != 2:
            return []
        for i in [year, month, number]:
            for x in i:
                if x not in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                    return []
        if int(month) < 1 or int(month) > 12 or int(number) < 1 or int(number) > 31:
            return []
    except Exception:
        return []
    sqlite_select_mechanics_by_date_before = f'SELECT * FROM mechanics WHERE `date_from_which_works` {pointer} "{date}" '
    cursor.execute(sqlite_select_mechanics_by_date_before)
    records = cursor.fetchall()

    return result(records)


def sort_by_date_between(date_1, date_2):
    try:
        date1 = f'{date_1.split(".")[2]}.{date_1.split(".")[1]}.{date_1.split(".")[0]}'
        date2 = f'{date_2.split(".")[2]}.{date_2.split(".")[1]}.{date_2.split(".")[0]}'

        year_1, month_1, number_1 = date1.split('.')
        if len(year_1) != 4 or len(month_1) != 2 or len(number_1) != 2:
            return []
        for i in [year_1, month_1, number_1]:
            for x in i:
                if x not in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                    return []
        if int(month_1) < 1 or int(month_1) > 12 or int(number_1) < 1 or int(number_1) > 31:
            return []

        year_2, month_2, number_2 = date2.split('.')
        if len(year_2) != 4 or len(month_2) != 2 or len(number_2) != 2:
            return []
        for i in [year_2, month_2, number_2]:
            for x in i:
                if x not in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                    return []
        if int(month_2) < 1 or int(month_2) > 12 or int(number_2) < 1 or int(number_2) > 31:
            return []
    except Exception:
        return []
    sqlite_select_mechanics_by_date_between = f'SELECT * FROM mechanics WHERE `date_from_which_works` ' \
                                              f'BETWEEN "{date1}" AND "{date2}"'
    cursor.execute(sqlite_select_mechanics_by_date_between)
    records = cursor.fetchall()

    return result(records)


def change_status(phone):
    sqlite_select_mechanics_status = f'SELECT status_mechanic FROM mechanics WHERE `phone_mechanic` = "{phone}" '
    cursor.execute(sqlite_select_mechanics_status)
    records = cursor.fetchall()
    if records[0][0] == 'активний':
        cursor.execute(f"UPDATE mechanics SET `status_mechanic` = 'неактивний' WHERE `phone_mechanic` = '{phone}'")
        base.commit()
    if records[0][0] == 'неактивний':
        cursor.execute(f"UPDATE mechanics SET `status_mechanic` = 'активний' WHERE `phone_mechanic` = '{phone}'")
        base.commit()


def change(surname, name, middle_name, phone, date, previous_phone):
    try:
        cursor.execute(
            f'UPDATE mechanics SET `surname_mechanic` = "{surname}",`name_mechanic` = "{name}",'
            f'`middle_name_mechanic` = "{middle_name}",'
            f'`phone_mechanic` = "{phone}",`date_from_which_works` = "{date}" '
            f'WHERE `phone_mechanic` = "{previous_phone}"')
        base.commit()
        return True

    except Exception:
        mes.showerror('Помилка', "Механік з такими даними вже існує.")
