import customtkinter as tk
from tkinter import PhotoImage, Listbox
from PIL import Image
from tkinter import messagebox as mes

from database.database_service_sections import get_service_sections, add_service_sections, change_status, \
    delete_service_sections, sort, change


class ServiceSections:
    def __init__(self, bg, fg, active_color, hover_color, function):
        self.root = tk.CTkToplevel()
        self.root.title('Service sections')
        self.root.geometry('420x505+800+300')
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

        self.service_sections_listbox = Listbox(frame, width=60, height=10, yscrollcommand=scrollbar.set,
                                                # width was 60
                                                xscrollcommand=scrollbar_2.set, bg=bg, fg=fg,
                                                selectbackground=active_color,
                                                font=('Century Gothic', 18))  # font was 18

        self.service_sections_listbox.pack(side='left', fill='both')

        scrollbar.configure(command=self.service_sections_listbox.yview)
        scrollbar_2.configure(command=self.service_sections_listbox.xview)

        self.list_service_sections = get_service_sections()
        if not self.list_service_sections:
            pass
        else:
            for i in self.list_service_sections:
                self.service_sections_listbox.insert(tk.END, f'Назва: {i[0]}  Статус: {i[1]} ')

        filter_label = tk.CTkLabel(self.root, text='Фільтрувати за', font=('Century Gothic', 16))
        filter_label.place(x=10, y=220)

        self.filter_menu = tk.CTkOptionMenu(self.root,
                                            values=['', 'назвою', 'статусом'],
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
                                     compound='right', hover_color=hover_color, corner_radius=6,
                                     command=self.delete)
        delete_button.place(x=220, y=270)

        choose_button = tk.CTkButton(self.root, text='Обрати', font=('Century Gothic', 16), image=choose_image,
                                     compound='right', hover_color=hover_color, corner_radius=6, command=self.choose)
        choose_button.place(x=50, y=320)

        change_status_button = tk.CTkButton(self.root, text='Змінити ст.', font=('Century Gothic', 16),
                                            image=change_status_image, command=self.change_status,
                                            compound='right', hover_color=hover_color, corner_radius=6)
        change_status_button.place(x=220, y=320)

        add_label = tk.CTkLabel(self.root, text='Додавання/зміна даних', font=('Century Gothic', 18))
        add_label.place(relx=.5, y=390, anchor='center')

        self.name = tk.CTkEntry(self.root, border_width=2, width=300, font=('Century Gothic', 14),
                                placeholder_text='name')
        self.name.place(relx=.5, y=430, anchor='center')

        add_button = tk.CTkButton(self.root, text='Додати', font=('Century Gothic', 16), image=add_image,
                                  compound='right', hover_color=hover_color, corner_radius=6, command=self.add)
        add_button.place(x=50, y=460)

        self.change_button = tk.CTkButton(self.root, text='Змінити', font=('Century Gothic', 16), image=change_image,
                                          compound='right', hover_color=hover_color, corner_radius=6,
                                          command=self.change)
        self.change_button.place(x=220, y=460)
        self.root.mainloop()

    def add(self):
        name = self.name.get()
        if name.strip() == '':
            mes.showerror('Помилка', 'Ви не ввели назву розділу.')
        else:
            if add_service_sections(name):
                mes.showinfo('Повідомлення', 'Розділ успішно доданий.')
                list_service_sections = get_service_sections()
                self.list_service_sections = list_service_sections

                self.service_sections_listbox.delete(0, tk.END)
                for i in list_service_sections:
                    self.service_sections_listbox.insert(tk.END, f'Назва: {i[0]}  Статус: {i[1]} ')
                self.name.delete(0, tk.END)
                self.update_services_listbox_main_window()

                self.last_change_name = ' '

    def change_status(self):
        index = [x for x in self.service_sections_listbox.curselection()]
        if not index:
            return None
        name = self.list_service_sections[index[0]][0]

        change_status(name)
        list_service_sections = get_service_sections()
        self.list_service_sections = list_service_sections
        self.service_sections_listbox.delete(0, tk.END)
        for x in list_service_sections:
            self.service_sections_listbox.insert(tk.END, f'Назва: {x[0]}  Статус: {x[1]} ')
        self.update_services_listbox_main_window()

    def delete(self):
        index = [x for x in self.service_sections_listbox.curselection()]
        if not index:
            return None
        name = self.list_service_sections[index[0]][0]
        if delete_service_sections(name):
            mes.showinfo('Повідомлення', 'Розділ успішно видалений.')
            self.service_sections_listbox.delete(0, tk.END)
            list_service_sections = get_service_sections()
            self.list_service_sections = list_service_sections
            if not list_service_sections:
                pass
            else:
                for x in list_service_sections:
                    self.service_sections_listbox.insert(tk.END, f'Назва: {x[0]}  Статус: {x[1]} ')
            if name == self.last_change_name:
                self.last_change_name = ''
            self.update_services_listbox_main_window()

        else:
            mes.showerror('Помилка', 'Ви не можете видалити цей розділ, так як є послуги які за ним закріплені.')

    def sort(self):

        def result():
            for i in self.list_service_sections:
                self.service_sections_listbox.insert(tk.END, f'Назва: {i[0]}  Статус: {i[1]} ')

        f = self.filter_menu.get()
        self.service_sections_listbox.delete(0, tk.END)
        if f == '':
            self.list_service_sections = get_service_sections()
            result()
            return None
        inf = self.information.get()
        if inf == '':
            # mes.showerror('Помилка', 'Ви не ввели дані для пошуку.')
            pass

        elif f == 'назвою':
            self.list_service_sections = sort('name_service_section', inf)
            result()

        elif f == 'статусом':
            self.list_service_sections = sort('status_service_section', inf)
            result()

    def choose(self):
        index = [x for x in self.service_sections_listbox.curselection()]
        if not index:
            return None
        name = self.list_service_sections[index[0]][0]

        self.name.delete(0, tk.END)

        self.name.insert(0, name)

        self.last_change_name = name

    def change(self):
        if self.last_change_name == '':
            mes.showerror('Помилка', 'Ви видалили цей розділ.')
            self.name.delete(0, tk.END)
            self.last_change_name = ' '
        elif self.last_change_name == ' ':
            pass

        else:
            name = self.name.get()
            if name.strip() == '':
                mes.showerror('Помилка', 'Ви не ввели назву розділу.')
            elif change(name, self.last_change_name):
                mes.showinfo('Повідомлення', 'Дані успішно змінено.')
                self.service_sections_listbox.delete(0, tk.END)
                list_service_sections = get_service_sections()
                self.list_service_sections = list_service_sections
                for x in list_service_sections:
                    self.service_sections_listbox.insert(tk.END, f'Назва: {x[0]}  Статус: {x[1]} ')
                self.name.delete(0, tk.END)

                self.last_change_name = ' '
                self.update_services_listbox_main_window()
