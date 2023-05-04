import customtkinter as tk
from tkinter import PhotoImage, Listbox
from PIL import Image

from database.database_applications import get_active_applications, get_full_active_applications, delete_applications, \
    sort, sort_by_services, sort_by_mechanics, sort_by_sum_more_or_less, sort_by_sum_between, \
    sort_by_date_before_or_after, sort_by_date_between


class InactiveApplications:

    def __init__(self, bg, fg, active_color, hover_color):
        self.root = tk.CTkToplevel()
        self.root.title('Inactive applications')
        self.root.geometry('420x365+800+450')
        self.root.resizable(False, False)
        self.root.iconphoto(False, PhotoImage(file='image/icon.png'))
        self.root.grab_set()

        self.bg = bg
        self.fg = fg
        self.active_color = active_color
        self.hover_color = hover_color

        search_image = tk.CTkImage(Image.open('image/search.png').resize((50, 50), Image.ANTIALIAS))
        delete_image = tk.CTkImage(Image.open('image/delete.png').resize((50, 50), Image.ANTIALIAS))
        information_image = tk.CTkImage(Image.open('image/information.png').resize((50, 50), Image.ANTIALIAS))

        frame = tk.CTkFrame(self.root, width=210, height=320, corner_radius=10)
        frame.place(x=5, y=5)

        scrollbar = tk.CTkScrollbar(frame, orientation='vertical')
        scrollbar_2 = tk.CTkScrollbar(frame, orientation='horizontal')

        scrollbar.pack(side='right', fill='y')
        scrollbar_2.pack(side='bottom', fill='both')

        self.applications_listbox = Listbox(frame, width=60, height=10, yscrollcommand=scrollbar.set,  # width was 60
                                            xscrollcommand=scrollbar_2.set, bg=bg, fg=fg,
                                            selectbackground=active_color, font=('Century Gothic', 18))  # font was 18

        self.applications_listbox.pack(side='left', fill='both')

        scrollbar.configure(command=self.applications_listbox.yview)
        scrollbar_2.configure(command=self.applications_listbox.xview)

        self.list_application = []
        self.active_application()

        filter_label = tk.CTkLabel(self.root, text='Фільтрувати за', font=('Century Gothic', 16))
        filter_label.place(x=10, y=220)

        self.filter_menu = tk.CTkOptionMenu(self.root, values=['', 'ім\'ям', 'прізвищем', 'по-батькові', 'телефоном',
                                                               'автомобілем', 'номер. авто', 'послугами', 'механіком',
                                                               'сумою', 'датою почат.', 'датою завер.'],
                                            dropdown_font=('Century Gothic', 14), width=125, height=28,
                                            font=('Century Gothic',
                                                  14), dropdown_hover_color=active_color)
        self.filter_menu.place(x=134, y=220)
        self.filter_menu.set("")

        self.information = tk.CTkEntry(self.root, border_width=2, width=135, font=('Century Gothic', 14))
        self.information.place(x=270, y=220)

        search_button = tk.CTkButton(self.root, text='Пошук', font=('Century Gothic', 16), image=search_image,
                                     compound='right', hover_color=hover_color, corner_radius=6, command=self.sort)
        search_button.place(x=50, y=270)

        delete_button = tk.CTkButton(self.root, text='Видалити', font=('Century Gothic', 16), image=delete_image,
                                     compound='right', hover_color=hover_color, corner_radius=6, command=self.delete)
        delete_button.place(x=135, y=320)

        information_button = tk.CTkButton(self.root, text='Інформація', font=('Century Gothic', 16),
                                          image=information_image, compound='right', hover_color=hover_color,
                                          corner_radius=6, command=self.full_application)
        information_button.place(x=220, y=270)

        self.root.mainloop()

    def active_application(self):
        self.list_application = get_active_applications('завершена')
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

        self.active_application()

    def sort(self):

        def result():
            for i in self.list_application:
                application = ' '.join(i.split()[1:]) + ' '
                self.applications_listbox.insert(tk.END, application)

        f = self.filter_menu.get()
        self.applications_listbox.delete(0, tk.END)
        if f == '':
            self.list_application = get_active_applications('завершена')
            result()
            return None

        inf = self.information.get()
        if inf == '':
            # mes.showerror('Помилка', 'Ви не ввели дані для пошуку.')
            pass
        elif f == 'ім\'ям':
            self.list_application = sort('name_client', inf, 'завершена')
            result()
        elif f == 'прізвищем':
            self.list_application = sort('surname_client', inf, 'завершена')
            result()
        elif f == 'по-батькові':
            self.list_application = sort('middle_name_client', inf, 'завершена')
            result()
        elif f == 'телефоном':
            self.list_application = sort('phone_client', inf, 'завершена')
            result()
        elif f == 'автомобілем':
            self.list_application = sort('car_client', inf, 'завершена')
            result()
        elif f == 'номер. авто':
            self.list_application = sort('number_of_the_car', inf, 'завершена')
            result()
        elif f == 'послугами':
            self.list_application = sort_by_services(inf, 'завершена')
            result()
        elif f == 'механіком':
            self.list_application = sort_by_mechanics(inf, 'завершена')
            result()
        elif f == 'сумою':
            if len(inf.split()) != 2:
                return None
            first, second = inf.split()

            if first == '>' or first == '<' or first == '=' or first == '<=' or first == '>=' or first == '<>' \
                    and second.isdigit():
                try:
                    list_ = sort_by_sum_more_or_less(first, int(second), 'завершена')
                except ValueError:
                    self.list_application = []
                    return None

                self.list_application = list_
                result()

            elif first.isdigit() and second.isdigit():
                try:
                    list_ = sort_by_sum_between(int(first), int(second), 'завершена')
                except ValueError:
                    self.list_application = []
                    return None

                self.list_application = list_
                result()
        elif f == 'датою почат.':
            if len(inf.split()) != 2:
                return None
            first, second = inf.split()

            if first == '>' or first == '<' or first == '=' or first == '<=' or first == '>=' or first == '<>':
                if len(second) == 10:
                    list_ = sort_by_date_before_or_after(first, second, 'завершена', 'date_start')
                    self.list_application = list_
                    result()

            elif len(second) == 10 and len(first) == 10:
                list_ = sort_by_date_between(first, second, 'завершена', 'date_start')
                self.list_application = list_
                result()
        elif f == 'датою завер.':
            if len(inf.split()) != 2:
                return None
            first, second = inf.split()

            if first == '>' or first == '<' or first == '=' or first == '<=' or first == '>=' or first == '<>':
                if len(second) == 10:
                    list_ = sort_by_date_before_or_after(first, second, 'завершена', 'date_end')
                    self.list_application = list_
                    result()

            elif len(second) == 10 and len(first) == 10:
                list_ = sort_by_date_between(first, second, 'завершена', 'date_end')
                self.list_application = list_
                result()
