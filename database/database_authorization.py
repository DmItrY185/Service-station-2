from database.database_main import cursor
import window_main

user = ''


def authorization(login, password):
    global user
    sqlite_select_users = 'SELECT * FROM authorization'
    cursor.execute(sqlite_select_users)
    records = cursor.fetchall()
    amount = len(records)
    list_ = []
    for i in range(amount):
        list_.append(i)
    for i in list_:
        if records[i][0] == login and records[i][1] == password:
            user = records[i][0]
            list_.clear()
            return True


def start_main(color_mode):
    window_main.WindowMain(color_mode, user)
