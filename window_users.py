import customtkinter as tk
from tkinter import PhotoImage
from tkinter import messagebox as mes
from PIL import Image

from database.database_users import add_new_users, delete_users


class AddUser:
    def __init__(self, hover_color):
        self.new_user = tk.CTkToplevel()
        self.new_user.title('Add user')
        self.new_user.geometry('270x240+1000+500')
        self.new_user.resizable(False, False)
        self.new_user.iconphoto(False, PhotoImage(file='image/icon.png'))
        self.new_user.grab_set()
        self.hover_color = hover_color

        self.check_password = tk.BooleanVar()
        self.check_password.set(False)
        self.check_password_2 = tk.BooleanVar()
        self.check_password_2.set(False)

        add_image = tk.CTkImage(Image.open('image/add.png').resize((50, 50), Image.ANTIALIAS))

        label_new_user = tk.CTkLabel(self.new_user, text='Додавання користувачів', font=('Century Gothic', 18))
        label_new_user.place(relx=.5, y=25, anchor='center')

        check_but_p = tk.CTkCheckBox(self.new_user, text='', width=0, variable=self.check_password, onvalue=True,
                                     offvalue=False,
                                     command=self.visible_password)
        check_but_p.place(relx=0.1, y=110, anchor='center')

        check_but_p_2 = tk.CTkCheckBox(self.new_user, text='', width=0, variable=self.check_password_2,
                                       onvalue=True, offvalue=False,
                                       command=self.visible_password)
        check_but_p_2.place(relx=0.1, y=150, anchor='center')

        self.login = tk.CTkEntry(self.new_user, border_width=2, placeholder_text='login', width=180,
                                 font=('Century Gothic', 14))
        self.login.place(relx=.5, y=70, anchor='center')

        self.password = tk.CTkEntry(self.new_user, border_width=2, placeholder_text='password', width=180,
                                    font=('Century Gothic', 14))
        self.password.place(relx=0.5, y=110, anchor='center')
        self.password.configure(show='*')

        self.password_2 = tk.CTkEntry(self.new_user, border_width=2, placeholder_text='confirm password', width=180,
                                      font=('Century Gothic', 14))
        self.password_2.place(relx=0.5, y=150, anchor='center')
        self.password_2.configure(show='*')

        add_button = tk.CTkButton(self.new_user, text='Додати', font=('Century Gothic', 16), width=180,
                                  image=add_image, compound='right',
                                  corner_radius=6, hover_color=self.hover_color, command=self.add_new_user)
        add_button.place(relx=0.5, y=200, anchor='center')

        self.new_user.mainloop()

    def visible_password(self):
        p = self.check_password.get()
        p_2 = self.check_password_2.get()
        if p:
            self.password.configure(show='')
        else:
            self.password.configure(show='*')
        if p_2:
            self.password_2.configure(show='')
        else:
            self.password_2.configure(show='*')

    def add_new_user(self):
        log = self.login.get()
        p = self.password.get()
        p_2 = self.password_2.get()
        if len(log) == 0:
            mes.showerror('Помилка', 'Ви не ввели логін.')
        elif ' ' in log:
            mes.showerror('Помилка', 'Логін не може містити пробіли.')
        elif len(p) == 0:
            mes.showerror('Помилка', 'Ви не ввели пароль.')
        elif ' ' in p:
            mes.showerror('Помилка', 'Пароль не може містити пробіли.')
        elif p != p_2:
            mes.showerror('Помилка', 'Паролі не співпадають.')
        else:
            if add_new_users(log, p):
                mes.showinfo('Повідомлення', 'Користувач успішно доданий.')
                self.check_password.set(False)
                self.check_password_2.set(False)
                self.login.delete(0, tk.END)
                self.password.delete(0, tk.END)
                self.password_2.delete(0, tk.END)


class DeleteUser:
    def __init__(self, hover_color, user):
        self.delete_user = tk.CTkToplevel()
        self.delete_user.title('Delete user')
        self.delete_user.geometry('250x200+1000+500')
        self.delete_user.resizable(False, False)
        self.delete_user.iconphoto(False, PhotoImage(file='image/icon.png'))
        self.delete_user.grab_set()

        self.hover_color = hover_color
        self.user = user

        delete_image = tk.CTkImage(Image.open('image/delete.png').resize((50, 50), Image.ANTIALIAS))

        main_label = tk.CTkLabel(self.delete_user, text='Видалення користувачів', font=('Century Gothic', 18))
        main_label.place(relx=.5, y=25, anchor='center')

        self.login = tk.CTkEntry(self.delete_user, border_width=2, placeholder_text='login', width=180,
                                 font=('Century Gothic', 14))
        self.login.place(relx=.5, y=70, anchor='center')

        self.password = tk.CTkEntry(self.delete_user, border_width=2, placeholder_text='password', width=180,
                                    font=('Century Gothic', 14))
        self.password.place(relx=.5, y=110, anchor='center')
        self.password.configure(show='*')

        delete_but = tk.CTkButton(self.delete_user, text='Видалити', font=('Century Gothic', 16), width=180,
                                  image=delete_image, compound='right',
                                  corner_radius=6, hover_color=self.hover_color, command=self.delete)
        delete_but.place(relx=.5, y=160, anchor='center')

        self.delete_user.mainloop()

    def delete(self):
        log = self.login.get()
        p = self.password.get()
        if len(log) == 0:
            mes.showerror('Помилка', 'Ви не ввели логін.')
        elif len(p) == 0:
            mes.showerror('Помилка', 'Ви не ввели пароль.')
        else:
            if not delete_users(log, p, self.user):
                mes.showerror('Помилка', f'Ви неправильно ввели логін або пароль.')
            else:
                self.login.delete(0, tk.END)
                self.password.delete(0, tk.END)
