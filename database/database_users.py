from database.database_main import base, cursor
from tkinter import messagebox as mes
import sys


def add_new_users(login, password):
    try:
        cursor.execute(f'INSERT INTO authorization (`login`, `password`) VALUES("{login}", "{password}")')
        base.commit()
        return True

    except Exception:
        mes.showerror('Помилка', "Користувач з таким логіном вже існує.")


def delete_users(login, password, user):
    sqlite_select_users = 'SELECT * FROM authorization'
    cursor.execute(sqlite_select_users)
    records = cursor.fetchall()
    amount = len(records)
    list_ = []
    for i in range(amount):
        list_.append(i)
    for i in list_:
        if records[i][0] == login and records[i][1] == password:
            if amount == 1:
                mes.showerror('Помилка',
                              '''Ви не можете видалити цього користувача, тому що це єдиний користувач який зареєстрований в БД. Додайте нового, та спробуйте ще раз.''')
                return True

            cursor.execute(f'DELETE FROM authorization WHERE login = "{login}"')
            base.commit()
            mes.showinfo('Повідомлення', f'Користувач {login} успішно видалений.')
            if records[i][0] == login and records[i][0] == user:
                sys.exit()
            return True
