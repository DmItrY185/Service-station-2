import customtkinter as tk
from tkinter import PhotoImage, Listbox
from PIL import Image
from tkinter import messagebox as mes

from database.database_services import get_services, add_services, change_status, \
    delete_services, sort_by_name, sort_by_price_between, change, sort_by_price_more_or_less, \
    get_active_service_sections, sort_by_service_section, check_before_changing


class Services:
    def __init__(self, bg, fg, active_color, hover_color, function):
        self.root = tk.CTkToplevel()
        self.root.title('Services')
        self.root.geometry('420x545+800+250')
        self.root.resizable(False, False)
        self.root.iconphoto(False, PhotoImage(file='image/icon.png'))
        self.root.grab_set()

        self.update_services_listbox_main_window = function

        self.bg = bg
        self.fg = fg
        self.active_color = active_color
        self.hover_color = hover_color

        self.last_change_name = ' '

        search_image = tk.CTkImage(Image.open('image/search.png').resize((50, 50), Image.ANTIALIAS))
        add_image = tk.CTkImage(Image.open('image/add_service_sections.png').resize((50, 50), Image.ANTIALIAS))
        delete_image = tk.CTkImage(Image.open('image/delete.png').resize((50, 50), Image.ANTIALIAS))
        choose_image = tk.CTkImage(Image.open('image/choose.png').resize((50, 50), Image.ANTIALIAS))
        change_image = tk.CTkImage(Image.open('image/change.png').resize((50, 50), Image.ANTIALIAS))
        change_status_image = tk.CTkImage(Image.open('image/change_status.png').resize((50, 50), Image.ANTIALIAS))

        frame = tk.CTkFrame(self.root, width=210, height=320, corner_radius=10)
        frame.place(x=5, y=5)

        scrollbar = tk.CTkScrollbar(frame, orientation='vertical')
        scrollbar_2 = tk.CTkScrollbar(frame, orientation='horizontal')

        scrollbar.pack(side='right', fill='y')
        scrollbar_2.pack(side='bottom', fill='both')

        self.services_listbox = Listbox(frame, width=60, height=10, yscrollcommand=scrollbar.set,
                                        xscrollcommand=scrollbar_2.set, bg=bg, fg=fg,
                                        selectbackground=active_color,
                                        font=('Century Gothic', 18))

        self.services_listbox.pack(side='left', fill='both')

        scrollbar.configure(command=self.services_listbox.yview)
        scrollbar_2.configure(command=self.services_listbox.xview)

        self.list_services = get_services()
        if not self.list_services:
            pass
        else:
            for i in self.list_services:
                self.services_listbox.insert(tk.END, f'Назва: {i[0]}  Ціна: {i[1]}  Розділ: {i[2]}  Статус: {i[3]} ')

        filter_label = tk.CTkLabel(self.root, text='Фільтрувати за', font=('Century Gothic', 16))
        filter_label.place(x=10, y=220)

        self.filter_menu = tk.CTkOptionMenu(self.root,
                                            values=['', 'назвою', 'розділом', 'ціною', 'статусом'],
                                            dropdown_font=('Century Gothic', 14), width=125, height=28,
                                            font=('Century Gothic', 14), dropdown_hover_color=active_color)
        self.filter_menu.place(x=131, y=220, anchor='nw')
        self.filter_menu.set("")

        self.information = tk.CTkEntry(self.root, border_width=2, width=135, font=('Century Gothic', 14))
        self.information.place(x=270, y=220, anchor='nw')

        search_button = tk.CTkButton(self.root, text='Пошук', font=('Century Gothic', 16), image=search_image,
                                     compound='right', hover_color=hover_color, corner_radius=6, command=self.sort)
        search_button.place(x=50, y=270)

        delete_button = tk.CTkButton(self.root, text='Видалити', font=('Century Gothic', 16), image=delete_image,
                                     compound='right', hover_color=hover_color, corner_radius=6, command=self.delete)
        delete_button.place(x=220, y=270)

        choose_button = tk.CTkButton(self.root, text='Обрати', font=('Century Gothic', 16), image=choose_image,
                                     compound='right', hover_color=hover_color, corner_radius=6, command=self.choose)
        choose_button.place(x=50, y=320)

        change_status_button = tk.CTkButton(self.root, text='Змінити ст.', font=('Century Gothic', 16),
                                            image=change_status_image,
                                            compound='right', hover_color=hover_color, corner_radius=6,
                                            command=self.change_status)
        change_status_button.place(x=220, y=320)

        add_label = tk.CTkLabel(self.root, text='Додавання/зміна даних', font=('Century Gothic', 18))
        add_label.place(relx=.5, y=390, anchor='center')

        self.name = tk.CTkEntry(self.root, border_width=2, width=300, font=('Century Gothic', 14),
                                placeholder_text='name')
        self.name.place(relx=.5, y=430, anchor='center')

        self.price = tk.CTkEntry(self.root, border_width=2, width=160, font=('Century Gothic', 14),
                                 placeholder_text='price')
        self.price.place(relx=.25, y=470, anchor='center')

        self.service_sections_menu = tk.CTkOptionMenu(self.root,
                                                      values=sorted(get_active_service_sections()),
                                                      dropdown_font=('Century Gothic', 14), width=125, height=28,
                                                      font=('Century Gothic', 14), dropdown_hover_color=active_color)
        self.service_sections_menu.place(relx=.75, y=470, anchor='center')
        self.service_sections_menu.set('Розділ')

        add_button = tk.CTkButton(self.root, text='Додати', font=('Century Gothic', 16), image=add_image,
                                  compound='right', hover_color=hover_color, corner_radius=6, command=self.add)
        add_button.place(x=50, y=500)

        self.change_button = tk.CTkButton(self.root, text='Змінити', font=('Century Gothic', 16), image=change_image,
                                          compound='right', hover_color=hover_color, corner_radius=6,
                                          command=self.change)
        self.change_button.place(x=220, y=500)

        self.root.mainloop()

    def add(self):
        name = self.name.get()
        pk = self.service_sections_menu.get()
        if '' in [name, self.price.get()]:
            mes.showerror('Помилка', 'Ви ввели не всі дані.')
            return None
        try:
            price = int(self.price.get())
        except ValueError:
            mes.showerror('Помилка', 'Ви неправильно ввели ціну.')
            return None

        if price == 0:
            mes.showerror('Помилка', 'Ви неправильно ввели ціну.')
            return None
        if pk == 'Розділ':
            mes.showerror('Помилка', 'Ви не обрали розділ.')
            return None
        if name.strip() == '':
            mes.showerror('Помилка', 'Ви не ввели назву послуги.')
        else:
            if add_services(name, price, pk):
                mes.showinfo('Повідомлення', 'Послуга успішно додана.')
                list_services = get_services()
                self.list_services = list_services

                self.services_listbox.delete(0, tk.END)
                for i in list_services:
                    self.services_listbox.insert(tk.END,
                                                 f'Назва: {i[0]}  Ціна: {i[1]}  Розділ: {i[2]}  Статус: {i[3]} ')

                self.price.configure(state=tk.NORMAL)
                self.name.delete(0, tk.END)
                self.price.delete(0, tk.END)
                self.update_services_listbox_main_window()

                self.last_change_name = ' '

    def change_status(self):
        index = [x for x in self.services_listbox.curselection()]
        if not index:
            return None

        if self.list_services[index[0]][-1] == '*неактивна*':
            mes.showerror('Помилка', 'Ви не можете зараз змінити статус цієї послуги.')
            return None

        name = self.list_services[index[0]][0]

        change_status(name)
        list_services = get_services()
        self.list_services = list_services
        self.services_listbox.delete(0, tk.END)
        for i in list_services:
            self.services_listbox.insert(tk.END, f'Назва: {i[0]}  Ціна: {i[1]}  Розділ: {i[2]}  Статус: {i[3]} ')
        self.update_services_listbox_main_window()

    def delete(self):
        index = [x for x in self.services_listbox.curselection()]
        if not index:
            return None
        name = self.list_services[index[0]][0]
        if delete_services(name):
            mes.showinfo('Повідомлення', 'Послуга успішно видалена.')
            self.services_listbox.delete(0, tk.END)
            list_services = get_services()
            self.list_services = list_services
            if not list_services:
                pass
            else:
                for i in list_services:
                    self.services_listbox.insert(tk.END,
                                                 f'Назва: {i[0]}  Ціна: {i[1]}  Розділ: {i[2]}  Статус: {i[3]} ')

            self.update_services_listbox_main_window()

            if name == self.last_change_name:
                self.last_change_name = ''
        else:
            mes.showerror('Помилка', 'Ви не можете видалити цю послугу, так як є заяки за якими вона закріплена.')

    def sort(self):

        def result():
            for x in self.list_services:
                self.services_listbox.insert(tk.END,
                                             f'Назва: {x[0]}  Ціна: {x[1]}  Розділ: {x[2]}  Статус: {x[3]} ')

        f = self.filter_menu.get()
        self.services_listbox.delete(0, tk.END)
        if f == '':
            self.list_services = get_services()
            result()
            return None

        inf = self.information.get()
        if inf == '':
            pass
        elif f == 'назвою':
            self.list_services = sort_by_name(inf)
            result()

        elif f == 'статусом':
            list_services = get_services()
            list_services_2 = []
            for i in list_services:
                if inf in i[-1]:
                    list_services_2.append(i)
            self.list_services = list_services_2
            result()

        elif f == 'ціною':
            if len(inf.split()) != 2:
                return None
            first, second = inf.split()

            if first == '>' or first == '<' or first == '=' or first == '<=' or first == '>=' or first == '<>' \
                    and second.isdigit():
                try:
                    list_ = sort_by_price_more_or_less(first, int(second))
                except ValueError:
                    self.list_services = []
                    return None

                self.list_services = list_
                result()

            elif first.isdigit() and second.isdigit():
                try:
                    list_ = sort_by_price_between(int(first), int(second))
                except ValueError:
                    self.list_services = []
                    return None

                self.list_services = list_
                result()

        elif f == 'розділом':
            self.list_services = sort_by_service_section(inf)
            result()

    def choose(self):
        index = [x for x in self.services_listbox.curselection()]
        if not index:
            return None

        if self.list_services[index[0]][-1] == '*неактивна*':
            mes.showerror('Помилка', 'Ви не можете зараз змінити цю послугу.')
            return None

        name = self.list_services[index[0]][0]
        price = self.list_services[index[0]][1]
        service_sections = self.list_services[index[0]][2]

        self.price.configure(state=tk.NORMAL)

        self.name.delete(0, tk.END)
        self.price.delete(0, tk.END)

        self.name.insert(0, name)
        self.price.insert(0, price)
        self.service_sections_menu.set(service_sections)
        self.last_change_name = name

        if check_before_changing(name) is False:
            self.price.configure(state=tk.DISABLED)

    def change(self):
        if self.last_change_name == '':
            mes.showerror('Помилка', 'Ви видалили цю послугу.')
            self.price.configure(state=tk.NORMAL)
            self.name.delete(0, tk.END)
            self.price.delete(0, tk.END)
            self.last_change_name = ' '
        elif self.last_change_name == ' ':
            pass

        else:
            name = self.name.get()
            service_sections = self.service_sections_menu.get()
            if '' in [name, self.price.get()]:
                mes.showerror('Помилка', 'Ви ввели не всі дані.')
                return None
            try:
                price = int(self.price.get())
            except ValueError:
                mes.showerror('Помилка', 'Ви неправильно ввели ціну.')
                return None

            if price == 0:
                mes.showerror('Помилка', 'Ви неправильно ввели ціну.')
                return None

            if name.strip() == '':
                mes.showerror('Помилка', 'Ви не ввели назву послуги.')
            elif change(name, self.last_change_name, price, service_sections):
                mes.showinfo('Повідомлення', 'Дані успішно змінено.')
                self.services_listbox.delete(0, tk.END)
                list_services = get_services()
                self.list_services = list_services
                for i in list_services:
                    self.services_listbox.insert(tk.END,
                                                 f'Назва: {i[0]}  Ціна: {i[1]}  Розділ: {i[2]}  Статус: {i[3]} ')

                self.price.configure(state=tk.NORMAL)

                self.name.delete(0, tk.END)
                self.price.delete(0, tk.END)

                self.last_change_name = ' '

                self.update_services_listbox_main_window()
