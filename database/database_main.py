import pymysql
from database.database_config import host, db_name, user, password

import customtkinter as tk
import sys

try:
    base = pymysql.connect(
        host=host,
        port=3306,
        user=user,
        password=password,
        database=db_name
    )
    cursor = base.cursor()

    # ------------------створюємо БД------------------
    # cursor.execute('CREATE DATABASE IF NOT EXISTS kursova')
    # base.commit()

    print('successfully connected')

    # # ------------------створюємо таблицю авторизації------------------
    # create_table_query = 'CREATE TABLE IF NOT EXISTS {}' \
    #                      '(`login` VARCHAR(50) PRIMARY KEY, ' \
    #                      '`password` VARCHAR(50));'.format('authorization')
    #
    # cursor.execute(create_table_query)
    # base.commit()
    # print('table created successfully')

    # # ------------------створюємо таблицю розділів послуг------------------
    # create_table_query = 'CREATE TABLE IF NOT EXISTS {}' \
    #                      '(`id_service_section` INT PRIMARY KEY AUTO_INCREMENT, ' \
    #                      '`name_service_section` VARCHAR(64) UNIQUE KEY,' \
    #                      '`status_service_section` VARCHAR(10) DEFAULT "активний");'.format('service_sections')
    #
    # cursor.execute(create_table_query)
    # base.commit()
    # print('table created successfully')
    #
    # # ------------------створюємо таблицю послуг------------------
    # create_table_query = 'CREATE TABLE IF NOT EXISTS {}' \
    #                      '(`id_service` INT PRIMARY KEY AUTO_INCREMENT, ' \
    #                      '`name_service` VARCHAR(768) UNIQUE KEY, ' \
    #                      '`price_service` INT,' \
    #                      '`id_service_section` INT,' \
    #                      'FOREIGN KEY(id_service_section) REFERENCES service_sections(id_service_section) ' \
    #                      'ON DELETE RESTRICT,' \
    #                      '`status_service` VARCHAR(9) DEFAULT "активна");'\
    #     .format('services')
    #
    # cursor.execute(create_table_query)
    # base.commit()
    # print('table created successfully')
    #
    # # ------------------створюємо таблицю механіків------------------
    # create_table_query = 'CREATE TABLE IF NOT EXISTS {}' \
    #                      '(`id_mechanic` INT PRIMARY KEY AUTO_INCREMENT, ' \
    #                      '`surname_mechanic` VARCHAR(50) UNIQUE KEY, ' \
    #                      '`name_mechanic` VARCHAR(50), ' \
    #                      '`middle_name_mechanic` VARCHAR(50), ' \
    #                      '`phone_mechanic` VARCHAR(10) UNIQUE KEY,' \
    #                      '`date_from_which_works` DATE,' \
    #                      '`status_mechanic` VARCHAR(10) DEFAULT "активний");'.format('mechanics')
    #
    # cursor.execute(create_table_query)
    # base.commit()
    # print('table created successfully')
    #
    # # ------------------створюємо таблицю заявок------------------
    # create_table_query = 'CREATE TABLE IF NOT EXISTS {}' \
    #                      '(`id_application` INT PRIMARY KEY AUTO_INCREMENT, ' \
    #                      '`surname_client` VARCHAR(50), ' \
    #                      '`name_client` VARCHAR(50), ' \
    #                      '`middle_name_client` VARCHAR(50), ' \
    #                      '`phone_client` VARCHAR(10),' \
    #                      '`car_client` VARCHAR(100),' \
    #                      '`number_of_the_car` VARCHAR(20),' \
    #                      '`date_start` DATE,' \
    #                      '`date_end` DATE,' \
    #                      '`id_mechanic` INT,' \
    #                      '`sum_application` INT,' \
    #                      '`status_application` VARCHAR(11) DEFAULT "виконується",' \
    #                      'FOREIGN KEY(id_mechanic) REFERENCES mechanics(id_mechanic) ON DELETE RESTRICT);'\
    #     .format('applications')
    #
    # cursor.execute(create_table_query)
    # base.commit()
    # print('table created successfully')
    #
    # # ------------------створюємо таблицю посередник(заявки - послуги)------------------
    # create_table_query = 'CREATE TABLE IF NOT EXISTS {}' \
    #                      '(`id_application` INT , ' \
    #                      '`id_service` INT,' \
    #                      'FOREIGN KEY(id_application) REFERENCES applications(id_application) ON DELETE CASCADE,' \
    #                      'FOREIGN KEY(id_service) REFERENCES services(id_service) ' \
    #                      'ON DELETE RESTRICT);'.format('serv_applic')
    #
    # cursor.execute(create_table_query)
    # base.commit()
    # print('table created successfully')

except Exception as ex:
    root = tk.CTk()
    root.title('Помилка')
    root.geometry('300x100+800+500')
    root.resizable(False, False)
    label = tk.CTkLabel(root, text='Невдалося підключитися до БД', font=('Century Gothic', 18))
    label.place(relx=.5, rely=.5, anchor='center')
    root.mainloop()

    sys.exit()
    # print('connection refused')
    # print(ex)
