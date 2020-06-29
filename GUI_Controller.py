'''
    Author: William Seagle
    Date: 04/04/2019
    Provides Main GUI for the Database Manager
'''

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from Login_Window import LoginScreen
from Main_Window import MainPage


class MainApplication(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent

        # Initialize Login Screen and Configs
        self.create_login_page()

    def on_closing(self):
        try:
            self.dbconnection.disconnect()
        except:
            pass
        finally:
            self.parent.destroy()

    def create_login_page(self):
        try:
            self.dbconnection.disconnect()
        except:
            pass
        self.dbconnection = None
        self.login = LoginScreen(self)
        self.parent.geometry("400x150")
        self.parent.title("Database Manager Login")
        self.login.pack(side="right", fill="both", expand=True)
        self.parent.bind('<Return>', self.login.attempt_login)
        self.center()
        self.parent.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_main_page(self, admin_rights, user, dbconn):
        self.main = MainPage(self, admin_rights, user, dbconn)
        self.main.pack(side="right", fill="both", expand=True)

        # Window Configs
        self.parent.geometry("750x420")
        self.parent.title("Database Manager")
        self.parent.unbind('<Return>')
        self.center()

    def center(self):
        self.parent.update_idletasks()

        # Get Screen Resolution
        screen_width = self.parent.winfo_screenwidth()
        screen_height = self.parent.winfo_screenheight()

        # Get Center Coordinates
        size = tuple(int(_)
                     for _ in self.parent.geometry().split('+')[0].split('x'))
        x = screen_width/2 - size[0]/2
        y = screen_height/2 - size[1]/2

        # Set Window in Center
        self.parent.geometry("+%d+%d" % (x, y))


if __name__ == "__main__":
    root = tk.Tk()
    # root.style = ttk.Style()
    # root.style.theme_use("clam")
    MainApplication(root).pack(side="left", fill="both", expand=True)
    root.mainloop()
