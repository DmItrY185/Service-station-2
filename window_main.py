import customtkinter as tk
from tkinter import PhotoImage, Listbox

from window_users import AddUser, DeleteUser
from window_mechanics import Mechanics
from window_service_sections import ServiceSections
from window_services import Services
from window_applications import Applications
from window_inactive_applications import InactiveApplications

from database.database_services import get_services_for_main_window
from database.database_applications import get_active_applications, get_full_active_applications


class WindowMain:
    def __init__(self, color_mode_, user):
        self.root = tk.CTk()
        self.root.title('Service station')
        self.root.geometry('700x500+500+300')
        self.root.resizable(False, False)
        self.root.iconphoto(False, PhotoImage(file='image/icon.png'))
        self.user = user

        tk.set_default_color_theme(color_mode_)
        tk.set_appearance_mode("dark")
        self.color_mode = tk.BooleanVar()
        self.color_mode.set(True)

        self.active_color = None
        self.hover_color = None
        self.mode_color = 'black'

        if color_mode_ == 'green':
            self.active_color = '#2fa572'
        elif color_mode_ == 'blue':
            self.active_color = '#3b8ed0'
        else:
            self.active_color = '#1F6DA9'

        if color_mode_ == 'green':
            self.hover_color = '#49844D'
        elif color_mode_ == 'blue':
            self.hover_color = '#0E56A8'
        else:
            self.hover_color = '#0C407C'

        self.menu = tk.CTkOptionMenu(self.root, values=['Додати', 'Видалити'], dropdown_font=('Century Gothic', 14),
                                     font=('Century Gothic', 14), dropdown_hover_color=self.active_color,
                                     command=self.users)
        self.menu.place(x=690, rely=.02, relwidth=0.22, relheight=.06, anchor='ne')
        self.menu.set("Користувачі")

        switch = tk.CTkSwitch(self.root, text='', command=self.mode_color_)
        switch.place(x=90, rely=.02, anchor='nw')

        user_label = tk.CTkLabel(self.root, text=f'Користувач: ' + self.user, font=('Century Gothic', 18))
        user_label.place(relx=.5, rely=.05, anchor='center')

        frame_services = tk.CTkFrame(self.root, width=180, height=95, corner_radius=10)
        frame_services.place(x=290, y=390)

        frame_applications_button = tk.CTkFrame(self.root, width=180, height=95, corner_radius=10)
        frame_applications_button.place(x=500, y=390)

        frame_mechanics = tk.CTkFrame(self.root, width=180, height=46, corner_radius=10)
        frame_mechanics.place(x=395, y=330)

        mechanics_button = tk.CTkButton(frame_mechanics, text='Механіки', font=('Century Gothic', 16),
                                        command=self.mechanics,
                                        hover_color=self.hover_color)
        mechanics_button.place(relx=.5, rely=.5, anchor='center')

        service_sections_button = tk.CTkButton(frame_services, text='Розділи послуг', font=('Century Gothic', 16),
                                               command=self.service_sections,
                                               hover_color=self.hover_color)
        service_sections_button.place(relx=.5, y=25, anchor='center')

        services_button = tk.CTkButton(frame_services, text='Послуги', font=('Century Gothic', 16),
                                       command=self.services,
                                       hover_color=self.hover_color)
        services_button.place(relx=.5, y=70, anchor='center')

        applications_button = tk.CTkButton(frame_applications_button, text='Заявки', font=('Century Gothic', 16),
                                           command=self.applications,
                                           hover_color=self.hover_color)
        applications_button.place(relx=.5, y=25, anchor='center')

        inactive_applications_button = tk.CTkButton(frame_applications_button, text='Завершені заявки',
                                                    font=('Century Gothic', 16),
                                                    command=self.inactive_application,
                                                    hover_color=self.hover_color)
        inactive_applications_button.place(relx=.5, y=70, anchor='center')

        frame_for_label_services = tk.CTkFrame(self.root, width=110, height=30, corner_radius=10)
        frame_for_label_services.place(x=70, y=45)

        label_services = tk.CTkLabel(frame_for_label_services, text='Послуги', font=('Century Gothic', 16))
        label_services.place(relx=.5, rely=.5, anchor='center')

        frame_services = tk.CTkFrame(self.root, width=210, height=320, corner_radius=10)
        frame_services.place(x=10, y=80)

        scrollbar_services = tk.CTkScrollbar(frame_services, orientation='vertical')
        scrollbar_2_services = tk.CTkScrollbar(frame_services, orientation='horizontal')

        scrollbar_services.pack(side='right', fill='y')
        scrollbar_2_services.pack(side='bottom', fill='both')

        self.services_listbox = Listbox(frame_services, width=36, height=25, yscrollcommand=scrollbar_services.set,
                                        xscrollcommand=scrollbar_2_services.set, bg='#3b3b3b', fg='white',
                                        selectbackground=self.active_color, font=('Century Gothic', 18))

        self.services_listbox.pack(side='left', fill='both')

        self.services_information()

        scrollbar_services.configure(command=self.services_listbox.yview)
        scrollbar_2_services.configure(command=self.services_listbox.xview)

        frame_for_label_applications = tk.CTkFrame(self.root, width=180, height=30, corner_radius=10)
        frame_for_label_applications.place(x=397, y=45)

        label_applications = tk.CTkLabel(frame_for_label_applications, text='Активні заявки',
                                         font=('Century Gothic', 16))
        label_applications.place(relx=.5, rely=.5, anchor='center')

        frame_application = tk.CTkFrame(self.root, width=210, height=320, corner_radius=10)
        frame_application.place(x=300, y=80)

        scrollbar_application = tk.CTkScrollbar(frame_application, orientation='vertical')
        scrollbar_2_application = tk.CTkScrollbar(frame_application, orientation='horizontal')

        scrollbar_application.pack(side='right', fill='y')
        scrollbar_2_application.pack(side='bottom', fill='both')

        self.listbox_application = Listbox(frame_application, width=58, height=10,
                                           yscrollcommand=scrollbar_application.set,
                                           xscrollcommand=scrollbar_2_application.set, bg='#3b3b3b',
                                           fg='white',
                                           selectbackground=self.active_color,
                                           font=('Century Gothic', 18))

        self.listbox_application.pack(side='left', fill='both')

        scrollbar_application.configure(command=self.listbox_application.yview)
        scrollbar_2_application.configure(command=self.listbox_application.xview)

        information_button = tk.CTkButton(self.root, text='Інформація',
                                          font=('Century Gothic', 16),
                                          command=self.full_application_information,
                                          hover_color=self.hover_color)
        information_button.place(x=415, y=290)

        self.list_application = []
        self.applications_information()

        self.root.mainloop()

    def applications_information(self):
        self.list_application = get_active_applications('виконується')
        self.listbox_application.delete(0, tk.END)
        for i in self.list_application:
            application = ' '.join(i.split()[1:]) + ' '
            self.listbox_application.insert(tk.END, application)

    def full_application_information(self):
        try:
            index_application_in_listbox = self.listbox_application.curselection()[0]
        except IndexError:
            return None
        index_application = self.list_application[index_application_in_listbox].split()[0]
        get_full_active_applications(index_application)

    def services_information(self):
        self.services_listbox.delete(0, tk.END)
        for i in get_services_for_main_window()[:-1]:
            self.services_listbox.insert(tk.END, i)

    def mode_color_(self):
        if self.color_mode.get():
            tk.set_appearance_mode("light")
            self.services_listbox['bg'] = 'white'
            self.services_listbox['fg'] = 'black'

            self.listbox_application['bg'] = 'white'
            self.listbox_application['fg'] = 'black'

            self.mode_color = 'white'

            self.color_mode.set(False)
        else:
            tk.set_appearance_mode("dark")
            self.services_listbox['bg'] = '#3b3b3b'
            self.services_listbox['fg'] = 'white'

            self.listbox_application['bg'] = '#3b3b3b'
            self.listbox_application['fg'] = 'white'

            self.mode_color = 'black'

            self.color_mode.set(True)

    def services(self):
        if self.mode_color == 'black':
            Services(bg='#3b3b3b', fg='white', active_color=self.active_color, hover_color=self.hover_color,
                     function=self.services_information)
        elif self.mode_color == 'white':
            Services(bg='white', fg='black', active_color=self.active_color, hover_color=self.hover_color,
                     function=self.services_information)
        else:
            Services(bg='#3b3b3b', fg='white', active_color=self.active_color, hover_color=self.hover_color,
                     function=self.services_information)

    def service_sections(self):

        if self.mode_color == 'black':
            ServiceSections(bg='#3b3b3b', fg='white', active_color=self.active_color, hover_color=self.hover_color,
                            function=self.services_information)
        elif self.mode_color == 'white':
            ServiceSections(bg='white', fg='black', active_color=self.active_color, hover_color=self.hover_color,
                            function=self.services_information)
        else:
            ServiceSections(bg='#3b3b3b', fg='white', active_color=self.active_color, hover_color=self.hover_color,
                            function=self.services_information)

    def mechanics(self):

        if self.mode_color == 'black':
            Mechanics(bg='#3b3b3b', fg='white', active_color=self.active_color, hover_color=self.hover_color)
        elif self.mode_color == 'white':
            Mechanics(bg='white', fg='black', active_color=self.active_color, hover_color=self.hover_color)
        else:
            Mechanics(bg='#3b3b3b', fg='white', active_color=self.active_color, hover_color=self.hover_color)

    def users(self, arg):
        if arg == 'Додати':
            self.menu.set("Користувачі")
            AddUser(self.hover_color)
        else:
            self.menu.set("Користувачі")
            DeleteUser(self.hover_color, self.user)

    def applications(self):

        if self.mode_color == 'black':
            Applications(bg='#3b3b3b', fg='white', active_color=self.active_color, hover_color=self.hover_color,
                         function=self.applications_information)
        elif self.mode_color == 'white':
            Applications(bg='white', fg='black', active_color=self.active_color, hover_color=self.hover_color,
                         function=self.applications_information)
        else:
            Applications(bg='#3b3b3b', fg='white', active_color=self.active_color, hover_color=self.hover_color,
                         function=self.applications_information)

    def inactive_application(self):

        if self.mode_color == 'black':
            InactiveApplications(bg='#3b3b3b', fg='white', active_color=self.active_color,
                                 hover_color=self.hover_color)
        elif self.mode_color == 'white':
            InactiveApplications(bg='white', fg='black', active_color=self.active_color, hover_color=self.hover_color)
        else:
            InactiveApplications(bg='#3b3b3b', fg='white', active_color=self.active_color,
                                 hover_color=self.hover_color)
