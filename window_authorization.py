import customtkinter as tk
from tkinter import messagebox as mes
from PIL import ImageTk, Image
from tkinter import PhotoImage

import keyboard

from database.database_authorization import authorization, start_main


class WindowAuthorization:

    def __init__(self):
        self.window = tk.CTk()
        self.window.title('Authorization')
        self.window.geometry('460x360+700+400')
        self.window.resizable(False, False)
        self.window.iconphoto(False, PhotoImage(file='image/icon.png'))

        fon = ImageTk.PhotoImage(Image.open('image/fon1.png'))
        l1 = tk.CTkLabel(self.window, image=fon)
        l1.pack()

        entry_image = tk.CTkImage(Image.open('image/entry.png').resize((50, 50), Image.ANTIALIAS))
        tk.set_appearance_mode("dark")
        tk.set_default_color_theme('green')

        self.menu = tk.CTkOptionMenu(self.window, values=['green', 'blue', 'dark-blue'], dropdown_hover_color='#49844D',
                                     dropdown_font=('Century Gothic', 14),
                                     font=('Century Gothic', 14))
        self.menu.place(x=450, rely=.03, relwidth=0.3, relheight=.08, anchor='ne')
        self.menu.set("Оберіть колір")

        frame1 = tk.CTkFrame(l1, width=230, height=230, corner_radius=10)
        frame1.place(relx=.5, rely=.5, anchor='center')

        frame2 = tk.CTkFrame(frame1, width=220, height=220, corner_radius=15, border_width=3)
        frame2.place(relx=.5, rely=.5, anchor='center')

        main_label = tk.CTkLabel(frame2, text='Вхід у систему', font=('Century Gothic', 22))
        main_label.place(relx=.5, y=35, anchor='center')

        self.login = tk.CTkEntry(frame2, border_width=2, placeholder_text='login', width=180,
                                 font=('Century Gothic', 14))
        self.login.place(relx=.5, y=90, anchor='center')

        self.password = tk.CTkEntry(frame2, border_width=2, placeholder_text='password', width=180,
                                    font=('Century Gothic', 14))
        self.password.place(relx=.5, y=130, anchor='center')
        self.password.configure(show='*')

        entrance_but = tk.CTkButton(frame2, text='Ввійти', command=self.entrance, font=('Century Gothic', 16),
                                    width=180, image=entry_image, compound='right', corner_radius=6)
        entrance_but.place(relx=.5, y=190, anchor='center')

        keyboard.add_hotkey('up', lambda: self.login.focus())
        keyboard.add_hotkey('down', lambda: self.password.focus())
        keyboard.add_hotkey('ctrl', self.choose_color_hotkey)
        self.window.mainloop()

    def choose_color_hotkey(self):
        color = self.menu.get()
        if color == 'Оберіть колір':
            self.menu.set('green')
        elif color == 'green':
            self.menu.set('blue')
        elif color == 'blue':
            self.menu.set('dark-blue')
        elif color == 'dark-blue':
            self.menu.set('green')

    def entrance(self):
        log = self.login.get()
        pas = self.password.get()
        color = self.menu.get()
        if color == 'Оберіть колір':
            mes.showerror('Помилка', 'Ви не обрали колір.')
            return None
        else:
            color_mode = color

        if authorization(log, pas):
            self.window.destroy()
            start_main(color_mode)
        else:
            mes.showerror('Помилка', '''Ви неправильно ввели логін або пароль.
            Спробуйте ще раз)''')


if __name__ == '__main__':
    WindowAuthorization()
