with open('database/config.txt') as file:
    data = file.readlines()
    data_list = []
    for i in data:
        data_list.append(i.split('= ')[1][:-1])
    host, user, password, db_name = data_list
