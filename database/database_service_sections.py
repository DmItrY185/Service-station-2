from database.database_main import base, cursor
from tkinter import messagebox as mes


def add_service_sections(name):
    try:
        cursor.execute(f'INSERT INTO service_sections (`name_service_section`) VALUES ("{name}")')
        base.commit()
        return True

    except Exception:
        mes.showerror('Помилка', "Розділ послуг з такою назвою вже існує.")


def get_service_sections():
    try:
        sqlite_select_service_sections = f'SELECT `name_service_section`, `status_service_section` FROM service_sections'
        cursor.execute(sqlite_select_service_sections)
        records = cursor.fetchall()
        list_service_sections = list(map(list, records))

        sorted_list_services_sections = sorted(list_service_sections, key=lambda x: x[0])
        return sorted_list_services_sections

    except Exception:
        return []


def delete_service_sections(name):
    try:
        cursor.execute(f'DELETE FROM service_sections WHERE `name_service_section` = "{name}"')
        base.commit()
        return True

    except Exception:
        return False


def change_status(name):
    sqlite_change_status_service_sections = f'SELECT status_service_section FROM service_sections ' \
                                            f'WHERE `name_service_section` = "{name}" '
    cursor.execute(sqlite_change_status_service_sections)
    records = cursor.fetchall()
    if records[0][0] == 'активний':
        cursor.execute(f"UPDATE service_sections SET `status_service_section` = 'неактивний' "
                       f"WHERE `name_service_section` = '{name}'")
        base.commit()
    if records[0][0] == 'неактивний':
        cursor.execute(f"UPDATE service_sections SET `status_service_section` = 'активний' "
                       f"WHERE `name_service_section` = '{name}'")
        base.commit()


def change(name, previous_name):
    try:
        cursor.execute(
            f'UPDATE service_sections SET `name_service_section` = "{name}" WHERE '
            f'`name_service_section` = "{previous_name}"')
        base.commit()
        return True

    except Exception:
        mes.showerror('Помилка', "Розділ послуг з такою назвою вже існує.")


def sort(pointer, information):
    try:
        sqlite_select_service_sections_by_name = f'SELECT `name_service_section`, `status_service_section` ' \
                                                 f'FROM service_sections WHERE `{pointer}` ' \
                                                 f'LIKE "%{information}%" '
        cursor.execute(sqlite_select_service_sections_by_name)
        records = cursor.fetchall()
        list_service_sections = list(map(list, records))

        sorted_list_services_sections = sorted(list_service_sections, key=lambda x: x[0])
        return sorted_list_services_sections

    except Exception:
        return []


# def sort_by_name(name):
#     try:
#         sqlite_select_users = f'SELECT * FROM service_sections WHERE name LIKE "%{name}%" '
#         cursor.execute(sqlite_select_users)
#         records = cursor.fetchall()
#         list_mechanics = []
#         for i in records:
#             list_mechanics.append(
#                 f'Назва: {i[1]}  Статус: {i[2]} ')
#         return list_mechanics
#     except Exception:
#         return []
#
#
# def sort_by_status(status):
#     try:
#         sqlite_select_users = f'SELECT * FROM service_sections WHERE status LIKE "%{status}%" '
#         cursor.execute(sqlite_select_users)
#         records = cursor.fetchall()
#         list_mechanics = []
#         for i in records:
#             list_mechanics.append(
#                 f'Назва: {i[1]}  Статус: {i[2]} ')
#         return list_mechanics
#     except Exception:
#         return []


# def get_service_sections():
#     try:
#         sqlite_select_users = f'SELECT * FROM service_sections'
#         cursor.execute(sqlite_select_users)
#         records = cursor.fetchall()
#         list_mechanics = []
#         for i in records:
#             list_mechanics.append(
#                 f'Назва: {i[1]}  Статус: {i[2]} ')
#         return list_mechanics
#     except Exception:
#         return []
