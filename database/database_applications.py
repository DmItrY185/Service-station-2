from database.database_main import base, cursor
from tkinter import messagebox as mes

from datetime import date as d


def get_available_services():
    try:
        sqlite_select_available_services = f'SELECT `name_service_section` FROM service_sections ' \
                                           f'WHERE `status_service_section` = "активний"'
        cursor.execute(sqlite_select_available_services)
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
            sqlite_select = f'SELECT services.name_service, services.price_service, services.id_service FROM ' \
                            f'services INNER JOIN service_sections ON services.id_service_section = ' \
                            f'service_sections.id_service_section WHERE service_sections.name_service_section = "{i}"' \
                            f' AND services.status_service = "активна"'
            cursor.execute(sqlite_select)
            records = cursor.fetchall()

            if len(i) == max_length:
                finish_list.append('              ' + i.upper())
            else:
                middle_of_word = len(i) // 2
                finish_list.append('              ' + ' ' * (max_length // 2 - middle_of_word) + i.upper())
            finish_list.append('')

            inf = []
            for x in records:
                inf.append(f' {x[0]}  {x[1]} грн. {x[2]}')
            inf.sort()

            for information in inf:
                finish_list.append(information)
            finish_list.append('')

        return finish_list

    except Exception:
        return []


def get_active_mechanics():
    sqlite_select_active_mechanics = f'SELECT `surname_mechanic`, `name_mechanic`, `middle_name_mechanic`  ' \
                                     f'FROM mechanics WHERE `status_mechanic` = "активний"'
    cursor.execute(sqlite_select_active_mechanics)
    records = cursor.fetchall()
    list_active_mechanics = []

    for i in records:
        list_active_mechanics.append(f'{i[0]} {i[1][0]}. {i[2][0]}.')

    sorted_list_active_mechanics = sorted(list_active_mechanics)
    return sorted_list_active_mechanics


def add_application(surname, name, middle_name, phone, car, number_of_the_car, date, mechanic, sum, id_services):
    sqlite_select_id_mechanics = f'SELECT id_mechanic FROM mechanics WHERE surname_mechanic = "{mechanic}"'
    cursor.execute(sqlite_select_id_mechanics)
    records = cursor.fetchall()
    id_mechanic = records[0][0]

    cursor.execute(
        'INSERT INTO applications (`surname_client`, `name_client`, `middle_name_client`, `phone_client`, `car_client`, `number_of_the_car`, `date_start`, `id_mechanic`, `sum_application`) '
        f'VALUES ("{surname}", "{name}", "{middle_name}", "{phone}", "{car}", "{number_of_the_car}", "{date}", '
        f'"{id_mechanic}", "{sum}")')
    base.commit()

    sqlite_select_last_id_applications = f'SELECT id_application FROM applications ORDER BY id_application DESC LIMIT 1'
    cursor.execute(sqlite_select_last_id_applications)
    records = cursor.fetchall()
    id_application = records[0][0]

    for i in id_services:
        cursor.execute(f'INSERT INTO serv_applic (`id_application`, `id_service`) VALUES ("{id_application}", "{i}")')
        base.commit()

    mes.showinfo('Повідомлення', 'Заявка успішно додана.')


def get_active_applications(status):
    sqlite_select = f'SELECT `id_application`, `surname_client`, `name_client`, `middle_name_client`, `phone_client`, `car_client`, `date_start`  FROM applications WHERE `status_application` = "{status}"'
    cursor.execute(sqlite_select)
    records = cursor.fetchall()
    list_active_application = []
    for i in records:
        date = f"{str(i[6]).split('-')[2]}.{str(i[6]).split('-')[1]}.{str(i[6]).split('-')[0]}"
        list_active_application.append(
            f'{i[0]} ПІБ: {i[1]} {i[2]} {i[3]}   Телефон: {i[4]}   Автомобіль: {i[5]}   Дата початку: {date} ')

    return list_active_application


def get_full_active_applications(id):
    sqlite_select_mechanics = f'SELECT mechanics.surname_mechanic, mechanics.name_mechanic, mechanics.middle_name_mechanic  FROM mechanics ' \
                              f'INNER JOIN applications ON mechanics.id_mechanic = applications.id_mechanic ' \
                              f'WHERE applications.id_application = {id}'
    cursor.execute(sqlite_select_mechanics)
    records = cursor.fetchall()
    mechanic = ''
    for i in records:
        mechanic = f'{i[0]} {i[1]} {i[2]}'

    sqlite_select_id_services = f'SELECT id_service FROM serv_applic WHERE id_application = {id}'
    cursor.execute(sqlite_select_id_services)
    records = cursor.fetchall()
    services_index = []
    for index in records:
        for i in index:
            services_index.append(i)

    list_services = []
    for i in services_index:
        sqlite_select_services = f'SELECT services.name_service, services.price_service ' \
                                 f'FROM services WHERE id_service = {i}'
        cursor.execute(sqlite_select_services)
        records = cursor.fetchall()
        for i in records:
            list_services.append(
                f'{i[0]}  {i[1]} грн.   '
            )

    sqlite_select_applications = f'SELECT * FROM applications WHERE `id_application` = {id}'
    cursor.execute(sqlite_select_applications)
    records = cursor.fetchall()
    list_full_active_application = []
    for i in records:
        if i[11] == 'виконується':
            date = f"{str(i[7]).split('-')[2]}.{str(i[7]).split('-')[1]}.{str(i[7]).split('-')[0]}"
            list_full_active_application.append(
                f'ПІБ: {i[1]} {i[2]} {i[3]}\n\nТелефон: {i[4]}\n\nАвтомобіль: {i[5]}\n\nНомерний знак: {i[6]}\n\n'
                f'Дата початку: {date}\n\nМеханік: {mechanic}\n\nПослуги: {" ".join(list_services)}\n\nСума: {i[10]} грн. \n\nСтатус: {i[11]}')

        elif i[11] == 'завершена':
            date_start = f"{str(i[7]).split('-')[2]}.{str(i[7]).split('-')[1]}.{str(i[7]).split('-')[0]}"
            date_end = f"{str(i[8]).split('-')[2]}.{str(i[8]).split('-')[1]}.{str(i[8]).split('-')[0]}"
            list_full_active_application.append(
                f'ПІБ: {i[1]} {i[2]} {i[3]}\n\nТелефон: {i[4]}\n\nАвтомобіль: {i[5]}\n\nНомерний знак: {i[6]}\n\n'
                f'Дата початку: {date_start}\n\nДата завершення: {date_end}\n\nМеханік: {mechanic}\n\nПослуги: {" ".join(list_services)}\n\nСума: {i[10]} грн. \n\nСтатус: {i[11]}')

    mes.showinfo('Повідомлення', list_full_active_application[0])


def delete_applications(id):
    cursor.execute(f'DELETE FROM applications WHERE `id_application` = "{id}"')
    base.commit()

    mes.showinfo('Повідомлення', 'Заявка успішно видалена.')


def completion_applications(id):
    cursor.execute(f"UPDATE applications SET `status_application` = 'завершена', date_end = '{d.today()}' "
                   f"WHERE `id_application` = '{id}'")
    base.commit()

    mes.showinfo('Повідомлення', 'Заявка успішно завершена.')


def sort(pointer, information, status):
    sqlite_select = f'SELECT `id_application`, `surname_client`, `name_client`, `middle_name_client`, `phone_client`, ' \
                    f'`car_client`, `date_start`  FROM applications WHERE `status_application` = "{status}"' \
                    f'AND `{pointer}` LIKE "%{information}%" '
    cursor.execute(sqlite_select)
    records = cursor.fetchall()
    list_active_application = []
    for i in records:
        date = f"{str(i[6]).split('-')[2]}.{str(i[6]).split('-')[1]}.{str(i[6]).split('-')[0]}"
        list_active_application.append(
            f'{i[0]} ПІБ: {i[1]} {i[2]} {i[3]}   Телефон: {i[4]}   Автомобіль: {i[5]}   Дата початку: {date} ')

    return list_active_application


def sort_by_services(information, status):
    sqlite_select = f'SELECT id_application FROM kursova.serv_applic JOIN services ON ' \
                    f'serv_applic.id_service = services.id_service WHERE services.name_service LIKE "%{information}%"'
    cursor.execute(sqlite_select)
    records = cursor.fetchall()
    list_id_active_application = list({i[0] for i in records})
    list_active_application = []

    for id in list_id_active_application:
        sqlite_select = f'SELECT `id_application`, `surname_client`, `name_client`, `middle_name_client`, ' \
                        f'`phone_client`, `car_client`, `date_start`  FROM ' \
                        f'applications WHERE `status_application` = "{status}" AND id_application = "{id}"'
        cursor.execute(sqlite_select)
        records = cursor.fetchall()
        for i in records:
            date = f"{str(i[6]).split('-')[2]}.{str(i[6]).split('-')[1]}.{str(i[6]).split('-')[0]}"
            list_active_application.append(
                f'{i[0]} ПІБ: {i[1]} {i[2]} {i[3]}   Телефон: {i[4]}   Автомобіль: {i[5]}   Дата початку: {date} ')

    return list_active_application


def sort_by_mechanics(information, status):
    sqlite_select = f'SELECT applications.id_application FROM kursova.applications JOIN mechanics ON ' \
                    f'applications.id_mechanic = mechanics.id_mechanic WHERE mechanics.name_mechanic LIKE "%{information}%" ' \
                    f'OR mechanics.surname_mechanic LIKE "%{information}%" OR mechanics.middle_name_mechanic LIKE "%{information}%"'
    cursor.execute(sqlite_select)
    records = cursor.fetchall()
    list_id_active_application = [i[0] for i in records]
    list_active_application = []

    for id in list_id_active_application:
        sqlite_select = f'SELECT `id_application`, `surname_client`, `name_client`, `middle_name_client`, ' \
                        f'`phone_client`, `car_client`, `date_start`  FROM ' \
                        f'applications WHERE `status_application` = "{status}" AND id_application = "{id}"'
        cursor.execute(sqlite_select)
        records = cursor.fetchall()
        for i in records:
            date = f"{str(i[6]).split('-')[2]}.{str(i[6]).split('-')[1]}.{str(i[6]).split('-')[0]}"
            list_active_application.append(
                f'{i[0]} ПІБ: {i[1]} {i[2]} {i[3]}   Телефон: {i[4]}   Автомобіль: {i[5]}   Дата початку: {date} ')
    return list_active_application


def sort_by_sum_more_or_less(pointer, sum, status):
    sqlite_select = f'SELECT `id_application`, `surname_client`, `name_client`, `middle_name_client`, `phone_client`, ' \
                    f'`car_client`, `date_start`  FROM applications ' \
                    f'WHERE `sum_application` {pointer} {sum} AND `status_application` = "{status}"'
    cursor.execute(sqlite_select)
    records = cursor.fetchall()
    list_active_application = []
    for i in records:
        date = f"{str(i[6]).split('-')[2]}.{str(i[6]).split('-')[1]}.{str(i[6]).split('-')[0]}"
        list_active_application.append(
            f'{i[0]} ПІБ: {i[1]} {i[2]} {i[3]}   Телефон: {i[4]}   Автомобіль: {i[5]}   Дата початку: {date} ')

    return list_active_application


def sort_by_sum_between(first_number, second_number, status):
    sqlite_select = f'SELECT `id_application`, `surname_client`, `name_client`, `middle_name_client`, ' \
                    f'`phone_client`, `car_client`, `date_start`  FROM applications ' \
                    f'WHERE `sum_application` > {first_number} AND `sum_application` < {second_number} ' \
                    f'AND `status_application` = "{status}";'
    cursor.execute(sqlite_select)
    records = cursor.fetchall()
    list_active_application = []
    for i in records:
        date = f"{str(i[6]).split('-')[2]}.{str(i[6]).split('-')[1]}.{str(i[6]).split('-')[0]}"
        list_active_application.append(
            f'{i[0]} ПІБ: {i[1]} {i[2]} {i[3]}   Телефон: {i[4]}   Автомобіль: {i[5]}   Дата початку: {date} ')

    return list_active_application


def sort_by_date_before_or_after(pointer, date_, status, pointer_date):
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

    except:
        return []
    sqlite_select = f'SELECT `id_application`, `surname_client`, `name_client`, `middle_name_client`, `phone_client`, ' \
                    f'`car_client`, `date_start`  FROM applications ' \
                    f'WHERE `{pointer_date}` {pointer} "{date}" AND `status_application` = "{status}"'
    cursor.execute(sqlite_select)
    records = cursor.fetchall()
    list_active_application = []
    for i in records:
        date = f"{str(i[6]).split('-')[2]}.{str(i[6]).split('-')[1]}.{str(i[6]).split('-')[0]}"
        list_active_application.append(
            f'{i[0]} ПІБ: {i[1]} {i[2]} {i[3]}   Телефон: {i[4]}   Автомобіль: {i[5]}   Дата початку: {date} ')

    return list_active_application


def sort_by_date_between(first_date, second_date, status, pointer_date):
    try:
        date_1 = f'{first_date.split(".")[2]}.{first_date.split(".")[1]}.{first_date.split(".")[0]}'
        date_2 = f'{second_date.split(".")[2]}.{second_date.split(".")[1]}.{second_date.split(".")[0]}'

        year_1, month_1, number_1 = date_1.split('.')
        if len(year_1) != 4 or len(month_1) != 2 or len(number_1) != 2:
            return []
        for i in [year_1, month_1, number_1]:
            for x in i:
                if x not in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                    return []
        if int(month_1) < 1 or int(month_1) > 12 or int(number_1) < 1 or int(number_1) > 31:
            return []

        year_2, month_2, number_2 = date_2.split('.')
        if len(year_2) != 4 or len(month_2) != 2 or len(number_2) != 2:
            return []
        for i in [year_2, month_2, number_2]:
            for x in i:
                if x not in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                    return []
        if int(month_2) < 1 or int(month_2) > 12 or int(number_2) < 1 or int(number_2) > 31:
            return []
    except:
        return []
    sqlite_select = f'SELECT `id_application`, `surname_client`, `name_client`, `middle_name_client`, `phone_client`, '\
                    f'`car_client`, `date_start`  FROM applications ' \
                    f'WHERE `{pointer_date}` BETWEEN "{date_1}" AND "{date_2}" AND `status_application` = "{status}";'
    cursor.execute(sqlite_select)
    records = cursor.fetchall()
    list_active_application = []
    for i in records:
        date = f"{str(i[6]).split('-')[2]}.{str(i[6]).split('-')[1]}.{str(i[6]).split('-')[0]}"
        list_active_application.append(
            f'{i[0]} ПІБ: {i[1]} {i[2]} {i[3]}   Телефон: {i[4]}   Автомобіль: {i[5]}   Дата початку: {date} ')

    return list_active_application


def chose_application(id):
    sqlite_select_mechanics = f'SELECT mechanics.surname_mechanic, mechanics.name_mechanic, ' \
                              f'mechanics.middle_name_mechanic  FROM mechanics ' \
                              f'INNER JOIN applications ON mechanics.id_mechanic = applications.id_mechanic ' \
                              f'WHERE applications.id_application = {id}'
    cursor.execute(sqlite_select_mechanics)
    records = cursor.fetchall()
    mechanic = ''
    for i in records:
        mechanic = f'{i[0]} {i[1][0]}. {i[2][0]}.'

    sqlite_select_id_services = f'SELECT id_service FROM serv_applic WHERE id_application = {id}'
    cursor.execute(sqlite_select_id_services)
    records = cursor.fetchall()
    services_index = []
    for index in records:
        for i in index:
            services_index.append(i)

    list_services = []
    for i in services_index:
        sqlite_select_services = f'SELECT services.name_service, services.price_service FROM ' \
                                 f'services WHERE id_service = {i}'
        cursor.execute(sqlite_select_services)
        records = cursor.fetchall()
        for i in records:
            list_services.append(
                f'{i[0]} {i[1]} грн. '
            )

    sqlite_select_applications = f'SELECT * FROM applications WHERE `id_application` = {id}'
    cursor.execute(sqlite_select_applications)
    records = cursor.fetchall()
    list_full_application = []

    for i in records:
        full_name = f'{i[1]} {i[2]} {i[3]}'
        phone = i[4]
        car = i[5]
        number_of_the_car = i[6]
        date = f"{str(i[7]).split('-')[2]}.{str(i[7]).split('-')[1]}.{str(i[7]).split('-')[0]}"
        sum_ = int(i[10])
        list_full_application = [full_name, phone, car, number_of_the_car, date, sum_, mechanic, list_services,
                                 services_index]

    return list_full_application


def change_application(id, surname, name, middle_name, phone, car, number_of_the_car, date, mechanic, sum, id_services):
    cursor.execute(f'DELETE FROM serv_applic WHERE `id_application` = "{id}"')
    base.commit()

    sqlite_select_id_mechanics = f'SELECT id_mechanic FROM mechanics WHERE surname_mechanic = "{mechanic}"'
    cursor.execute(sqlite_select_id_mechanics)
    records = cursor.fetchall()
    id_mechanic = records[0][0]

    for i in id_services:
        cursor.execute(f'INSERT INTO serv_applic (`id_application`, `id_service`) VALUES ("{id}", "{i}")')
        base.commit()

    cursor.execute(
        f'UPDATE applications SET `surname_client` = "{surname}",`name_client` = "{name}",'
        f'`middle_name_client` = "{middle_name}",'
        f'`phone_client` = "{phone}",`date_start` = "{date}", `car_client` = "{car}", '
        f'`number_of_the_car` = "{number_of_the_car}", '
        f'sum_application = "{sum}", `id_mechanic` = "{id_mechanic}"  WHERE `id_application` = "{id}"')
    base.commit()

    mes.showinfo('Повідомлення', 'Дані успішно змінено.')
