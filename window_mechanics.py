import customtkinter as tk
from tkinter import PhotoImage, Listbox
from PIL import Image
from tkinter import messagebox as mes

from database.database_mechanics import add_mechanics, get_mechanics, sort_by_date_between, \
    delete_mechanics, change_status, change, sort_by_date_before_or_after, sort


class Mechanics:
    def __init__(self, bg, fg, active_color, hover_color):
        self.root = tk.CTkToplevel()
        self.root.title('Mechanics')
        self.root.geometry('420x545+800+250')
        self.root.resizable(False, False)
        self.root.iconphoto(False, PhotoImage(file='image/icon.png'))
        self.root.grab_set()

        self.bg = bg
        self.fg = fg
        self.active_color = active_color
        self.hover_color = hover_color

        self.last_change_phone = ' '

        search_image = tk.CTkImage(Image.open('image/search.png').resize((50, 50), Image.ANTIALIAS))
        add_image = tk.CTkImage(Image.open('image/add.png').resize((50, 50), Image.ANTIALIAS))
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

        self.mechanics_listbox = Listbox(frame, width=60, height=10, yscrollcommand=scrollbar.set,  # width was 60
                                         xscrollcommand=scrollbar_2.set, bg=bg, fg=fg,
                                         selectbackground=active_color, font=('Century Gothic', 18))  # font was 18

        self.mechanics_listbox.pack(side='left', fill='both')

        scrollbar.configure(command=self.mechanics_listbox.yview)
        scrollbar_2.configure(command=self.mechanics_listbox.xview)

        list_mechanics = get_mechanics()
        if not list_mechanics:
            pass
        else:
            for i in list_mechanics:
                self.mechanics_listbox.insert(tk.END, i)

        filter_label = tk.CTkLabel(self.root, text='Фільтрувати за', font=('Century Gothic', 16))
        filter_label.place(x=10, y=220)

        self.filter_menu = tk.CTkOptionMenu(self.root,
                                            values=['', 'ім\'ям', 'прізвищем', 'по-батькові', 'телефоном', 'датою',
                                                    'статусом'],
                                            dropdown_font=('Century Gothic', 14), width=125, height=28,
                                            font=('Century Gothic', 14), dropdown_hover_color=active_color)
        self.filter_menu.place(x=135, y=220, anchor='nw')
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
                                placeholder_text='full name')
        self.name.place(relx=.5, y=430, anchor='center')

        self.phone = tk.CTkEntry(self.root, border_width=2, width=160, font=('Century Gothic', 14),
                                 placeholder_text='phone')
        self.phone.place(relx=.25, y=470, anchor='center')

        self.date = tk.CTkEntry(self.root, border_width=2, width=160, font=('Century Gothic', 14),
                                placeholder_text='date')
        self.date.place(relx=.75, y=470, anchor='center')

        add_button = tk.CTkButton(self.root, text='Додати', font=('Century Gothic', 16), image=add_image,
                                  compound='right', hover_color=hover_color, corner_radius=6, command=self.add)
        add_button.place(x=50, y=500)

        change_button = tk.CTkButton(self.root, text='Змінити', font=('Century Gothic', 16), image=change_image,
                                     compound='right', hover_color=hover_color, corner_radius=6,
                                     command=self.change)
        change_button.place(x=220, y=500)
        self.root.mainloop()

    def check_before_adding_changing(self):
        n = self.name.get()
        p = self.phone.get()
        d = self.date.get()
        all_data = [n, p, d]
        if '' in all_data:
            mes.showerror('Помилка', 'Ви ввели не всі дані.')
            return None
        elif len(n.split()) != 3:
            mes.showerror('Помилка', 'Ви неправильно ввели ПІБ.')
            return None
        elif len(p) != 10 or not p.isdigit():
            mes.showerror('Помилка', 'Ви неправильно ввели номер телефону.')
            return None
        elif len(d.split('.')) != 3:
            mes.showerror('Помилка', 'Ви неправильно ввели дату.')
            return None
        for x in d.split('.'):
            if not x.isdigit():
                mes.showerror('Помилка', 'Ви неправильно ввели дату.')
                return None
        if len(d.split('.')[0]) != 2:
            mes.showerror('Помилка', 'Ви неправильно ввели число.')
            return None
        elif int(d.split('.')[0]) > 31 or int(d.split('.')[0]) == 0:
            mes.showerror('Помилка', 'Ви неправильно ввели число.')
            return None
        elif len(d.split('.')[1]) != 2:
            mes.showerror('Помилка', 'Ви неправильно ввели місяць.')
            return None
        elif int(d.split('.')[1]) > 12 or int(d.split('.')[1]) == 0:
            mes.showerror('Помилка', 'Ви неправильно ввели місяць.')
            return None
        elif len(d.split('.')[2]) != 4:
            mes.showerror('Помилка', 'Ви неправильно ввели рік.')
            return None
        elif int(d.split('.')[2]) < 1950:
            mes.showerror('Помилка', 'Ви неправильно ввели рік.')
            return None
        return n, p, d

    def add(self):
        try:
            n, p, d = self.check_before_adding_changing()

        except TypeError:
            return None
        if add_mechanics(n.split()[0], n.split()[1], n.split()[2], p,
                         f'{d.split(".")[2]}.{d.split(".")[1]}.{d.split(".")[0]}'):
            mes.showinfo('Повідомлення', 'Механік успішно доданий.')
            self.mechanics_listbox.delete(0, tk.END)
            for x in get_mechanics():
                self.mechanics_listbox.insert(tk.END, x)
            self.name.delete(0, tk.END)
            self.phone.delete(0, tk.END)
            self.date.delete(0, tk.END)

            self.last_change_phone = ' '

    def change(self):
        if self.last_change_phone == '':
            mes.showerror('Помилка', 'Ви видалили цього механіка.')
            self.name.delete(0, tk.END)
            self.phone.delete(0, tk.END)
            self.date.delete(0, tk.END)
            self.last_change_phone = ' '
        elif self.last_change_phone == ' ':
            pass

        else:
            try:
                n, p, d = self.check_before_adding_changing()
            except TypeError:
                return None
            if change(n.split()[0], n.split()[1], n.split()[2], p,
                      f'{d.split(".")[2]}.{d.split(".")[1]}.{d.split(".")[0]}', self.last_change_phone):
                mes.showinfo('Повідомлення', 'Дані успішно змінено.')
                self.mechanics_listbox.delete(0, tk.END)
                for x in get_mechanics():
                    self.mechanics_listbox.insert(tk.END, x)
                self.name.delete(0, tk.END)
                self.phone.delete(0, tk.END)
                self.date.delete(0, tk.END)
                self.last_change_phone = ' '

    def sort(self):
        f = self.filter_menu.get()
        self.mechanics_listbox.delete(0, tk.END)
        if f == '':
            list_mechanics = get_mechanics()
            if not list_mechanics:
                pass
            else:
                for x in list_mechanics:
                    self.mechanics_listbox.insert(tk.END, x)
            return None
        inf = self.information.get()
        if inf == '':
            # mes.showerror('Помилка', 'Ви не ввели дані для пошуку.')
            pass
        elif f == 'ім\'ям':
            list_mechanics = sort('name_mechanic', inf)
            if not list_mechanics:
                pass
            else:
                for x in list_mechanics:
                    self.mechanics_listbox.insert(tk.END, x)
        elif f == 'прізвищем':
            list_mechanics = sort('surname_mechanic', inf)
            if not list_mechanics:
                pass
            else:
                for x in list_mechanics:
                    self.mechanics_listbox.insert(tk.END, x)
        elif f == 'по-батькові':
            list_mechanics = sort('middle_name_mechanic', inf)
            if not list_mechanics:
                pass
            else:
                for x in list_mechanics:
                    self.mechanics_listbox.insert(tk.END, x)
        elif f == 'телефоном':
            list_mechanics = sort('phone_mechanic', inf)
            if not list_mechanics:
                pass
            else:
                for x in list_mechanics:
                    self.mechanics_listbox.insert(tk.END, x)

        elif f == 'статусом':
            list_mechanics = sort('status_mechanic', inf)
            if not list_mechanics:
                pass
            else:
                for x in list_mechanics:
                    self.mechanics_listbox.insert(tk.END, x)
        elif f == 'датою':
            if len(inf.split()) != 2:
                return None
            first, second = inf.split()

            if first == '>' or first == '<' or first == '=' or first == '<=' or first == '>=' or first == '<>':
                if len(second) == 10:
                    list_mechanics = sort_by_date_before_or_after(first, second)
                    if not list_mechanics:
                        pass
                    else:
                        for x in list_mechanics:
                            self.mechanics_listbox.insert(tk.END, x)
                    return None

            if len(second) == 10 and len(first) == 10:
                list_mechanics = sort_by_date_between(first, second)
                if not list_mechanics:
                    pass
                else:
                    for x in list_mechanics:
                        self.mechanics_listbox.insert(tk.END, x)

    def delete(self):
        index = [x for x in self.mechanics_listbox.curselection()]
        if not index:
            return None
        phone_ = self.mechanics_listbox.get(index[0]).split()[5]
        if delete_mechanics(phone_):
            mes.showinfo('Повідомлення', 'Механік успішно видалений.')
            self.mechanics_listbox.delete(0, tk.END)
            list_mechanics = get_mechanics()
            if not list_mechanics:
                pass
            else:
                for x in list_mechanics:
                    self.mechanics_listbox.insert(tk.END, x)

            if phone_ == self.last_change_phone:
                self.last_change_phone = ''
        else:
            mes.showerror('Помилка', 'Ви не можете видалити цього механіка, так як є заявки за якими він закріплений.')

    def choose(self):
        index = [x for x in self.mechanics_listbox.curselection()]
        if not index:
            return None
        name = self.mechanics_listbox.get(index[0]).split()[1:4]
        name = f'{name[0]} {name[1]} {name[2]}'
        phone = self.mechanics_listbox.get(index[0]).split()[5]
        date = self.mechanics_listbox.get(index[0]).split()[10]

        self.last_change_phone = phone

        self.name.delete(0, tk.END)
        self.phone.delete(0, tk.END)
        self.date.delete(0, tk.END)

        self.name.insert(0, name)
        self.phone.insert(0, phone)
        self.date.insert(0, date)

    def change_status(self):
        index = [x for x in self.mechanics_listbox.curselection()]
        if not index:
            return None
        phone = self.mechanics_listbox.get(index[0]).split()[5]
        change_status(phone)
        list_mechanics = get_mechanics()
        self.mechanics_listbox.delete(0, tk.END)
        for x in list_mechanics:
            self.mechanics_listbox.insert(tk.END, x)
