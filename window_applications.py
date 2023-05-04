import customtkinter as tk
from tkinter import PhotoImage, Listbox
from PIL import Image
from tkinter import messagebox as mes

from database.database_applications import get_available_services, get_active_mechanics, add_application, \
    get_active_applications, get_full_active_applications, delete_applications, completion_applications, sort, \
    sort_by_services, sort_by_mechanics, sort_by_sum_more_or_less, sort_by_sum_between, sort_by_date_before_or_after, \
    sort_by_date_between, chose_application, change_application


class Applications:

    def __init__(self, bg, fg, active_color, hover_color, function):
        self.root = tk.CTkToplevel()
        self.root.title('Applications')
        self.root.geometry('935x465+300+350')
        self.root.resizable(False, False)
        self.root.iconphoto(False, PhotoImage(file='image/icon.png'))
        self.root.grab_set()

        self.bg = bg
        self.fg = fg
        self.active_color = active_color
        self.hover_color = hover_color

        self.last_chose_application_id = ''

        self.update_applications_listbox_main_window = function

        search_image = tk.CTkImage(Image.open('image/search.png').resize((50, 50), Image.ANTIALIAS))
        add_image = tk.CTkImage(Image.open('image/add_service_sections.png').resize((50, 50), Image.ANTIALIAS))
        delete_image = tk.CTkImage(Image.open('image/delete.png').resize((50, 50), Image.ANTIALIAS))
        choose_image = tk.CTkImage(Image.open('image/choose.png').resize((50, 50), Image.ANTIALIAS))
        change_image = tk.CTkImage(Image.open('image/change.png').resize((50, 50), Image.ANTIALIAS))
        change_status_image = tk.CTkImage(Image.open('image/change_status.png').resize((50, 50), Image.ANTIALIAS))
        information_image = tk.CTkImage(Image.open('image/information.png').resize((50, 50), Image.ANTIALIAS))

        frame = tk.CTkFrame(self.root, width=210, height=320, corner_radius=10)
        frame.place(x=5, y=5)

        scrollbar = tk.CTkScrollbar(frame, orientation='vertical')
        scrollbar_2 = tk.CTkScrollbar(frame, orientation='horizontal')

        scrollbar.pack(side='right', fill='y')
        scrollbar_2.pack(side='bottom', fill='both')

        self.applications_listbox = Listbox(frame, width=60, height=15, yscrollcommand=scrollbar.set,
                                            xscrollcommand=scrollbar_2.set, bg=bg, fg=fg,
                                            selectbackground=active_color, font=('Century Gothic', 18))

        self.applications_listbox.pack(side='left', fill='both')

        scrollbar.configure(command=self.applications_listbox.yview)
        scrollbar_2.configure(command=self.applications_listbox.xview)

        self.list_application = []
        self.active_application()

        filter_label = tk.CTkLabel(self.root, text='Фільтрувати за', font=('Century Gothic', 16))
        filter_label.place(x=10, y=270)

        self.filter_menu = tk.CTkOptionMenu(self.root, values=['', 'ім\'ям', 'прізвищем', 'по-батькові', 'телефоном',
                                                               'автомобілем', 'номер. авто', 'послугами', 'механіком',
                                                               'сумою', 'датою'],
                                            dropdown_font=('Century Gothic', 14), width=125, height=28,
                                            font=('Century Gothic',
                                                  14), dropdown_hover_color=active_color)
        self.filter_menu.place(x=134, y=270)
        self.filter_menu.set("")

        self.information = tk.CTkEntry(self.root, border_width=2, width=135, font=('Century Gothic', 14))
        self.information.place(x=270, y=270)

        search_button = tk.CTkButton(self.root, text='Пошук', font=('Century Gothic', 16), image=search_image,
                                     compound='right', hover_color=hover_color, corner_radius=6, command=self.sort)
        search_button.place(x=50, y=320)

        delete_button = tk.CTkButton(self.root, text='Видалити', font=('Century Gothic', 16), image=delete_image,
                                     compound='right', hover_color=hover_color, corner_radius=6, command=self.delete)
        delete_button.place(x=220, y=320)

        information_button = tk.CTkButton(self.root, text='Інформація', font=('Century Gothic', 16),
                                          image=information_image, compound='right', hover_color=hover_color,
                                          corner_radius=6, command=self.full_application)
        information_button.place(x=50, y=370)

        change_status_button = tk.CTkButton(self.root, text='Завершити', font=('Century Gothic', 16),
                                            image=change_status_image, compound='right', hover_color=hover_color,
                                            corner_radius=6, command=self.completion)
        change_status_button.place(x=220, y=370)

        choose_button = tk.CTkButton(self.root, text='Обрати', font=('Century Gothic', 16), image=choose_image,
                                     compound='right', hover_color=hover_color, corner_radius=6, command=self.chose)
        choose_button.place(x=135, y=420)

        # Available services
        frame_available_services = tk.CTkFrame(self.root, width=110, height=220, corner_radius=10)
        frame_available_services.place(x=440, y=5)

        scrollbar_available_services = tk.CTkScrollbar(frame_available_services, orientation='vertical')
        scrollbar_2_available_services = tk.CTkScrollbar(frame_available_services, orientation='horizontal')

        scrollbar_available_services.pack(side='right', fill='y')
        scrollbar_2_available_services.pack(side='bottom', fill='both')

        self.available_services_listbox = Listbox(frame_available_services, width=31, height=10,
                                                  yscrollcommand=scrollbar_available_services.set,
                                                  xscrollcommand=scrollbar_2_available_services.set, bg=bg, fg=fg,
                                                  selectbackground=active_color,
                                                  font=('Century Gothic', 18))

        self.available_services_listbox.pack(side='left', fill='both')

        scrollbar_available_services.configure(command=self.available_services_listbox.yview)
        scrollbar_2_available_services.configure(command=self.available_services_listbox.xview)

        self.available_services = get_available_services()[:-1]
        for i in self.available_services:
            if i.strip().isupper() or i == '':
                self.available_services_listbox.insert(tk.END, i)
            else:
                service = ' '.join(i.split()[:-1]) + ' '
                self.available_services_listbox.insert(tk.END, service)

        # Selected services
        frame_selected_services = tk.CTkFrame(self.root, width=110, height=220, corner_radius=10)
        frame_selected_services.place(x=710, y=5)

        scrollbar_selected_services = tk.CTkScrollbar(frame_selected_services, orientation='vertical')
        scrollbar_2_selected_services = tk.CTkScrollbar(frame_selected_services, orientation='horizontal')

        scrollbar_selected_services.pack(side='right', fill='y')
        scrollbar_2_selected_services.pack(side='bottom', fill='both')

        self.selected_services_listbox = Listbox(frame_selected_services, width=31, height=10,
                                                 yscrollcommand=scrollbar_selected_services.set,
                                                 xscrollcommand=scrollbar_2_selected_services.set, bg=bg, fg=fg,
                                                 selectbackground=active_color,
                                                 font=('Century Gothic', 18))

        self.selected_services_listbox.pack(side='left', fill='both')

        self.list_selected_services_index = []

        scrollbar_selected_services.configure(command=self.selected_services_listbox.yview)
        scrollbar_2_selected_services.configure(command=self.selected_services_listbox.xview)

        button_add_services = tk.CTkButton(self.root, text=' > ', width=1, font=('Century Gothic', 12),
                                           hover_color=hover_color,
                                           corner_radius=6, command=self.select_services)
        button_add_services.place(x=672, y=60)

        button_minus_services = tk.CTkButton(self.root, text=' < ', width=1, font=('Century Gothic', 12),
                                             hover_color=hover_color,
                                             corner_radius=6, command=self.unselect_services)
        button_minus_services.place(x=672, y=120)

        self.mechanic_menu = tk.CTkOptionMenu(self.root, values=get_active_mechanics(),
                                              dropdown_font=('Century Gothic', 14), width=125, height=28,
                                              font=('Century Gothic', 14), dropdown_hover_color=active_color)
        self.mechanic_menu.place(x=490, y=220, anchor='nw')
        self.mechanic_menu.set("Механік")

        self.sum = tk.CTkEntry(self.root, border_width=2, width=70, font=('Century Gothic', 14), placeholder_text='sum')
        self.sum.place(x=780, y=220, anchor='nw')
        self.sum.configure(state=tk.DISABLED)
        self.sum_int = 0

        self.name = tk.CTkEntry(self.root, border_width=2, width=300, font=('Century Gothic', 14),
                                placeholder_text='full name')
        self.name.place(x=530, y=270)

        self.car = tk.CTkEntry(self.root, border_width=2, width=200, font=('Century Gothic', 14),
                               placeholder_text='car')
        self.car.place(x=450, y=320)

        self.number_of_the_car = tk.CTkEntry(self.root, border_width=2, width=160, font=('Century Gothic', 14),
                                             placeholder_text='number of the car')
        self.number_of_the_car.place(x=740, y=320)

        self.phone = tk.CTkEntry(self.root, border_width=2, width=160, font=('Century Gothic', 14),
                                 placeholder_text='phone')
        self.phone.place(x=470, y=370)

        self.date = tk.CTkEntry(self.root, border_width=2, width=160, font=('Century Gothic', 14),
                                placeholder_text='date')
        self.date.place(x=740, y=370)

        self.add_button = tk.CTkButton(self.root, text='Додати', font=('Century Gothic', 16), image=add_image,
                                       compound='right', hover_color=hover_color, corner_radius=6, command=self.add)
        self.add_button.place(x=480, y=420)

        change_button = tk.CTkButton(self.root, text='Змінити', font=('Century Gothic', 16), image=change_image,
                                     compound='right', hover_color=hover_color, corner_radius=6, command=self.change)
        change_button.place(x=750, y=420)

        self.root.mainloop()

    def check_before_adding_changing(self):
        sum_ = self.sum_int
        name_ = self.name.get()
        mechanic_ = self.mechanic_menu.get()
        car = self.car.get()
        number_of_the_car = self.number_of_the_car.get()
        phone = self.phone.get()
        date = self.date.get()
        all_data = [name_, car, number_of_the_car, phone, date]
        if sum_ == 0:
            mes.showerror('Помилка', 'Ви не обрали послугу.')
            return None
        elif mechanic_ == 'Механік':
            mes.showerror('Помилка', 'Ви не обрали механіка.')
            return None
        elif '' in all_data:
            mes.showerror('Помилка', 'Ви ввели не всі дані.')
            return None
        elif len(name_.split()) != 3:
            mes.showerror('Помилка', 'Ви неправильно ввели ПІБ.')
            return None
        elif len(phone) != 10 or not phone.isdigit():
            mes.showerror('Помилка', 'Ви неправильно ввели номер телефону.')
            return None
        elif len(date.split('.')) != 3:
            mes.showerror('Помилка', 'Ви неправильно ввели дату.')
            return None
        for x in date.split('.'):
            if not x.isdigit():
                mes.showerror('Помилка', 'Ви неправильно ввели дату.')
                return None
        if len(date.split('.')[0]) != 2:
            mes.showerror('Помилка', 'Ви неправильно ввели число.')
            return None
        elif int(date.split('.')[0]) > 31 or int(date.split('.')[0]) == 0:
            mes.showerror('Помилка', 'Ви неправильно ввели число.')
            return None
        elif len(date.split('.')[1]) != 2:
            mes.showerror('Помилка', 'Ви неправильно ввели місяць.')
            return None
        elif int(date.split('.')[1]) > 12 or int(date.split('.')[1]) == 0:
            mes.showerror('Помилка', 'Ви неправильно ввели місяць.')
            return None
        elif len(date.split('.')[2]) != 4:
            mes.showerror('Помилка', 'Ви неправильно ввели рік.')
            return None
        elif int(date.split('.')[2]) < 1950:
            mes.showerror('Помилка', 'Ви неправильно ввели рік.')
            return None

        list_services_id = self.list_selected_services_index

        surname, name, middle_name = name_.split()
        mechanic = mechanic_.split()[0]

        return surname, name, middle_name, phone, car, number_of_the_car, date, mechanic, sum_, list_services_id

    def select_services(self):
        try:
            index = self.available_services_listbox.curselection()[0]
        except IndexError:
            return None

        if self.available_services[index] == '' or self.available_services[index].strip().isupper():
            return None

        id_services = int(self.available_services[index].split()[-1])
        if id_services not in self.list_selected_services_index:
            self.selected_services_listbox.insert(tk.END, ' '.join(self.available_services[index].split()[:-1]) + ' ')
            self.list_selected_services_index.append(id_services)

            self.sum_int += int(self.available_services[index].split()[-3])
            self.sum.configure(state=tk.NORMAL)
            self.sum.delete(0, tk.END)
            self.sum.insert(0, self.sum_int)
            self.sum.configure(state=tk.DISABLED)

    def unselect_services(self):
        try:
            index = self.selected_services_listbox.curselection()[0]
        except IndexError:
            return None

        self.sum_int -= int(self.selected_services_listbox.get(index).split()[-2])
        self.sum.configure(state=tk.NORMAL)
        self.sum.delete(0, tk.END)
        self.sum.insert(0, self.sum_int)
        self.sum.configure(state=tk.DISABLED)

        self.list_selected_services_index.pop(index)
        self.selected_services_listbox.delete(index)

    def add(self):
        try:
            surname, name, middle_name, phone, car, number_of_the_car, date, mechanic, sum_, list_services_id = \
                self.check_before_adding_changing()
        except TypeError:
            return None

        add_application(surname, name, middle_name, phone, car, number_of_the_car,
                        f'{date.split(".")[2]}.{date.split(".")[1]}.{date.split(".")[0]}', mechanic, sum_,
                        list_services_id)

        self.mechanic_menu.set('Механік')

        self.sum.configure(state=tk.NORMAL)
        self.sum.delete(0, tk.END)
        self.sum.configure(placeholder_text='sum')
        self.sum.configure(state=tk.DISABLED)
        self.sum_int = 0

        self.name.delete(0, tk.END)
        self.car.delete(0, tk.END)
        self.number_of_the_car.delete(0, tk.END)
        self.phone.delete(0, tk.END)
        self.date.delete(0, tk.END)
        self.selected_services_listbox.delete(0, tk.END)
        self.list_selected_services_index = []

        self.active_application()
        self.update_applications_listbox_main_window()

    def active_application(self):
        self.list_application = get_active_applications('виконується')
        self.applications_listbox.delete(0, tk.END)
        for i in self.list_application:
            application = ' '.join(i.split()[1:]) + ' '
            self.applications_listbox.insert(tk.END, application)

    def full_application(self):
        try:
            index_application_in_listbox = self.applications_listbox.curselection()[0]
        except IndexError:
            return None
        index_application = self.list_application[index_application_in_listbox].split()[0]
        get_full_active_applications(index_application)

    def delete(self):
        try:
            index_application_in_listbox = self.applications_listbox.curselection()[0]
        except IndexError:
            return None
        index_application = self.list_application[index_application_in_listbox].split()[0]
        delete_applications(index_application)

        if self.last_chose_application_id == index_application:
            self.last_chose_application_id = 'deleted'

        self.active_application()
        self.update_applications_listbox_main_window()

    def completion(self):
        try:
            index_application_in_listbox = self.applications_listbox.curselection()[0]
        except IndexError:
            return None
        index_application = self.list_application[index_application_in_listbox].split()[0]
        completion_applications(index_application)

        if self.last_chose_application_id == index_application:
            self.last_chose_application_id = 'completed'

        self.active_application()
        self.update_applications_listbox_main_window()

    def sort(self):

        def result():
            for i in self.list_application:
                application = ' '.join(i.split()[1:]) + ' '
                self.applications_listbox.insert(tk.END, application)

        f = self.filter_menu.get()
        self.applications_listbox.delete(0, tk.END)
        if f == '':
            self.list_application = get_active_applications('виконується')
            result()
            return None

        inf = self.information.get()
        if inf == '':
            pass
        elif f == 'ім\'ям':
            self.list_application = sort('name_client', inf, 'виконується')
            result()
        elif f == 'прізвищем':
            self.list_application = sort('surname_client', inf, 'виконується')
            result()
        elif f == 'по-батькові':
            self.list_application = sort('middle_name_client', inf, 'виконується')
            result()
        elif f == 'телефоном':
            self.list_application = sort('phone_client', inf, 'виконується')
            result()
        elif f == 'автомобілем':
            self.list_application = sort('car_client', inf, 'виконується')
            result()
        elif f == 'номер. авто':
            self.list_application = sort('number_of_the_car', inf, 'виконується')
            result()
        elif f == 'послугами':
            self.list_application = sort_by_services(inf, 'виконується')
            result()
        elif f == 'механіком':
            self.list_application = sort_by_mechanics(inf, 'виконується')
            result()
        elif f == 'сумою':
            if len(inf.split()) != 2:
                return None
            first, second = inf.split()

            if first == '>' or first == '<' or first == '=' or first == '<=' or first == '>=' or first == '<>' \
                    and second.isdigit():
                try:
                    list_ = sort_by_sum_more_or_less(first, int(second), 'виконується')
                except ValueError:
                    self.list_application = []
                    return None
                
                self.list_application = list_
                result()

            elif first.isdigit() and second.isdigit():
                try:
                    list_ = sort_by_sum_between(int(first), int(second), 'виконується')
                except ValueError:
                    self.list_application = []
                    return None

                self.list_application = list_
                result()
        elif f == 'датою':
            if len(inf.split()) != 2:
                return None
            first, second = inf.split()

            if first == '>' or first == '<' or first == '=' or first == '<=' or first == '>=' or first == '<>':
                if len(second) == 10:
                    list_ = sort_by_date_before_or_after(first, second, 'виконується', 'date_start')
                    self.list_application = list_
                    result()

            elif len(second) == 10 and len(first) == 10:
                list_ = sort_by_date_between(first, second, 'виконується', 'date_start')
                self.list_application = list_
                result()

    def chose(self):
        try:
            index_application_in_listbox = self.applications_listbox.curselection()[0]
        except IndexError:
            return None
        index_application = self.list_application[index_application_in_listbox].split()[0]
        self.last_chose_application_id = index_application

        full_name, phone, car, number_of_the_car, date, sum_, mechanic, list_services, \
            services_index = chose_application(index_application)

        self.name.delete(0, tk.END)
        self.phone.delete(0, tk.END)
        self.car.delete(0, tk.END)
        self.number_of_the_car.delete(0, tk.END)
        self.date.delete(0, tk.END)

        self.name.insert(0, full_name)
        self.phone.insert(0, phone)
        self.car.insert(0, car)
        self.number_of_the_car.insert(0, number_of_the_car)
        self.date.insert(0, date)

        self.sum_int = sum_
        self.sum.configure(state=tk.NORMAL)
        self.sum.delete(0, tk.END)
        self.sum.insert(0, self.sum_int)
        self.sum.configure(state=tk.DISABLED)

        self.mechanic_menu.set(mechanic)

        self.list_selected_services_index = services_index

        self.selected_services_listbox.delete(0, tk.END)
        for i in list_services:
            self.selected_services_listbox.insert(tk.END, i)

        self.add_button.configure(state=tk.DISABLED)

    def change(self):

        def clearing_the_fields():
            self.mechanic_menu.set('Механік')

            self.sum.configure(state=tk.NORMAL)
            self.sum.delete(0, tk.END)
            self.sum.configure(placeholder_text='sum')
            self.sum.configure(state=tk.DISABLED)
            self.sum_int = 0

            self.name.delete(0, tk.END)
            self.car.delete(0, tk.END)
            self.number_of_the_car.delete(0, tk.END)
            self.phone.delete(0, tk.END)
            self.date.delete(0, tk.END)
            self.selected_services_listbox.delete(0, tk.END)
            self.list_selected_services_index = []

            self.add_button.configure(state=tk.NORMAL)

        if self.last_chose_application_id == '':
            return None

        if self.last_chose_application_id == 'deleted':
            mes.showerror('Помилка', 'Ви видалили цю заявку.')
            self.last_chose_application_id = ''
            clearing_the_fields()
            return None

        if self.last_chose_application_id == 'completed':
            mes.showerror('Помилка', 'Ви завершили цю заявку.')
            self.last_chose_application_id = ''
            clearing_the_fields()
            return None

        try:
            surname, name, middle_name, phone, car, number_of_the_car, date, mechanic, sum_, list_services_id = \
                self.check_before_adding_changing()
        except TypeError:
            return None

        change_application(self.last_chose_application_id, surname, name, middle_name, phone, car, number_of_the_car,
                           f'{date.split(".")[2]}.{date.split(".")[1]}.{date.split(".")[0]}', mechanic, sum_,
                           list_services_id)

        self.active_application()
        self.update_applications_listbox_main_window()

        self.last_chose_application_id = ''

        clearing_the_fields()
