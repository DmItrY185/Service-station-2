from database.database_main import base, cursor
from tkinter import messagebox as mes


def add_services(name, sum_, fk):
    try:
        sqlite_select_id_service_sections = f'SELECT `id_service_section` FROM ' \
                                            f'service_sections WHERE name_service_section = "{fk}"'
        cursor.execute(sqlite_select_id_service_sections)
        records = cursor.fetchall()
        fk = records[0][0]
    except IndexError:
        return 0

    try:
        cursor.execute(
            f'INSERT INTO services (`name_service`, `price_service`, `id_service_section`) '
            f'VALUES ("{name}", "{sum_}", "{fk}")')
        base.commit()
        return True

    except Exception:
        mes.showerror('Помилка', "Послуга з такою назвою вже існує.")


def get_services():
    try:
        sqlite_select_services = f'SELECT services.name_service, services.price_service, ' \
                                 f'service_sections.name_service_section, ' \
                                 f'services.status_service FROM ' \
                                 f'services INNER JOIN service_sections ON ' \
                                 f'services.id_service_section = service_sections.id_service_section'
        cursor.execute(sqlite_select_services)

        records = cursor.fetchall()
        list_services = list(map(list, records))

        return get(list_services)

    except Exception:
        return []


def delete_services(name):
    try:
        cursor.execute(f'DELETE FROM services WHERE name_service = "{name}"')
        base.commit()
        return True

    except Exception:
        return False


def change_status(name):
    sqlite_select_status = f'SELECT `status_service` FROM services WHERE name_service = "{name}" '
    cursor.execute(sqlite_select_status)
    records = cursor.fetchall()
    if records[0][0] == 'активна':
        cursor.execute(f"UPDATE services SET `status_service` = 'неактивна' WHERE `name_service` = '{name}'")
        base.commit()
    if records[0][0] == 'неактивна':
        cursor.execute(f"UPDATE services SET `status_service` = 'активна' WHERE `name_service` = '{name}'")
        base.commit()


def change(name, previous_name, sum_, fk):
    sqlite_select_id = f'SELECT `id_service_section` FROM service_sections WHERE name_service_section = "{fk}"'
    cursor.execute(sqlite_select_id)
    records = cursor.fetchall()
    fk = records[0][0]
    try:
        cursor.execute(
            f'UPDATE services SET `name_service` = "{name}", `price_service` = {sum_}, `id_service_section` = {fk} '
            f'WHERE `name_service` = "{previous_name}"')
        base.commit()
        return True

    except Exception:
        mes.showerror('Помилка', "Послуга з такою назвою вже існує.")


def sort_by_name(name):
    try:
        sqlite_select_services_by_name = f'SELECT services.name_service, services.price_service, ' \
                                         f'service_sections.name_service_section, ' \
                                         f'services.status_service FROM ' \
                                         f'services INNER JOIN service_sections ON services.id_service_section = ' \
                                         f'service_sections.id_service_section WHERE services.name_service ' \
                                         f'LIKE "%{name}%"'
        cursor.execute(sqlite_select_services_by_name)
        records = cursor.fetchall()
        list_services = list(map(list, records))

        return get(list_services)

    except Exception:
        return []


def sort_by_price_more_or_less(pointer, price):
    try:
        sqlite_select_services_by_price_more = f'SELECT services.name_service, services.price_service, ' \
                                               f'service_sections.name_service_section, ' \
                                               f'services.status_service FROM ' \
                                               f'services INNER JOIN service_sections ' \
                                               f'ON services.id_service_section = ' \
                                               f'service_sections.id_service_section ' \
                                               f'WHERE services.price_service {pointer} {price};'
        cursor.execute(sqlite_select_services_by_price_more)
        records = cursor.fetchall()
        list_services = list(map(list, records))

        return get(list_services)

    except Exception:
        return []


def sort_by_price_between(price_1, price_2):
    try:
        sqlite_select_services_by_price_between = f'SELECT services.name_service, services.price_service, ' \
                                                  f'service_sections.name_service_section, ' \
                                                  f'services.status_service FROM ' \
                                                  f'services INNER JOIN service_sections ' \
                                                  f'ON services.id_service_section = ' \
                                                  f'service_sections.id_service_section WHERE services.price_service ' \
                                                  f'> {price_1} AND services.price_service < {price_2};'
        cursor.execute(sqlite_select_services_by_price_between)
        records = cursor.fetchall()
        list_services = list(map(list, records))

        return get(list_services)

    except Exception:
        return []


def sort_by_service_section(service_section):
    try:
        sqlite_select_services_by_service_sections = f'SELECT services.name_service, services.price_service, ' \
                                                     f'service_sections.name_service_section, services.status_service '\
                                                     f'FROM ' \
                                                     f'services INNER JOIN service_sections ' \
                                                     f'ON services.id_service_section = ' \
                                                     f'service_sections.id_service_section WHERE ' \
                                                     f'service_sections.name_service_section LIKE "%{service_section}%";'
        cursor.execute(sqlite_select_services_by_service_sections)
        records = cursor.fetchall()
        list_services = list(map(list, records))

        return get(list_services)

    except Exception:
        return []


def get(list_services):
    try:
        sqlite_select_inactive_services = f'SELECT `name_service_section` FROM service_sections WHERE ' \
                                          f'`status_service_section` = "неактивний"'
        cursor.execute(sqlite_select_inactive_services)
        records = cursor.fetchall()
        list_service_sections = [i[0] for i in records]

        for i in list_services:
            if i[2] in list_service_sections:
                i[3] = '*неактивна*'

        sorted_list_services = sorted(list_services, key=lambda x: x[0])
        return sorted_list_services

    except Exception:
        return []


def get_active_service_sections():
    try:
        sqlite_select_active_services = f'SELECT `name_service_section` FROM service_sections WHERE ' \
                                        f'`status_service_section` = "активний" '
        cursor.execute(sqlite_select_active_services)
        records = cursor.fetchall()
        list_service_sections = []
        for i in records:
            list_service_sections.append(i[0])
        return list_service_sections

    except Exception:
        return []


def get_services_for_main_window():
    try:
        sqlite_select_active_service_sections = f'SELECT `name_service_section` FROM service_sections ' \
                                                f'WHERE `status_service_section` = "активний"'
        cursor.execute(sqlite_select_active_service_sections)
        records = cursor.fetchall()
        list_service_sections = []
        for i in records:
            list_service_sections.append(i[0])

        list_service_sections.sort()

        finish_list = []

        max_length = 0
        for i in list_service_sections:
            if len(i) > max_length:
                max_length = len(i)

        for i in list_service_sections:
            sqlite_select_services = f'SELECT services.name_service, services.price_service FROM ' \
                                     f'services INNER JOIN service_sections ON services.id_service_section = ' \
                                     f'service_sections.id_service_section WHERE ' \
                                     f'service_sections.name_service_section = "{i}"' \
                                     f' AND services.status_service = "активна"'
            cursor.execute(sqlite_select_services)
            records = cursor.fetchall()

            if len(i) == max_length:
                finish_list.append('                ' + i.upper())
            else:
                middle_of_word = len(i) // 2
                finish_list.append('                ' + ' ' * (max_length // 2 - middle_of_word) + i.upper())
            finish_list.append('')

            inf = []
            for x in records:
                inf.append(f' {x[0]}  {x[1]} грн.')
            inf.sort()

            for information in inf:
                finish_list.append(information)
            finish_list.append('')

        return finish_list

    except Exception:
        return []


def check_before_changing(name):
    cursor.execute(f'SELECT id_service FROM services WHERE name_service = "{name}"')
    records = cursor.fetchall()
    id = records[0][0]

    cursor.execute(f'SELECT EXISTS(SELECT * FROM serv_applic WHERE id_service = "{id}")')
    records = cursor.fetchall()

    if records[0][0] == 0:
        return True
    elif records[0][0] == 1:
        return False
